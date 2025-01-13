from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declared_attr


class TimestampMixin:
    @declared_attr
    def created_at(cls):
        return Column(DateTime(timezone=True), nullable=False, default=func.now())

    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now()
        )

    @declared_attr
    def deleted_at(cls):
        return Column(DateTime(timezone=True), nullable=True)