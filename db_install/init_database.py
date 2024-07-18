from sqlalchemy import create_engine
import pandas as pd
import os

# Define MySQL connection parameters
db_user = os.environ['DB_USER']
db_pass = os.environ['DB_PASSWORD']
db_host = 'localhost'
db_name = 'canada_stats'

# Create SQLAlchemy engine
engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_pass}@{db_host}/{db_name}')

# Test the connection
try:
    engine.connect()
    print("Connected successfully!")
except Exception as e:
    print("Connection failed:", e)


df_h = pd.read_csv('../data/homicides.csv')
df_h.to_sql('homicides', con=engine, if_exists='replace', index=False)

df_pc = pd.read_csv('../data/persons_charged.csv')
df_pc.to_sql('persons_charged', con=engine, if_exists='replace', index=False)

df_pc = pd.read_csv('../data/provinces.csv')
df_pc.to_sql('provinces', con=engine, if_exists='replace', index=False)

print('Data was ingested successfully!!')

# Close the connection
engine.dispose()