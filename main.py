Earn Tips 24 Telegram Bot - Premium Version

import logging import os import random import firebase_admin from firebase_admin import credentials, db from telegram import (Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ChatAction) from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext) from dotenv import load_dotenv from datetime import datetime

load_dotenv()

Firebase setup

cred = credentials.Certificate(os.getenv("FIREBASE_CREDENTIALS_PATH")) firebase_admin.initialize_app(cred, { 'databaseURL': os.getenv("FIREBASE_DB_URL") })

Telegram Bot Token

TOKEN = os.getenv("7343006860:AAEzZkUuwM_3nfXWqyMG6ZORnlrYvmtewcI") ADMIN_ID = int(os.getenv("6243881362"))

Logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO) logger = logging.getLogger(name)

Start command

user_captcha = {}

def start(update: Update, context: CallbackContext): user = update.effective_user context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

captcha = random.randint(1000, 9999)
user_captcha[user.id] = captcha
context.bot.send_message(chat_id=user.id, text=f"Welcome {user.first_name}!\nPlease verify: What is {captcha}?")

Captcha verification

def verify_captcha(update: Update, context: CallbackContext): user = update.effective_user text = update.message.text.strip()

if user.id not in user_captcha:
    return

if text.isdigit() and int(text) == user_captcha[user.id]:
    # Register user if not exists
    ref = db.reference(f"users/{user.id}")
    if not ref.get():
        ref.set({
            "id": user.id,
            "name": user.full_name,
            "balance": 0,
            "ref_by": context.args[0] if context.args else "",
            "join_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "team": []
        })
        # Add to referrer team
        if context.args:
            parent_ref = db.reference(f"users/{context.args[0]}/team")
            team = parent_ref.get() or []
            team.append(user.id)
            parent_ref.set(team)
    show_main_menu(update, context)
    del user_captcha[user.id]
else:
    update.message.reply_text("Incorrect captcha, try again.")
    start(update, context)

Show main menu

def show_main_menu(update: Update, context: CallbackContext): keyboard = [ [InlineKeyboardButton("👤 Profile", callback_data='profile')], [InlineKeyboardButton("🎁 Refer & Earn", callback_data='refer')], [InlineKeyboardButton("👥 Team Member", callback_data='team')], [InlineKeyboardButton("💡 Earn Tips", callback_data='tips')], [InlineKeyboardButton("💸 Withdraw Cash", callback_data='withdraw')], [InlineKeyboardButton("🛠️ Support", callback_data='support')], [InlineKeyboardButton("🌐 Language", callback_data='language')] ] context.bot.send_message(update.effective_chat.id, "Please choose:", reply_markup=InlineKeyboardMarkup(keyboard))

Callback query handler

def menu_callback(update: Update, context: CallbackContext): query = update.callback_query user_id = query.from_user.id query.answer()

ref = db.reference(f"users/{user_id}")
user_data = ref.get()

if query.data == "profile":
    msg = f"👤 Name: {user_data['name']}\n🆔 ID: {user_data['id']}\n💰 Balance: {user_data['balance']}\n🕒 Joined: {user_data['join_date']}"
    query.edit_message_text(msg)

elif query.data == "refer":
    link = f"https://t.me/{context.bot.username}?start={user_id}"
    msg = f"🎁 Refer & Earn\nName: {user_data['name']}\nReferral Link: {link}\nEarn ৳50 for each successful referral."
    query.edit_message_text(msg)

elif query.data == "team":
    team = user_data.get("team", [])
    names = []
    for uid in team:
        u = db.reference(f"users/{uid}").get()
        if u:
            names.append(f"- {u['name']}")
    team_msg = "\n".join(names) if names else "No team members yet."
    query.edit_message_text(f"👥 Total Team: {len(team)}\n{team_msg}")

elif query.data == "tips":
    buttons = [
        [InlineKeyboardButton("📧 Gmail Account Sale", url="https://link1.com")],
        [InlineKeyboardButton("📱 Whatsapp Number Sale", url="https://link2.com")],
        [InlineKeyboardButton("🎮 BDT Game", url="https://link3.com")],
        [InlineKeyboardButton("💻 Web & App Buy", url="https://link4.com")]
    ]
    query.edit_message_text("💡 Choose an option to earn:", reply_markup=InlineKeyboardMarkup(buttons))

elif query.data == "withdraw":
    balance = user_data['balance']
    if balance < 1000:
        query.edit_message_text(f"Your balance is ৳{balance}. Minimum ৳1000 required to withdraw.")
    else:
        context.user_data['withdraw'] = True
        query.edit_message_text("Send your withdrawal method (Bkash/Nagad/Rocket/Upay) and amount.")

elif query.data == "support":
    query.edit_message_text("🛠️ Contact us for support: https://t.me/U011111111")

elif query.data == "language":
    langs = [
        [InlineKeyboardButton("বাংলা", callback_data='lang_bn')],
        [InlineKeyboardButton("English", callback_data='lang_en')],
        [InlineKeyboardButton("हिन्दी", callback_data='lang_hi')],
        [InlineKeyboardButton("中文", callback_data='lang_cn')],
        [InlineKeyboardButton("日本語", callback_data='lang_jp')],
        [InlineKeyboardButton("العربية", callback_data='lang_ar')]
    ]
    query.edit_message_text("Choose your language:", reply_markup=InlineKeyboardMarkup(langs))

Withdrawal input handler

def withdraw_handler(update: Update, context: CallbackContext): if not context.user_data.get('withdraw'): return user_id = update.effective_user.id text = update.message.text.strip()

try:
    method, amount = text.split()
    amount = int(amount)
    user_ref = db.reference(f"users/{user_id}")
    user_data = user_ref.get()
    if amount > user_data['balance']:
        update.message.reply_text("❌ You cannot withdraw more than your balance.")
    else:
        user_ref.update({"balance": user_data['balance'] - amount})
        context.bot.send_message(ADMIN_ID, f"Withdraw Request\nUser: {user_data['name']}\nID: {user_id}\nMethod: {method}\nAmount: ৳{amount}")
        update.message.reply_text("✅ Withdrawal request sent. Please wait.")
    context.user_data['withdraw'] = False
except:
    update.message.reply_text("❗ Please send in format: Method Amount\nExample: Bkash 1000")

Admin command to view all users

def view_users(update: Update, context: CallbackContext): if update.effective_user.id != ADMIN_ID: return users = db.reference("users").get() msg = "All Users:\n" for uid, data in users.items(): msg += f"{data['name']} - {uid} - ৳{data['balance']}\n" update.message.reply_text(msg)

Admin command to set balance

def set_balance(update: Update, context: CallbackContext): if update.effective_user.id != ADMIN_ID: return try: uid, amount = context.args[0], int(context.args[1]) db.reference(f"users/{uid}").update({"balance": amount}) update.message.reply_text(f"✅ Balance set to ৳{amount} for {uid}") except: update.message.reply_text("Usage: /setbalance user_id amount")

Main entry

if name == 'main': updater = Updater(TOKEN) dp = updater.dispatcher

dp.add_handler(CommandHandler('start', start))
dp.add_handler(MessageHandler(Filters.text & Filters.regex(r'^[0-9]{4}$'), verify_captcha))
dp.add_handler(CallbackQueryHandler(menu_callback))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, withdraw_handler))

dp.add_handler(CommandHandler("viewusers", view_users))
dp.add_handler(CommandHandler("setbalance", set_balance, pass_args=True))

updater.start_polling()
updater.idle()

