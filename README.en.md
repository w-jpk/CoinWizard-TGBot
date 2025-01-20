# CoinWizard Telegram Bot

This project is a Telegram bot that helps users manage their virtual balance, conduct trades and interact with cryptocurrency options. The bot was created to demonstrate the capabilities of the Telegram API and the use of a SQLite database to store user information.

## Contents

  - [Warning](#important-warning)
  - [Installation and configuration](#installation-and-configuration)
  - [Creating a config.py file](#creating-a-configpy-file)
  - [Bot functionality](#bot-functionality)
  - [Project structure](#project-structure)
  - [Updates](#updates)

## Important warning

This bot is created solely for **entertainment and educational purposes**. It is not intended to be used in real financial transactions or trading. All data, including balance, transactions and trading results, are virtual and have no relation to real money or assets.

The developers and creators of the bot **do not bear any responsibility** for any actions taken by users based on the information provided by the bot. Use of the bot is at your own risk.

If you want to engage in real trading or investments, contact licensed financial institutions and consultants.

---

⚠️ **Important!** If you see a similar bot that requires you to transfer real money or promises a guaranteed profit, do not trust such offers! This may be a scam. Never transfer money to strangers or trust dubious sources. Be vigilant and remain cautious!

## Installation and setup

### 1. Clone the repository

To start working with the project, clone the repository to your computer:

```bash
git clone https://github.com/w-jpk/CoinWizard-TGBot.git
cd CoinWizard_TGBot
```

## Creating a config.py file

The bot requires a token, which you receive when creating a bot through BotFather in Telegram.

1. Create a config.py file in the root directory of the project.
2. Add the following line to it, replacing "YOUR BOT TOKEN" with your token:

```python
# config.py
BOT_TOKEN = "YOUR BOT TOKEN"
adm = YOUR ID
check = ID of the chat where the checks will be sent
card = "your details"
```

### Example:

```python
# config.py
BOT_TOKEN = "1234567890:ABCdefGhIJKlmNoPQRstuVWXyz"
amd = [12345, 67890] - you can add multiple administrators
check = -123456789 - the chat where the notifications will be sent
card = "4100 1234 5678 9012" - details for the transfer
```

### Important: Never share your token publicly or add it to the repository. Make sure the config.py file is added to .gitignore to avoid accidental token leakage.

## Launching the bot

Once you have configured the config.py file, you can launch the bot:

```bash
python bot.py
```

The bot will start working and will respond to commands and messages in Telegram.

## Bot functionality

The bot provides the following features:

- Personal account:
- View balance.
- View statistics (number of successful and unsuccessful transactions, withdrawals, etc.).
- Balance replenishment (virtual).
- Withdrawal of funds (virtual).
- Options:
- Ability to "invest" in cryptocurrencies (BTC, ETH, BNB and others).
- Simulation of trades with a 50% probability of success.
- Technical support:
- Link to chat with support.
- Information about the service:
- Brief description of the bot's capabilities.

## Project structure

```plaintext
CoinWizard_TGBot/
├── bot.py # Main bot file
├── database.py # File for working with the SQLite database
├── config.py # File for storing the bot token (created manually)
├── README.md # Project documentation
└── assets/ # Folder for storing images and other resources
└── project-1.jpg # Example of an image for your personal account
```

## Updates

- ### 01/12/2025

  - Bot added to GitHub;
  - Added:

    - Cryptocurrency functionality;
    - "🗃 Verification" message;
    - Message "🔷 About the service";
    - Message "📜 Certificate";
    - Message "Service guarantee";
    - Message "📈 Network status".

  - Chat link has been updated in the following places:

  ```
  elif text == "🧑🏻‍💻 Tech support":
  ...the rest of the code...
  [InlineKeyboardButton("📩 Write", url="https://t.me/durov")] # Change the link to your account

  elif query.data == "verify":
  ...the rest of the code...
  [InlineKeyboardButton("💬 Contact tech support", url="https://t.me/durov")] # Change the link to your account
  ```

- ### 01/18/2025

  - Card top-up functionality has been updated. Now you can enter and replenish any amount.

- ### 01/19/2025

  - Added game functionality (Options -> Select option -> Enter amount -> Select chart direction -> Select time -> Wait for result);
  - Added verification item in the DB;
  - Changes made to the code;
  - Added commands for the administrator:
  ```
  /add_balance User ID amount - command to replenish the user's balance.
  example: /add_balance 123456789 10000

  /verify_user User ID 0 or 1 - command to verify the user.
  Example: /verify_user 123456789 1

  /set_balance User ID amount - command to set a specific balance for the user.
  Example: /set_balance 123456789 10000

  /withdraw_funds User ID amount - command to withdraw the user's funds.
  Example: /withdraw_funds 123456789 10000

  /broadcast message - command to send an announcement to all users.
  Example: /broadcast important message!

  /user_info User ID - command to get user data.
  Example: /user_info 123456789
  ```
  - A new replenishment method has been added. Now replenishment occurs through administrator confirmation. How it works: The user selects to top up via a bank card -> The bot sends him the details and waits for a screenshot of the receipt -> After receiving the receipt, the bot sends this message to the administrator and the administrator checks the receipt, after which he tops up the user's account using the /add_balance command.

  - A new withdrawal method has been added;
  - A system of promo codes has been added: PROMO100, PROMO500, PROMO1000;
  - Verification check for withdrawal of funds has been added;
  - The verification request has been updated;
  - The /help command has been added for the administration;
  - The mechanism for contacting technical support has been changed.

- ### 01/20/2025

  - A referral system has been added: the transferred user receives 1,000₽, the creator of the referral receives 5,000₽;
  - Moved the details to the config.py file, now the file looks like this:
  ```
  # config.py
  BOT_TOKEN = "1234567890:ABCdefGhIJKlmNoPQRstuVWXyz"
  amd = [12345, 67890] - you can add multiple administrators
  check = -123456789 - chat where notifications are sent
  card = "4100 1234 5678 9012" - details for transfer
  ```
  - Updated [Warning](#important-warning);
  - Referral system moved to "🔷 About the service";
  - Added new cryptocurrencies;
  - Added functionality for processing cryptocurrencies;
  - Changes have been made to the game;
  - Updated referral system: new user will not receive anything, but the author of the link will receive 1,000₽ on the balance.