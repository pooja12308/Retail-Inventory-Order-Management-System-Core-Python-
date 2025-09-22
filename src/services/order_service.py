from typing import List, Dict
from src.dao import product_dao, customer_dao, order_dao

class OrderError(Exception):
    pass

def create_order(cust_id: int, items: List[Dict]) -> Dict:
    # check customer exists
    customer = customer_dao.get_by_id(cust_id)
    if not customer:
        raise OrderError(f"Customer {cust_id} not found")

    total_amount = 0
    enriched_items = []

    # check stock and calculate total
    for it in items:
        prod = product_dao.get_product_by_id(it["prod_id"])
        if not prod:
            raise OrderError(f"Product {it['prod_id']} not found")
        if prod["stock"] < it["quantity"]:
            raise OrderError(f"Not enough stock for product {prod['name']}")
        enriched_items.append({"prod_id": prod["prod_id"], "quantity": it["quantity"], "price": prod["price"]})
        total_amount += prod["price"] * it["quantity"]

    # deduct stock
    for it in enriched_items:
        prod = product_dao.get_product_by_id(it["prod_id"])
        product_dao.update_product(it["prod_id"], {"stock": prod["stock"] - it["quantity"]})

    # create order
    order = order_dao.create_order(cust_id, total_amount)
    order_dao.add_order_items(order["order_id"], enriched_items)

    return order_dao.get_order(order["order_id"])

def get_order_details(order_id: int) -> Dict:
    order = order_dao.get_order(order_id)
    if not order:
        raise OrderError(f"Order {order_id} not found")
    return order

def cancel_order(order_id: int) -> Dict:
    order = order_dao.get_order(order_id)
    if not order:
        raise OrderError(f"Order {order_id} not found")
    if order["status"] != "PLACED":
        raise OrderError("Only PLACED orders can be cancelled")

    # restore stock
    for item in order["items"]:
        prod = product_dao.get_product_by_id(item["prod_id"])
        product_dao.update_product(item["prod_id"], {"stock": prod["stock"] + item["quantity"]})

    # update status
    return order_dao.update_order_status(order_id, "CANCELLED")
def complete_order(order_id: int) -> Dict:
    order = order_dao.get_order(order_id)
    if not order:
        raise OrderError(f"Order {order_id} not found")
    if order["status"] != "PLACED":
        raise OrderError("Only PLACED orders can be completed")
    return order_dao.update_order_status(order_id, "COMPLETED")
