from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import Column, Integer, String, create_engine, Double
import baseballdb as cfg
import pandas as pd


class Base(DeclarativeBase):
    pass


class AwardsShare(Base):
    __tablename__ = "awardsshare"

    awardsshareID = Column(Integer, primary_key=True)
    awardID = Column(String(255))
    yearID = Column(Integer)
    playerID = Column(Integer)
    lgID = Column(String(2))
    pointsWon = Column(Double)
    pointsMax = Column(Integer)
    votesFirst = Column(Double)

# Run once for awardsshareplayers, once for awardssharemanagers
csv_file = 'AwardsSharePlayers.csv'

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

# Inserting Data into the Database
for index, row in df.iterrows():
    # Replace NaN values with None
    row = row.where(pd.notna(row), None)

    # Create a new object of the class with data from the row
    new_row = AwardsShare(**row.to_dict())

    # Add the new object to the session
    session.add(new_row)

# Committing the Changes to the Database
session.commit()

# Optionally, you can uncomment the following line to rollback changes
# session.rollback()
