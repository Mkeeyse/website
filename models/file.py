from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class File(Base):
    __tablename__ = 'file'

    file_number = Column(String, primary_key=True)
    date_added = Column(DateTime, default=func.now())
    category = Column(String)
    ref_num = Column(String)
    title = Column(String)
    status = Column(String)
