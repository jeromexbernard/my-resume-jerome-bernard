import os
import json
from unittest import mock
from azure.functions import HttpRequest, HttpResponse
from backend.api.function_app import http_trigger  # Adjust the import path

def test_http_trigger():
    # Mocking environment variables
    with mock.patch.dict(os.environ, {
        "AzureWebJobsScriptRoot": "mocked_root",
        "ResourceTokenKey": "mocked_token_key",
        "AzureResumeConnectionStringURI": "mocked_connection_uri"
    }):
        # Mocking Cosmos DB client and container
        with mock.patch("api.function_app.CosmosClient") as mock_cosmos_client:  # Adjust the import path
            mock_container = (
                mock_cosmos_client.return_value.get_database_client.return_value.get_container_client.return_value
            )
            mock_container.read_item.return_value = {"id": "1", "partition_key": "1", "count": 0}

            # Mocking HttpRequest
            req = HttpRequest(
                method="GET",
                url="/api/http_trigger",
                route="http_trigger"
            )

            # Invoke the function
            result = http_trigger(req)

            # Assert the response
            assert isinstance(result, HttpResponse)
            assert result.status_code == 200

            # Assert the expected JSON response
            expected_response = {"count": 1}
            assert json.loads(result.get_body().decode("utf-8")) == expected_response

            # Assert that the container.upsert_item was called with the expected arguments
            mock_container.upsert_item.assert_called_once_with({"id": "1", "partition_key": "1", "count": 1})
