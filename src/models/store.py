from pydantic import BaseModel, Field
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from fastapi_users.db.sqlalchemy import GUID
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class StoreModel(Base):
    __tablename__ = 'store'
    id = Column(Integer, unique=True, primary_key=True, index=True)
    user_id = Column(GUID, unique=False, index=True, nullable=False)
    email = Column(String(320), unique=False, index=True, nullable=False)
    enterdate = Column(DateTime, unique=True, index=False, nullable=False)
    filename = Column(String(512), unique=False, index=True)
    url = Column(String(512), unique=True, index=True, nullable=False)
    path = Column(String(512), unique=True, index=True, nullable=False)


def ResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {
        "error": error,
        "code": code,
        "message": message
    }
