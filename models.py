from extensions import db
from sqlalchemy.orm import Mapped, mapped_column
import uuid

class Coin(db.Model):
    __tablename__ = "coins"
    id: Mapped[int] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid64))
    coin_name: Mapped[str] = mapped_column(nullable=False, unique=True)

class Duty(db.Model):
    __tablename__ = "duties"
    id: Mapped[int] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid64))
    duty_name: Mapped[str] = mapped_column(nullable=False, unique=True)

class Ksb(db.Model):
    __tablename__ = "KSB"
    id: Mapped[int] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid64))
    ksb_name: Mapped[str] = mapped_column(nullable=False, unique=True)

