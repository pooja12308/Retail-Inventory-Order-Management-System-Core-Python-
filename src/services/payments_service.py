from src.dao import payment_dao, order_dao

class PaymentError(Exception):
    pass

def create_payment_for_order(order_id: int):
    order = order_dao.get_order(order_id)
    if not order:
        raise PaymentError("Order not found")
    return payment_dao.create_payment(order_id, order["total_amount"])

def pay_order(order_id: int, method: str):
    payment = payment_dao.get_payment_by_order(order_id)
    if not payment:
        raise PaymentError("Payment record not found")
    payment = payment_dao.mark_paid(payment["payment_id"], method)
    order_dao.update_order_status(order_id, "COMPLETED")
    return payment

def refund_order(order_id: int):
    payment = payment_dao.get_payment_by_order(order_id)
    if not payment:
        raise PaymentError("Payment record not found")
    payment = payment_dao.mark_refunded(payment["payment_id"])
    return payment
