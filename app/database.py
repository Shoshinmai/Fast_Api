from .config import setting
from sqlmodel import create_engine, SQLModel, Session

# DATABASE_URL = os.environ.get("")
DATABASE_URL = f"postgresql://{setting.database_username}:{setting.database_password}@{setting.database_hostname}:{setting.database_port}/{setting.database_name}"
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
        
        
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
# while True:
#     try:
#         conn = psycopg2.connect(host = "localhost", database= "fastapiprac", user = "postgres", password= "2416", cursor_factory= RealDictCursor)
#         cursor = conn.cursor()
#         print("Connection to Database is established")
#         break
#     except Exception as error:
#         print("Connection to Database is failed")
#         print("ERROR: ",error)
#         time.sleep(5)