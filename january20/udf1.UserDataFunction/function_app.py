import datetime
import fabric.functions as fn
import logging

udf = fn.UserDataFunctions()

@udf.function()
def hello_fabric(name: str) -> str:
    logging.info('Python UDF trigger function processed a request.')

    return f"Welcome to Fabric Functions, {name}, at {datetime.datetime.now()}!"


import datetime

@udf.connection(argName="myLakehouse", alias="lh1")
@udf.connection(argName="myLakehouse2", alias="lh2")
@udf.generic_connection(argName="keyvault", audienceType="KeyVault")
@udf.function()
def query_data_from_tables(myLakehouse: fn.FabricLakehouseClient, myLakehouse2: fn.FabricLakehouseClient, keyvault: fn.FabricItem) -> str:
    logging.info(myLakehouse.endpoints["sqlendpoint"]["AccessToken"])
    logging.info(myLakehouse2.endpoints["fileendpoint"]["AccessToken"])

    return 'Test Completed'

@udf.connection(argName="myLakehouse", alias="lh1")
@udf.connection(argName="myLakehouse2", alias="lh2")
@udf.function()
def find_max_conn_failures(myLakehouse: fn.FabricLakehouseClient, myLakehouse2: fn.FabricLakehouseClient) -> str:
    logging.info(myLakehouse.endpoints["sqlendpoint"]["AccessToken"])
    logging.info(myLakehouse2.endpoints["fileendpoint"]["AccessToken"])

    return 'Test Completed'

@udf.connection(argName="beclient", alias="be1")
@udf.function()
def testing_business_events(beclient: fn.FabricBusinessEventsClient) -> str:
    beclient.GetBusinessEventsClient()
    return beclient.endpoints["beendpoint"]["AccessToken"]

@udf.connection(argName="beclient", alias="be1")
@udf.function()
def testing_business_events_object(beclient: fn.FabricBusinessEventsClient) -> str:
    # Print internal kwargs on the FabricBusinessEventsClient
    logging.info(f"FabricBusinessEventsClient._internal_kwargs: {beclient._internal_kwargs}")
    
    # Or get the EventGrid client and print its internal kwargs
    client = beclient.GetBusinessEventsClient()
    logging.info(f"FabricEventGridPublisherClient._internal_kwargs: {client._internal_kwargs}")
    
    # Return as string for the response
    return str(beclient._internal_kwargs)

@udf.connection(argName="beclient", alias="be1", allowedEvents=["businessEvent5", "businessEvent2", "businessEvent4"])
@udf.function()
def testing_business_events_client(beclient: fn.FabricBusinessEventsClient) -> str:
    # Print all attributes
    logging.info(f"All attributes: {vars(beclient)}")
    
    # Or use __dict__
    logging.info(f"__dict__: {beclient.__dict__}")
    return str(vars(beclient))

@udf.connection(argName="beclient", alias="be1")
@udf.function()
def publish_business_events(beclient: fn.FabricBusinessEventsClient) -> str:
    client = beclient.GetBusinessEventsClient()

    event_data = {
                    "test": "yadi",
                    "status": "send",
                }

    result = client.GenerateEvent(type= "be_one", version_id="V1", event_data=event_data)
    logging.info(f"Generated Event: {result}")

    return 'Event Sends successfully'