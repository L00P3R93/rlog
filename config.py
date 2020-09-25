import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or None

    MAIL_SERVER = os.getenv('MAIL_SERVER') or None
    MAIL_PORT = int(os.getenv('MAIL_PORT')) or None
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS').lower() in ['true','on','1']
    MAIL_USERNAME = os.getenv('MAIL_USERNAME') or None
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD') or None

    RLOG_MAIL_SUBJECT_PREFIX = os.getenv('RLOG_MAIL_SUBJECT_PREFIX') or None
    RLOG_MAIL_SENDER = os.getenv('RLOG_MAIL_SENDER') or None
    RLOG_ADMIN = os.getenv('RLOG_ADMIN') or None

    SSL_REDIRECT = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIRES = True

    RLOG_FOLLOWERS_PER_PAGE = 20
    RLOG_POSTS_PER_PAGE = 20
    RLOG_COMMENTS_PER_PAGE = 50
    RLOG_SLOW_DB_QUERY_TIME = 0.5

    MAX_CONTENT_LENGTH = 1024 * 1024
    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.gif']
    UPLOAD_PATH = 'uploads'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        #email errors to admin
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls,'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER,cls.MAIL_PORT),
            fromaddr=cls.RLOG_MAIL_SENDER,
            toaddrs=[cls.RLOG_ADMIN],
            subject=cls.RLOG_MAIL_SUBJECT_PREFIX+' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls,app):
        ProductionConfig.init_app(app)

        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.INFO)
        app.logger.appHandler(syslog_handler)

config = {
    'development' : DevelopmentConfig,
    'testing' : TestingConfig,
    'production' : ProductionConfig,
    'unix' : UnixConfig,

    'default' : DevelopmentConfig
}
