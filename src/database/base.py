import os
import databases
import sqlalchemy
from sqlalchemy.orm import sessionmaker


username = os.getenv('MYSQL_ROOT_USER', "root")
password = os.getenv('MYSQL_ROOT_PASSWORD', 'devpassword')
hostname = os.getenv('MYSQL_HOST', 'mysql')
database_name = os.getenv('MYSQL_DATABASE', 'data_db')
port = os.getenv('MYSQL_PORT', '3306')

DATABASE_URL = "mysql://%s:%s@%s:%s/%s" % (username, password, hostname, port, database_name)
print(DATABASE_URL)
database = databases.Database(DATABASE_URL)

engine = sqlalchemy.create_engine(
    DATABASE_URL
)
Session = sessionmaker(bind=engine)
