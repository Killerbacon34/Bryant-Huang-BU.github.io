import pandas as pd


def find_unique_players(file1, file2):
    # Read CSV files into pandas DataFrames
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Extract the "playerID" columns from both DataFrames
    player_ids_file1 = set(df1['schoolID'])
    player_ids_file2 = set(df2['schoolID'])

    # Find values in file1 that do not exist in file2
    unique_players = player_ids_file1 - player_ids_file2

    # Print or return the result
    print("Schools in", file1, "but not in", file2, ":", unique_players)


# Replace 'file1.csv' and 'file2.csv' with the actual file paths
find_unique_players('CollegePlaying.csv', 'Schools.csv')
