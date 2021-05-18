
from flask import Flask, render_template,request
import json
import os
from azure.cosmos import exceptions, CosmosClient, PartitionKey
from forms import SubmitForm
from PIL import Image
import base64
import io
from datetime import datetime
import matplotlib.pyplot as plt

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


date = []



def draw_graph(items):
    x_axis = [item['data']['time'] for item in items]
    label1 = [item['label'] for item in items]
    label2 = [item['data']['animal_activity'] for item in items]
    label3 = [item['data']['temp_without_drink_cycles'] for item in items]   
    for index, item in enumerate(x_axis):
        x_axis[index] = datetime.strptime(item, '%Y-%m-%d %H:%M:%S')
    zipped_lists = zip(x_axis, label1, label2, label3)
    sorted_pairs = sorted(zipped_lists)
    tuples = zip(*sorted_pairs)
    x_axis, label1, label2, label3 = [ list(tuple) for tuple in  tuples]
    return {"x_axis":x_axis, "label1": label1, "label2": label2, "label3":label3}



@app.route("/", methods=['GET', 'POST'])
def main_page():
    form = SubmitForm()
    img_data = {"x_axis":[], "label1": []}
    if(form.is_submitted()):
        result = request.form
        id = result['cowID']
        items = search(id)
        img_data = draw_graph(items)

    else:
        items = []
    return render_template('display.html', form=form, items=items, img_data=img_data)


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