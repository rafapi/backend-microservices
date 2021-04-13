from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import insert

from src.models import Product


DATABASE_URL = "postgresql+psycopg2://root:root@localhost:35432/main"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# product = Product(id=2, title='ti 3', image='im 3')
product = insert(Product).values(id=3, title='ti 4', image='im 4')

db: Session = SessionLocal()
db.execute(product)
db.commit()
# db.refresh(product)
