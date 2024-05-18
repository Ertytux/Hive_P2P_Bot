from datetime import datetime

def getIdfromHash(msg:str)->str:
    now=datetime.now()
    modmsg=msg+" "+now.strftime('%Y-%m-%d %H:%M:%S') 
    hz= modmsg.__hash__().__abs__()    
    return  str(hz)

# C-2.04.2024 4:37 
    
