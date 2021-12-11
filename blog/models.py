from .database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)