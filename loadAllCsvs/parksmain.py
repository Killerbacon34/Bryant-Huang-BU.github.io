from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import Column, String, create_engine
import baseballdb as cfg
import pandas as pd


class Base(DeclarativeBase):
    pass


class Parks(Base):
    __tablename__ = "parks"

    parkID = Column(String(255), primary_key=True)  # required
    park_alias = Column(String(255))
    park_name = Column(String(255))
    city = Column(String(255))
    state = Column(String(255))
    country = Column(String(255))


csv_file = 'Parks.csv'

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

# Get all existing parks
allParks = session.query(Parks).all()

# Inserting Data into the Database
for index, row in df.iterrows():

    foundMatch = False

    # Replace NaN values with None
    row = row.where(pd.notna(row), None)

    # Create a new object of the class with data from the row
    new_row = Parks(**row.to_dict())

    # Remove the previous instance of the park
    for park in allParks:
        if new_row.parkID == park.parkID:
            foundMatch = True
            session.delete(park)
            break

    # Add the new object to the session
    session.add(new_row)
    if not foundMatch:
        if new_row.park_name is not None:
            print(new_row.park_name)

# Committing the Changes to the Database
session.commit()

# Optionally, you can uncomment the following line to rollback changes
# session.rollback()
