from app.DataBase import db_model
from app.DataBase.db_conn import engine,SessionLocal



db_model.Base.metadata.create_all(bind=engine) 
#  this will create the database tables when the application starts

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()