from models import db
from sqlalchemy.orm import sessionmaker, Session

def pegar_sessao():
    """
        Get a db session and returns it
    """
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session ## Yield sends a return with that result without exiting the function
    finally:
        session.close()