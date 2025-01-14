import common

from app.db.models import Base, Node

from pathlib import Path

import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

yaml_path = Path(__file__).resolve().parent.parent.parent / "data"


# Function to load YAML data
def load_data(data_path: Path) -> dict:
    with open(data_path, 'r') as f:
        return yaml.safe_load(f)


def sync_nodes(nodes: dict, db: Session):
    # nodes = yaml_data.get("nodes", {})
    for node_name, node_fields in nodes.items():
        # Check if the node exists in the database
        db_node = db.query(Node).filter(Node.name == node_name).first()

        if db_node:
            # Update the node if fields don't match
            updated = False
            for field, value in node_fields.items():
                if getattr(db_node, field) != value:
                    setattr(db_node, field, value)
                    updated = True
            if updated:
                print(f"Updating node '{node_name}' in the database.")
        else:
            # Insert a new node
            print(f"Inserting new node '{node_name}' into the database.")
            db_node = Node(name=node_name, **node_fields)
            db.add(db_node)

    db.commit()
    print("Sync complete.")



# Function to import data into the database
def import_data(yaml_data, session):

    pass
    # for parent_data in yaml_data.get('parents', []):

    # for parent_data in yaml_data.get('parents', []):
    #     # Create or get the Parent
    #     parent = session.query(Parent).filter_by(name=parent_data['name']).first()
    #     if not parent:
    #         parent = Parent(name=parent_data['name'])
    #         session.add(parent)
    #         session.flush()  # Ensure parent ID is available for child relationships

    #     # Add children for this parent
    #     for child_data in parent_data.get('children', []):
    #         # Avoid duplicates by checking existing children
    #         if not any(child.name == child_data['name'] for child in parent.children):
    #             child = Child(name=child_data['name'], parent=parent)
    #             session.add(child)
    # session.commit()


if __name__ == '__main__':

    # Database setup
    from app.core.config import settings


    # load data from yaml file
    if not yaml_path.exists():
        raise(f"Data path '{yaml_path}' does not exist!")

    # Load data from YAML
    yaml_data = load_data(yaml_path / "data.yaml")

    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(engine)

    # Import data
    with Session(engine) as session:
        nodes = yaml_data.get('nodes', {})
        print(nodes)
        sync_nodes(nodes, session)

        # import_data(yaml_data, session)
