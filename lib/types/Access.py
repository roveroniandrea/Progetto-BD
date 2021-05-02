from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

from lib.initDB import Base


class Access(Base):
    """Type definition for the accesses table in DB"""

    __tablename__ = 'accesses'
    user = Column(String, ForeignKey('users.email'))
    form = Column(Integer, ForeignKey('forms.id'))
    access_id = Column(Integer, primary_key=True)

    userRel = relationship('User', back_populates='accessesRel')
    """1:M relationship with users table"""

    formRel = relationship('Form', back_populates='accessesRel')
    """1:M relationship with forms table"""
