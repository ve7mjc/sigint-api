from app.db.database import get_db
from app.db.models import Node

from common.schemas.node import NodeRegistration, NodeRegisterRequest, NodeRegisterResponse

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

# import json

router = APIRouter(
    prefix="/nodes",
    tags=["nodes"]
)


@router.post("/register", response_model=NodeRegisterResponse)
async def register_node(
        request: NodeRegisterRequest,
        db: Session = Depends(get_db)
    ):

    new_registration = False

    # check for node exists under name
    db_node = db.query(Node).filter(Node.name == request.name).first()
    if not db_node:
        # Create a Node instance
        db_node = Node(
            name=request.name,
        )

        # Insert into the database
        db.add(db_node)
        db.commit()
        db.refresh(db_node)  # Fetch the updated object with its ID

        new_registration = True

        # raise HTTPException(status_code=404, detail=f"Node with name '{request.node_name}' not found.")

    node_registration = NodeRegistration(
        id=db_node.id,
        name=db_node.name
    )

    # Return the created node
    return NodeRegisterResponse(
        registration=node_registration,
        new_registration=new_registration
    )

