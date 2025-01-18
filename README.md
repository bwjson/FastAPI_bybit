This is a parody for a crypto exchange using FastAPI as a main backend framework. I also used here Redis for simple caching, sqlalchemy as an ORM, alembic for migrations.<br>

This project generally is API with no frontend part<br>

![image](https://github.com/user-attachments/assets/141c1cc2-c99e-4c64-95a7-c807936c29f7)

You can create wallet, exchange and trade. For getting stock information used official site of KASE (Kazakhstan Exchange). <br>

Generally, project is trying to use onion architecture:
1. Handlers (http)
2. Service (business logic)
3. Repository (Work with postgres)<br>

How to run migrations?
1. Fill the .env file using .env-example and install and run Redis server
2. ```pip install -r requirements.txt```
3. ```alembic upgrade head```

How to run the server?<br><br>
```uvicorn src.main:app --reload```
