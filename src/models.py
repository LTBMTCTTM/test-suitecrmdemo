from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import Generator

Base = declarative_base()


class Leads(Base):
    __tablename__ = 'leads'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    phone_work = Column(String(50))
    first_name = Column(String(120))
    last_name = Column(String(120))


# Tạo engine để kết nối tới MySQL
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:mauFJcuf5dhRMQrjj@172.21.0.1/quotes"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Tạo Session để thao tác với database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
