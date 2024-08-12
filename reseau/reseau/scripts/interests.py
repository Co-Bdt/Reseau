import reflex as rx
from models import Interest


# List of interests to insert
interests_string = """Business
Physique
Mental
Relations"""


# @rx.script  # TODO: potentielle feature intéressante
def insert_interests():
    """Script to insert interests in the sqlite database."""

    print("Inserting interests in the database")
    # Import the string as a list of interests to insert
    interests_list = interests_string.split("\n")

    with rx.session() as session:
        interests = session.exec(Interest.select()).all()
        if interests:
            print("Interests already inserted")
            return

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


def main():
    insert_interests()


if __name__ == "__main__":
    main()