import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from .db_session import SqlAlchemyBase


class Post(SqlAlchemyBase):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)

    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    author = Column(String, nullable=False)

    # 💥 ВОТ ЭТА СТРОКА ТЕБЕ НУЖНА
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
