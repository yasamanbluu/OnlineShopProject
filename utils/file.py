import csv
import os
from utils.exceptions import FileReadError, FileWriteError, RecordNotFoundError

# Define the expected fields based on project requirements
USERS_FIELDS = ['username', 'password', 'balance', 'role']
PRODUCTS_FIELDS = ['product_id', 'name', 'price', 'stock', 'category']
ORDERS_FIELDS = ['username', 'product_id', 'quantity', 'total_price', 'date']


class CSVHandler:
    """A generic class to handle CRUD operations on a single CSV file."""

    def __init__(self, filepath, fieldnames):
        self.filepath = filepath
        self.fieldnames = fieldnames
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Creates the file and directory with headers if it doesn't exist."""
        if not os.path.exists(self.filepath):
            # Ensure the directory exists (e.g., 'data/' folder)
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            try:
                with open(self.filepath, mode='w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                    writer.writeheader()
            except Exception as e:
                raise FileWriteError(f"Could not create file {self.filepath}: {e}")

    def read_all(self):
        """Reads all records from the CSV file and returns a list of dictionaries."""
        records = []
        try:
            with open(self.filepath, mode='r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    records.append(row)
            return records
        except Exception as e:
            raise FileReadError(f"Error reading from {self.filepath}: {e}")

    def write_all(self, records):
        """Overwrites the entire CSV file with the provided list of dictionaries."""
        try:
            with open(self.filepath, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()
                writer.writerows(records)
        except Exception as e:
            raise FileWriteError(f"Error writing to {self.filepath}: {e}")

    def append_record(self, record):
        """Appends a single dictionary record to the end of the CSV file."""
        try:
            with open(self.filepath, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                # Ensure header is written if file was somehow emptied
                if os.path.getsize(self.filepath) == 0:
                    writer.writeheader()
                writer.writerow(record)
        except Exception as e:
            raise FileWriteError(f"Error appending to {self.filepath}: {e}")

    def update_record(self, match_field, match_value, update_data):
        """
        Finds a record where match_field == match_value and updates it with update_data.
        Example: update_record('username', 'hamidi', {'balance': '9000'})
        """
        records = self.read_all()
        updated = False

        for row in records:
            if row.get(match_field) == str(match_value):
                row.update(update_data)
                updated = True
                break

        if not updated:
            raise RecordNotFoundError(f"Record with {match_field}='{match_value}' not found in {self.filepath}")

        self.write_all(records)

    def delete_record(self, match_field, match_value):
        """Deletes a record where match_field == match_value."""
        records = self.read_all()
        initial_count = len(records)

        # Keep all rows except the one matching the delete criteria
        records = [row for row in records if row.get(match_field) != str(match_value)]

        if len(records) == initial_count:
            raise RecordNotFoundError(
                f"Record with {match_field}='{match_value}' not found to delete in {self.filepath}")

        self.write_all(records)


class Database:
    """
    Central Database class that initializes CSVHandlers for all entities.
    Person 1 (Backend) will use an instance of this class to interact with data.
    """

    def __init__(self, data_dir='data'):
        self.users = CSVHandler(os.path.join(data_dir, 'users.csv'), USERS_FIELDS)
        self.products = CSVHandler(os.path.join(data_dir, 'products.csv'), PRODUCTS_FIELDS)
        self.orders = CSVHandler(os.path.join(data_dir, 'orders.csv'), ORDERS_FIELDS)