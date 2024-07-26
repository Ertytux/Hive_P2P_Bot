from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from getlang import getlang
from tools import is_number
from genid import getIdfromHash
from config import blacklist, tokenAcepted, boturl
import dbmanager as dmr
from messages import *
from verifyhive import veryfyHiveUser, encodeTransE, verifytransactE
import qrcode
import os
import json



async def posr(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    chatid = update.message.chat_id
    scode = getlang(user.language_code)

    if chatid in blacklist:
        msg = {'es': 'Usuario restringido',
               'en': 'Restricted user'}
        await update.message.reply_text(msg.get(scode))
        return None
    if user.username == '' or user.username == None:
        await update.message.reply_markdown(messages_statU.get(scode))
        return None
    username = user.username.lower()
    xchatid, xhiveuser = await dmr.getUserchatid(username)
    if xhiveuser == None or xhiveuser == '':
        await update.message.reply_text(messages_notSt.get(scode))
        return None
    statusx = veryfyHiveUser(xhiveuser)
    if statusx == -1:
        msg = {'es': 'Usuario de HIVE no válido',
               'en': 'Invalid HIVE user'}
        await update.message.reply_text(msg.get(scode))
        return None
    if statusx == 0:
        msg = {'es': 'Servicio exclusivo para usuarios que han delegado.',
               'en': 'Exclusive service for users who have delegated.'}
        await update.message.reply_text(msg.get(scode))
        await update.message.reply_markdown(messages_notHP.get(scode))
        return None
    mtext = update.message.text
    stext = mtext.split()

    if len(stext) != 3:
        errms = {'es': f"""
Comando incorrecto debe ser por ejemplo: 
/pos 10 HBD 
""", 'en': f"""
Incorrect command must be for example: 
/pos 10 HBD 
"""}
        await update.message.reply_text(errms.get(scode))
        return None

    if not is_number(stext[1]):
        msg = {'es': "Formato de monto de entrada incorrecto",
               'en': "Incorrect input amount format"}
        await update.message.reply_text(msg.get(scode))
        return None
    amounI = float(stext[1])

    tokenI: str = stext[2]
    if tokenI.upper() not in tokenAcepted:
        errms = {'es': f"""
Solo se aceptan los siguientes tokens:  
{tokenAcepted}
""", 'en': f"""
Only the following tokens are accepted:  
{tokenAcepted}
"""}
        await update.message.reply_markdown(errms.get(scode))
        return None
    dtf = {
        'to': xhiveuser,
        'amount': f"{amounI:.3f} {tokenI.upper()}"
    }
    jst = json.dumps(dtf)
    memo = getIdfromHash(jst)
    odata = encodeTransE(xhiveuser, float(f"{(amounI):.3f}"), tokenI, memo)
    sig = f"hive://sign/op/{odata}"
    img = qrcode.make(sig)
    img.save(f"orders/QR_{memo}.png")
    docpay=rf"""
 <!DOCTYPE html>
<html>
<head>
<title>Pay with KeyChain</title>
<script src=
"https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js">
</script>
</head>
<body>
<div>
<center>
<h1> Invoice </h1>
Pay to: <pre>{xhiveuser}<pre>
<br>
Amount: <pre>{f"{amounI:.3f} {tokenI.upper()}"}<pre>
<br>
<b>Direct Link</b><br>
<a href="{sig}">Clic Here to Pay (Only Mobile)</a>
<br>
<h1>Or scan the QR</h1>
<div id="qrcode"></div>
<script>
var qrcode = new QRCode("qrcode","{sig}");
</script>
</center>
</div>
</body>
</html> 
"""
    with open(f"orders/Pay_{memo}.html",'w') as f:
        f.write(docpay)
    
    msg = {'es': rf"""
Muestre o envíe el QR a su cliente para recibir {amounI:.3f} {tokenI.upper()}
en su usuario registrado {xhiveuser} con el memo `{memo}`.  

También puede enviar o compartir el documento HTML adjuntado con un enlace de pago automático
accesible desde la aplicación móvil Hive-KeyChain.

Cuando su cliente le diga que efectuó el pago verifique en su billetera de
Hive-Keychain o dando click en el botón Confirmar.

""", 'en': rf"""
Show or send the QR to your customer to receive {amounI:.3f} {tokenI.upper()}
in your registered user {xhiveuser} with memo `{memo}`.     

You can also send or share the attached HTML document with an accessible automatic payment link 
from the Hive-KeyChain mobile application.

When your customer tells you that he made the payment check-in this on
Hive-Keychain or by clicking on the Confirm button.

"""}
    txmsg = {'es': "Confirmar",
             'en': "Confirm"}
    tsmsg = {'es': "Cancelar",
             'en': "Cancel"}
    keyboard = [[InlineKeyboardButton(
        txmsg.get(scode), url=f"{boturl}?start=sposr_{memo}")],
        [InlineKeyboardButton(tsmsg.get(scode), callback_data=f"Erase_{memo}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_photo(chat_id=chatid,
                                 photo=open(f"orders/QR_{memo}.png", 'rb'),
                                 caption=msg.get(scode),
                                 parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
    await context.bot.send_document(chat_id=chatid,document=open(f"orders/Pay_{memo}.html",'rb'))   
    os.remove(f"orders/QR_{memo}.png")
    os.remove(f"orders/Pay_{memo}.html")
    
    context.user_data[memo] = odata


async def sposr(update: Update, context: ContextTypes.DEFAULT_TYPE, stext: list) -> None:
    user = update.effective_user
    scode = getlang(user.language_code)
    odata = context.user_data.get(stext[1])
    status = await verifytransactE(odata)
    if status:
        msg = {'es': "Transacción Confirmada!!!",
               'en': "Transaction Confirmed!!!"}
        del context.user_data[stext[1]]
    else:
        msg = {'es': "Transferencia en HIVE sin confirmar, intente nuevamente en unos segundos",
               'en': "Transfer in HIVE unconfirmed, please try again in a few seconds"}
    await update.message.reply_text(msg.get(scode))
