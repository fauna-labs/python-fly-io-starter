from flask import Flask, Response
import os, json
from fauna import fql
from fauna.client import Client
from fauna.encoding import QuerySuccess
import utils


client = Client(secret=os.getenv('FAUNA_SECRET_KEY', 'unknown'))

app = Flask(__name__)

@app.route('/')
def index():
    return json.dumps({
        'greeting': 'Hello Fly'
        })


@app.route('/read', methods=['GET'])
def read():
    try:
        q = fql("""
                order.all() {
                  orderName: .name,
                  customer: .customer.firstName + " " + .customer.lastName,
                  orderProducts {
                    product: .product.name,
                    price,
                    quantity
                  }
                }
                """)
        res: QuerySuccess = client.query(q)
        return utils.generate_response(res.data.data, res.stats)
    except Exception as e:
        return utils.generate_error_response(e)