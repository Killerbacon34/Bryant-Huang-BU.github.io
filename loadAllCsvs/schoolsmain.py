from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import Column, Integer, String, create_engine
import baseballdb as cfg
import pandas as pd


class Base(DeclarativeBase):
    pass


class Schools(Base):
    __tablename__ = "schools"

    schoolID = Column(String(15), primary_key=True)  # required
    school_name = Column(String(255))
    school_city = Column(String(55))
    school_state = Column(String(55))
    school_country = Column(String(55))


csv_file = 'Schools.csv'

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

# Getting existing schools
existingSchools = session.query(Schools).all()

# Inserting Data into the Database
for index, row in df.iterrows():
    foundExistingSchool = False

    # Replace NaN values with None
    row = row.where(pd.notna(row), None)

    # Create a new object of the class with data from the row
    new_row = Schools(**row.to_dict())

    # Add the new object to the session
    for school in existingSchools:
        if (school.schoolID == new_row.schoolID):
            foundExistingSchool = True
            break
    if not foundExistingSchool:
        session.add(new_row)

# Committing the Changes to the Database
session.commit()

# Optionally, you can uncomment the following line to rollback changes
# session.rollback()
