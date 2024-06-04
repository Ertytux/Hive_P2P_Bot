import aiosqlite as dbm

from datetime import datetime


userfile = "./db/users.db"


async def checkUser(usern: str) -> bool:
    kDB = await dbm.connect(userfile)
    cursor = await kDB.execute(rf"select * from users where username='{usern}';")
    row = await cursor.fetchone()
    await cursor.close()
    await kDB.close()

    if row == None:
        return False
    if row[0] == None:
        return False
    return True
# OK


async def getUserInfo(usern: str) -> dict:
    kDB = await dbm.connect(userfile)
    cursor = await kDB.execute(rf"select hiveuser, norders from users where username='{usern}';")
    a,b = tuple(await cursor.fetchone())
    await cursor.close()
    await kDB.close()    
    try:
        return {'hiveuser': a, 'norders': int(b)}
    except:
        return {}


async def getUserchatid(usern: str) -> tuple:
    kDB = await dbm.connect(userfile)
    cursor = await kDB.execute(rf"select chatid,hiveuser from users where username='{usern}';")
    row = await cursor.fetchone()
    await cursor.close()
    await kDB.close()
    return tuple(row)
# OK


async def getUserNorder(usern: str) -> int:
    kDB = await dbm.connect(userfile)
    command = f"""
SELECT norders FROM users WHERE username='{usern}';
"""
    cursor = await kDB.execute(command)
    row = await cursor.fetchone()
    await cursor.close()
    await kDB.close()
    return int(row[0])
# OK


async def setUserchatid(usern: str, chatid: int) -> None:
    kDB = await dbm.connect(userfile)
    commad = f"""
REPLACE INTO users (username,chatid,status,norders,reputation,amounts) VALUES ('{usern}',{chatid},0,0,5,0);
"""
    await kDB.execute(commad)
    await kDB.commit()
    await kDB.close()
# OK


async def setUserhiveuser(usern: str, hiveuser: str, status: int) -> None:
    kDB = await dbm.connect(userfile)
    commad = f"""
    UPDATE users SET hiveuser='{hiveuser}', status={status} WHERE username='{usern}';
"""
    await kDB.execute(commad)
    await kDB.commit()
    await kDB.close()
# OK


async def getUserstatus(usern: str) -> int:
    kDB = await dbm.connect(userfile)
    commad = f"""
SELECT status FROM users where username='{usern}';
    """
    cursor = await kDB.execute(commad)
    row = await cursor.fetchone()
    await cursor.close()
    await kDB.close()

    if row == None:
        return 0
    if len(row) == 0:
        return 0
    if row[0] == None:
        return 0

    status = 1
    # row[0] DB

    return status


async def setOrder(id: str, owner: str, stype: str, amounI: float, tokenI: str, amounO: float, tokenO: str,
                   pmetod: str, chatlink: str, status: str) -> None:
    kDB = await dbm.connect(userfile)
    datex: str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    commad = f"""
    INSERT INTO postorders 
    (id,owner,type,amouni,tokeni,amouno,tokeno,pmethod,chatlink,status,order_date) 
    VALUES ('{id}','{owner}','{stype}',{amounI},'{tokenI}',{amounO},'{tokenO}',
    '{pmetod}','{chatlink}','{status}','{datex}');    
"""
    await kDB.execute(commad)
    await kDB.commit()
    await kDB.close()
# OK


async def cancelOrder(id: str) -> None:
    kDB = await dbm.connect(userfile)
    command = f"""
UPDATE postorders SET status='cancel',chatlink='' WHERE id='{id}' ;    
"""
    await kDB.execute(command)
    await kDB.commit()
    await kDB.close()
# OK


async def getOrderlist(usern: str) -> tuple:
    kDB = await dbm.connect(userfile)
    command = f"""
SELECT id,status FROM postorders 
WHERE (owner='{usern}' OR taker='{usern}') AND NOT (status='cancel' OR status='finish') ;
"""
    cursor = await kDB.execute(command)
    await kDB.commit()
    row = await cursor.fetchall()
    await cursor.close()
    await kDB.close()
    return tuple(row)
