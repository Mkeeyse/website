import uuid
from sqlalchemy import Column, String, DateTime, func, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

class File(Base):
    __tablename__ = 'file'

    file_number = Column(Integer, autoincrement=True, primary_key=True)
    date_added = Column(DateTime, default=func.now())
    category = Column(String)
    ref_num = Column(String)
    title = Column(String)
    status = Column(String)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4)

    def __init__(self, category, ref_num, title, status):
        self.category = category
        self.ref_num = ref_num
        self.title = title
        self.status = status
