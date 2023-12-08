import os
import json
import azure.functions as func
from azure.cosmos import CosmosClient
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="GetResumeCounter")

def main(req: func.HttpRequest) -> func.HttpResponse:
    with open("local.settings.json", "r") as settings_file:
        settings = json.load(settings_file)
        connection_string_PriKey = settings["Values"]["ResourceTokenKey"]
        connection_string_URI = settings["Values"]["AzureResumeConnectionStringURI"]

     # Set the database and container names
    database_name = "AzureResume"
    container_name = "Counter"

    # Get the database and container
    client = CosmosClient(connection_string_URI, connection_string_PriKey)
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)

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