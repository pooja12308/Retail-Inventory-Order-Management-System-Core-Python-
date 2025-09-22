from src.config import get_supabase
from typing import Optional, Dict, List
_sb = get_supabase

def create_payment(order_id: int, amount: float) -> Dict:
    db = _sb()
    payload = {"order_id": order_id, "amount": amount, "status": "PENDING"}
    db.table("payments").insert(payload).execute()
    resp = db.table("payments").select("*").eq("order_id", order_id).limit(1).execute()
    return resp.data[0] if resp.data else {}

def mark_paid(payment_id: int, method: str) -> Dict:
    db = _sb()
    db.table("payments").update({"status": "PAID", "method": method, "paid_at": "now()"}).eq("payment_id", payment_id).execute()
    resp = db.table("payments").select("*").eq("payment_id", payment_id).limit(1).execute()
    return resp.data[0] if resp.data else {}

def mark_refunded(payment_id: int) -> Dict:
    db = _sb()
    db.table("payments").update({"status": "REFUNDED"}).eq("payment_id", payment_id).execute()
    resp = db.table("payments").select("*").eq("payment_id", payment_id).limit(1).execute()
    return resp.data[0] if resp.data else {}

def get_payment_by_order(order_id: int) -> Optional[Dict]:
    db = _sb()
    resp = db.table("payments").select("*").eq("order_id", order_id).limit(1).execute()
    return resp.data[0] if resp.data else None
