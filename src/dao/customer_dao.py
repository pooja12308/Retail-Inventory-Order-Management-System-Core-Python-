# src/dao/customer_dao.py
from src.config import get_supabase
from typing import Optional, Dict, List

_sb = get_supabase

def create_customer(name: str, email: str, phone: str, city: str = None) -> Dict:
    db = _sb()
    payload = {"name": name, "email": email, "phone": phone}
    if city:
        payload["city"] = city
    db.table("customers").insert(payload).execute()
    resp = db.table("customers").select("*").eq("email", email).limit(1).execute()
    return resp.data[0] if resp.data else {}

def get_by_id(cust_id: int) -> Optional[Dict]:
    db = _sb()
    resp = db.table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
    return resp.data[0] if resp.data else None

def list_customers(limit: int = 100) -> List[Dict]:
    db = _sb()
    resp = db.table("customers").select("*").order("cust_id").limit(limit).execute()
    return resp.data or []
