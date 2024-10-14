import smtplib
from email.message import EmailMessage
from celery import Celery
from src.config import SMTP_PASSWORD, SMTP_USER, REDIS_PORT, REDIS_HOST
from src.transaction.models import TransactionType

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery('tasks', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}')


def get_email_template_report(order_id: int, wallet_id: int, stock: str, amount: int, type: TransactionType):
    email = EmailMessage()
    email['Subject'] = f'Bybit. Order #{order_id} was successfully executed'
    email['From'] = SMTP_USER
    email['To'] = SMTP_USER

    email.set_content(
        '<div>'
        f'<h1 style="color: blue;">Здравствуйте, а вот и ваш отчет. Зацените 😊</h1>'
        f'<p>Ваш ордер на {amount} акций "{stock}" был успешно исполнен.</p>'
        f'<p><strong>Детали ордера:</strong></p>'
        f'<ul>'
        f'<li>ID ордера: {order_id}</li>'
        f'<li>ID кошелька: {wallet_id}</li>'
        f'<li>Тип транзакции: {type}</li>'
        f'</ul>'
        '<img src="https://seeklogo.com/images/B/bybit-logo-4C31FD6A08-seeklogo.com.png" width="150" alt="Bybit Logo">'
        '</div>',
        subtype='html'
    )
    return email


@celery.task
def send_email_order_report(order_id: int, wallet_id: int, stock: str, amount: int, type: TransactionType):
    email = get_email_template_report(order_id, wallet_id, stock, amount, type)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)