import requests 
from pycoingecko import CoinGeckoAPI


cg = CoinGeckoAPI()
tkG={'HIVE':'hive','HBD':'hive_dollar'}

yadio_url = 'https://api.yadio.io/exrates/USD'

def getPrices()->str:
    try:
        response = requests.get(yadio_url)
        pCUP=float(response.json().get('USD').get('CUP'))
        pMLC=float(response.json().get('USD').get('MLC'))
        idx=tkG.get('HIVE')
        pHive=1.0/float(cg.get_price(ids=idx, vs_currencies='usd')[idx]['usd'])
        idx=tkG.get('HBD')
        pHBD=1.0/float(cg.get_price(ids=idx, vs_currencies='usd')[idx]['usd'])
        msg=rf"""
1 USD  = {pCUP:.2f} CUP, {pMLC:.4f} MLC, {pHive:.4f} HIVE, {pHBD:.4f} HBD, {1.0:.4f} USD

1 CUP  = {pCUP/pCUP:.2f} CUP, {pMLC/pCUP:.4f} MLC, {pHive/pCUP:.4f} HIVE, {pHBD/pCUP:.4f} HBD, {1.0/pCUP:.4f} USD

1 MLC  = {pCUP/pMLC:.2f} CUP, {pMLC/pMLC:.4f} MLC, {pHive/pMLC:.4f} HIVE, {pHBD/pMLC:.4f} HBD, {1.0/pMLC:.4f} USD

1 HIVE = {pCUP/pHive:.2f} CUP, {pMLC/pHive:.4f} MLC, {pHive/pHive:.4f} HIVE, {pHBD/pHive:.4f} HBD, {1.0/pHive:.4f} USD

1 HBD  = {pCUP/pHBD:.2f} CUP, {pMLC/pHBD:.4f} MLC, {pHive/pHBD:.4f} HIVE, {pHBD/pHBD:.4f} HBD, {1.0/pHBD:.4f} USD
"""
    except:
        msg="No disponible//Not available!!!"
    return msg

def getPrice(coin:str)->str:
    try:
        response = requests.get(yadio_url)
        pcoin=float(response.json().get('USD').get(coin.upper()))
        idx=tkG.get('HIVE')
        pHive=1.0/float(cg.get_price(ids=idx, vs_currencies='usd')[idx]['usd'])
        idx=tkG.get('HBD')
        pHBD=1.0/float(cg.get_price(ids=idx, vs_currencies='usd')[idx]['usd'])
        msg=rf"""
1 USD  = {pcoin:.8f} {coin.upper()}, {pHive:.8f} HIVE, {pHBD:.8f} HBD, {1.0:.8f} USD

1 {coin.upper()}  = {1.0:.8f} {coin.upper()}, {pHive/pcoin:.8f} HIVE, {pHBD/pcoin:.8f} HBD, {1.0/pcoin:.8f} USD


"""
    except:
        msg="No esta disponible//It is not available!!!"
    return msg


