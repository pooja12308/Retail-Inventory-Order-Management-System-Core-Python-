# src/services/report_service.py
from typing import List, Dict
from datetime import datetime, timedelta
from src.dao import order_dao, product_dao, customer_dao

def top_products(limit: int = 5) -> List[Dict]:
    """
    Return top-selling products by total quantity sold.
    """
    items = order_dao.list_order_items()
    product_sales = {}
    for item in items:
        pid = item["prod_id"]
        qty = item["quantity"]
        product_sales[pid] = product_sales.get(pid, 0) + qty

    # sort by quantity sold
    sorted_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:limit]
    result = []
    for pid, qty in sorted_products:
        product = product_dao.get_product_by_id(pid)
        if product:
            product["total_sold"] = qty
            result.append(product)
    return result

def total_revenue_last_month() -> float:
    """
    Calculate total revenue from orders completed in the last month.
    """
    today = datetime.utcnow()
    last_month = today - timedelta(days=30)
    orders = order_dao.list_orders_after(last_month)
    revenue = sum(order.get("total_amount", 0) for order in orders if order.get("status") == "COMPLETED")
    return revenue

def total_orders_per_customer() -> List[Dict]:
    """
    Return total number of orders per customer.
    """
    customers = customer_dao.list_customers()
    result = []
    for cust in customers:
        orders = order_dao.list_orders_by_customer(cust["cust_id"])
        cust["total_orders"] = len(orders)
        result.append(cust)
    return result

def frequent_customers(min_orders: int = 2) -> List[Dict]:
    """
    Return customers who placed more than `min_orders` orders.
    """
    all_customers = total_orders_per_customer()
    return [c for c in all_customers if c["total_orders"] > min_orders]
