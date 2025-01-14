from common.schemas import MinioObjectCreateBase
from common.schemas.geo import Coordinate

from typing import Optional
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class Node(BaseModel):

    id: Optional[UUID] = None
    name: Optional[str] = None

    # position information
    fixed_location: Optional[Coordinate] = None

    antenna_height: Optional[float] = None


class NodeReport(BaseModel):

    @model_validator(mode="after")
    def validate_id_or_name(cls, values):
        if not values.node_id and not values.node_name:
            raise ValueError("Either 'node_id' or 'node_name' must be provided.")
        return values


class NodeConfig(BaseModel):
    name: str
    fixed_location: Optional[Coordinate] = None
    antenna_height: Optional[float] = None

class NodeRegistration(BaseModel):
    id: UUID
    name: str

# Sent by a node wishing to register/join
class NodeRegisterRequest(BaseModel):
    name: str
    fixed_location: Optional[Coordinate] = None
    antenna_height: Optional[float] = None

# Response to node
class NodeRegisterResponse(BaseModel):
    registration: Optional[NodeRegistration]
    new_registration: Optional[bool] = False