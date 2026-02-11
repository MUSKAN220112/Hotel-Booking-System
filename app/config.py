class Config:
    SECRET_KEY = 'your_secret_key'
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'your_database_uri'

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = 'development_database_uri'

class ProductionConfig(Config):
    DATABASE_URI = 'production_database_uri'

class TestingConfig(Config):
    TESTING = True
    DATABASE_URI = 'testing_database_uri'