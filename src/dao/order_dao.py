from src.config import get_supabase
from typing import List, Dict, Optional

_sb = get_supabase

def create_order(cust_id: int, total_amount: float, status: str = "PLACED") -> Dict:
    db = _sb()
    db.table("orders").insert({"cust_id": cust_id, "total_amount": total_amount, "status": status}).execute()
    resp = db.table("orders").select("*").eq("cust_id", cust_id).order("order_id", desc=True).limit(1).execute()
    return resp.data[0] if resp.data else {}

def add_order_items(order_id: int, items: List[Dict]):
    db = _sb()
    for item in items:
        db.table("order_items").insert({
            "order_id": order_id,
            "prod_id": item["prod_id"],
            "quantity": item["quantity"],
            "price": item["price"]
        }).execute()

def get_order(order_id: int) -> Optional[Dict]:
    db = _sb()
    order_resp = db.table("orders").select("*").eq("order_id", order_id).limit(1).execute()
    if not order_resp.data:
        return None
    order = order_resp.data[0]

    cust_resp = db.table("customers").select("*").eq("cust_id", order["cust_id"]).limit(1).execute()
    order["customer"] = cust_resp.data[0] if cust_resp.data else {}

    items_resp = db.table("order_items").select("*").eq("order_id", order_id).execute()
    order["items"] = items_resp.data or []

    return order

def update_order_status(order_id: int, status: str) -> Optional[Dict]:
    db = _sb()
    db.table("orders").update({"status": status}).eq("order_id", order_id).execute()
    return get_order(order_id)

def list_order_items() -> List[Dict]:
    """
    Return all order items in the system.
    """
    db = _sb()
    resp = db.table("order_items").select("*").execute()
    return resp.data or []

def list_orders_after(date) -> List[Dict]:
    """
    Return all orders created after the given date (datetime object).
    """
    db = _sb()
    resp = db.table("orders").select("*").gte("order_date", date.isoformat()).execute()
    return resp.data or []

def list_orders_by_customer(cust_id: int) -> List[Dict]:
    """
    Return all orders of a given customer.
    """
    db = _sb()
    resp = db.table("orders").select("*").eq("cust_id", cust_id).execute()
    return resp.data or []
