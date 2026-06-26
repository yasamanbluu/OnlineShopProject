import csv
from datetime import datetime


def read_orders():  # کل سفارش ها را میخواند
    orders = []

    try:
        with open("data/orders.csv", "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                orders.append(row)
    except FileNotFoundError:
        print("orders.csv was not found.")

    return orders


def orders_count():  # تعداد سفارش ها را گزارش میکند
    orders = read_orders()
    return len(orders)


def total_sales():
    orders = read_orders()
    return sum(int(order["total_price"]) for order in orders)


def report_by_product(product_id):
    orders = read_orders()

    count = 0
    income = 0

    for order in orders:
        if order["product_id"] == product_id:
            count += int(order["quantity"])
            income += int(order["total_price"])
    return {
        "product_id": product_id,
        "sold_count": count,
        "income": income
    }


def report_by_date(start, end):
    orders = read_orders()
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")

    count = 0
    income = 0

    for order in orders:
        order_date = datetime.strptime(order["date"], "%Y-%m-%d")
        if start <= order_date <= end:

            count += 1
            income += int(order["total_price"])

    return {
        "order_count": count,
        "income": income
    }
