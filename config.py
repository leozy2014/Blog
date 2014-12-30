import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY = 'HELLOSSSDSFWEJHEFKJHJIJIDADAYANYAHANAHAN'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True


class Dev(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'data.db')
    DEBUG = True



config = {'Default':Dev,
          'Dev':Dev,
          }
