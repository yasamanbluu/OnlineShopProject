
class DatabaseError(Exception):
    """Base class for all database-related errors."""
    pass

class FileReadError(DatabaseError):
    """Raised when there is an issue reading the CSV file."""
    pass

class FileWriteError(DatabaseError):
    """Raised when there is an issue writing to the CSV file."""
    pass

class RecordNotFoundError(DatabaseError):
    """Raised when a specific record is not found during an update or delete operation."""
    pass

# Business logic exceptions that might be triggered by database state
class OutOfStockError(Exception):
    """Raised when trying to purchase more items than available in stock."""
    pass

class UserNotFoundError(Exception):
    """Raised when a user cannot be found in the database."""
    pass

class ProductNotFoundError(Exception):
    """Raised when a product cannot be found in the database."""
    pass