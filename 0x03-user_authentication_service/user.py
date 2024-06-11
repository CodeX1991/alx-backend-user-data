#!/usr/bin/env python3
"""User authentication"""


from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


# Create an instance of the declaration
Base = declarative_base()


class User(Base):
    """A user model for the table=users"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
