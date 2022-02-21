from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# import db.db_models.user_db_model 

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://mauricio:123@localhost:3306/fastapi_playground"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

# if __name__ == '__main__':
#     print('mauricio@localhost:3306')
