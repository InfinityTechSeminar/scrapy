from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

'''
Default config
'''
DATABASE = {
    'drivername': 'mysql+pymysql',
    'host': 'localhost',
    'port': '3306',
    'username': 'root',
    'password': 'root',
    'database': 'test',
    'query': {
        'charset': 'utf8mb4',
        'use_unicode': 1
    },
    'debug': False,
    'pool_size': 150,
    'max_overflow': 0
}

'''
Create new connect from settings
@example
    import project.extensions.orm.connection as connection
    from project.extensions.orm import from_settings

    from_settings(settings)
    connection.from_settings(settings)
'''
def from_settings(settings):
    database = settings.get('DATABASE', DATABASE)
    return create_engine(URL(**database), 
        encoding='utf-8', 
        echo=settings.get('MYSQL_DEBUG', False), 
        pool_size=settings.get('MYSQL_POOL_SIZE', 150), 
        max_overflow=settings.get('MYSQL_MAX_OVERFLOW', 0))

'''
Export only method: from_settings
'''
__all__ = ['from_settings']
