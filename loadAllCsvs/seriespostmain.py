from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import Column, Integer, String, create_engine, Double
import baseballdb as cfg
import pandas as pd


class Base(DeclarativeBase):
    pass


class Teams(Base):
    __tablename__ = "teams"

    teamsID = Column(Integer, primary_key=True)
    teamID = Column(String(3))
    yearID = Column(Integer)
    lgID = Column(String(2))
    divID = Column(String(1))
    franchID = Column(String(3))
    team_name = Column(String(50))
    team_rank = Column(Integer)
    team_G = Column(Integer)
    team_G_home = Column(Integer)
    team_W = Column(Integer)
    team_L = Column(Integer)
    DivWin = Column(String(1))
    WCWin = Column(String(1))
    LgWin = Column(String(1))
    WSWin = Column(String(1))
    team_R = Column(Integer)
    team_AB = Column(Integer)
    team_H = Column(Integer)
    team_2B = Column(Integer)
    team_3B = Column(Integer)
    team_HR = Column(Integer)
    team_BB = Column(Integer)
    team_SO = Column(Integer)
    team_SB = Column(Integer)
    team_CS = Column(Integer)
    team_HBP = Column(Integer)
    team_SF = Column(Integer)
    team_RA = Column(Integer)
    team_ER = Column(Integer)
    team_ERA = Column(Double)
    team_CG = Column(Integer)
    team_SHO = Column(Integer)
    team_SV = Column(Integer)
    team_IPouts = Column(Integer)
    team_HA = Column(Integer)
    team_HRA = Column(Integer)
    team_BBA = Column(Integer)
    team_SOA = Column(Integer)
    team_E = Column(Integer)
    team_DP = Column(Integer)
    team_FP = Column(Double)
    park_name = Column(String(50))
    team_attendance = Column(Integer)
    team_BPF = Column(Integer)
    team_PPF = Column(Integer)


csv_file = 'Teams.csv'

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
    new_row = Teams(**row.to_dict())

    # Add the new object to the session
    session.add(new_row)

# Committing the Changes to the Database
session.commit()

# Optionally, you can uncomment the following line to rollback changes
# session.rollback()
