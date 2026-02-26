import datetime
import fabric.functions as fn
import logging

udf = fn.UserDataFunctions()

@udf.function()
def hello_fabric(name: str) -> str:
    logging.info('Python UDF trigger function processed a request.')

    return f"Welcome to Fabric Functions, {name}, at {datetime.datetime.now()}!"

@udf.connection(argName="beclient", alias="LH1")
@udf.function()
def testing_business_events(beclient: fn.FabricBusinessEventsClient) -> str:
    return beclient._credential.get_token().token