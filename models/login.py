from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()

class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    user_name = Column(String(50), unique=True, nullable=False)
    user_password = Column(String(128), nullable=False)

    def __init__(self, user_name, user_password):
        self.user_name = user_name
        self.set_password(user_password)

    def set_password(self, password):
        self.user_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.user_password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'user_name': self.user_name,
        }
