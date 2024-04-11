from .local import *
import dj_database_url

DEBUG = False


DATABASES= {'default': dj_database_url.parse(env('DATABASE_URL'))}


# set admin
ADMINS = (
 ('Ejeh Faith', 'entireandfit@gmail.com'), ('Big Steve', 'mrejembistephen@gmail.com')
)
ALLOWED_HOSTS = ['*']