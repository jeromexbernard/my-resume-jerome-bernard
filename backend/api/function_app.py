import os
import json
import azure.functions as func
from azure.cosmos import CosmosClient
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# Check if running locally or in Azure
if os.environ.get("AzureWebJobsScriptRoot"):
    # Running in Azure, use application settings
    connection_string_PriKey = os.environ["ResourceTokenKey"]
    connection_string_URI = os.environ["AzureResumeConnectionStringURI"]
else:
    # Running locally, use local.settings.json
    try:
        with open("local.settings.json", "r") as settings_file:
            settings = json.load(settings_file)
            connection_string_PriKey = settings["Values"]["ResourceTokenKey"]
            connection_string_URI = settings["Values"]["AzureResumeConnectionStringURI"]
    except FileNotFoundError:
        # Default values for testing purposes
        connection_string_PriKey = "mocked_token_key"
        connection_string_URI = "mocked_connection_uri"

# Set the database and container names
database_name = "AzureResume"
container_name = "Counter"

# Get the database and container
client = CosmosClient(connection_string_URI, connection_string_PriKey)
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Get the item from the container with id '1'
    item = container.read_item(item="1", partition_key="1")

    # Increment the count
    item["count"] += 1

    # Update the item in the container
    container.upsert_item(item)

    return func.HttpResponse(
        json.dumps({"count": item["count"]}),
        mimetype="application/json",
        status_code=200
    )