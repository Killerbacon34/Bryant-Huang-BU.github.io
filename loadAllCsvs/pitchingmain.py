from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import Column, Integer, String, create_engine, Double
import baseballdb as cfg
import pandas as pd


class Base(DeclarativeBase):
    pass


class Pitching(Base):
    __tablename__ = "pitching"

    pitchingID = Column(Integer, primary_key=True)  # required
    playerID = Column(String(9))
    yearID = Column(Integer)
    stint = Column(Integer)
    teamID = Column(String(3))

    p_W = Column(Integer)
    p_L = Column(Integer)
    p_G = Column(Integer)
    p_GS = Column(Integer)
    p_CG = Column(Integer)
    p_SHO = Column(Integer)
    p_SV = Column(Integer)
    p_IPOuts = Column(Integer)
    p_H = Column(Integer)
    p_ER = Column(Integer)
    p_HR = Column(Integer)
    p_BB = Column(Integer)
    p_SO = Column(Integer)
    p_BAOpp = Column(Double)
    p_ERA = Column(Double)
    p_IBB = Column(Integer)
    p_WP = Column(Integer)
    p_HBP = Column(Integer)
    p_BK = Column(Integer)
    p_BFP = Column(Integer)
    p_GF = Column(Integer)
    p_R = Column(Integer)
    p_SH = Column(Integer)
    p_SF = Column(Integer)
    p_GIDP = Column(Integer)


csv_file = 'Pitching.csv'

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
    new_row = Pitching(**row.to_dict())

    # Add the new object to the session
    session.add(new_row)

# Committing the Changes to the Database
session.commit()

# Optionally, you can uncomment the following line to rollback changes
# session.rollback()
