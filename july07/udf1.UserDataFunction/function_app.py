import fabric.functions as fn
import logging

udf = fn.UserDataFunctions()

import psutil
import json
import sys

@udf.function()
def return_list(data: list) -> list:
    return data

@udf.function()
def return_data(size: int, data: list) -> str:
    try:
        ram = psutil.virtual_memory()
        logging.info(f"RAM START: {ram}")
        size_bytes = int(size) * 1024 * 1024
        logging.info(f"Setting bytearray size to: {size} bytes")
        data_new = bytearray(size_bytes)
        logging.info(f"Size of Data: {sys.getsizeof(data_new) / (1024 * 1024)} MB")
        logging.info(f"RAM NEW: {psutil.virtual_memory()} MB")
        return "Success"
    except Exception as e:
        logging.error(f"Error: {e}")
        return "Error"


# This samples converts the input 2D list to a numpy array. The output is normalized to the range [0, 1] and we calculate the mean of each column.
# Complete these steps before testing this function
# 1. Select library management and add numpy library
# 2. Pass input as a list of lists, an example to use for this sample:
# [1, 2, 3, 4, 5]

import numpy as np
import json 

@udf.function()
def transform_data(data: list)-> dict:

    # Convert the 2D list to a numpy array
    np_data = np.array(data)

    # Normalize the data (scale values to range [0, 1])
    min_vals = np.min(np_data, axis=0)
    max_vals = np.max(np_data, axis=0)
    normalized_data = (np_data - min_vals) / (max_vals - min_vals)
    # Calculate the mean of each column
    column_means = np.mean(np_data, axis=0)
    norm = np.array(normalized_data)

    return { "NormalizedData": norm.tolist(), "Mean": float(column_means) }

import time

@udf.function()
def sleep(data: int) -> str:
    time.sleep(data)
    return f"Slept for {data} seconds!"

import json
import sys
@udf.function()
def generate_json_array(nums: int)-> dict:
    numbers = list(range(nums + 1))
    json_array = json.dumps(numbers)
    size = sys.getsizeof(json_array) / (1024 * 1024)
    logging.info(f"Size of payload: {size} MB")
    return json_array



# This sample reads data from a table in a lakehouse 
# Complete these steps before testing this function
# 1. Select 'Manage connections' and add a connection to a Lakehouse 

import datetime

# Replace the alias "<My Lakehouse alias>" with your connection alias.
@udf.connection(argName="myLakehouse", alias="lake1")
@udf.function()
def query_data_from_tables(myLakehouse: fn.FabricLakehouseClient) -> list:
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

