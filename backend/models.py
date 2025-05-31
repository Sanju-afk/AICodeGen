from sqlalchemy import Column,Integer,Boolean,String,DateTime,Text,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index = True)
    username = Column(String(50), unique = True, index = True)
    hashed_password = Column(String(100))
    disabled = Column(Boolean, default = False)
    codes = relationship("CodeGenerationRequest", back_populates="owner")


class CodeGenerationRequest(Base):
    __tablename__ = "code_generation_requests"
    id = Column(Integer,primary_key = True, index = True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="codes")
    prompt = Column(Text, nullable = False)
    language = Column(String(50), nullable= False)
    generated_code = Column(Text, nullable = True)
    created_at = Column(DateTime, default = datetime.datetime.now)
    
