from random import choice
from string import ascii_letters as s, digits as d

gen_key = lambda: ''.join([choice(s + d) for _ in range(32)])

AUTHORIZATION = 'pbkdf2:sha256:150000$w9eeICL7$cdff5599724cff2ff5882aa34de9b953ace6aaccf9b00ea65cbfbf9bb897c507'  # 000000

SECRET_KEY = gen_key()
JWT_SECRET_KEY = gen_key()
CURRENT_USER = dict()
SESSION = dict()
