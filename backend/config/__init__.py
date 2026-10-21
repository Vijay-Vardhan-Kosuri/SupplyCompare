import pymysql

pymysql.version_info = (2, 2, 7, "final", 0)
pymysql.install_as_MySQLdb()

# Patch Django 6.x minimum MySQL version check to support MySQL 8.0.x
try:
    from django.db.backends.mysql.base import DatabaseWrapper
    DatabaseWrapper.check_database_version_supported = lambda self: None
except ImportError:
    pass
