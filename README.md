# Hive_P2P_Bot

This is a Python-based Telegram Bot for publishing and managing P2P exchange offers native to the HIVE blockchain. This development has been made by the [HiveCuba](https://ecency.com/hive-10053/@ertytux/hivecuba-p2p-como-funciona-es) community. It is based on a guaranteed custody mechanism by the guarantor account, trusted and supported by the community owner of the bot. It has zero commissions for users who have a subscription delegation to a manager HIVE account (sometimes the same as HIVE's Bot account or the trusted community HIVE account).

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
python3 -m venv env
```

* Activate the virtual environment

```Bash
#Windows
env\Scripts\activate

#macOS or Linux
env/bin/activate
```

* Install the packages from the requirements.txt file

```Bash
pip install flask
pip install -r requeriment.txt
```

* Creating a Telegram bot:
  - Contact [@BotFather](https://t.me/BotFather) on Telegram.
  - Use the `/newbot` command to create a new bot.
  - Follow the instructions to choose a name and username for your bot.
  - You'll receive a unique _YOUR_BOT_TOKEN_ API token for your bot. Save it securely.
* Add to your bot's command configuration as the following:

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
* With the information collected in the previous steps edit the _env_example_ file (Linux / macOS) or .env_example.bat (Windows).

```Bash
#env_example file Linux or macOS
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

* Windows .env_example.bat
**Note:** You can copy .env_example.bat to a new .env.bat and execute call .env.bat

```Bash
set hcbtoken=YOUR_BOT_TOKEN
set hcburl=https://t.me/YOUR_BOT_USERNAME

set hivesqlserver=vip.hivesql.io
set hivesqldb=DBHive
set hivesqluser=YOUR_HIVESQL_USERNAME
set hivesqlpsw=YOUR_HIVESQL_PASSWD

set hcbchat=@YOUR_TELEGRAM_OFFERT_CHANNEL


set bothiveuser=YOUR_BOT_HIVE_USERNAME
set activekey=YOUR_BOT_HIVE_ACTIVE_KEY

set bothivedelegate=YOUR_DELEGATE_HIVE_USERNAME
```

* Edit the file _src/config.py_ with your personalized settings. You must designate at least one Telegram user as an administrator and support
* Run and setup into operations the bot with the command:

```Bash
#Linux or macOS
./run.sh

#Windows
call .env_sample.bat
```

**Note:** Deactivate the virtual environment after finishing.
* To exit the virtual environment, execute the following command:

```Bash
cd Hive_P2P_Bot

Windows
env\Scripts\deactivate

macOS or Linux
env/bin/deactivate
```

**That's all!!**

## How you can contribute

* If it is of interest to you, you can use the [HiveCuBaP2P_Bot](https://t.me/HiveCuBaP2P_Bot) functional bot to get acquainted and check its functionality.
* Any suggestion, change proposal, or code can be made here on GitHub, we apply our [FOSS](https://osssoftware.org/blog/free-and-open-source-software-foss-core-principles/) policies in our development and everyone is welcome to contribute.

## Donations

You can donate to our project using HIVE or HBD with the account `hivecuba.p2p` with the memo `Donate` or using bitcoin lighting to the account `hivecuba.p2p@sats.v4v.app`.

![QR](https://api.v4v.app/p/hivecuba.p2p.png)

Thank you very much in advance!!

## License

MIT
