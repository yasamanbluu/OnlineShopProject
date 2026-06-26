import csv


def add_comment(username, product_id, comment):
    print("comment is saved.")
    with open("data/reviews.csv", "a", newline="", encoding="utf-8") as file:

        csv_writer = csv.writer(file)
        csv_writer.writerow([username, product_id, comment])


def get_comments(product_id):
    comments = []
    with open("data/reviews.csv", "r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            if row["product_id"] == product_id:
                comments.append(row["comment"])
    return comments
