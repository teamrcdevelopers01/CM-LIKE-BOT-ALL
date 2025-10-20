# Final version
# FREE FIRE MAX AUTO-LIKE BOT 🤖 (MODDING BY CM)
#YOUTUBE CHANNEL 👉 MODA OF CM HACK
#ANY ISHU CONTACT OWNER - @rc_team_01 [ CM ]
import telegram
# VERSION 2 - FINAL FIX
import telegram
from telegram.ext import Application, CommandHandler, ContextTypes
# ... बाकी का सारा कोड वैसा ही रहेगा
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram import Update
import requests
import os
import asyncio
from datetime import datetime
import threading
import random
from tinydb import TinyDB, Query

# --- Configuration --- ⚙️
BOT_TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = 6296339174  # 👑 Apna Telegram User ID yahan daalein

# --- Database Setup --- 🗄️
db = TinyDB('db.json')
users_table = db.table('users')
config_table = db.table('config')
groups_table = db.table('groups') # Groups ke liye naya table

# --- API Configuration --- 🌐
API_URLS = {
    "default": "https://28-0.vercel.app",
}

# --- Stylish MODDING BY CM Message --- 🎨
def get_stylish_header():
    stylish_messages = [
        "╔═══════════════════════╗\n║    🚨 MODDING BY CM 🚨    ║\n╚═══════════════════════╝",
        "✦ ────────────────────── ✦\n        🚨 MODDING BY CM 🚨\n✦ ────────────────────── ✦",
        "▄︻デ══━一 🚨 MODDING BY CM 🚨 一━══デ︻▄"
    ]
    return random.choice(stylish_messages)

# --- Helper Functions ---
def get_api_url():
    """🌐 Database se current API URL prapt karta hai"""
    settings = config_table.get(doc_id=1)
    if settings and 'api_url' in settings:
        return settings['api_url']
    config_table.upsert({'doc_id': 1, 'api_url': API_URLS['default']}, doc_ids=[1])
    return API_URLS['default']

async def is_owner(update: Update):
    """🛂 Check karta hai ki user owner hai ya nahi"""
    if update.effective_user.id == OWNER_ID:
        return True
    await update.message.reply_text("❌ You are not authorized to use this command.")
    return False

# --- API Interaction --- 📡
async def call_api(uid, api_url):
    try:
        response = requests.get(f"{api_url}/{uid}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling API for UID {uid}: {e}")
        return {"status": "error", "message": str(e)}

