from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

try:
    # Connection to the cloud database without roles
    # connectionUri = 'postgresql://faflvpwpjkadib:308b7218f2f64308116d0372d4b2d30951688393b469bec7f93fb59c0c564f0f@ec2-54-74-156-137.eu-west-1.compute.amazonaws.com:5432/dflk02u18ei8hg'

    # Connection to local database with roles
    connectionUri = 'postgresql://flask_application:flask_application@localhost:5432/postgres'

    engine = create_engine(connectionUri, echo=False)
    Base = declarative_base()
    """All DB types classes must extend this class"""

    from lib.types import Form, Question, User, Access
    from lib.types.answers import Answer, DateAnswer, MultipleAnswer, OpenAnswer, SingleAnswer

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)  # creazione della factory
    """Factory for creating a session to the DB"""

except Exception as e:
    print("Failed to connect to DB: " + str(e))
    quit()
