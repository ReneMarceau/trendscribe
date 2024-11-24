from datetime import datetime
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
from typing import List, Optional

Base = declarative_base()

class ProcessedPost(Base):
    __tablename__ = 'processed_posts'
    
    url = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    processed_date = Column(DateTime, default=datetime.utcnow)

class DatabaseHandler:
    def __init__(self, db_url: str = "sqlite:///posts.db"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def is_post_processed(self, url: str) -> bool:
        with self.Session() as session:
            return session.query(ProcessedPost).filter_by(url=url).first() is not None

    def mark_post_processed(self, url: str, title: str):
        with self.Session() as session:
            post = ProcessedPost(url=url, title=title)
            session.add(post)
            session.commit()

    def get_processed_posts(self) -> List[ProcessedPost]:
        with self.Session() as session:
            return session.query(ProcessedPost).all()
