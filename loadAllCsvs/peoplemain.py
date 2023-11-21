from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import Column, Integer, String, Date, create_engine
import baseballdb as cfg
import pandas as pd


class Base(DeclarativeBase):
    pass


class People(Base):
    __tablename__ = "people"

    playerID = Column(String(9), primary_key=True)
    birthYear = Column(Integer)
    birthMonth = Column(Integer)
    birthDay = Column(Integer)
    birthCountry = Column(String(255))
    birthState = Column(String(255))
    birthCity = Column(String(255))
    deathYear = Column(Integer)
    deathMonth = Column(Integer)
    deathDay = Column(Integer)
    deathCountry = Column(String(255))
    deathState = Column(String(255))
    deathCity = Column(String(255))
    nameFirst = Column(String(255))
    nameLast = Column(String(255))
    nameGiven = Column(String(255))
    weight = Column(Integer)
    height = Column(Integer)
    bats = Column(String(255))
    throws = Column(String(255))
    debutDate = Column(Date)
    finalGameDate = Column(Date)


csv_file = 'People.csv'

# Building the Database Connection String
engineStr = ("mysql+pymysql://" +
             cfg.mysql['user'] + ":" +
             cfg.mysql['password'] + "@" +
             cfg.mysql['host'] + ":3306/" +
             cfg.mysql['db'])

# Creating the Database Engine and Tables
engine = create_engine(engineStr)
Base.metadata.create_all(engine)

# Creating a Session to Interact with the Database
Session = sessionmaker(bind=engine)
session = Session()

# Reading Data from CSV into a Pandas DataFrame
df = pd.read_csv(csv_file)

# Get all existing people
allPeople = session.query(People).all()

# Inserting Data into the Database
for index, row in df.iterrows():

    foundMatch = False

    # Replace NaN values with None
    row = row.where(pd.notna(row), None)

    # Create a new object of the class with data from the row
    new_row = People(**row.to_dict())

    # Remove the previous instance of the player
    for person in allPeople:
        if new_row.playerID == person.playerID:
            foundMatch = True
            session.delete(person)
            break

    # Add the new object to the session
    session.add(new_row)
    if not foundMatch:
        if new_row.nameLast is not None and new_row.nameLast is not None:
            print(new_row.nameFirst + " " + new_row.nameLast)

# Committing the Changes to the Database
session.commit()

# Optionally, you can uncomment the following line to rollback changes
# session.rollback()
