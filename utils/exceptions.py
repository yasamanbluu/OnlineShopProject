# utils/exceptions.py

# --- Database Layer Exceptions ---

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


# --- Business Logic & Backend Exceptions ---

class OutOfStockError(Exception):
    """Raised when trying to purchase more items than available in stock."""
    pass

class InsufficientBalanceError(Exception):
    """Raised when a user does not have enough balance to complete a purchase."""
    pass

class AuthenticationError(Exception):
    """Raised when username or password is incorrect during login."""
    pass

class UserNotFoundError(Exception):
    """Raised when a user cannot be found in the database."""
    pass

class ProductNotFoundError(Exception):
    """Raised when a product cannot be found in the database."""
    pass

class InvalidDataError(Exception):
    """Raised when provided data (like review rating out of 1-5 bounds) is invalid."""
    pass