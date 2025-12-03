from __future__ import annotations

import csv
from datetime import datetime, date
from pathlib import Path
from decimal import Decimal

from sqlalchemy.orm import Session

from app.db import SessionLocal
from app import models

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR/"data"

def load_instruments(session: Session):
    path = DATA_DIR / "instruments.csv"
    with path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            ticker = row["ticker"].strip()
            existing = (
                session.query(models.Instrument)
                .filter(models.Instrument.ticker == ticker)
                .one_or_none()
            )
            if existing:
                continue

            inst = models.Instrument(
                ticker = ticker,
                name = row.get("name") or None,
                asset_class = row.get("asset_class") or None,
                currency = row.get("currency") or None,
                sector = row.get("sector") or None,
                issuer = row.get("issuer") or None,
            )
            session.add(inst)
        session.commit()
    
def load_portfolios(session: Session):
    path = DATA_DIR/"portfolios.csv"
    with path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"].strip()
            existing = (
                session.query(models.Portfolio)
                .filter(models.Portfolio.name == name)
                .one_or_none()
            )
            if existing:
                continue
                
            pf = models.Portfolio(
                name=name,
                description=row.get("description") or None,
                base_currency=row.get("base_currency") or None,
            )
            session.add(pf)
        session.commit()

def load_prices(session: Session):
    path=DATA_DIR/"prices.csv"
    with path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            ticker=row["ticker"].strip()
            inst = (
                session.query(models.Instrument)
                .filter(models.Instrument.ticker == ticker)
                .one_or_none()
            )
            if not inst:
                continue
                
            dt = date.fromisoformat(row["date"])

            existing = (
                session.query(models.Price)
                .filter(
                    models.Price.instrument_id == inst.id,
                    models.Price.date == dt,
                )
                .one_or_none()
            )
            if existing:
                continue

            price = models.Price(
                instrument_id=inst.id,
                date = dt,
                close= Decimal(row["close"]),
                open=Decimal(row["open"]) if row.get("open") else None,
                high=Decimal(row["high"]) if row.get("high") else None,
                low=Decimal(row["low"]) if row.get("low") else None,
                volume=float(row["volume"]) if row.get("volume") else None,
            )
            session.add(price)
        session.commit()

def load_holdings(session: Session):
    path = DATA_DIR / "holdings.csv"
    with path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            portfolio_name = row["portfolio_name"].strip()
            ticker = row["ticker"].strip()

            pf = (
                session.query(models.Portfolio)
                .filter(models.Portfolio.name == portfolio_name)
                .one_or_none()
            )
            inst = (
                session.query(models.Instrument)
                .filter(models.Instrument.ticker == ticker)
                .one_or_none()
            )

            if not pf or not inst:
                continue

            dt = date.fromisoformat(row["date"])
            existing = (
                session.query(models.Holding)
                .filter(
                    models.Holding.portfolio_id == pf.id,
                    models.Holding.instrument_id == inst.id,
                    models.Holding.date == dt,
                )
                .one_or_none()
            )
            if existing:
                continue

            holding = models.Holding(
                portfolio_id=pf.id,
                instrument_id=inst.id,
                date=dt,
                quantity=Decimal(row["quantity"]),
                market_value=Decimal(row["market_value"])
                if row.get("market_value")
                else None,
                weight=float(row["weight"]) if row.get("weight") else None,
            )
            session.add(holding)
    session.commit()


def load_trades(session: Session):
    path = DATA_DIR / "trades.csv"
    with path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            portfolio_name = row["portfolio_name"].strip()
            ticker = row["ticker"].strip()

            pf = (
                session.query(models.Portfolio)
                .filter(models.Portfolio.name == portfolio_name)
                .one_or_none()
            )
            inst = (
                session.query(models.Instrument)
                .filter(models.Instrument.ticker == ticker)
                .one_or_none()
            )

            if not pf or not inst:
                continue

            trade_dt = datetime.fromisoformat(row["trade_datetime"])

            trade = models.Trade(
                portfolio_id=pf.id,
                instrument_id=inst.id,
                trade_datetime=trade_dt,
                side=row["side"].strip().upper(),
                quantity=Decimal(row["quantity"]),
                price=Decimal(row["price"]),
                commission=Decimal(row["commission"])
                if row.get("commission")
                else None,
                broker=row.get("broker") or None,
                trader=row.get("trader") or None,
            )
            session.add(trade)
    session.commit()

def main():
    session = SessionLocal()
    try:
        load_instruments(session)
        load_portfolios(session)
        load_prices(session)
        load_holdings(session)
        load_trades(session)
        print("Sample data loaded successfully.")
    finally:
        session.close()


if __name__ == "__main__":
    main()