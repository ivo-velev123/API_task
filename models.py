from extensions import db
from sqlalchemy import Table, Column, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
import uuid


class Coin(db.Model):
    __tablename__ = "coins"
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    coin_name: Mapped[str] = mapped_column(nullable=False, unique=True)

    def to_dict(self):
        return {
            "id": self.id,
            "coin_name": self.coin_name,
        }


class Duty(db.Model):
    __tablename__ = "duties"
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    duty_name: Mapped[str] = mapped_column(nullable=False, unique=True)


class Ksb(db.Model):
    __tablename__ = "ksbs"
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    ksb_name: Mapped[str] = mapped_column(nullable=False, unique=True)


coins_duties = Table(
    "coins_duties",
    db.metadata,
    Column("coin_id", String, ForeignKey("coins.id"), primary_key=True),
    Column("duty_id", String, ForeignKey("duties.id"), primary_key=True),
)

duties_ksbs = Table(
    "duties_ksbs",
    db.metadata,
    Column("duty_id", String, ForeignKey("duties.id"), primary_key=True),
    Column("ksb_id", String, ForeignKey("ksbs.id"), primary_key=True),
)
