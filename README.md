 
# Hive_P2P_Bot

This is a Python-based Telegram Bot for publishing and managing P2P exchange offers native to the HIVE blockchain. This development has been made by the [HiveCuba](https://ecency.com/hive-10053/@ertytux/hivecuba-p2p-como-funciona-es) community.  It is based on a guaranteed custody mechanism by the guarantor account, trusted and supported by the community owner of the bot. It has zero commissions for users who have a subscription delegation to a manager HIVE account (sometimes the same as HIVE's Bot account or the trusted community HIVE account).


![imagen.png](https://files.peakd.com/file/peakd-hive/ertytux/23tGXuviKJMM4EcWuqfYgmyWKoSXEFkiWp8DeDUN79pQTPyWN38KKAy22tzdN8rddxvg1.png)

<sub>
Screenshot in https://t.me/HiveCuBaP2P_Bot
</sub>



See more [here](https://ecency.com/hive-10053/@ertytux/hivecuba-p2p-como-funciona-es)

## Software requirements

We recommend that you use the latest stable Ubuntu version as an operating system, it must have **Python>=3.10** installed with the package manager **pip**:

```Bash
sudo apt update
sudo apt install python3-pip
```

## Requirements for deployment

To run the P2P Bot you need:

* Cloning the Bot project
```Bash
git clone https://github.com/Ertytux/Hive_P2P_Bot.git
```
* Create an exclusive virtual environment
```Bash
cd Hive_P2P_Bot
python3 -mvev env
```
* Creating a Telegram bot: 
   - Contact [@BotFather](https://t.me/BotFather) on Telegram.
   - Use the `/newbot` command to create a new bot.
   - Follow the instructions to choose a name and username for your bot.
   - You'll receive a unique *YOUR_BOT_TOKEN* API token for your bot. Save it securely.
* Add to your bot's command configuration the following:
```Bash
start -Reset your user's settings
escrow -Learn about our escrow system at HIVE
hiveuser -Register your HIVE user
userinfo -Display the user's information
buy -Place a purchase order
sell -Place a sales order
cancel -Delete an order
listorder -Show the list of active orders
prices -Know the reference prices according to Coingecko and yadio.io
price -To know the price of a currency using Coingecko as a reference and yadio.io
msg -Send messages to the offers channel (Admins only)
```
* Have an account in HIVESQL, see https://hivesql.io/registration/.
* Create a receptor account in HIVE that operates the bot.
* Designate an account manager in HIVE that will receive HP delegations to have zero fees.
* Create a Telegram channel for offers and add the bot user as administrator. You can also associate a chat group to serve as support.
* With the information collected in the previous steps edit the *env_example* file.
```Bash
#BOT
export hcbtoken=YOUR_BOT_TOKEN
export hcburl=https://t.me/YOUR_BOT_USERNAME

#HIVESQL
export hivesqlserver=vip.hivesql.io 
export hivesqldb=DBHive
export hivesqluser=YOUR_HIVESQL_USERNAME
export hivesqlpsw=YOUR_HIVESQL_PASSWD

#TELEGRAM PUBLIC OFFERT CHANNEL YOUR_BOT_USERNAME must be admin
export hcbchat=@YOUR_TELEGRAM_OFFERT_CHANNEL


#HIVE BOT ACCOUNT 
export bothiveuser=YOUR_BOT_HIVE_USERNAME
export activekey=YOUR_BOT_HIVE_ACTIVE_KEY

#HIVE ACCOUNT TO DELEGATE AND GET 0 FEE
export bothivedelegate=YOUR_DELEGATE_HIVE_USERNAME
```
* Edit the file *src/config.py* with your personalized settings. You must designate at least one Telegram user as an administrator and support
* Run and setup into operations the bot with the command:
```Bash
./run.sh
```
**That's all!!**

## How you can contribute

* If it is of interest to you, you can use the [HiveCuBaP2P_Bot](https://t.me/HiveCuBaP2P_Bot) functional bot to get acquainted and check its functionality.
* Any suggestion, change proposal, or code can be made here on GitHub, we apply our [FOSS](https://osssoftware.org/blog/free-and-open-source-software-foss-core-principles/) policies in our development and everyone is welcome to contribute.

## Donations
You can donate to our project using HIVE or HBD with the account `hivecuba.p2p` con el memo `Donate` or using bitcoin lighting to the account `hivecuba.p2p@sats.v4v.app`. 

Thank you very much in advance!!

## License

MIT




