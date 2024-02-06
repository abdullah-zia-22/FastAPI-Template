from sqlalchemy import Column, Integer, String,Boolean
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class User(Base):
   __tablename__ = 'user'
   id = Column(Integer, primary_key=True, autoincrement=True)
   email = Column(String(255), nullable=False)
   username = Column(String(50), nullable=False)
   password = Column(String(255), nullable=False)
   isActive = Column(Boolean, nullable=False, default=0)
