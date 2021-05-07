
from flask import Flask
import json
import os
from azure.cosmos import exceptions, CosmosClient, PartitionKey



app = Flask(__name__)



endpoint = 'https://dairyfarm-cosmos-account.documents.azure.com:443/'
key = 'QBTn18VZOfCtE2DZP9iAJDDkzPH1XjodRZa7nHNBsIFXgBa54arYsdDyIgsV7vm6wYtecMb9WPP4RhDaPpoCAQ=='

client = CosmosClient(endpoint, key)


database_name = 'dairyCosDB'
database = client.create_database_if_not_exists(id=database_name)


container_name = 'dairyContainer'
container = database.create_container_if_not_exists(
    id=container_name, 
    partition_key=PartitionKey(path="/lastName"),
    offer_throughput=400
)


@app.route("/")
def hello():
	query = "SELECT * FROM c WHERE c.id = '0f3077d3-c60c-4d5f-a01d-58e06127ad25' "
	items = list(container.query_items(
	query=query,
	enable_cross_partition_query=True
	))
	request_charge = container.client_connection.last_response_headers['x-ms-request-charge']

	return 'Query returned {0} items. Operation consumed {1} request units'.format(len(items), request_charge)


