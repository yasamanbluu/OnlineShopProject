import csv


def image_path(product_id):
    with open("data/products.csv", "r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)

        for product in csv_reader:
            if product["product_id"] == product_id:
                return product["image_url"]

    return None
