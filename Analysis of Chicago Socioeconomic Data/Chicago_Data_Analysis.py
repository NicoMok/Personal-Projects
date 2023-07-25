# ANALYZING CHICAGO SOCIOECONOMIC DATA WITH SQL AND PYTHON
# https://data.cityofchicago.org/Health-Human-Services/Census-Data-Selected-socioeconomic-indicators-in-C/kn9c-c2s2?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkDB0201ENSkillsNetwork20127838-2021-01-01


import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


hostname="localhost"
dbname="socio" # Database name
uname="root"
pwd="Ubc123civil2023!"

######### FUNCTIONS ##########################################################
def create_server_connection(host_name, user_name, user_password):
    # Creates a connection to the MYSQL server.
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection

def create_database(connection, query):
    # Creates a cursor object, then allows you to execute query using cursor.
    # Query must be of the form: CREATE DATABASE db_name
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")
        
def create_db_connection(host_name, user_name, user_password, db_name):
    # This function should only be executed once the database is created.
    # Re-connectsto the MYSQL server, but specifies the database you want to connect to.
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection
##########################################################################

# 1. Read csv data into pandas data frame df.
df = pd.read_csv('https://data.cityofchicago.org/resource/jcxq-k9xf.csv')

# 2. Connect to server
connection = create_server_connection("localhost", "root", 'Ubc123civil2023!')

# 3. Create a database within the server then connect to it.
create_database_query = "CREATE DATABASE SOCIO"
create_database(connection, create_database_query)
connection = create_db_connection("localhost", "root", 'Ubc123civil2023!', 'SOCIO')

# 4. Connect to database
engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
				.format(host=hostname, db=dbname, user=uname, pw=pwd))

df.to_sql("chicago_socioeconomic_data", engine, if_exists='replace', index=False,method="multi")
# Dataframe.sql(name, con, schema=None, if_exists='fail', index=True, index_label=None, chunksize=None, dtype=None, method=None
# Writes dataframe into sql table
# name: name of SQL table to be created from dataframe
# connection: the connection object (which database to connect to)
# if_exists: if table exists, what should be done?
# index=True: write dataframe index as a column.
# method="multi": pass multiple rows of SQL data in single INSERT clause.
#
# to_sql: only works for SQLite. To use it with MySQL, you'll have to use the create_engine
# function and pass that as the connection!

# 5. Check if connection was successful: Count the number of rows within the table
def getAllData(connection):
    statement = """SELECT COUNT(*) FROM chicago_socioeconomic_data;"""
    cursor_obj = connection.cursor() # connect to surver.
    
    cursor_obj.execute(statement) # execute the select statement
    output = cursor_obj.fetchall()
    print(output)
    # Result of print(output): The number of rows within the table
    # table as a tuple.
    #
    # [(78)]
    
connection = create_db_connection("localhost", "root", 'Ubc123civil2023!', 'socio')
getAllData(connection) # get number of rows within the table
connection.close()

# 6. Number of community areas with hardship > 50?
def getNo(connection):
    statement = """SELECT COUNT(*)
                    FROM chicago_socioeconomic_data
                    WHERE hardship_index > 50;"""
    cursor_obj = connection.cursor() # connect to surver.
    
    cursor_obj.execute(statement) # execute the select statement
    output = cursor_obj.fetchall()
    print(output)
    # Result of print(output): The number of rows within the table
    # table as a tuple.
    #
    # [(38)]
    
connection = create_db_connection("localhost", "root", 'Ubc123civil2023!', 'socio')
getNo(connection) # get number of rows within the table
connection.close()

# 7. Max. value of hardship index in dataset.
def getMaxI(connection):
    statement = """SELECT MAX(hardship_index)
                    FROM chicago_socioeconomic_data;
                """
    cursor_obj = connection.cursor() # connect to surver.
    
    cursor_obj.execute(statement) # execute the select statement
    output = cursor_obj.fetchall()
    print(output)
    # Result of print(output): The number of rows within the table
    # table as a tuple.
    #
    # [(98)]
    
connection = create_db_connection("localhost", "root", 'Ubc123civil2023!', 'socio')
getMaxI(connection) # get number of rows within the table
connection.close()

# 8. Community with highest hardship index.
def getMaxC(connection):
    statement = """SELECT community_area_name 
                    FROM chicago_socioeconomic_data
                    WHERE hardship_index=(SELECT MAX(hardship_index) FROM chicago_socioeconomic_data);
                """
    cursor_obj = connection.cursor() # create a cursor object.
    
    cursor_obj.execute(statement) # execute the select statement
    output = cursor_obj.fetchall()
    print(output)
    # Result of print(output):
    #
    # [(Riverdale)]
    
connection = create_db_connection("localhost", "root", 'Ubc123civil2023!', 'socio')
getMaxC(connection) # get number of rows within the table
connection.close()

# 9. Chicago community areas with per capita income > $60,000.
def getIncome(connection):
    statement = """SELECT community_area_name 
                    FROM chicago_socioeconomic_data
                    WHERE per_capita_income_ > 60000;
                """
    cursor_obj = connection.cursor() # create a cursor object.
    
    cursor_obj.execute(statement) # execute the select statement
    output = cursor_obj.fetchall()
    print(output)
    # Result of print(output):
    #
    # [[('Lake View',), ('Lincoln Park',), ('Near North Side',), ('Loop',)]
    
connection = create_db_connection("localhost", "root", 'Ubc123civil2023!', 'socio')
getIncome(connection) # get number of rows within the table
connection.close()

# 10. Scatter plot using the variables hardship_index and per_capita_income_.
# Explain the correlation between the 2 variables.
plot = sns.jointplot(x='per_capita_income_', y='hardship_index', data = df)
plot.show()

# There's a negative correlation between the hardship index and the per capita income.
# As the per capita income increases, the hardship index decreases.
