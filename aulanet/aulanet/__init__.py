try:
    import pymysql

    pymysql.install_as_MySQLdb()
except ImportError:
    # Si no está instalado (ej. en Producción con SQLite), no pasa nada.
    pass
