from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import os

conn_str = os.environ['DATABASE_URL']
conn_str = conn_str.replace('postgres','postgresql+psycopg2')

print(conn_str)

engine = create_engine(conn_str)
Session = sessionmaker(bind=engine)
session = Session()
# Step 2: Create a MetaData instance
metadata = MetaData()

# Step 3: Reflect the existing gm_shops table
#gm_shops = Table('gm_shops', metadata, autoload_with=engine)
# alternatives?
metadata.reflect(bind=engine)
gm_shops = metadata.tables['gm_shops']