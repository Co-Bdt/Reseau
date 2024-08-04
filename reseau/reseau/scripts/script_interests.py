import reflex as rx
from ..models.interest import Interest


# List of interests to insert
interests_string = """Business
Physique
Mental
Relations"""


# @rx.script  # TODO: potentielle feature intéressante
def insert_interests():
    """Script to insert cities in the sqlite database."""

    print("Inserting cities in the database")
    # Import the string as a list of interests to insert
    interests_list = interests_string.split("\n")

    with rx.session() as session:
        for interest in interests_list:
            interest = Interest(
                name=interest,
            )
            session.add(interest)
        session.commit()

    print("Inserting interests - Done")

    print("Testing the insertion")
    # Test the insertion
    with rx.session() as session:
        interests = session.exec(Interest.select()).all()
        for city in interests:
            print(city.name)
