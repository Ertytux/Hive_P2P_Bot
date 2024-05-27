# from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ForceReply, ReplyKeyboardRemove
# from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

from config import hcbchatid, blacklist, admins, supports, boturl, hcbchatid, receptor, manager
import datetime
from tools import is_number, getHoursfromDate
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
# , ConversationHandler
# import asyncio
import qrcode

from genid import getIdfromHash
from verifyhive import veryfyHiveUser, verifytransact, sendHive, getFee, encodeTrans, reputationHiveUser
import dbmanager as dmr
from messages import *
import rates as rt
import os


tokenAcepted = ['HIVE', 'HBD']
squence = ['amouni', 'tokeni', 'amouno', 'tokeno', 'pmetod']


# Communities
communities = {'mycomm': hcbchatid}

# Lang
slang = ['es', 'en']


def getlang(scode: str) -> str:
    if scode in slang:
        return scode
    return 'en'

# commands


async def escrow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # /escrow
    user = update.effective_user
    scode = getlang(user.language_code)
    if user.username == '' or user.username == None:
        await update.message.reply_markdown(messages_statU.get(scode))
    else:
        await update.message.reply_markdown(messages_escrow.get(scode))
# OKX

async def fees(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # /fees
    user = update.effective_user
    scode = getlang(user.language_code)
    if user.username == '' or user.username == None:
        await update.message.reply_markdown(messages_statU.get(scode))
    else:
        await update.message.reply_markdown(messages_fees.get(scode))
# OKX


async def prices(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # /prices
    user = update.effective_user
    scode = getlang(user.language_code)
    if user.username == '' or user.username == None:
        await update.message.reply_markdown(messages_statU.get(scode))
    else:
        await update.message.reply_text(rt.getPrices())
# OKX


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # /price
    user = update.effective_user
    scode = getlang(user.language_code)
    if user.username == '' or user.username == None:
        await update.message.reply_markdown(messages_statU.get(scode))
        return None
    stext = update.message.text.split()
    if len(stext) < 2:
        msg = {'es': 'Comando incorrecto, debe ser por ejemplo: /price VES ',
               'en': 'Incorrect command, it must be for example: /price GHS '}
        await update.message.reply_text(msg.get(scode))
        return None
    await update.message.reply_text(rt.getPrice(stext[1]))
# OKX


async def userinfo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # /userinfo
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
    else:
        username = user.username.lower()
        data = await dmr.getUserInfo(username)
        if scode == 'es':
            msg = rf"""
**Usuario de Telegram**: `{username}` [link](https://t.me/{username})
**Usuario de HIVE**: `{data.get('hiveuser')}`
**Delega a** `{manager}`: {'Si' if veryfyHiveUser(data.get('hiveuser'))==1 else 'No'}
**Número de órdenes completadas**: `{data.get('norders')}`
**Reputación en HIVE**: `{await reputationHiveUser(data.get('hiveuser')):.2f}`
"""
        else:
            msg = rf"""
**Telegram user**: `{username}` [link](https://t.me/{username})
**HIVE user**: `{data.get('hiveuser')}`
** Delegate to** `{manager}`: {'Yes' if veryfyHiveUser(data.get('hiveuser'))==1 else 'No'}
**Number of completed orders**: `{data.get('norders')}`
**Reputation on HIVE**: `{await reputationHiveUser(data.get('hiveuser')):.2f}`
"""
        await update.message.reply_markdown(msg)
# OKX


async def hiveuser(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # /hiveuser
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
    else:
        username = user.username.lower()
        stext = update.message.text.split()
        if len(stext) < 2:
            msg = {'es': 'Comando incorrecto, debe ser por ejemplo: /hiveuser juanperes ',
                   'en': 'Incorrect command, must be for example: /hiveuser juanperes '}
            await update.message.reply_text(msg.get(scode))
            return None
        hiveU = stext[1].lower()
        status = veryfyHiveUser(hiveU)
        await dmr.setUserhiveuser(username, hiveU, status)
        if status:
            msg = {'es': f"Usuario {hiveU} registrado correctamente, gracias por apoyar a `{manager}`",
                   'en': f"User {hiveU} is now successfully registered, thank you for supporting `{manager}`"}
            await update.message.reply_markdown(msg.get(scode))
        else:
            msg = {'es': f"Usuario {hiveU} registrado correctamente, delegue al menos 50 HP a `{manager}` para disfrutar cero comisiones",
                   'en': f"User {hiveU} is now registered correctly, delegate at least 50 HP to `{manager}` to enjoy zero commissions"}
            await update.message.reply_markdown(msg.get(scode))
            await update.message.reply_markdown(messages_notHP.get(scode))
# OKX


async def msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # /msg
    user = update.effective_user
    scode = getlang(user.language_code)
    if user.username == '' or user.username == None:
        await update.message.reply_markdown(messages_statU.get(scode))
        return None
    else:
        username = user.username.lower()
        stext = update.message.text.split()
        if username not in admins:
            msg = {'es': "Usted no tiene permisos para enviar mensajes al canal",
                   'en': "You don't have permissions to send messages to the channel"}
            await update.message.reply_text(msg.get(scode))
            return None
        if len(stext) < 2:
            msg = {'es': 'Comando incorrecto, debe ser por ejemplo: /msg mensaje ',
                   'en': 'Incorrect command, must be for example: /msg message '}
            await update.message.reply_text(msg.get(scode))
            return None
        sent_message = await context.bot.send_message(chat_id=hcbchatid, text=str.join(" ", stext[1:]))
        msout = {'es': f"""
Link del mensaje publicado https://t.me/{sent_message.chat.username}/{sent_message.message_id}              
        """, 'en': f"""
Link of the published message https://t.me/{sent_message.chat.username}/{sent_message.message_id}              
        """}
        await update.message.reply_markdown(msout.get(scode))
# OKX


async def release(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # /release
    user = update.effective_user
    scode = getlang(user.language_code)
    if user.username == '' or user.username == None:
        await update.message.reply_markdown(messages_statU.get(scode))
        return None
    else:
        username = user.username.lower()

        if username not in admins:
            msg = {'es': "Usted no tiene permisos",
                   'en': "You don't have permissions"}
            await update.message.reply_text(msg.get(scode))
            return None
        stext = update.message.text.split()

        if len(stext) < 2:
            msg = {'es': 'Comando incorrecto, debe ser por ejemplo: /release 34564564576445234563 ',
                   'en': 'Incorrect command, must be for example: /release 34564564576445234563 '}
            await update.message.reply_text(msg.get(scode))
            return None

        orderid = stext[1]
        (owner, stype, amouni, tokeni, amouno, tokeno,
         pmethod, taker, chatlink, dstatus, order_date) = await dmr.getOrderdata(orderid)

    # sell default

        receiver = taker
        if stype == 'buy':
            receiver = owner

        chatid_r, hiveuser_r = await dmr.getUserchatid(receiver)

        if dstatus == 'finish':
            msg = {'es': f"Esta orden {orderid} ya fue completada",
                   'en': f"This order {orderid} has been completed"}
            await update.message.reply_text(msg.get(scode))
            return None

        if dstatus == 'payed':
            fee = await getFee(receiver, tokeni, amouni)
            sendHive(hiveuser_r, amouni-fee, tokeni)
            await dmr.setOrderfinish(orderid)
            await dmr.incremetUserordercount(receiver)
            msg = {'es': f"Orden {orderid} completada",
                   'en': f"Order {orderid} completed"}
            await context.bot.send_message(chat_id=chatid_r, text=msg.get(scode))

        else:
            msg = {'es': f"Error en orden {orderid} contacte a soporte.",
                   'en': f"Error in order {orderid} contact support."}
            await update.message.reply_text(msg.get(scode))
# ok


async def back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    scode = getlang(user.language_code)
    if user.username == '' or user.username == None:
        await update.message.reply_markdown(messages_statU.get(scode))
        return None
    else:
        username = user.username.lower()

        if username not in admins:
            msg = {'es': "Usted no tiene permisos",
                   'en': "You don't have permissions"}
            await update.message.reply_text(msg.get(scode))
            return None
        stext = update.message.text.split()

        if len(stext) < 2:
            msg = {'es': 'Comando incorrecto, debe ser por ejemplo: /back 34564564576445234563 ',
                   'en': 'Incorrect command, must be for example: /back 34564564576445234563 '}
            await update.message.reply_text(msg.get(scode))
            return None
        orderid = stext[1]
        (owner, stype, amouni, tokeni, amouno, tokeno,
         pmethod, taker, chatlink, dstatus, order_date) = await dmr.getOrderdata(orderid)
        if dstatus == 'payed':
            sender = owner
            if stype == 'buy':
                sender = taker
            chatid_s, hiveuser_s = await dmr.getUserchatid(sender)

            await scancel(update, context, stext)
            try:
                fee = await getFee(sender, tokeni, amouni)
                sendHive(hiveuser_s, amouni-fee, tokeni)
                await update.message.reply_text(
                    rf"{amouni-fee:.3f} {tokeni} send to {hiveuser_s}->{sender}")
            except:
                await update.message.reply_text("Parameters Error, verify on HIVE!!")
        else:
            await update.message.reply_text("Error, Order not Payed!!")


async def orderinfo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    scode = getlang(user.language_code)
    if user.username == '' or user.username == None:
        await update.message.reply_markdown(messages_statU.get(scode))
        return None
    else:
        username = user.username.lower()

        if username not in admins:
            msg = {'es': "Usted no tiene permisos",
                   'en': "You don't have permissions"}
            await update.message.reply_text(msg.get(scode))
            return None
        stext = update.message.text.split()

        if len(stext) < 2:
            msg = {'es': 'Comando incorrecto, debe ser por ejemplo: /orderinfo 34564564576445234563 ',
                   'en': 'Incorrect command, must be for example: /orderinfo 34564564576445234563 '}
            await update.message.reply_text(msg.get(scode))
            return None
        orderid = stext[1]
        (owner, stype, amouni, tokeni, amouno, tokeno,
         pmethod, taker, chatlink, dstatus, order_date) = await dmr.getOrderdata(orderid)
        msg = {'es': rf"""
Datos de la orden {orderid}:
[(owner, stype, amouni, tokeni, amouno, tokeno, pmethod, taker, chatlink, dstatus, order_date)]  
{(owner, stype, amouni, tokeni, amouno, tokeno, pmethod, taker, chatlink, dstatus, order_date)}  
""", 'en': rf"""
Order data {orderid}:
[(owner, stype, amouni, tokeni, amouno, tokeno, pmethod, taker, chatlink, dstatus, order_date)]  
{(owner, stype, amouni, tokeni, amouno, tokeno, pmethod, taker, chatlink, dstatus, order_date)}  
"""}
        await update.message.reply_text(msg.get(scode))


async def notify(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # /notify
    user = update.effective_user
    scode = getlang(user.language_code)
    if user.username == '' or user.username == None:
        await update.message.reply_markdown(messages_statU.get(scode))
        return None
    else:
        username = user.username.lower()
        if username not in admins:
            msg = {'es': "Usted no tiene permisos para enviar mensajes al canal",
                   'en': "You don't have permissions to send messages to the channel"}
            await update.message.reply_text(msg.get(scode))
            return None
        stext = update.message.text.split()
        uchatid = update.message.chat_id
        if len(stext) < 2:
            msg = {'es': 'Comando incorrecto, debe ser por ejemplo: /notify mensaje ',
                   'en': 'Incorrect command, must be for example: /notify message '}
            await update.message.reply_text(msg.get(scode))
            return None
        chat_ids = await dmr.getUsersChats()
        msg = str.join(" ", stext[1:])
        for rx in chat_ids:
            chat_idr = rx[0]
            if rx != None:
                if uchatid != int(chat_idr):
                    try:
                        await context.bot.send_message(chat_id=int(chat_idr), text=msg)
                    except:
                        continue
        msg = {'es': f"Mensaje enviado a {len(chat_ids)} usuarios.",
               'en': f"Message sent to {len(chat_ids)} users."}
        await update.message.reply_text(msg.get(scode))
# OKX


async def setorder(stype: str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Set ORDER
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

    mtext = update.message.text
    if '@' in mtext:
        msgN = {'es': "No se admite una orden que revele explícitamente el nombre de usuario.",
                'en': "An order that explicitly reveals the user name is not allowed."}
        await update.message.reply_text(msgN.get(scode))
        return None

    stext = mtext.split()
    if not len(stext) < 5:
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

        if not is_number(stext[3]):
            msg = {'es': "Formato de monto de salida incorrecto",
                   'en': "Incorrect output amount format"}
            await update.message.reply_text(msg.get(scode))
            return None
        amounO = float(stext[3])
        tokenO: str = stext[4]
        pmethod: str = str.join(" ", stext[5:])
        if scode == 'es':
            rtype = "🟢 #COMPRA"
            if stype == "sell":
                rtype = "🔴 #VENTA"
            ormsg = rf"""
{rtype} 

💰 {amounI} #{tokenI.upper()} **por** {amounO} #{tokenO.upper()}        
💹 Tasa de cambio: {(amounO/amounI):.3f}             
🏧 Medio de pago: {pmethod}           

Cuenta garante: @`{receptor}`

Datos del ofertante:
🔁 Operaciones terminadas: {await dmr.getUserNorder(username)}  
🎖 Reputación en HIVE: {await reputationHiveUser(xhiveuser):.2f}   
"""
#
            idx = getIdfromHash(ormsg)

        # ormsg = ormsg+"\n" + \
        #    f"Tomar orden `{idx}` [AQUI]()     "
            keyboard = [[InlineKeyboardButton(
                f"Tomar orden {idx}", url=f"{boturl}?start=take_{idx}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            sent_message = await context.bot.send_message(chat_id=hcbchatid, text=ormsg, parse_mode='Markdown', reply_markup=reply_markup)
            chatlink = f"https://t.me/{sent_message.chat.username}/{sent_message.message_id}"
            status = "nuevo"
            await dmr.setOrder(idx, username, stype, amounI, tokenI, amounO, tokenO, pmethod, chatlink, status)
            msout = f"""
Oferta `{idx}` 
Publicada en {chatlink} 

Puede cancelarla **si aún no ha sido tomada**.  

🚨 Una vez tomada **solo la parte que envía HIVE o HBD** podrá cancelar la orden y la otra parte podrá
abrir una disputa.            
"""
            keyboard = [[InlineKeyboardButton(
                f"Cancelar orden {idx}", url=f"{boturl}?start=cancel_{idx}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_markdown(msout, reply_markup=reply_markup)
        else:  # EN
            rtype = "🟢 #BUY"
            if stype == "sell":
                rtype = "🔴 #SELL"
            ormsg = rf"""
{rtype} 

💰 {amounI} #{tokenI.upper()} **by** {amounO} #{tokenO.upper()}        
💹 Exchange rate: {(amounO/amounI):.3f}             
🏧 Means of payment: {pmethod}           

Guarantor account: @`{receptor}`

Details of the bidder:
🔁 Completed operations: {await dmr.getUserNorder(username)}  
🎖 Reputation in HIVE: {await reputationHiveUser(username):.2f}   
"""
#
            idx = getIdfromHash(ormsg)

        # ormsg = ormsg+"\n" + \
        #    f"Tomar orden `{idx}` [AQUI]()     "
            keyboard = [[InlineKeyboardButton(
                f"Take order {idx}", url=f"{boturl}?start=take_{idx}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            sent_message = await context.bot.send_message(chat_id=hcbchatid, text=ormsg, parse_mode='Markdown', reply_markup=reply_markup)
            chatlink = f"https://t.me/{sent_message.chat.username}/{sent_message.message_id}"
            status = "nuevo"
            await dmr.setOrder(idx, username, stype, amounI, tokenI, amounO, tokenO, pmethod, chatlink, status)
            msout = f"""
Offer `{idx}` 
Published in {chatlink} 

You can cancel it ** if it hasn't been taken yet**.

🚨 Once taken **only the party sending HIVE or HBD** will be able to cancel the order, and the other party will
open a dispute.           
"""
            keyboard = [[InlineKeyboardButton(
                f"Cancel order {idx}", url=f"{boturl}?start=cancel_{idx}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_markdown(msout, reply_markup=reply_markup)

    else:
        errms = {'es': f"""
Comando incorrecto debe ser por ejemplo: 
/{stype} 10 HBD 3000 CUP Trasfermóvil o Enzona
""", 'en': f"""
Incorrect command must be for example: 
/{stype} 10 HBD 3000 CUP Transfermobile or Enzone
"""}
        await update.message.reply_text(errms.get(scode))
 # OKX


async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # /buy
    stype = "buy"
    await setorder(stype, update, context)
# OKX


async def sell(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # /sell
    stype = "sell"
    await setorder(stype, update, context)
# OKX


async def scancel(update: Update, context: ContextTypes.DEFAULT_TYPE, stext: list) -> None:
    # /cancel
    user = update.effective_user
    scode = getlang(user.language_code)
    username = user.username.lower()
    if len(stext) < 2:
        msg = {'es': "Comando incorrecto, utilice por ejemplo: /cancel 3453453626423413423",
               'en': "Incorrect command, use for example: /cancel 3453453626423413423"}
        await update.message.reply_text(msg.get(scode))
        return None
    orderid = stext[1]
    (owner, stype, amouni, tokeni, amouno, tokeno,
        pmethod, taker, chatlink, dstatus, order_date) = await dmr.getOrderdata(orderid)
    if dstatus == 'cancel':
        msg = {'es': f"La orden `{orderid}` ya ha sido cancelada con anterioridad a su acción.",
               'en': f"The `{orderid}` order has already been cancelled prior to your action."}
        await update.message.reply_markdown(msg.get(scode))
        return None
    if dstatus == 'finish':
        msg = {'es': f"""
No se puede cancelar una orden *finalizada*.
""", 'en': f"""
A *completed* order cannot be cancelled.
"""}
        await update.message.reply_markdown(msg.get(scode))
        return None
    owner_id, owner_hive = await dmr.getUserchatid(owner)
    skk = int(chatlink.split("/").pop()) if chatlink != '' else None

    if username in admins:
        await dmr.cancelOrder(orderid)
        try:
            await context.bot.delete_message(chat_id=hcbchatid, message_id=skk)
            msg = {'es': f"Orden  {orderid} eliminada correctamente",
                   'en': f"Order {orderid} successfully deleted"}
            await update.message.reply_text(msg.get(scode))
        except:
            msg = {'es': f"""
Orden  {orderid} eliminada.
Elimine el enlace -> {chatlink} -- mensaje {skk} manualmente""",
                   'en': f"""
Order {orderid} removed.
Delete the link -> {chatlink} -- message {skk} manually"""}
            await update.message.reply_text(msg.get(scode))
        msg = {'es': f"Orden {orderid} cancelada por un administrador",
               'en': f"Order {orderid} cancelled by an administrator"}
        await context.bot.send_message(chat_id=owner_id, text=msg.get(scode))
        if dstatus != 'nuevo':
            taker_id, taker_hive = await dmr.getUserchatid(taker)
            await context.bot.send_message(chat_id=taker_id, text=msg.get(scode))
        return None

    if dstatus == 'nuevo' and username == owner:
        await dmr.cancelOrder(orderid)
        if chatlink != '':
            await context.bot.delete_message(chat_id=hcbchatid, message_id=skk)
        msg = {'es': f"Orden {orderid} cancelada",
               'en': f"Order {orderid} cancelled"}
        await context.bot.send_message(chat_id=owner_id, text=msg.get(scode))
        return None
    sender = owner if stype == 'sell' else taker
    if dstatus == 'tomado' and username == sender:
        await dmr.cancelOrder(orderid)
        # if  chatlink!='':
        # await context.bot.delete_message(chat_id=hcbchatid, message_id=skk)
        taker_id, taker_hive = await dmr.getUserchatid(taker)
        msg = {'es': f"Orden {orderid} cancelada pues no se hará el depósito en garantía.",
               'en': f"Order {orderid} cancelled as the security deposit will not be made."}
        await context.bot.send_message(chat_id=owner_id, text=msg.get(scode))
        await context.bot.send_message(chat_id=taker_id, text=msg.get(scode))
        return None
    msg = {'es': f"Usted no puede cancelar la orden  {orderid}.",
           'en': f"You cannot cancel the {orderid} order."}
    await update.message.reply_text(msg.get(scode))
# OK


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user.username == '' or user.username == None:
        await update.message.reply_markdown(messages_statU)
    else:
        stext = update.message.text.split()
        await scancel(update, context, stext)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    if query.data == "_Erase_":
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.id)
        return None
    return None


async def stake(update: Update, context: ContextTypes.DEFAULT_TYPE, stext: list) -> None:
    # start=take
    user = update.effective_user
    scode = getlang(user.language_code)
    chatid = update.message.chat_id

    if user.username == '' or user.username == None:
        await update.message.reply_markdown(messages_statU)
        return None

    username = user.username.lower()

    if not await dmr.checkUser(username):
        msg = {'es': 'Inicie primero el bot con el comando /start y registre su usuario de hive con el comando /hiveuser',
               'en': 'First start the bot with the /start command and register your hive user with the /hiveuser command'}
        await update.message.reply_text()
        return None

    if chatid in blacklist:
        msg = {'es': 'Usuario restringido',
               'en': 'Restricted user'}
        await update.message.reply_text(msg.get(scode))
        return None

    xchatid, xhiveuser = await dmr.getUserchatid(username)

    if xhiveuser == None or xhiveuser == '':
        msg = {'es': 'Debe registrar primero su usuario de HIVE con: /hiveuser nombreusuario',
               'en': 'You must first register your HIVE user with: /hiveuser username'}
        await update.message.reply_text(msg.get(scode))
        return None

    if len(stext) < 2:
        msg = {'es': "Error en Orden.",
               'en': "Error in Order."}
        await update.message.reply_text(msg.get(scode))
        return None

    orderid = stext[1]
    status = await dmr.getOrderstatus(orderid)
    match status:
        case '':
            msg = {'es': "Error en Orden.",
                   'en': "Error in Order."}
            await update.message.reply_text(msg.get(scode))
            return None
        case 'cancel':
            msg = {'es': "La orden ya ha sido cancelada",
                   'en': "The order has already been cancelled"}
            await update.message.reply_text(msg.get(scode))
            return None
        case 'tomado':
            msg = {'es': "La orden ya fue tomado por un usuario.",
                   'en': "The order has already been taken by a user."}
            await update.message.reply_text(msg.get(scode))
            return None
        case 'finish':
            msg = {'es': "La orden ya fue terminada.",
                   'en': "The order has already been completed."}
            await update.message.reply_text(msg.get(scode))
            return None
        case _:
            (owner, stype, amouni, tokeni, amouno, tokeno,
             pmethod, taker, chatlink, dstatus, order_date) = await dmr.getOrderdata(orderid)
            if scode == 'es':
                if owner == username:
                    keyboard = [[InlineKeyboardButton(
                        f"Cancelar orden {orderid}", url=f"{boturl}?start=cancel_{orderid}")]]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    await update.message.reply_markdown(
                        f"Usted no puede tomar su propia orden pero si cancelarla",
                        reply_markup=reply_markup)
                    return None
                optmsg = "vender" if stype == "buy" else "comprar"
                fee = await getFee(username, tokeni, amouni)
                keyboard = [[InlineKeyboardButton(
                    "Confirmar", url=f"{boturl}?start=totake_{orderid}")],
                    [InlineKeyboardButton("Cancelar", callback_data="_Erase_")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                msg = f"""
Usted va a {optmsg}    
Monto {amouni}  {tokeni.upper()}   
Por    
{amouno} {tokeno.upper()}   
Utilizando {pmethod}    
Correspondiente a las orden {orderid} 

Se le aplicará una comisión de {fee:.3f} {tokeni.upper()}       
Puede evitar las comisiones en próximas operaciones delegando al menos 50 HP al usuario de HIVE `{manager}`.

Si está de acuerdo **Confirme**. En caso contrario **Cancele**.  
"""
                await update.message.reply_markdown(msg, reply_markup=reply_markup)
            else:  # EN
                if owner == username:
                    keyboard = [[InlineKeyboardButton(
                        f"Cancel order {orderid}", url=f"{boturl}?start=cancel_{orderid}")]]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    await update.message.reply_markdown(
                        f"You can't take your own order but you cancel it",
                        reply_markup=reply_markup)
                    return None
                optmsg = "sell" if stype == "buy" else "buy"
                fee = await getFee(username, tokeni, amouni)
                keyboard = [[InlineKeyboardButton(
                    "Confirm", url=f"{boturl}?start=totake_{orderid}")],
                    [InlineKeyboardButton("Cancel", callback_data="_Erase_")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                msg = f"""
You are going to {optmsg}    
Amount {amouni}  {tokeni.upper()}   
with   
{amouno} {tokeno.upper()}   
Using {pmethod}    
Corresponding to the order {orderid} 

Will be charged a commission of {fee:.3f} {tokeni.upper()}       
You can avoid commissions on upcoming trades by delegating at least 50 HP to the HIVE user `{manager}`.

If you agree please **Confirm**. Otherwise **Cancel**.  
"""
                await update.message.reply_markdown(msg, reply_markup=reply_markup)


# OK


async def totake(update: Update, context: ContextTypes.DEFAULT_TYPE, stext: list) -> None:
    # start=totake
    user = update.effective_user
    scode = getlang(user.language_code)
    chatid = update.message.chat_id

    if chatid in blacklist:
        msg = {'es': 'Usuario restringido',
               'en': 'Restricted user'}
        await update.message.reply_text(msg.get(scode))
        return None

    username = user.username.lower()
    xchatid, xhiveuser = await dmr.getUserchatid(username)

    if xhiveuser == None or xhiveuser == '':
        msg = {'es': 'Debe registrar primero su usuario de HIVE con /hiveuser nombreusuario',
               'en': 'You must first register your HIVE user with /hiveuser username'}
        await update.message.reply_text(msg.get(scode))
        return None

    if len(stext) < 2:
        msg = {'es': "Error en Orden.",
               'en': "Error in Order."}
        await update.message.reply_text(msg.get(scode))
        return None

    orderid = stext[1]
    status = await dmr.getOrderstatus(orderid)
    match status:
        case '':
            msg = {'es': "Error en Orden.",
                   'en': "Error in Order."}
            await update.message.reply_text(msg.get(scode))
            return None
        case 'cancel':
            msg = {'es': "Orden cancelada antes de ser tomada",
                   'en': "Order cancelled before being taken"}
            await update.message.reply_text(msg.get(scode))
            return None
        case 'tomado':
            msg = {'es': "La orden ya fue tomado por un usuario.",
                   'en': "The order has already been taken by a user."}
            await update.message.reply_text(msg.get(scode))
            return None
        case 'finish':
            msg = {'es': "La orden ya fue terminada.",
                   'en': "The order has already been completed."}
            await update.message.reply_text(msg.get(scode))
            return None
        case _:
            (owner, stype, amouni, tokeni, amouno, tokeno,
                pmethod, taker, chatlink, dstatus, order_date) = await dmr.getOrderdata(orderid)
            skk = int(chatlink.split("/").pop())
            if chatlink != '':
                await context.bot.delete_message(chat_id=hcbchatid, message_id=skk)
            taker = username
            await dmr.setOrdertaker(orderid, taker)
            sender = taker if stype == 'buy' else owner
            receiver = owner if stype == 'buy' else taker

            chatid_s, hiveuser_s = await dmr.getUserchatid(sender)
            chatid_r, hiveuser_r = await dmr.getUserchatid(receiver)

            # Msg for sender
            fee = await getFee(sender, tokeni, amouni)
            odata = encodeTrans(float(f"{(amouni+fee):.3f}"), tokeni, orderid)
            sig = f"hive://sign/op/{odata}"
            if scode == 'es':
                sendmsg_s = rf"""
Orden tomada `{orderid}`
Usded recibirá `{amouno}` `{tokeno}` por {pmethod}.

Debe enviar **exactamente** `{(amouni+fee):.3f}`  `{tokeni}` al usuario de HIVE `{receptor}`

Poner en el Memo *(Obligatorio)*: `{orderid}`

En el monto a enviar está incluido un fee de {fee:.3f} {tokeni}     
Puede evitar las comisiones en próximas operaciones delegando al menos 50 HP al usuario de HIVE `{manager}`.

Puede escanear el **QR** mostrado desde la aplicación móvil KeyChain. 

Al realizar la transferencia **Confirme**. 

El usuario receptor será notificado sobre el depósito en garantía de los fondos. 

Tiene la posibilidad de **Cancelar** la orden si no ha realizado el depósito.
"""
                img = qrcode.make(sig)
                img.save(f"orders/QR_{orderid}.png")
                keyboard = [
                    [InlineKeyboardButton(
                        "Confirmar", url=f"{boturl}?start=hivesend_{orderid}")],
                    [InlineKeyboardButton(
                        "Cancelar", url=f"{boturl}?start=cancel_{orderid}")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await context.bot.send_photo(chat_id=chatid_s,
                                             photo=open(
                                                 f"orders/QR_{orderid}.png", 'rb'),
                                             caption=sendmsg_s,
                                             parse_mode='Markdown', reply_markup=reply_markup)
                os.remove(f"orders/QR_{orderid}.png")

            # await context.bot.send_message(chat_id=chatid_s,
            #                               text=sendmsg_s, parse_mode='Markdown',
            #                               reply_markup=reply_markup)

                # Msg for receiver
                keyboard = [[InlineKeyboardButton(
                    "Enviar Disputa", url=f"{boturl}?start=dispute_{orderid}")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                fee = await getFee(receiver, tokeni, amouni)
                sendmsg_r = f"""
Orden tomada `{orderid}`   
Usted recibirá  `{(amouni-fee):.3f}`  `{tokeni}` 

Le será descontado un fee de {fee:.3f} {tokeni}        
Puede evitar las comisiones en próximas operaciones delegando al menos 50 HP al usuario de HIVE `{manager}`.

*IMPORTANTE*
Espere una notificación de nuestra parte indicando que se le ha depositado los fondos en garantía.
Una orden tomada solo puede ser cancelada por la parte que envía HIVE/HBD o un administrador 
del bot mediante una disputa.
"""
                await context.bot.send_message(chat_id=chatid_r, text=sendmsg_r,
                                               parse_mode='Markdown',
                                               reply_markup=reply_markup)
            else:  # EN
                sendmsg_s = rf"""
Order taken `{orderid}`
You will receive `{amouno}` `{tokeno}` using {pmethod}.

You must send **exactly** `{(amouni+fee):.3f}`  `{tokeni}` to the HIVE user `{receptor}`

With this Memo *(Mandatory)*: `{orderid}`

A fee of {fee:.3f} {tokeni} is included in the amount to be sent.     
You can avoid commissions on upcoming trades by delegating at least 50 HP to the HIVE user `{manager}`.

You can scan the **QR** displayed from the KeyChain mobile app. 

When making the transfer **Confirm**.

The receiving user will be notified about it. 

You have the possibility to **Cancel** the order if you have not made the deposit.
"""
                img = qrcode.make(sig)
                img.save(f"orders/QR_{orderid}.png")
                keyboard = [
                    [InlineKeyboardButton(
                        "Confirm", url=f"{boturl}?start=hivesend_{orderid}")],
                    [InlineKeyboardButton(
                        "Cancel", url=f"{boturl}?start=cancel_{orderid}")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await context.bot.send_photo(chat_id=chatid_s,
                                             photo=open(
                                                 f"orders/QR_{orderid}.png", 'rb'),
                                             caption=sendmsg_s,
                                             parse_mode='Markdown', reply_markup=reply_markup)
                os.remove(f"orders/QR_{orderid}.png")

            # await context.bot.send_message(chat_id=chatid_s,
            #                               text=sendmsg_s, parse_mode='Markdown',
            #                               reply_markup=reply_markup)

                # Msg for receiver
                keyboard = [[InlineKeyboardButton(
                    "Submit Dispute", url=f"{boturl}?start=dispute_{orderid}")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                fee = await getFee(receiver, tokeni, amouni)
                sendmsg_r = f"""
Order taken `{orderid}`   
You will receive  `{(amouni-fee):.3f}`  `{tokeni}` 

A fee of {fee:.3f} {tokeni} will be deducted          
You can avoid commissions on upcoming trades by delegating at least 50 HP to the HIVE user `{manager}`.

*IMPORTANT*
Expect a notification from us stating that the escrow funds have been deposited to you.
An order taken can only be cancelled by the sending party HIVE/HBD or an administrator 
of the bot through a dispute.
"""
                await context.bot.send_message(chat_id=chatid_r, text=sendmsg_r,
                                               parse_mode='Markdown',
                                               reply_markup=reply_markup)

# OKX


async def finish(update: Update, context: ContextTypes.DEFAULT_TYPE, stext: list) -> None:
    # start-finish
    user = update.effective_user
    scode = getlang(user.language_code)
    username = user.username.lower()

    if len(stext) < 2:
        msg = {'es': "Error en Orden.",
               'en': "Error in Order."}
        await update.message.reply_text(msg.get(scode))
        return None

    orderid = stext[1]
    (owner, stype, amouni, tokeni, amouno, tokeno,
        pmethod, taker, chatlink, dstatus, order_date) = await dmr.getOrderdata(orderid)

    # sell default
    sender = owner
    receiver = taker
    if stype == 'buy':
        sender = taker
        receiver = owner

    chatid_r, hiveuser_r = await dmr.getUserchatid(receiver)
    chatid_s, hiveuser_s = await dmr.getUserchatid(sender)

    if sender != username:
        msg = {'es': f"Usted no es el emisor de HIVE/HBD en la orden {orderid}",
               'en': f"You are not the HIVE/HBD issuer in the {orderid} order"}
        await update.message.reply_text(msg.get(scode))
        return None

    if dstatus == 'finish':
        msg = {'es': f"Esta orden {orderid} ya fue completada",
               'en': f"This order {orderid} has already been completed"}
        await update.message.reply_text(msg.get(scode))
        return None

    if dstatus == 'payed' and sender == username:
        fee = await getFee(receiver, tokeni, amouni)
        sendHive(hiveuser_r, amouni-fee, tokeni)
        await dmr.setOrderfinish(orderid)
        await dmr.incremetUserordercount(owner)
        await dmr.incremetUserordercount(taker)
        msg = {'es': f"Orden {orderid} completada",
               'en': f"Order {orderid} completed"}
        await context.bot.send_message(chat_id=chatid_r, text=msg.get(scode))
        await context.bot.send_message(chat_id=chatid_s, text=msg.get(scode))
    else:
        msg = {'es': f"Error en orden {orderid} contacte a soporte.",
               'en': f"Error in order {orderid} contact support."}
        await update.message.reply_text(msg.get(scode))
# OKX


async def hivesend(update: Update, context: ContextTypes.DEFAULT_TYPE, stext: list) -> None:
    # start hivesend
    user = update.effective_user
    scode = getlang(user.language_code)
    username = user.username.lower()
    orderid = stext[1]
    memo = f"{orderid}"
    status = await verifytransact(memo)
    ostatus = await dmr.getOrderstatus(orderid)
    if status:
        if ostatus == 'tomado':
            (owner, stype, amouni, tokeni, amouno, tokeno,
                pmethod, taker, chatlink, dstatus, order_date) = await dmr.getOrderdata(orderid)
            sender = taker if stype == 'buy' else owner
            chatid_s, hiveuser_s = await dmr.getUserchatid(sender)
            receiver = owner if stype == 'buy' else taker
            chatid_r, hiveuser_r = await dmr.getUserchatid(receiver)
            await dmr.setOrderstatus(orderid, 'payed')
            fee = await getFee(receiver, tokeni, amouni)
            if scode == 'es':
                keyboard = [[InlineKeyboardButton(
                    "Confirmar pago", url=f"{boturl}?start=fiatsend_{orderid}")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                rmsg = f"""
Orden `{orderid}`

Se ha realizado el depósito en garantía en `{receptor}` correctamente.

Contacte al usuario  de telegram `{sender}` [->link](https://t.me/{sender}) para que le especifique los datos del envío.
Si demora más de 3 horas luego de esta notificación @`{sender}` puede realizar una disputa y
solicitar la cancelación de la operación. En este caso lo contactaremos para garantizar que no ha enviado aún 
los fondos.

Usted recibe:
{(amouni-fee):.3f} : {tokeni}

Le será descontado  un fee de {fee:.3f} {tokeni}        
Puede evitar las comisiones en próximas operaciones delegando al menos 50 HP al usuario de HIVE `{manager}`.


Proceda a realizar el envío del pago acordado de:
{amouno} : {tokeno}    
Utilizando {pmethod}

Al terminar **Confirme** el pago.     
"""
                await context.bot.send_message(chat_id=chatid_r,
                                               text=rmsg,
                                               parse_mode='Markdown',
                                               reply_markup=reply_markup)

                keyboard = [[InlineKeyboardButton(
                    "Enviar Disputa", url=f"{boturl}?start=dispute_{orderid}")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                smsg = f"""
Se ha notificado a @`{receiver}` [->link](https://t.me/{receiver}) sobre la orden  `{orderid}`. Deben contactarse mutuamente y ponerse de acuerdo sobre los
datos del pago utilizando  {pmethod}.

Si ocurre una demora excesiva (espere al menos 3 horas), problema o un pago fuera de lo acordado efectúe una disputa.
"""
                await context.bot.send_message(chat_id=chatid_s, text=smsg,
                                               parse_mode='Markdown',
                                               reply_markup=reply_markup)
            else:
                keyboard = [[InlineKeyboardButton(
                    "Confirm payment", url=f"{boturl}?start=fiatsend_{orderid}")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                rmsg = f"""
Order `{orderid}`

The security deposit has been made in `{receptor}` correctly.

Contact the telegram user @`{sender}` [->link](https://t.me/{sender}) to specify the payment details.
If it takes more than 3 hours after this notification @`{sender}` you can make a dispute and
request the cancellation of the operation. In this case we will contact you to guarantee that you have not sent yet 
the funds.

You receive:
{(amouni-fee):.3f} : {tokeni}

A fee of {fee:.3f} {tokeni} will be deducted      

You can avoid commissions on upcoming trades by delegating at least 50 HP to the HIVE user `{manager}`.


Proceed to make the shipment of the agreed payment of:
{amouno} : {tokeno}    
Using {pmethod}

At the end **Confirm** the payment.     
"""
                await context.bot.send_message(chat_id=chatid_r,
                                               text=rmsg,
                                               parse_mode='Markdown',
                                               reply_markup=reply_markup)

                keyboard = [[InlineKeyboardButton(
                    "Submit Dispute", url=f"{boturl}?start=dispute_{orderid}")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                smsg = f"""
@`{receiver}` [->link](https://t.me/{receiver}) has been notified about the `{orderid}` command. They should contact each other and agree on the
payment data using {pmethod}.

If there is an excessive delay (wait at least 3 hours), problem or an out-of-date payment, make a dispute.
"""
                await context.bot.send_message(chat_id=chatid_s, text=smsg,
                                               parse_mode='Markdown',
                                               reply_markup=reply_markup)

        else:
            if scode == 'es':
                keyboard = [[InlineKeyboardButton(
                    "Enviar Disputa", url=f"{boturl}?start=dispute_{orderid}")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                if ostatus == 'finish':
                    msg = f"""
Esta orden    `{orderid}` ya fue completada, en caso de problema realice una disputa.
"""
                else:
                    msg = f"""
Existe un error en la  `{orderid}`, realice una disputa para verificar y resolver el problema.
"""
                await update.message.reply_markdown(msg, reply_markup=reply_markup)
            else:
                keyboard = [[InlineKeyboardButton(
                    "Submit Dispute", url=f"{boturl}?start=dispute_{orderid}")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                if ostatus == 'finish':
                    msg = f"""
This order `{orderid}` has already been completed, in case of problem make a dispute.
"""
                else:
                    msg = f"""
There is an error in the `{orderid}`, perform a dispute to verify and resolve the issue.
"""
                await update.message.reply_markdown(msg, reply_markup=reply_markup)

    else:
        msg = {'es': "Transferencia en HIVE sin confirmar, intente nuevamente en unos segundos",
               'en': "Transfer in HIVE unconfirmed, please try again in a few seconds"}
        await update.message.reply_text(msg.get(scode))
# OKX


# start fiatsend
async def fiatsend(update: Update, context: ContextTypes.DEFAULT_TYPE, stext: list) -> None:
    user = update.effective_user
    scode = getlang(user.language_code)
    username = user.username.lower()
    xchatid, xhiveuser = await dmr.getUserchatid(username)

    if xhiveuser == None or xhiveuser == '':
        msg = {'es': 'Debe registrar primero su usuario de HIVE con: /hiveuser nombreusuario',
               'en': 'You must first register your HIVE user with: /hiveuser username'}
        await update.message.reply_text(msg.get(scode))
        return None

    orderid = stext[1]
    (owner, stype, amouni, tokeni, amouno, tokeno,
                pmethod, taker, chatlink, dstatus, order_date) = await dmr.getOrderdata(orderid)
    sender = owner if stype == 'sell' else taker

    status = await dmr.getOrderstatus(orderid)
    if status == 'payed':
        chatid_s, hiveuser_s = await dmr.getUserchatid(sender)
        amouno, tokeno, pmethod = await dmr.getOrdepay(orderid)
        if scode == 'es':
            keyboard = [[InlineKeyboardButton(
                "Liberar Fondos", url=f"{boturl}?start=finish_{orderid}")],
                [InlineKeyboardButton(
                    "Enviar Disputa", url=f"{boturl}?start=dispute_{orderid}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            smsg = f"""
@`{username}` [link](https://t.me/{username}) ha confirmado el envío acordado.

Verifique que ha recibido el monto acordado de:
{amouno} : {tokeno}  
Utilizando el método de pago  {pmethod}

Una vez todo esté correcto libere los fondos.  
*Importante* Una vez ejecute esta acción no se puede deshacer.

En caso de problemas o demora excesiva haga una disputa.
"""
            await context.bot.send_message(chat_id=chatid_s, text=smsg,
                                           parse_mode='Markdown',
                                           reply_markup=reply_markup)
            keyboard = [[InlineKeyboardButton(
                "Enviar Disputa", url=f"{boturl}?start=dispute_{orderid}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            rmsg = f"""
Se ha notificado a @`{sender}` [->link](https://t.me/{sender}) 

Si ocurre una demora excesiva, problemas o un pago fuera de lo acordado efectúe una disputa.
"""
            await update.message.reply_markdown(rmsg, reply_markup=reply_markup)
        else:  # EN
            keyboard = [[InlineKeyboardButton(
                "Releasing Funds", url=f"{boturl}?start=finish_{orderid}")],
                [InlineKeyboardButton(
                    "Submit Dispute", url=f"{boturl}?start=dispute_{orderid}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            smsg = f"""
`{username}` [link](https://t.me/{username}) has confirmed the agreed payment.

Verify that you have received the agreed upon amount of:
{amouno} : {tokeno}  
Using the payment method  {pmethod}

Once everything is correct, release the funds. 
*Important* Once executed this action, it cannot be undone.

In case of problems or excessive delay make a dispute.
"""
            await context.bot.send_message(chat_id=chatid_s, text=smsg,
                                           parse_mode='Markdown',
                                           reply_markup=reply_markup)
            keyboard = [[InlineKeyboardButton(
                "Submit Dispute", url=f"{boturl}?start=dispute_{orderid}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            rmsg = f"""
@`{sender}` [->link](https://t.me/{sender}) has been notified

If an excessive delay, problems or an out-of-agreement payment occurs, make a dispute.
"""
            await update.message.reply_markdown(rmsg, reply_markup=reply_markup)

    else:
        if scode == 'es':
            match status:
                case 'finish':
                    word = 'completada'
                case 'cancel':
                    word = 'cancelada, contacte a soporte'
                case 'nuevo':
                    word = 'sin depósito en garantía contacte a soporte'
                case _:
                    word = 'en estado de error contacte a soporte'
            await update.message.reply_text(f"Esta orden {orderid} está {word}")
        else:
            match status:
                case 'finish':
                    word = 'finish'
                case 'cancel':
                    word = 'cancelled, contact support'
                case 'nuevo':
                    word = 'no guarantee deposit, contact support'
                case _:
                    word = 'in error status contact support'
            await update.message.reply_text(f"This order {orderid} status is {word}")

# OK


async def dispute(update: Update, context: ContextTypes.DEFAULT_TYPE, stext: list) -> None:
    # start-dispute
    user = update.effective_user
    chatid = update.message.chat_id
    scode = getlang(user.language_code)

    if chatid in blacklist:
        msg = {'es': 'Usuario restringido',
               'en': 'Restricted user'}
        await update.message.reply_text(msg.get(scode))
        return None

    username = user.username.lower()

    if len(stext) < 2:
        msg = {'es': "Error en Orden.",
               'en': "Error in Order."}
        await update.message.reply_text(msg.get(scode))
        return None

    orderid = stext[1]
    (owner, stype, amouni, tokeni, amouno, tokeno,
        pmethod, taker, chatlink, dstatus, order_date) = await dmr.getOrderdata(orderid)
    for support in supports:
        chatid, hiveuser = await dmr.getUserchatid(support)
        msg = {'es': f"""
El usuario {username} ha iniciado una disputa sobre la orden {orderid}
Datos de la orden:
[(owner, stype, amouni, tokeni, amouno, tokeno, pmethod, taker, chatlink, dstatus, order_date)]  
{(owner, stype, amouni, tokeni, amouno, tokeno, pmethod, taker, chatlink, dstatus, order_date)}  
""", 'en': f"""
The user {username} has initiated a dispute about the order {orderid}
Order data:
[(owner, stype, amouni, tokeni, amouno, tokeno, pmethod, taker, chatlink, dstatus, order_date)]  
{(owner, stype, amouni, tokeni, amouno, tokeno, pmethod, taker, chatlink, dstatus, order_date)}  
"""}
        await context.bot.send_message(chat_id=chatid, text=msg.get(scode))
        msg = {'es': "Disputa enviada, espere ser contactado por nuestro soporte",
               'en': "Dispute submitted, expect to be contacted by our support"}
        await update.message.reply_text(msg.get(scode))
# OKX


async def listorders(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # /listorders
    user = update.effective_user
    scode = getlang(user.language_code)
    if user.username == '' or user.username == None:
        await update.message.reply_markdown(messages_statU)
        return None
    username = user.username.lower()
    rows = await dmr.getOrderlist(username)
    if rows == None or len(rows) == 0:
        msg = {'es': "No tiene órdenes activas ",
                'en': "There is no active orders"}
        await update.message.reply_text(msg.get(scode))
        return None
    if scode == 'es':
        ordermsg = """
Listado de órdenes activas: 
"""
        for element in rows:
            action = ""
            if element[1] == "nuevo":
                action = f"[cancelar]({boturl}?start=cancel_{element[0]}"
            ordermsg += f"ID:`{element[0]}` Estado: {element[1]} {action} \n"
    else:  # EN
        ordermsg = """
List of active orders:
"""
        for element in rows:
            action = ""
            if element[1] == "nuevo":
                action = f"[cancel]({boturl}?start=cancel_{element[0]}"
            ordermsg += f"ID:`{element[0]}` State: {element[1]} {action} \n"

    await update.message.reply_markdown(ordermsg)
# OKX


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # /start
    user = update.effective_user
    scode = getlang(user.language_code)
    if user.username == '' or user.username == None:
        await update.message.reply_markdown(messages_statU.get(scode))
    else:
        username = user.username.lower()
        chatid = update.message.chat_id
        stext = update.message.text.split()
        if len(stext) == 1:
            await update.message.reply_html(
                rf"Hola {user.mention_html()}!",)
            await update.message.reply_markdown(messages_about.get(scode))
            if not await dmr.checkUser(username):
                await dmr.setUserchatid(username, chatid)
        else:
            textstruct = stext[1].split('_')
            command = textstruct[0]
            match command:
                case 'cancel':
                    await scancel(update, context, textstruct)
                case 'take':
                    await stake(update, context, textstruct)
                case 'totake':
                    await totake(update, context, textstruct)
                case 'hivesend':
                    await hivesend(update, context, textstruct)
                case 'fiatsend':
                    await fiatsend(update, context, textstruct)
                case 'finish':
                    await finish(update, context, textstruct)
                case 'dispute':
                    await dispute(update, context, textstruct)
                case _:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text="Enlaces de órdenes por implementar")
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)


async def dailyOrderClean(context: ContextTypes.DEFAULT_TYPE) -> None:
    # Unactive DB
    activeOrders = await dmr.getOrderNew()
    for orders in activeOrders:
        ido = orders[0]
        sdat = orders[1]
        if getHoursfromDate(sdat) > 36:
            (owner, stype, amouni, tokeni, amouno, tokeno,
             pmethod, taker, chatlink, dstatus, order_date) = await dmr.getOrderdata(ido)
            if dstatus == 'nuevo':
                await dmr.cancelOrder(ido)
                if chatlink != "" and chatlink != None:
                    skk = int(chatlink.split("/").pop())
                    await context.bot.delete_message(
                        chat_id=hcbchatid, message_id=skk)
                xchatid, xhiveuser = await dmr.getUserchatid(owner)
                msg = f"""
`{ido}` order canceled for having more than 36 hours published.
"""
                await context.bot.send_message(chat_id=xchatid, text=msg, parse_mode='Markdown')
# OKX


async def setdailyOrderClean(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user.username == '' or user.username == None:
        await update.message.reply_markdown(messages_statU)
        return None
    else:
        username = user.username.lower()
        if username not in admins:
            await update.message.reply_text("You do not have permissions to send messages")
            return None
        job_queue = context.job_queue
        job_queue.run_daily(await dailyOrderClean, time=datetime.time(
            hour=5, minute=0, second=0))
        await update.message.reply_text("Daily order cleaning activated")
# DB


async def stopdailyOrderClean(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user.username == '' or user.username == None:
        await update.message.reply_markdown(messages_statU)
        return None
    else:
        username = user.username.lower()
        if username not in admins:
            await update.message.reply_text("You do not have permissions to send messages")
            return None
        job_queue = context.job_queue
        job_queue.stop()
        await update.message.reply_text("Daily order cleaning disabled")
# DB


async def orderClean(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user.username == '' or user.username == None:
        await update.message.reply_markdown(messages_statU)
        return None

    username = user.username.lower()
    if username not in admins:
        await update.message.reply_text("You do not have permission to carry out this operation")
        return None
    activeOrders = await dmr.getOrderNew()
    rmsg = ""
    for orders in activeOrders:
        ido = orders[0]
        sdat = orders[1]
        if getHoursfromDate(sdat) > 36:
            (owner, stype, amouni, tokeni, amouno, tokeno,
                pmethod, taker, chatlink, dstatus, order_date) = await dmr.getOrderdata(ido)
            if dstatus == 'nuevo':
                await dmr.cancelOrder(ido)
                if chatlink != "" and chatlink != None:
                    skk = int(chatlink.split("/").pop())
                    try:
                        await context.bot.delete_message(
                            chat_id=hcbchatid, message_id=skk)
                    except:
                        print(chatlink, " can not be deleted, verify \n", await dmr.getOrderdata(ido))
                xchatid, xhiveuser = await dmr.getUserchatid(owner)
                msg = f"""
`{ido}` order canceled for having more than 36 hours published. 
"""
                await context.bot.send_message(chat_id=xchatid, text=msg, parse_mode='Markdown')
                rmsg += msg
    rmsg += "\n"
    rmsg += "Cleaning of daily orders carried out"
    await update.message.reply_markdown(rmsg)
# OKX
