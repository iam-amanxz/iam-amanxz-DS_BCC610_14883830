# importing
import pymongo
import json
import pandas as pd
import os

# csv path
dirname = os.path.dirname(__file__)
file = os.path.join(dirname, 'co-emissions.csv')

# reading csv and assigning to 'data'
data = pd.read_csv(file)

################################ clean up ###############################
# dropping all columns before 1980 (1980 - 2017 remains)
data.drop(data[data.Year < 2000].index, inplace=True)

# dropping rows with all null values in rows
data.dropna(how="all", inplace=True)

# dropping rows with all null values in columns
data.dropna(axis="columns", how="all", inplace=True)

# filling NA values
data["Entity"].fillna("No Country", inplace=True)
data["Code"].fillna("No Code", inplace=True)
data["Year"].fillna("No Year", inplace=True)
data["Per capita CO2 emissions (tonnes per capita)"].fillna(0, inplace=True)

# Sort by Year && Country
data.sort_values(["Year", "Entity"], inplace=True)

# renaming columns
data.rename(columns={"Entity": "Country",
                     "Per capita CO2 emissions (tonnes per capita)": "CO2 emissions (metric tons)"},
            inplace=True)

# changing 'year' column datatype to 'str'
data = data.astype({"Year": str})
####################################################################################
################################ Storing to Database ###############################
# database connection setup
client = ('mongodb://localhost:27017/')
mongo_client = pymongo.MongoClient(client)
database = mongo_client['emission-data']
emission_collection = database['emission']

# converting 'data' to JSON
records = json.loads(data.T.to_json()).values()

# inserting into mongodb
try:
    emission_collection.insert_many(records)
    print('Database created successfully')
except pymongo.errors.ServerSelectionTimeoutError as err:
    print(err)

mongo_client.close()
