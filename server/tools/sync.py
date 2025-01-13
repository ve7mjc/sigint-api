from app.db.models import Base, Node

import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import Session



# Function to load YAML data
def load_yaml(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

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


    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(engine)

    # Load data from YAML
    yaml_file = 'data.yaml'  # Replace with the path to your YAML file
    yaml_data = load_yaml(yaml_file)

    # Import data
    with Session(engine) as session:
        import_data(yaml_data, session)
