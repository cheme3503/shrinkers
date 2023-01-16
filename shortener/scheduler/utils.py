from functools import wraps
from django.db import connection

def db_auto_reconnect(func):
    """Mysql Gone Away 대응"""
    @wraps(func)
    def wrapper(*args,**kwargs):
        try:
            connection.connection.ping()

        except Exception:
            connection.close()

        return  func(*args, **kwargs)

    return wrapper
