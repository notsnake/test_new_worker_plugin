class AuthenticationException(Exception):
    """Wrong user name or password"""
    pass

class NotAvailableException(Exception):
    """Server is not available"""

    pass