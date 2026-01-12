from extensions import db
from sqlalchemy.orm import Mapped, mapped_column
import uuid

class Coin(db.Model):
    __tablename__ = "coins"
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    coin_name: Mapped[str] = mapped_column(nullable=False, unique=True)

class Duty(db.Model):
    __tablename__ = "duties"
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    duty_name: Mapped[str] = mapped_column(nullable=False, unique=True)

class Ksb(db.Model):
    __tablename__ = "KSB"
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    ksb_name: Mapped[str] = mapped_column(nullable=False, unique=True)

