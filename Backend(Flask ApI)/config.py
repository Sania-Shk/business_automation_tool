# This file will store configurations like database URL and secret keys.


class Config:
    SECRET_KEY = "your_secret_key_here"
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:sql-404@localhost/business_data_automation"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
