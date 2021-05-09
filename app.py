
from flask import Flask, render_template,request
import json
import os
from azure.cosmos import exceptions, CosmosClient, PartitionKey

from flask_table import Table, Col
from forms import SubmitForm

# Declare your table
class ItemTable(Table):
    name = Col('Time')
    activity=Col('Activity')
    temp=Col('temperature')
    description = Col('Label')

# Get some objects
class Item(object):
    def __init__(self, name, description,act,temp):
        self.name = name
        self.description = description
        self.activity = act
        self.temp = temp





app = Flask(__name__)
app.config['SECRET_KEY'] = 'cs5412'



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




@app.route("/", methods=['GET', 'POST'])
def main_page():
    form = SubmitForm()
    if(form.is_submitted()):
        result = request.form
        id = result['cowID']
        items = search(id)
        table = ItemTable(items)
    else:
        table = ItemTable([])
    return render_template('display.html', form=form, Table=table)


def search(id):
    query = "SELECT * FROM c WHERE ARRAY_CONTAINS(c.data,{'CowID': \"%s\"},true)" % (id)
    items = list(container.query_items(query=query,enable_cross_partition_query=True))
    print(query)
    print(items)
    t=[]
    for item in items:
        t.append(Item(item['data'][0]['time'], item['label'], item['data'][0]["animal_activity"],
        item['data'][0]["temp_without_drink_cycles"]))
    return t


# @app.route("/table")
# def table():
# 	table = ItemTable(items)
# 	return table.__html__()



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)