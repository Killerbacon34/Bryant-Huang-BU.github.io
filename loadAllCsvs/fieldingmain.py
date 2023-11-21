from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import Column, Integer, String, create_engine
import baseballdb as cfg
import pandas as pd


class Base(DeclarativeBase):
    pass


class Fielding(Base):
    __tablename__ = "fielding"

    fieldingID = Column(Integer, primary_key=True)  # required
    playerID = Column(String(9))
    yearID = Column(Integer)
    teamID = Column(String(3))
    stint = Column(Integer)
    position = Column(String(2))
    f_G = Column(Integer)
    f_GS = Column(Integer)
    f_InnOuts = Column(Integer)
    f_PO = Column(Integer)
    f_A = Column(Integer)
    f_E = Column(Integer)
    f_DP = Column(Integer)
    f_PB = Column(Integer)
    f_WP = Column(Integer)
    f_SB = Column(Integer)
    f_CS = Column(Integer)
    f_ZR = Column(Integer)


csv_file = 'Fielding.csv'

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
    new_row = Fielding(**row.to_dict())

    # Add the new object to the session
    if not (new_row.position == 'OF' and new_row.yearID >= 1954):
        session.add(new_row)

# Committing the Changes to the Database
session.commit()

# Optionally, you can uncomment the following line to rollback changes
# session.rollback()
