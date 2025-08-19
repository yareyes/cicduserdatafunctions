import datetime
import fabric.functions as fn
import logging

udf = fn.UserDataFunctions()

@udf.function()
def hello_fabric(name: str) -> str:
    logging.info('Python UDF trigger function processed a request.')

    return f"Welcome to Fabric Functions, {name}, at {datetime.datetime.now()}!"

# Select 'Manage connections' and add a connection to a Fabric SQL Database 
# Replace the alias "<alias for sql database>" with your connection alias.
@udf.connection(argName="sqlDB",alias="dmtsdb")
@udf.function()
def read_from_sql_db(sqlDB: fn.FabricSqlConnection)-> list:
    '''
    Description: Read employee data from SQL database using sample query.
    
    Args:
        sqlDB (fn.FabricSqlConnection): Fabric SQL database connection.
    
    Returns:
        list: Employee records as tuples with name and department ID.
        
    Example:
        Returns [('John Smith', 31), ('Kayla Jones', 33)]
    '''
    
    # Replace with the query you want to run
    query = "SELECT * FROM (VALUES ('John Smith', 31), ('Kayla Jones', 33)) AS Employee(EmpName, DepID);"

    # Establish a connection to the SQL database
    connection = sqlDB.connect()
    cursor = connection.cursor()

    # Execute the query
    cursor.execute(query)

    # Fetch all results
    results = []
    for row in cursor.fetchall():
        results.append(row)

    # Close the connection
    cursor.close()
    connection.close()
        
    return results





import datetime
# Select 'Manage connections' and add a connection to a Lakehouse.
# Replace the alias "<My Lakehouse alias>" with your connection alias.
@udf.connection(argName="myLakehouse", alias="lake815")
@udf.function()
def query_data_from_tables(myLakehouse: fn.FabricLakehouseClient) -> list:
    '''
    Description: Query employee data from lakehouse tables and return as JSON objects.

    Args:
    - myLakehouse (fn.FabricLakehouseClient): Fabric lakehouse connection

    Returns: list: Employee records as dictionaries with EmpName and DepID fields
    '''
    # Connect to the Lakehouse SQL Endpoint
    connection = myLakehouse.connectToSql()
    
    # Use connection to execute a query
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM (VALUES ('John Smith',  31) , ('Kayla Jones', 33)) AS Employee(EmpName, DepID);")
    
    rows = [x for x in cursor]
    columnNames = [x[0] for x in cursor.description]
    
    # Turn the rows into a json object
    values = []
    for row in rows:
        item = {}
        for prop, val in zip(columnNames, row):
            if isinstance(val, (datetime.date, datetime.datetime)):
                val = val.isoformat()
            item[prop] = val
        values.append(item)

    # Close the connection
    cursor.close()
    connection.close()

    return values



import datetime
#Select 'Manage connections' to connect to a Warehouse
#Replace the alias "<My Warehouse Alias>" with your connection alias.
@udf.connection(argName="myWarehouse", alias="wh1")
@udf.function()
def query_data_from_warehouse(myWarehouse: fn.FabricSqlConnection) -> list:
    '''
    Description: Query employee data from a Fabric warehouse and return as JSON objects.
    
    Args:
        myWarehouse (fn.FabricSqlConnection): Fabric warehouse connection.
    
    Returns:
        list: Employee records as dictionaries with EmpName and DepID fields.
        
    Example:
        Returns [{'EmpName': 'John Smith', 'DepID': 31}, {'EmpName': 'Kayla Jones', 'DepID': 33}]
    '''
    whSqlConnection = myWarehouse.connect()
    # Use connection to execute a query
    cursor = whSqlConnection.cursor()
    cursor.execute(f"SELECT * FROM (VALUES ('John Smith',  31) , ('Kayla Jones', 33)) AS Employee(EmpName, DepID);")
    
    rows = [x for x in cursor]
    columnNames = [x[0] for x in cursor.description]
    # Turn the rows into a json object
    values = []
    for row in rows:
        item = {}
        for prop, val in zip(columnNames, row):
            if isinstance(val, (datetime.date, datetime.datetime)):
                val = val.isoformat()
            item[prop] = val
        values.append(item)
    
    cursor.close()
    whSqlConnection.close()

    return values


import datetime

@udf.context(argName="udfContext")
@udf.function()
def get_function_invocation_details(udfContext: fn.UserDataFunctionContext) -> str:
    '''
    Description: Get function invocation details including user info and invocation ID.
    
    Args:
        udfContext (fn.UserDataFunctionContext): Context containing invocation metadata.
    
    Returns:
        str: Welcome message with username, timestamp, and invocation ID.
        
    Example:
       Returns "Welcome to Fabric Functions, user@example.com, at 2025-07-01 10:30:00! Invocation ID: abc123"
    '''
    invocation_id = udfContext.invocation_id
    invoking_users_username = udfContext.executing_user['PreferredUsername']
    # Other executing_user keys include: 'Oid', 'TenantId'
 
    return f"Welcome to Fabric Functions, {invoking_users_username}, at {datetime.datetime.now()}! Invocation ID: {invocation_id}"




from sklearn.feature_extraction.text import CountVectorizer

@udf.function()
def vectorize_string(text: str) -> str:
    '''
    Description: Vectorize a string of text using CountVectorizer and return vectorized representation.

    Args:
    - text (str): Input text string to be vectorized

    Returns: str: Formatted string containing vectorized text array and feature names
    '''
    try:
        # Initialize the CountVectorizer
        vectorizer = CountVectorizer()
        
        # Fit and transform the input text to vectorize it
        vectorized_text = vectorizer.fit_transform([text])
        vectors = ''.join(str(x) for x in vectorized_text.toarray())
        featurenames= " ,".join(str(x) for x in vectorizer.get_feature_names_out())
        print("Vectorized text:\n", vectorized_text.toarray())
        print("Feature names:\n",vectorizer.get_feature_names_out())
        return "vectorized_text: " + vectors + "\nfeature_names: " + featurenames
    except Exception as e:
        return "An error occurred during vectorization: " + str(e)
