import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from T_binance import get_spot_balance
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

STATUS_FILE = "status.json"

def read_status():
    with open(STATUS_FILE, "r") as file:
        return json.load(file)

def write_status(data):
    with open(STATUS_FILE, "w") as file:
        json.dump(data, file, indent=4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 Welcome! Here are some things I can do:\n\n"
        "1️⃣ Use /status to check the current balance and trading state.\n"
        "2️⃣ Use /set_balance <value> to update the balance.\n"
        "3️⃣ Use the buttons to toggle the trading state."
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    status_data = read_status()
    balance = status_data["balance"]
    trading = status_data["trading"]
    trading_status = "🟢 Active" if trading else "🔴 Inactive"
    await update.message.reply_text(
        f"📊 **Status**\n\n💰 Balance: `{balance}`\n📈 Trading State: {trading_status}",
        parse_mode="Markdown",
    )

async def set_balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        new_balance = context.args[0]
        status_data = read_status()
        status_data["balance"] = new_balance
        write_status(status_data)
        await update.message.reply_text(f"💰 Balance updated to: `{new_balance}`", parse_mode="Markdown")
    except (IndexError, ValueError):
        await update.message.reply_text("❌ Usage: /set_balance <new_balance>")

async def set_trading_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    new_state = query.data == "true"
    status_data = read_status()
    status_data["trading"] = new_state
    write_status(status_data)
    trading_status = "🟢 Active" if new_state else "🔴 Inactive"
    await query.edit_message_text(f"📈 Trading state updated to: {trading_status}")

async def toggle_trading(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton("🟢 Enable Trading", callback_data="true"),
            InlineKeyboardButton("🔴 Disable Trading", callback_data="false"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("⚙️ Toggle trading state:", reply_markup=reply_markup)

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("❓ Sorry, I don't understand that command.")


async def get_balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:    
    # spend_amount = get_spot_balance('USDT')
    await update.message.reply_text(f"USDT Balance: {get_spot_balance("USDT")}")
    # print(f"USDT Balance: {spend_amount}")

def main():
    
    application = Application.builder().token("7863452906:AAGv91bX0MZ2-B5f-UyISYeBd6O3fBj_EAM").build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("set_balance", set_balance))
    application.add_handler(CommandHandler("toggle_trading", toggle_trading))
    application.add_handler(CommandHandler("get_balance", get_balance))
    application.add_handler(CallbackQueryHandler(set_trading_callback))

    # Handle unknown commands
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    # Start the bot
    application.run_polling()
    print("Bot is running... Press Ctrl+C to stop.")

if __name__ == "__main__":
    main()
