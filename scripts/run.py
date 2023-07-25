# Copyright Fauna, Inc.
# SPDX-License-Identifier: MIT-0

import os
from fauna import fql
from fauna.client import Client
from fauna.encoding import QuerySuccess
from data import customers, stores, products, orders

client = Client(secret=os.getenv("FAUNA_SECRET_KEY", "unknown"))


def create_document(collection, data):
    try:
        res: QuerySuccess = client.query(
            fql(
                """
                let createColl = Collection.byName(${collection}) == null
                if (createColl) {
                  Collection.create({
                    name: ${collection}
                  })
                }
                """,
                collection=collection,
            )
        )

        postProcess = fql("newdoc.id")

        if collection == "product":
            postProcess = fql(
                """
                ${coll}.byId(newdoc.id).update({
                  store: store.byId(newdoc.store)
                })
                """,
                coll=data['coll'],
            )
        elif collection == "order":
            postProcess = fql(
                """
                ${coll}.byId(newdoc.id).update({
                  customer: customer.byId(newdoc.customer),
                  creationDate: Time(newdoc.creationDate),
                  orderProducts: newdoc.orderProducts.map(x=>{
                    Object.assign(x, { product: product.byId(x.product) })
                  })
                })
                """,
                coll=data['coll'],
            )

        res = client.query(
            fql(
                """
                ${data}.map(x=>{
                  if (!${coll}.byId(x.id).exists()) {
                    let newdoc = ${coll}.create(x)
                    ${postProcess}
                  }
                })
                """,
                coll=data['coll'],
                data=data['data'],
                postProcess=postProcess
            )
        )
        print(res.data)
    except Exception as e:
        print(e)



create_document("customer", customers)
create_document("store", stores)
create_document("product", products)
create_document("order", orders)