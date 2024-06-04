import os

# Bot Main Config
envnhcbchatir = "hcbchat"
hcbchatid = os.environ.get(envnhcbchatir)
envnhbbsupchat = "hcbsup"
hcbsup = os.environ.get(envnhbbsupchat)

envboturl = "hcburl"
boturl = os.environ.get(envboturl)

# read bot token
envnhcbtoken = "hcbtoken"
hcbtoken = os.environ.get(envnhcbtoken)

# HIVESQL
env_hivesqlserver = "hivesqlserver"
env_hivesqluser = "hivesqluser"
env_hivesqlpsw = "hivesqlpsw"
env_hivesqldb = "hivesqldb"

hivesqlserver = os.environ.get(env_hivesqlserver)
hivesqluser = os.environ.get(env_hivesqluser)
hivesqlpsw = os.environ.get(env_hivesqlpsw)
hivesqldb = os.environ.get(env_hivesqldb)

env_bothiveuser = 'bothiveuser'
env_activekey = "activekey"
env_bothivedelegate = 'bothivedelegate'

receptor = os.environ.get(env_bothiveuser)
activekey = os.environ.get(env_activekey)

manager = os.environ.get(env_bothivedelegate)

# Fees
fpp = 0.3e-2
fhbd = 0.05
fhive = 0.17

# Min Delegation to Zero fee
dHP = 50.0


# admins and support
admins = ['ertytux', 'manuphotos']
supports = ['ertytux', 'manuphotos']

# Telegram user ID in blacklist
blacklist = ['5697805901']

# Supported languages
slang = ['es', 'en']

# Communities
communities = {'mycomm': 'hivecuba'}

# HIVE tokens to exchange
tokenAcepted = ['HIVE', 'HBD']
