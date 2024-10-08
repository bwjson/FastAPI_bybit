from fastapi_users import schemas

class UserRead(schemas.BaseUser[int]):
	id: int
	email: str
	username: str
	is_active: bool
	is_superuser: bool
	is_verified: bool

	class Config:
		from_attributes = True

class UserCreate(schemas.BaseUser[int]):
	email: str
	username: str
	password: str
	is_active: bool
	is_superuser: bool
	is_verified: bool

