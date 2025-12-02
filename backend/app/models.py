from datetime import datetime, date
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Numeric,
)
from sqlalchemy.orm import relationship

from .db import Base


class Instrument(Base):
    __tablename__ = "instruments"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(32), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=True)
    asset_class = Column(String(32), nullable=True)
    currency = Column(String(8), nullable=True)
    sector = Column(String(64), nullable=True)
    issuer = Column(String(128), nullable=True)

    prices = relationship("Price", back_populates="instrument")
    holdings = relationship("Holding", back_populates="instrument")
    trades = relationship("Trade", back_populates="instrument")


class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True, index=True)
    instrument_id = Column(Integer, ForeignKey("instruments.id"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    close = Column(Numeric(18, 6), nullable=False)
    open = Column(Numeric(18, 6), nullable=True)
    high = Column(Numeric(18, 6), nullable=True)
    low = Column(Numeric(18, 6), nullable=True)
    volume = Column(Float, nullable=True)

    instrument = relationship("Instrument", back_populates="prices")


class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False, unique=True)
    description = Column(String(512), nullable=True)
    base_currency = Column(String(8), nullable=True)

    holdings = relationship("Holding", back_populates="portfolio")
    trades = relationship("Trade", back_populates="portfolio")


class Holding(Base):
    __tablename__ = "holdings"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False, index=True)
    instrument_id = Column(Integer, ForeignKey("instruments.id"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    quantity = Column(Numeric(20, 4), nullable=False)
    market_value = Column(Numeric(20, 4), nullable=True)
    weight = Column(Float, nullable=True)

    portfolio = relationship("Portfolio", back_populates="holdings")
    instrument = relationship("Instrument", back_populates="holdings")


class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False, index=True)
    instrument_id = Column(Integer, ForeignKey("instruments.id"), nullable=False, index=True)

    trade_datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    side = Column(String(4), nullable=False)   # BUY / SELL
    quantity = Column(Numeric(20, 4), nullable=False)
    price = Column(Numeric(18, 6), nullable=False)
    commission = Column(Numeric(18, 6), nullable=True)
    broker = Column(String(128), nullable=True)
    trader = Column(String(128), nullable=True)

    portfolio = relationship("Portfolio", back_populates="trades")
    instrument = relationship("Instrument", back_populates="trades")
