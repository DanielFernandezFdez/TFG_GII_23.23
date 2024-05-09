import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'v2s7*fp(z8WUr1hCUR({"-Q|yG5muk`?Nd|Ut@cz2E:ZJ[}0/')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///BDLibros.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', '9.gbPCDn!Ufm&o-a)k-nbEcSImx+.Rkef#{s=AjFsIUeZWr!')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=365*100) 