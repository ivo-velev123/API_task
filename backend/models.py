from backend.extensions import db
from sqlalchemy import Table, Column, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid

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


class Coin(db.Model):
    __tablename__ = "coins"
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    coin_name: Mapped[str] = mapped_column(nullable=False, unique=True)

    duties = relationship("Duty", secondary=coins_duties, back_populates="coins")

    def to_dict(self, include_duties=False):
        result = {
            "id": self.id,
            "coin_name": self.coin_name,
        }
        if include_duties:
            result["duties"] = [duty.to_dict() for duty in self.duties]
        return result


class Duty(db.Model):
    __tablename__ = "duties"
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    duty_name: Mapped[str] = mapped_column(nullable=False, unique=True)
    duty_description: Mapped[str] = mapped_column(nullable=True, unique=True)

    coins = relationship("Coin", secondary=coins_duties, back_populates="duties")
    ksbs = relationship("Ksb", secondary=duties_ksbs, back_populates="duties")

    def to_dict(self, include_ksbs=False):
        result = {
            "id": self.id,
            "duty_name": self.duty_name,
            "description": self.duty_description,
        }
        if include_ksbs:
            result["ksbs"] = [ksb.to_dict() for ksb in self.ksbs]
        return result


class Ksb(db.Model):
    __tablename__ = "ksbs"
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    ksb_name: Mapped[str] = mapped_column(nullable=False, unique=True)

    duties = relationship("Duty", secondary=duties_ksbs, back_populates="ksbs")

    def to_dict(self):
        return {
            "id": self.id,
            "ksb_name": self.ksb_name,
        }
