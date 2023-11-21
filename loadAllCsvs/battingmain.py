from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import Column, Integer, String, create_engine
import baseballdb as cfg
import pandas as pd


class Base(DeclarativeBase):
    pass


class Batting(Base):
    __tablename__ = "batting"

    battingID = Column(Integer, primary_key=True)  # required
    playerID = Column(String(9))
    yearID = Column(Integer)
    stint = Column(Integer)
    teamID = Column(String(3))
    b_G = Column(Integer)
    b_AB = Column(Integer)
    b_R = Column(Integer)
    b_H = Column(Integer)
    b_2B = Column(Integer)
    b_3B = Column(Integer)
    b_HR = Column(Integer)
    b_RBI = Column(Integer)
    b_SB = Column(Integer)
    b_CS = Column(Integer)
    b_BB = Column(Integer)
    b_SO = Column(Integer)
    b_IBB = Column(Integer)
    b_HBP = Column(Integer)
    b_SH = Column(Integer)
    b_SF = Column(Integer)
    b_GIDP = Column(Integer)


csv_file = 'Batting.csv'

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
    new_row = Batting(**row.to_dict())

    # Add the new object to the session
    session.add(new_row)

# Committing the Changes to the Database
session.commit()

# Optionally, you can uncomment the following line to rollback changes
# session.rollback()