# OK


async def getOrderstatus(id: str) -> str:
    kDB = await dbm.connect(userfile)
    command = f"""
SELECT status FROM postorders WHERE id='{id}' ;
"""
    cursor = await kDB.execute(command)
    await kDB.commit()
    row = await cursor.fetchone()
    await cursor.close()
    await kDB.close()
    if row == None:
        return ""
    if len(row) == 0:
        return ""
    if row[0] == None:
        return ""
    return row[0]
# OK


async def setOrderstatus(id: str, status: str) -> str:
    kDB = await dbm.connect(userfile)
    command = f"""
UPDATE  postorders SET status='{status}' WHERE id='{id}' ;
"""
    await kDB.execute(command)
    await kDB.commit()
    await kDB.close()
# OK


async def getOrderdata(id: str) -> tuple:
    kDB = await dbm.connect(userfile)
    command = f"""
SELECT * FROM postorders WHERE id='{id}' ;
"""
    cursor = await kDB.execute(command)
    await kDB.commit()
    row = await cursor.fetchone()
    await cursor.close()
    await kDB.close()
    owner = row[1]
    stype = row[2]
    amouni = float(row[3])
    tokeni = row[4]
    amouno = float(row[5])
    tokeno = row[6]
    pmethod = row[7]
    taker = row[8]
    chatlink = row[9]
    status = row[10]
    order_date = row[11]
    return owner, stype, amouni, tokeni, amouno, tokeno, pmethod, taker, chatlink, status, order_date
# OK


async def getOrdepay(id: str) -> tuple:
    kDB = await dbm.connect(userfile)
    command = f"""
SELECT amouno,tokeno,pmethod  FROM postorders WHERE id='{id}' ;
"""
    cursor = await kDB.execute(command)
    row = await cursor.fetchone()
    await cursor.close()
    await kDB.close()
    amouno = float(row[0])
    tokeno = row[1]
    pmethod = row[2]
    return amouno, tokeno, pmethod
# OK


async def setOrdertaker(id: str, taker: str) -> None:
    kDB = await dbm.connect(userfile)
    command = f"""
UPDATE postorders SET taker='{taker}',status='tomado',chatlink=''  WHERE id= '{id}';
"""
    await kDB.execute(command)
    await kDB.commit()
    await kDB.close()
# OK


async def setOrderfinish(id: str) -> None:
    kDB = await dbm.connect(userfile)
    command = f"""
UPDATE postorders SET status='finish' WHERE id= '{id}';
"""
    await kDB.execute(command)
    await kDB.commit()
    await kDB.close()
# OK


async def incremetUserordercount(usern: str) -> None:
    kDB = await dbm.connect(userfile)
    command = f"""
SELECT norders from users WHERE username= '{usern}';
"""
    cursor = await kDB.execute(command)
    await kDB.commit()
    row = await cursor.fetchone()

    try:
        norders = int(row[0]) + 1
    except:
        norders = 0

    command = f"""
UPDATE users SET norders={norders} WHERE username= '{usern}';
"""
    await kDB.execute(command)
    await kDB.commit()
    await kDB.close()
# OK


async def getOrderNew() -> list:
    kDB = await dbm.connect(userfile)
    command = f"""
SELECT id,order_date FROM postorders  WHERE status='nuevo';
"""
    cursor = await kDB.execute(command)
    await kDB.commit()
    row = await cursor.fetchall()
    await kDB.close()
    return row
# OK


async def getUsersChats() -> tuple:
    kDB = await dbm.connect(userfile)
    command = f"""
SELECT chatid FROM users  ;
"""
    cursor = await kDB.execute(command)
    await kDB.commit()
    row = await cursor.fetchall()
    await kDB.close()
    return row
# OK
