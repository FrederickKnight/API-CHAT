class AppError(Exception):
    def __init__(self, error: str, message: str, details: str = ""):
        self.error = error
        self.message = message
        self.details = details

class ValidationError(AppError):
    def __init__(self, details: str = "Invalid input data"):
        super().__init__("Validation Error", "Invalid data provided", details)

class DatabaseError(AppError):
    def __init__(self, details: str = "Database operation failed"):
        super().__init__("Database Error", "A database error occurred", details)
        
class AttributeError(AppError):
    def __init__(self, details: str = "Expected a valid attribute"):
        super().__init__("Attribute Error", "Invalid attribute in query", details)
        
class VersionError(AppError):
    def __init__(self, details: str = "The given Version of the API is incorrect or null"):
        super().__init__("Version Error", "Invalid versioning in API", details)
        
class InvalidIDError(AppError):
    def __init__(self, details: str = "Expected a number/interger id"):
        super().__init__("Invalid ID Error", "Invalid ID provided", details)

class InvalidFile(AppError):
    def __init__(self, details: str = "Expected a valid file"):
        super().__init__("Invalid file", "Invalid File provided, or not File at all", details)