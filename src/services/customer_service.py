from src.dao.customer_dao import CustomerDAO
from typing import Dict, Optional

class CustomerError(Exception):
    pass

class CustomerService:
    def __init__(self):
        self.dao = CustomerDAO()  # instantiate the class

    def add_customer(self, name: str, email: str, phone: str, city: Optional[str] = None) -> Dict:
        existing = self.dao.get_by_email(email)
        if existing:
            raise CustomerError(f"Customer with email {email} already exists")
        return self.dao.create_customer(name, email, phone, city)
