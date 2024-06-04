from config import slang

def getlang(scode: str) -> str:
    if scode in slang:
        return scode
    return 'en'

