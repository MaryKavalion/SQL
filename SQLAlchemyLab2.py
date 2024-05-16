from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from urllib.parse import unquote
from sqlalchemy import text
import pandas as pd

server_name   = "localhost"
database_name = "bookstore"

connection_string = f"DRIVER=ODBC Driver 17 for SQL Server;SERVER={server_name};DATABASE={database_name};Trusted_Connection=yes"
url_string        = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})

print('Connecting to database using URL string:')
unquoted_url = unquote(str(url_string))
print(unquoted_url, '\n')

try:    
    engine = create_engine(url_string)
    with engine.connect() as connection:
        print(f'Successfully connected to {database_name}!')
except Exception as e:
    print('Error while connecting to database:\n')
    print(e)

import pandas as pd

title = input("Search books: ")

parametrized_query = text(
    "SELECT b.Title, c.Cover, s.StoreName, sb.Quantity "
    "FROM Books b "
    "JOIN covers c ON b.ISBN13 = c.ISBN13 "
    "JOIN StockBalance sb ON c.ID = sb.BookID "
    "LEFT JOIN Stores s ON sb.StoreID = s.ID "
    "WHERE b.Title LIKE :title "
    "ORDER BY b.Title"
)

params = {"title": f"%{title}%"}  

df = pd.read_sql(parametrized_query, con=engine, params=params)

print(df)

