from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import Column, Integer, String, create_engine
import baseballdb as cfg
import pandas as pd


class Base(DeclarativeBase):
    pass


class Appearances(Base):
    __tablename__ = "appearances"

    appearancesID = Column(Integer, primary_key=True)
    playerID = Column(String(9))
    yearID = Column(Integer)
    teamID = Column(String(3))
    G_all = Column(Integer)
    GS = Column(Integer)
    G_batting = Column(Integer)
    G_defense = Column(Integer)
    G_p = Column(Integer)
    G_c = Column(Integer)
    G_1b = Column(Integer)
    G_2b = Column(Integer)
    G_3b = Column(Integer)
    G_ss = Column(Integer)
    G_lf = Column(Integer)
    G_cf = Column(Integer)
    G_rf = Column(Integer)
    G_of = Column(Integer)
    G_dh = Column(Integer)
    G_ph = Column(Integer)
    G_pr = Column(Integer)


csv_file = 'Appearances.csv'

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
    new_row = Appearances(**row.to_dict())

    # Add the new object to the session
    session.add(new_row)

# Committing the Changes to the Database
session.commit()

# Optionally, you can uncomment the following line to rollback changes
# session.rollback()
