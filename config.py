import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    '''
    This is the Base configuration class that allows
    the production, development and testing environments to
    be created and configured.
    '''
    SECRET_KEY = '@neddox1isAwesome'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEFAULT_PER_PAGE = 20
    MAX_PER_PAGE = 100
    DEBUG = True
    ERROR_404_HELP = False


class DevelopmentConfig(Config):
    pg_db_username = 'api'
    pg_db_password = 'password'
    pg_db_name = 'bucketlist'
    pg_db_hostname = 'localhost'

    # PostgreSQL
    SQLALCHEMY_DATABASE_URI = "postgresql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER=pg_db_username,
                                                                                            DB_PASS=pg_db_password,
                                                                                            DB_ADDR=pg_db_hostname,
                                                                                            DB_NAME=pg_db_name)


class TestingConfig(Config):
    TESTING = True
    pg_db_username = 'api'
    pg_db_password = 'password'
    pg_db_name = 'test'
    pg_db_hostname = 'localhost'

    # PostgreSQL
    SQLALCHEMY_DATABASE_URI = "postgresql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER=pg_db_username,
                                                                                            DB_PASS=pg_db_password,
                                                                                            DB_ADDR=pg_db_hostname,
                                                                                            DB_NAME=pg_db_name)


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'bucketlist.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# The above allows us to import all the above configuration in one dictionary.
