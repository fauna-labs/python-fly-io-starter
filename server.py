# Copyright Fauna, Inc.
# SPDX-License-Identifier: MIT-0

from flask import Flask
import os, json
from fauna import fql
from fauna.client import Client
from fauna.encoding import QuerySuccess
import utils


client = Client(secret=os.getenv("FAUNA_SECRET_KEY", "unknown"))

app = Flask(__name__)


@app.route("/")
def index():
    return json.dumps({"greeting": "Hello python-fly-io-starter"})


@app.route("/read", methods=["GET"])
def read():
    try:
        q = fql(
            """
                order.all() {
                  orderName: .name,
                  customer: .customer.firstName + " " + .customer.lastName,
                  orderProducts {
                    product: .product.name,
                    price,
                    quantity
                  }
                }
              """
        )
        res: QuerySuccess = client.query(q)
        return utils.generate_response(res)
    except Exception as e:
        return utils.generate_error_response(e)
