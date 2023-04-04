import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = True
    DEVELOPMENT = True
    CSRF_ENABLED = True
    # SECRET_KEY = os.getenv("SECRET_KEY", "default-key")


class ProductionConfig(Config):
    DEBUG = False
    DEVELOPMENT = False
    

class StagingConfig(Config):
    DEVELOPMENT = False

class DevelopmentConfig(Config):
    pass