# --- Bot User Commands --- 🤖

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    header = get_stylish_header()
    start_message = (
        f"{header}\n\n"
        f"👋 **Welcome, {user.first_name}!**\n\n"
        "I am your FREE FIRE MAX Auto-Like Bot. I can help you get likes on your profile automatically!\n\n"
        "**Here's how to get started:**\n"
        "1. Set your FF MAX UID using: `/like <Your_UID>`\n"
        "2. Turn on auto-likes using: `/autolike on`\n\n"
        "**Available Commands:**\n"
        "  - `/start` - Show this welcome message\n"
        "  - `/help` - Get detailed command info\n"
        "  - `/like <UID>` - Set or update your UID\n"
        "  - `/autolike <on/off>` - Enable or disable auto-likes\n"
        "  - `/mylike` - Check your current settings\n"
        "  - `/status` - Check the bot's status\n"
    )
    await update.message.reply_text(start_message, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    header = get_stylish_header()
    help_text = (
        f"{header}\n\n"
        "**Need help? Here's what I can do:**\n\n"
        "🔹 **/like `<Your_UID>`**\n"
        "   - Example: `/like 123456789`\n\n"
        "🔹 **/autolike `<on/off>`**\n"
        "   - Example: `/autolike on`\n\n"
        "🔹 **/mylike**\n"
        "   - Check your current status.\n\n"
        "🔹 **/status**\n"
        "   - Check the bot's operational status.\n"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def like(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    User = Query()
    if not context.args:
        await update.message.reply_text("❌ Usage: `/like <Your_UID>`")
        return
    uid = context.args[0]
    if not uid.isdigit() or len(uid) < 6:
        await update.message.reply_text("❌ Invalid UID.")
        return
    users_table.upsert({"user_id": user_id, "uid": uid}, User.user_id == user_id)
    await update.message.reply_text(f"✅ Your UID `{uid}` has been saved! Sending a like...", parse_mode='Markdown')
    api_response = await call_api(uid, get_api_url())
    if api_response and api_response.get("status") == "success":
        await update.message.reply_text("🎉 Like sent successfully!")
    else:
        await update.message.reply_text("😞 Sorry, couldn't send a like.")

async def autolike(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    User = Query()
    if not context.args or context.args[0].lower() not in ['on', 'off']:
        await update.message.reply_text("❌ Usage: `/autolike <on/off>`")
        return
    user_data = users_table.get(User.user_id == user_id)
    if not user_data or 'uid' not in user_data:
        await update.message.reply_text("🤔 Please set your UID first using `/like <UID>`.")
        return
    status = context.args[0].lower() == 'on'
    users_table.update({"autolike": status}, User.user_id == user_id)
    status_text = "ENABLED" if status else "DISABLED"
    await update.message.reply_text(f"✅ Auto-like has been **{status_text}**!", parse_mode='Markdown')

async def mylike(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    User = Query()
    user_data = users_table.get(User.user_id == user_id)
    if not user_data or 'uid' not in user_data:
        await update.message.reply_text("🤔 You haven't set your UID yet.")
        return
    uid = user_data.get("uid")
    autolike_status = "ON" if user_data.get("autolike", False) else "OFF"
    await update.message.reply_text(f"**Your Settings:**\n- **UID:** `{uid}`\n- **Auto-Like:** `{autolike_status}`", parse_mode='Markdown')

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    User = Query()
    total_users = len(users_table)
    autolike_enabled_users = users_table.count(User.autolike == True)
    status_message = (
        f"**🤖 Bot Status:**\n\n"
        f"  - **Total Users:** {total_users}\n"
        f"  - **Auto-Like ON:** {autolike_enabled_users}\n"
        f"  - **Status:** `Running` ✅\n\n{get_stylish_header()}"
    )
    await update.message.reply_text(status_message, parse_mode='Markdown')

# --- Bot Admin Commands --- 🛠️

async def groupid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_owner(update): return
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"This Group's ID is: `{chat_id}`", parse_mode='Markdown')

async def addgroup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_owner(update): return
    if not context.args:
        await update.message.reply_text("Usage: /addgroup <group_id>")
        return
    group_id = context.args[0]
    try:
        gid = int(group_id)
        Group = Query()
        if groups_table.contains(Group.id == gid):
            await update.message.reply_text("This group is already in the list.")
        else:
            groups_table.insert({'id': gid})
            await update.message.reply_text(f"✅ Group {gid} added successfully!")
    except ValueError:
        await update.message.reply_text("Invalid Group ID.")

async def removegroup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_owner(update): return
    if not context.args:
        await update.message.reply_text("Usage: /removegroup <group_id>")
        return
    group_id = context.args[0]
    try:
        gid = int(group_id)
        Group = Query()
        if groups_table.remove(Group.id == gid):
            await update.message.reply_text(f"✅ Group {gid} removed successfully!")
        else:
            await update.message.reply_text("Group not found in the list.")
    except ValueError:
        await update.message.reply_text("Invalid Group ID.")

async def listgroups(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_owner(update): return
    all_groups = groups_table.all()
    if not all_groups:
        await update.message.reply_text("No groups have been added yet.")
        return
    message = "**Approved Groups:**\n"
    for group in all_groups:
        message += f"- `{group['id']}`\n"
    await update.message.reply_text(message, parse_mode='Markdown')

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_owner(update): return
    message_to_send = " ".join(context.args)
    if not message_to_send:
        await update.message.reply_text("Usage: /broadcast <message>")
        return
    
    all_groups = groups_table.all()
    if not all_groups:
        await update.message.reply_text("No groups to broadcast to. Add groups using /addgroup.")
        return
        
    sent_count = 0
    failed_count = 0
    for group in all_groups:
        try:
            await context.bot.send_message(chat_id=group['id'], text=message_to_send)
            sent_count += 1
            await asyncio.sleep(0.5) # Avoid hitting rate limits
        except Exception as e:
            failed_count += 1
            print(f"Failed to send to group {group['id']}: {e}")
    
    await update.message.reply_text(f"📣 Broadcast finished!\n- Sent to: {sent_count} groups\n- Failed for: {failed_count} groups")


async def setapi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_owner(update): return
    if not context.args:
        await update.message.reply_text("Usage: /setapi <url>")
        return
    new_api_url = context.args[0]
    config_table.upsert({'doc_id': 1, 'api_url': new_api_url}, doc_ids=[1])
    await update.message.reply_text(f"✅ API URL updated to: {new_api_url}")

async def apiinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_owner(update): return
    await update.message.reply_text(f"ℹ️ Current API URL: {get_api_url()}")

async def resetapi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_owner(update): return
    config_table.upsert({'doc_id': 1, 'api_url': API_URLS['default']}, doc_ids=[1])
    await update.message.reply_text("✅ API URL has been reset to default.")

# --- Auto-Like Scheduler --- ⏳
async def auto_like_scheduler():
    while True:
        User = Query()
        api_url = get_api_url()
        users_to_like = users_table.search(User.autolike == True)
        print(f"[{datetime.now()}] Scheduler: Found {len(users_to_like)} users to like.")
        for user_data in users_to_like:
            if "uid" in user_data:
                await call_api(user_data["uid"], api_url)
                await asyncio.sleep(5)
        await asyncio.sleep(600)

# --- Main Function --- 🚀
def main():
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN is not set.")
        return

    application = Application.builder().token(BOT_TOKEN).build()
    
    # User handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("autolike", autolike))
    application.add_handler(CommandHandler("like", like))
    application.add_handler(CommandHandler("mylike", mylike))
    application.add_handler(CommandHandler("status", status))

    # Admin handlers
    application.add_handler(CommandHandler("groupid", groupid))
    application.add_handler(CommandHandler("addgroup", addgroup))
    application.add_handler(CommandHandler("removegroup", removegroup))
    application.add_handler(CommandHandler("listgroups", listgroups))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CommandHandler("setapi", setapi))
    application.add_handler(CommandHandler("apiinfo", apiinfo))
    application.add_handler(CommandHandler("resetapi", resetapi))

    # Scheduler thread
    scheduler_thread = threading.Thread(target=lambda: asyncio.run(auto_like_scheduler()), daemon=True)
    scheduler_thread.start()

    print("🎮 FREE FIRE MAX Bot starting... (Full Admin Control)")
    print("🚨 MODDING BY CM - All Commands Functional!")
    application.run_polling()

if __name__ == '__main__':
    main()
