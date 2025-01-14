from app.db.mixins import TimestampMixin

from uuid import uuid4
from sqlalchemy import Column, Float, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship

from datetime import datetime


Base = declarative_base(cls=TimestampMixin)


class Node(Base):
    __tablename__ = "nodes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    name = Column(String, unique=True, nullable=False)

    label = Column (String, nullable=True)

    intercepts = relationship('Intercept', back_populates='node')


class Intercept(Base):
    __tablename__ = "intercepts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    node_id = Column(UUID(as_uuid=True), ForeignKey('nodes.id'), nullable=False)
    node = relationship('Node', back_populates='intercepts')

    time_start = Column(DateTime(timezone=True), nullable=False)
    duration = Column(Float, nullable=False)

    frequency_center = Column(Float, nullable=False)

    audio_file_id = Column(UUID(as_uuid=True), ForeignKey('intercept_audio_files.id'), nullable=True)
    # relationship
    audio_file = relationship('InterceptAudioFile', back_populates='intercept', uselist=True)


class MinioFileRecordBase(Base):
    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    etag = Column(String, nullable=False)
    bucket = Column(String, nullable=False)
    object_name = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    content_type = Column(String, nullable=True)


class AudioFileBase(MinioFileRecordBase):
    __abstract__ = True


class InterceptAudioFile(AudioFileBase):
    __tablename__ = "intercept_audio_files"

    # intercept_id = Column(Integer, ForeignKey('intercepts.id'), nullable=False)

    intercept = relationship('Intercept', back_populates='audio_file')





"""

consider the fact that we could serialize data (ie. json) for metadata in the weeds - the most important part of the "SQL" table fields will pertain to relationships and searching/filtering of data


- frequency (decimal, MHz)
- time_start (timestamp, iso8601)
- time_stop (timestamp, iso8601)
- duration_secs (float)
- demodulation (if applicable)
    - type: fm, am
- location
  - latitude
  - longitude
  - elevation (wgs elliptoid?)
  - we really ought to consider getting to ECEF where possible
- sensor
  - type
  - gain?
  - other settings?

"""

