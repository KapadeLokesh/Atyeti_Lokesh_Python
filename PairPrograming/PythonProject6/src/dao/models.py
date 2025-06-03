import sqlalchemy
from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class LogSummary(Base):
    __tablename__ = 'log_summary6'
    id = Column(Integer, primary_key=True,autoincrement=True)
    info_count = Column(Integer)
    warning_count = Column(Integer)
    error_count = Column(Integer)
    log_file = Column(String(255))
    created_at = Column(TIMESTAMP,server_default=func.now())

class ErrorSummary(Base):
    __tablename__= "error_summary"
    id = Column(Integer,primary_key=True,autoincrement=True)
    error_count = Column(Integer)
    log_file = Column(String(255))
    created_at = Column(TIMESTAMP,server_default=func.now())

class WarningSummary(Base):
    __tablename__= "warning_summary"
    id = Column(Integer,primary_key=True,autoincrement=True)
    warning_count = Column(Integer)
    log_file = Column(String(255))
    created_at = Column(TIMESTAMP,server_default=func.now())

class InfoSummary(Base):
    __tablename__= "info_summary"
    id = Column(Integer,primary_key=True,autoincrement=True)
    info_count = Column(Integer)
    log_file = Column(String(255))
    created_at = Column(TIMESTAMP,server_default=func.now())