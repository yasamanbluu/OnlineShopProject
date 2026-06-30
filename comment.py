from validators import require_text, require_positive_int
from datetime import datetime


class Comment:
    """کلاس کامنت‌ها/نقد و نظرات reviews.csv"""

    def __init__(self, username, product_id, comment_text, rating, date=None):
        self.username = require_text(username, "Username")
        self.product_id = str(product_id)
        self.comment_text = require_text(comment_text, "Comment text")

        # امتیاز باید بین 1 تا 5 باشد
        rating = int(require_positive_int(rating, "Rating"))
        if rating > 5 or rating < 1:
            raise ValueError("Rating must be between 1 and 5")
        self.rating = rating

        # تاریخ
        if date is None:
            self.date = datetime.now().strftime("%Y-%m-%d")
        else:
            self.date = date

    def to_csv_row(self):
        """برای ذخیره در reviews.csv"""
        return {
            "username": self.username,
            "product_id": self.product_id,
            "comment": self.comment_text,
            "rating": self.rating,
            "date": self.date,
        }

