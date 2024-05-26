from config import manager,hcbchatid,hcbsup,fpp,fhive,fhbd

messages_about = {'es': rf"""
Este es un bot para la publicación y gestión de ofertas de intercambio P2P en HIVE.

Utilice los comandos:	
/start -Reiniciar la configuración de su usuario 🟢
/escrow -Conocer sobre  nuestro sistema de escrow en HIVE 🔄		
/hiveuser -Registrar su usuario de HIVE	👤	
/buy -Poner una orden de COMPRA	🔺	
/sell -Poner una orden de VENTA	🔻	
/cancel -Eliminar una orden	🔴	
/listorder -Mostrar el listado de órdenes activas	📝	
/prices -Conocer los precios de referencia según Coingecko y yadio.io 📈
/price -Conocer el precio de una moneda usando de referencia  Coingecko y yadio.io 💶
/msg -Enviar mensajes al canal de ofertas (Solo Admins) 🔐

Visite el canal de ofertas {hcbchatid}		

Si algo sale mal, intente ejecutar /start o comentarnos en nuestro [grupo de soporte]({hcbsup}), recuerde que estamos en proceso de desarrollo.

Gracias!!
""", 'en': rf"""
This is a bot for publishing and managing P2P exchange offers on HIVE.

Use the commands:	
/start - Restart your user's settings 🟢
/escrow - Learn about our  escrow system in HIVE 🔄		
/hiveuser - Register your HIVE username 👤	
/buy - Place a BUYING order 🔺	
/sell - Place a SELLING order 🔻		
/cancel - Delete an order 🔴	
/listorder - Show the list of active orders 📝	
/prices - Know about the prices of reference according to Coingecko and yadio.io 📈
/price - Know the price of one currency using the reference Coingecko and yadio.io 💶
/msg - Send messages to the offers channel (Admins only) 🔐

Visit the offers channel {hcbchatid}		

If something goes wrong, try to run /start or comment us in our [support group]({hcbsup}), remember that we are in the process of development.

Thank you!!
"""}

messages_support = {'es': f"""
 Puede plantear sus dificultades en el [grupo de soporte]({hcbsup})
""", 'en': f"""
You can raise your difficulties in the [support group]({hcbsup})
"""}


messages_statU = {'es': """
Para usar este bot, debes activar tu nombre de usuario de Telegram. Para activarlo, abra el menú de hamburguesas en la esquina superior izquierda y seleccione: 

Configuración - > Editar perfil - > Nombre de usuario
""", 'en': """
To use this bot, you need to activate your Telegram username. To activate it, open the hamburger menu in the upper left corner and select: 

Settings - > Edit profile - > Username
"""}

messages_registre = {'es': """ 
No ha registrado su usuario de HIVE, utilice        
/hiveuser nombreUsuarioHive 
""", 'en': """
You have not registered your HIVE username, please use        
/hiveuser hiveusername
"""}

messages_escrow = {'es': """
Vea el post en  `hivecuba` [HiveCuba P2P: ¿Como funciona?](https://ecency.com/hive-10053/@ertytux/hivecuba-p2p-como-funciona-es)
""", 'en': """
See the post on `hivecuba` [HiveCuba P2P: How does it work?](https://ecency.com/hive-10053/@ertytux/hivecuba-p2p-como-funciona-es)
"""}

messages_notHP = {'es': rf"""
Delegar Hive Power: Delegar  a la cuenta  `{manager}`  permite que el poder de voto de la comunidad sea cada vez mayor. Esto se traduce en una mayor capacidad para recompensar el contenido de calidad y apoyar a los creadores.  Es bueno recordarles que delegar no te da derecho a votos, el voto siempre dependerá del contenido. 

Al delegar a `{manager}` cubrimos los costos de operaciones de este bot. WIN-WIN 

Delegar, es basicamente decirle a la blockchain que los recursos y el poder de voto del Hive Power que vas a delegar se los de a otra cuenta. Nunca pierdes tu Hive Power.
""", 'en': rf"""
Delegating Hive Power: Delegating to the  account `{manager}` allows the voting power of the community to be increased every time. This translates into a greater ability to reward quality content and support creators.  It is good to remind them that delegating does not give you the right to votes, the vote will always depend on the content. 

By delegating to `{manager}` we cover the operating costs of this bot. WIN-WIN 

Delegating, is basically telling the blockchain that the resources and voting power of the Hive Power that you are going to delegate will be given to another account. You never lose your Hive Power.
"""}


messages_notSt={'es':"""
Debe registrar su usuario de HIVE para poder operar en nuestro bot:  
/hiveuser nombreUsuarioHive            
Además, si ha delegado al menos 50 HP a la cuenta  `{manager}` disfrutará cero comisiones.   
""",'en':"""
You must register your HIVE username in order to operate on our bot:  
/hiveuser hiveusername              
In addition, if you have delegated at least 50 HP to the `{manager}` account you can enjoy zero fees.
"""}

messages_fees={'es':rf"""
Nuestra comisión es del {fpp*100:.2f}% sobre el monto transferido, más:
* {fhbd} para HBD
* {fhive} para HIVE

Este se alade al monto a transferir si usted envía o se descuenta si usted recibe.

Si usted delega al menos 50 HP a `{manager}` no tiene que preocuparse por comisiones 😁

""",
'':rf"""
Our commission is from the {fpp*100:.2f}% on the amount transferred, plus:
* {fhbd} for HBD
* {fhive} for HIVE

This is added to the amount to be transferred if you send or discounted if you receive.

If you have delegated at least 50 HP to the `{manager}` account you can enjoy zero fees 😁
"""}




