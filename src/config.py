class DevelopmentConfig():
    DEBUG = True
    MYSQL_HOST = "127.0.0.1"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "admin"
    MYSQL_DB = "flask"

config ={
    'development': DevelopmentConfig
}