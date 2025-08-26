from ycaro_airlines_v2.config import db
from ycaro_airlines_v2.models.flight import Flight, City, Route


def create_tables():
    db.create_tables(
        [
            City,
            Route,
            Flight,
        ]
    )


def reset_tables():
    with db.atomic():
        db.drop_tables(
            [
                Flight,
                City,
                Route,
            ]
        )
