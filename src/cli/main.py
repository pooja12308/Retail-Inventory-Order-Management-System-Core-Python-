import argparse
import json
from src.services import product_service, order_service
from src.dao import product_dao, customer_dao

# ----------------- Product Commands -----------------
class cmd_product:
    def cmd_product_add(self, args):
        try:
            p = product_service.add_product(args.name, args.sku, args.price, args.stock, args.category)
            print("Created product:")
            print(json.dumps(p, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    def cmd_product_list(self, args):
        ps = product_dao.list_products(limit=100)
        print(json.dumps(ps, indent=2, default=str))

# ----------------- Customer Commands -----------------
def cmd_customer_add(args):
    try:
        c = customer_dao.create_customer(args.name, args.email, args.phone, args.city)
        print("Created customer:")
        print(json.dumps(c, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

# ----------------- Order Commands -----------------
class cmd_order:
    def cmd_order_create(self, args):
        items = []
        for item in args.item:
            try:
                pid, qty = item.split(":")
                items.append({"prod_id": int(pid), "quantity": int(qty)})
            except Exception:
                print("Invalid item format:", item)
                return
        try:
            ord = order_service.create_order(args.customer, items)
            print("Order created:")
            print(json.dumps(ord, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    def cmd_order_show(self, args):
        try:
            o = order_service.get_order_details(args.order)
            print(json.dumps(o, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    def cmd_order_cancel(self, args):
        try:
            o = order_service.cancel_order(args.order)
            print("Order cancelled (updated):")
            print(json.dumps(o, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    def cmd_order_complete(self, args):
        try:
            o = order_service.complete_order(args.order)
            print("Order completed:")
            print(json.dumps(o, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

# ----------------- Payment Commands -----------------
class cmd_payment:
    def cmd_pay_order(self, args):
        from src.services import payment_service
        try:
            p = payment_service.pay_order(args.order, args.method)
            print("Payment completed:")
            print(json.dumps(p, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    def cmd_refund_order(self, args):
        from src.services import payment_service
        try:
            p = payment_service.refund_order(args.order)
            print("Payment refunded:")
            print(json.dumps(p, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

# ----------------- Report Commands -----------------
class cmd_report:
    def top_products(self, args):
        from src.services import report_service
        data = report_service.top_products(limit=args.limit)
        print(json.dumps(data, indent=2, default=str))

    def revenue_last_month(self, args):
        from src.services import report_service
        total = report_service.total_revenue_last_month()
        print(f"Total revenue last month: {total}")

    def total_orders(self, args):
        from src.services import report_service
        data = report_service.total_orders_per_customer()
        print(json.dumps(data, indent=2, default=str))

    def frequent_customers(self, args):
        from src.services import report_service
        data = report_service.frequent_customers(min_orders=args.min_orders)
        print(json.dumps(data, indent=2, default=str))

# ----------------- Build CLI Parser -----------------
def build_parser():
    cp = cmd_product()
    co = cmd_order()
    cpay = cmd_payment()
    crep = cmd_report()

    parser = argparse.ArgumentParser(prog="retail-cli")
    sub = parser.add_subparsers(dest="cmd")

    # Product
    p_prod = sub.add_parser("product")
    pprod_sub = p_prod.add_subparsers(dest="action")
    addp = pprod_sub.add_parser("add")
    addp.add_argument("--name", required=True)
    addp.add_argument("--sku", required=True)
    addp.add_argument("--price", type=float, required=True)
    addp.add_argument("--stock", type=int, default=0)
    addp.add_argument("--category", default=None)
    addp.set_defaults(func=cp.cmd_product_add)
    listp = pprod_sub.add_parser("list")
    listp.set_defaults(func=cp.cmd_product_list)

    # Customer
    pcust = sub.add_parser("customer")
    pcust_sub = pcust.add_subparsers(dest="action")
    addc = pcust_sub.add_parser("add")
    addc.add_argument("--name", required=True)
    addc.add_argument("--email", required=True)
    addc.add_argument("--phone", required=True)
    addc.add_argument("--city", default=None)
    addc.set_defaults(func=cmd_customer_add)

    # Order
    porder = sub.add_parser("order")
    porder_sub = porder.add_subparsers(dest="action")
    createo = porder_sub.add_parser("create")
    createo.add_argument("--customer", type=int, required=True)
    createo.add_argument("--item", required=True, nargs="+")
    createo.set_defaults(func=co.cmd_order_create)
    showo = porder_sub.add_parser("show")
    showo.add_argument("--order", type=int, required=True)
    showo.set_defaults(func=co.cmd_order_show)
    cano = porder_sub.add_parser("cancel")
    cano.add_argument("--order", type=int, required=True)
    cano.set_defaults(func=co.cmd_order_cancel)
    completeo = porder_sub.add_parser("complete")
    completeo.add_argument("--order", type=int, required=True)
    completeo.set_defaults(func=co.cmd_order_complete)

    # Payment
    ppay = sub.add_parser("payment")
    ppay_sub = ppay.add_subparsers(dest="action")
    payo = ppay_sub.add_parser("pay")
    payo.add_argument("--order", type=int, required=True)
    payo.add_argument("--method", required=True, choices=["Cash", "Card", "UPI"])
    payo.set_defaults(func=cpay.cmd_pay_order)
    refundo = ppay_sub.add_parser("refund")
    refundo.add_argument("--order", type=int, required=True)
    refundo.set_defaults(func=cpay.cmd_refund_order)

    # Report
    prep = sub.add_parser("report")
    prep_sub = prep.add_subparsers(dest="action")
    top_prod = prep_sub.add_parser("top-products")
    top_prod.add_argument("--limit", type=int, default=5)
    top_prod.set_defaults(func=crep.top_products)
    revenue = prep_sub.add_parser("revenue-last-month")
    revenue.set_defaults(func=crep.revenue_last_month)
    total_orders = prep_sub.add_parser("total-orders")
    total_orders.set_defaults(func=crep.total_orders)
    freq_cust = prep_sub.add_parser("frequent-customers")
    freq_cust.add_argument("--min-orders", type=int, default=2)
    freq_cust.set_defaults(func=crep.frequent_customers)

    return parser

# ----------------- Main -----------------
def main():
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return
    args.func(args)

if __name__ == "__main__":
    main()
