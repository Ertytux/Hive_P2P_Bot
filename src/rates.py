import requests 
from pycoingecko import CoinGeckoAPI


cg = CoinGeckoAPI()
tkG={'HIVE':'hive','HBD':'hive_dollar'}
tkY={'USD':'usd','CUP':'cup','MLC':'mlc'}

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


def getExchange(amount:str, coinFrom:str, coinTo:str)->str:
    """
    Convert an amount from one currency to another\n
    Currency: USD, CUP, MLC, HIVE, HBD
    """
    try:
        # response = requests.get(yadio_url)
        urlYadio = 'https://api.yadio.io/convert/'
        urlYadioRate = 'https://api.yadio.io/exrates/USD'
        divisorSlash = '/'
        if (coinFrom.upper() in tkY and coinTo.upper() in tkY):
            """Exchange Yadio CUP MLC USD from Yadio"""
            convertUrlYadio = f"{urlYadio}{amount}{divisorSlash}{coinFrom.upper()}{divisorSlash}{coinTo.upper()}"
            response = requests.get(convertUrlYadio)
            result = response.json().get('result')
            rate = response.json().get('rate')
            msg = f"Amount {coinTo.upper()}: {result:.8f} {coinTo.upper()}\nRate: {rate:.8f} USD"
            # return exchange_result
        elif (coinFrom.upper() in tkG and coinTo.upper() in tkG and coinFrom.upper() != coinTo.upper()):
            """Exchange HBD/Hive from Coingecko"""
            idxFrom = tkG.get(coinFrom.upper())
            idxTo = tkG.get(coinTo.upper())
            if idxFrom == 'hive':
                """Exchange Hive to HBD from Coingecko""" 
                pHive=float(cg.get_price(ids=idxFrom, vs_currencies='usd')[idxFrom]['usd'])
                vHive=float(amount)*pHive
                pHBD=float(cg.get_price(ids=idxTo, vs_currencies='usd')[idxTo]['usd'])
                result=vHive/pHBD
                msg = f"Amount {coinTo.upper()}: {result:.8f} {coinTo.upper()}\nRate: {pHBD:.8f} USD"
                #return exchange_result
            else:
                """Exchange HBD to Hive from Coingecko"""
                pHBD=float(cg.get_price(ids=idxFrom, vs_currencies='usd')[idxFrom]['usd'])
                vHBD=float(amount)*pHBD
                pHive=float(cg.get_price(ids=idxTo, vs_currencies='usd')[idxTo]['usd'])
                result=vHBD/pHive
                msg = f"Amount {coinTo.upper()}: {result:.8f} {coinTo.upper()}\nRate: {pHive:.8f} USD"
                # return exchange_result
        elif (coinFrom.upper() in tkY and coinTo.upper() in tkG):
            """Exchange from Yadio to Coingecko"""
            response = requests.get(urlYadioRate)
            pcoin=float(response.json().get('USD').get(coinFrom.upper()))
            vcoin=float(amount)/pcoin
            idxTo = tkG.get(coinTo.upper())
            pcoinGecko=float(cg.get_price(ids=idxTo, vs_currencies='usd')[idxTo]['usd'])
            result=vcoin/pcoinGecko
            msg = f"Amount {coinTo.upper()}: {result:.8f} {coinTo.upper()}\nRate: {pcoinGecko:.8f} USD"
        elif (coinFrom.upper() in tkG and coinTo.upper() in tkY):
            """Exchange from Coingecko to Yadio"""
            response = requests.get(urlYadioRate)
            idxFrom = tkG.get(coinFrom.upper())
            pcoinGecko=float(cg.get_price(ids=idxFrom, vs_currencies='usd')[idxFrom]['usd'])
            vcoin=float(amount)*pcoinGecko
            pcoin=float(response.json().get('USD').get(coinTo.upper()))
            result=vcoin*pcoin
            msg = f"Amount {coinTo.upper()}: {result:.8f} {coinTo.upper()}\nRate: {pcoin:.8f} USD"
        else:
            msg=f"No es posible realizar esa conversión\nIt is not available this exchange!!!"
    except:
        msg=f"No esta disponible\nIt is not available!!!"
    return msg