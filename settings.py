import os
APP_PATH  = os.path.abspath(os.path.dirname(__file__))
DATA_PATH = os.path.join(APP_PATH, 'data')

pj = os.path.join
pjd = lambda *s: pj(DATA_PATH, *s)
pja = lambda *s: pj(APP_PATH, *s)

DATABASE = 'sqlite:///' + pjd('lego.db')

SECRET_KEY = "dwksdfksdfhgfghf677655676567sfwwe"


