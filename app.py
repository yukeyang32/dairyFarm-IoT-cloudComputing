
from flask import Flask, render_template,request
import json
import os
from azure.cosmos import exceptions, CosmosClient, PartitionKey
from forms import SubmitForm






app = Flask(__name__)
app.config['SECRET_KEY'] = 'cs5412'



endpoint = 'https://dairyfarm-cosmos-account.documents.azure.com:443/'
key = 'QBTn18VZOfCtE2DZP9iAJDDkzPH1XjodRZa7nHNBsIFXgBa54arYsdDyIgsV7vm6wYtecMb9WPP4RhDaPpoCAQ=='

client = CosmosClient(endpoint, key)


database_name = 'dairyCosDB'
database = client.create_database_if_not_exists(id=database_name)


container_name = 'CowContainer'
container = database.create_container_if_not_exists(
    id=container_name, 
    partition_key=PartitionKey(path="/PartitionId"),
    offer_throughput=400
)




@app.route("/", methods=['GET', 'POST'])
def main_page():
    form = SubmitForm()
    if(form.is_submitted()):
        result = request.form
        id = result['cowID']
        items = search(id)
    else:
        items = []

    return render_template('display.html', form=form, items=items)


def search(id):
    query = "SELECT * FROM c WHERE c.data.CowID = \"%s\"" % (id)
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    return items

def delete(id):
    query = "SELECT * FROM c WHERE c.data.CowID = \"%s\"" % (id)
    for item in container.query_items(query=query, enable_cross_partition_query=True):
        container.delete_item(item, partition_key=PartitionKey(path="/PartitionId"))


# @app.route("/table")
# def table():
# 	table = ItemTable(items)
# 	return table.__html__()



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)