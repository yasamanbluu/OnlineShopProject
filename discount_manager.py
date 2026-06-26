import csv


def get_discount(product_id):

    with open("products.csv", "r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for product in csv_reader:
            if product["product_id"] == product_id:
                return int(product["discount"])
    return 0


def final_price(price, discount):
    return price - (price * discount)


def get_final_price(product_id):

    with open("products.csv", "r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for product in csv_reader:
            if product["product_id"] == product_id:
                price = int(product["price"])
                discount = int(product["discount"])
                return final_price(price, discount)

    return None


def update_discount(product_id, new_discount):
    products = []
    with open("products.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for product in reader:
            if product["product_id"] == product_id:
                product["discount"] = str(new_discount)
            products.append(product)

    with open("products.csv", "w", newline="", encoding="utf-8") as file:
        fieldnames = ["product_id", "name", "price",
                      "stock", "category", "discount"]
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)

        csv_writer.writeheader()
        csv_writer.writerows(products)
    print("Discount updated successfully.")
