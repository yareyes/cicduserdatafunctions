# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {}
# META }

# CELL ********************

# Get functions
myFunctions = notebookutils.udf.getFunctions('udf1', '38fc12c8-cf17-4dc4-b28f-21c3fd1c7a57')

# Invoke the function
# UPDATE BELOW: Update the request body based on the inputs to your function
myFunctions.hello_fabric(name = "string")



# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
