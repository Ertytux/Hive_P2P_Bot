from datetime import datetime
import base64


def is_number(s: str) -> bool:
    """ Returns True if string is a number. """
    try:
        float(s)
        return True
    except ValueError:
        return False


def getHoursfromDate(strdate: str) -> int:
    now = datetime.now()
    tmk = datetime.strptime(strdate, '%Y-%m-%d %H:%M:%S')
    dtime = now-tmk
    return int((dtime.days*86400+dtime.seconds)//3600)


b64u_lookup = {'/': '_', '_': '/', '+': '-', '-': '+', '=': '.', '.': '='}
def btoa(x): return base64.b64decode(x)
def atob(x): return base64.b64encode(bytes(x, 'utf-8')).decode('utf-8')


def genb64U(x: str) -> str:
    lt = list(x)
    tro = []
    for el in lt:
        em = b64u_lookup.get(el, el)
        tro.append(em)
    return "".join(tro)


