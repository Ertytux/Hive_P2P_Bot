from beem.account import Account
from beem.exceptions import AccountDoesNotExistsException
from beem import Hive
from beembase import operations
from beem.transactionbuilder import TransactionBuilder
from beem.amount import Amount
import json
import dbmanager as dmr
from tools import  genb64U
import pymssql
from config import (hivesqldb, hivesqlpsw, hivesqlserver,
                    hivesqluser, fhbd, fhive,fpp, receptor, 
                    manager, activekey,dHP)


hive = Hive()



async def connectMs(SQLCommand, limit):
    conn = pymssql.connect(server=hivesqlserver,
                           user=hivesqluser,
                           password=hivesqlpsw,
                           database=hivesqldb, timeout=15)
    cursor = conn.cursor()
    cursor.execute(SQLCommand)
    result = cursor.fetchmany(limit)
    conn.close()
    return result


def veryfyHiveUser(hiveuser: str) -> int:
    try:
        isdelegate = Account(hiveuser).get_vesting_delegations(manager)
    except:
        # hiversuser not exist
        return 0
    if len(isdelegate) == 0:
        return 0
    user_delegate_vests = int(isdelegate[0]['vesting_shares']['amount'])
    delegation = hive.vests_to_hp(user_delegate_vests)/1e6
    if delegation >= dHP:
        return 1
    return 0


def beem_reputationHiveUser(hiveuser: str):
    try:
        return Account(hiveuser).get_reputation()
    except:
        return 0


async def reputationHiveUser(hiveuser: str):
    try:
        command = rf"""
    SELECT reputation_ui
    FROM Accounts
    WHERE name='{hiveuser}'    
"""
        res = await connectMs(command, 1)
        return float(res[0][0])
    except:
        return float(0)


async def getFee(userx: str, token: str, amoun: float) -> float:
    user_id, user_hiveuser = await dmr.getUserchatid(userx)
    fee: float = 0.0
    # return fee
    if veryfyHiveUser(user_hiveuser) != 1:
        if token.upper() == 'HBD':
            fee = fpp*amoun + fhbd
        if token.upper() == 'HIVE':
            fee = fpp*amoun + fhive
    return fee


async def verifytransact(memo: str) -> bool:
    try:
        manager_ac = Account(receptor)
        transac = manager_ac.get_account_history(index=-1, limit=1000)
        stext = memo.split("_")
        orderid = stext[0]
        (owner, stype, amouni, tokeni, amouno, tokeno,
         pmethod, taker, chatlink, dstatus, order_date) = await dmr.getOrderdata(orderid)
        sender = owner if stype == 'sell' else taker
        fee = await getFee(sender, tokeni, amouni)

        for tr in transac:
            if tr == None:
                continue
            if tr.get('memo', '') == memo:
                amount_obj = Amount(tr['amount'])
                stamount = f"{amount_obj.amount_decimal:.3f} {amount_obj.symbol}"
                etamount = f"{(amouni+fee):.3f} {tokeni.upper()}"
                if stamount == etamount:
                    return True
        return False
    except AccountDoesNotExistsException:
        return False


def sendHive(hiveuser: str, amount: float, token: str) -> None:
    transfer_op = operations.Transfer(
        **{
            "to": hiveuser,
            "from": receptor,
            "memo": "Thank you for using our HiveP2PBot service!",
            "amount": f"{amount:.3f} {token.upper()}"
        })
    tx = TransactionBuilder(blockchain_instance=hive)
    tx.appendOps(transfer_op)
    tx.appendWif(activekey)
    tx.sign()
    tx.broadcast()


def encodeTrans(amount:float,token:str,memo:str)->str:
    transfer_op =["transfer", {
      'to':manager,
      'amount':f"{amount:.3f} {token.upper()}",
      'memo': memo
      }]
    jst=json.dumps(transfer_op)   
    return genb64U(jst)

