import datetime
import fabric.functions as fn
import logging

udf = fn.UserDataFunctions()

@udf.function()
def hello_fabric(name: str) -> str:
    logging.info('Python UDF trigger function processed a request.')

    return f"Welcome to Fabric Functions, {name}, at {datetime.datetime.now()}!"


from azure.identity import ManagedIdentityCredential
@udf.function()
def testing_msi_token() -> str:
    # System-assigned managed identity
    credential = ManagedIdentityCredential()

    # Example: get token for UDF
    # token = credential.get_token("https://analysis.windows-int.net/powerbi/api/.default")
    # token = credential.get_token("api://fabric/userdatafunctions/ppe")
    token = credential.get_token("https://eventgrid.azure.net/.default")
    access_token = token.token
    return access_token

  
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import datetime
@udf.connection(argName="myLakehouse", alias="LH1")
@udf.generic_connection(argName="cosmosDb", audienceType="KeyVault")
@udf.function()
def query_data_from_tables(myLakehouse: fn.FabricLakehouseClient, cosmosDb: fn.FabricItem) -> list:
    return "done"


from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import datetime
@udf.generic_connection(argName="cosmosDb", audienceType="KeyVault")
@udf.generic_connection(argName="keyvault", audienceType="CosmosDB")
@udf.function()
def two_generic(keyvault: fn.FabricItem, cosmosDb: fn.FabricItem) -> list:
    return "done"


@udf.connection(argName="myLakehouse", alias="LH1")
@udf.connection(argName="myLakehouse2", alias="TestW")
@udf.function()
def two_data_connection(myLakehouse: fn.FabricLakehouseClient, myLakehouse2: fn.FabricSqlConnection) -> list:
    return "done"

from azure.core.messaging import CloudEvent
from fabric.functions.eventgrid import get_eventgrid_client
@udf.generic_connection(argName="cosmosDb", audienceType="EventGrid", eventgrid_endpoint="https://businesseventstest.westus-1.eventgrid.azure.net", namespace_topic="topic1")
@udf.function()
def event_grid(cosmosDb: fn.FabricItem) -> list:
    client = get_eventgrid_client(cosmosDb, "https://businesseventstest.westus-1.eventgrid.azure.net", namespace_topic="topic1")
    client.send([CloudEvent(source="udf", type="topic1", data={"id": "123"})])

import datetime

@udf.context(argName="udfContext")
@udf.function()
def get_function_invocation_details(udfContext: fn.UserDataFunctionContext) -> str:
    invocation_id = udfContext.invocation_id
    invoking_users_username = udfContext.executing_user['PreferredUsername']
    # Other executing_user keys include: 'Oid', 'TenantId'
 
    return f"Welcome to Fabric Functions, {invoking_users_username}, at {datetime.datetime.now()}! Invocation ID: {invocation_id}"

@udf.context(argName="udfContext")
@udf.generic_connection(argName="cosmosDb", audienceType="KeyVault")
@udf.function()
def get_function_invocation_details_keyvault(udfContext: fn.UserDataFunctionContext, cosmosDb: fn.FabricItem) -> str:
    # logging.info(f"All attributes: {vars(cosmosDb)}")
    
    # Or use __dict__
    logging.info(f"__dict__: {cosmosDb.__dict__}")

    invocation_id = udfContext.invocation_id
    invoking_users_username = udfContext.executing_user['PreferredUsername']
    # Other executing_user keys include: 'Oid', 'TenantId'
 
    return f"Welcome to Fabric Functions, {invoking_users_username}, at {datetime.datetime.now()}! Invocation ID: {invocation_id}"
