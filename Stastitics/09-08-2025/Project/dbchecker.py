import pandas as pd
import sqlite3

# Define the path to your database and the table name
db_path = "data/github_trending.db"
table_name = "trending_repos"

# Establish a connection to the database
conn = sqlite3.connect(db_path)

print(f"Printing data from table '{table_name}'...")

# Use pandas to execute the SQL query and load data into a DataFrame
try:
    # The SQL query selects all columns (*) from your table
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    
    # Print the entire DataFrame
    print(df)

except pd.io.sql.DatabaseError:
    print(f"Error: The table '{table_name}' was not found in the database.")
    print("Please check the table name and try again.")

# Close the database connection
conn.close()