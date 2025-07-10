import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

TOKEN = os.environ["TG_BOT_TOKEN"]

PROMPTS = {
    "brooch": os.environ.get("PROMPT_BROOCH", "پرامپ سنجاق سینه"),
    "bracelet": os.environ.get("PROMPT_BRACELET", "پرامپ دستبند"),
    "earring": os.environ.get("PROMPT_EARRING", "پرامپ گوشواره"),
    "necklace": os.environ.get("PROMPT_NECKLACE", "پرامپ گردنبند"),
    "watch": os.environ.get("PROMPT_WATCH", "پرامپ ساعت"),
    "keychain": os.environ.get("PROMPT_KEYCHAIN", "پرامپ جاکلیدی"),
    "ring": os.environ.get("PROMPT_RING", "پرامپ انگشتر"),
    "ball": os.environ.get("PROMPT_BALL", "پرامپ گوی"),
    "wallet": os.environ.get("PROMPT_WALLET", "پرامپ کیف پول"),
    "night": os.environ.get("PROMPT_NIGHT", "پرامپ شب‌خواب")
}

user_context = {}

keyboard = [
    [InlineKeyboardButton("📌 سنجاق سینه", callback_data='brooch'),
     InlineKeyboardButton("💍 دستبند", callback_data='bracelet')],
    [InlineKeyboardButton("🧏‍♀️ گوشواره", callback_data='earring'),
     InlineKeyboardButton("📿 گردنبند", callback_data='necklace')],
    [InlineKeyboardButton("⌚ ساعت", callback_data='watch'),
     InlineKeyboardButton("🔑 جاکلیدی", callback_data='keychain')],
    [InlineKeyboardButton("💎 انگشتر", callback_data='ring'),
     InlineKeyboardButton("🔮 گوی", callback_data='ball')],
    [InlineKeyboardButton("💼 کیف پول", callback_data='wallet'),
     InlineKeyboardButton("🌙 شب‌خواب", callback_data='night')]
]

markup = InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("نوع محصول رو انتخاب کن:", reply_markup=markup)

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_context[query.from_user.id] = query.data
    await query.edit_message_text(f"✅ نوع انتخاب‌شده: {query.data}.\nحالا عکستو بفرست تا ادیت شه.")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in user_context:
        await update.message.reply_text("لطفاً اول نوع محصول رو با دکمه‌ها انتخاب کن.")
        return
    product_type = user_context[user_id]
    prompt = PROMPTS.get(product_type, "ادیت عمومی")
    await update.message.reply_text(f"🖼 در حال ادیت عکس با پرامپ: {prompt}\n(شبیه‌سازی ادیت انجام می‌شه...)")
    await update.message.reply_photo(photo=update.message.photo[-1].file_id, caption=f"[Mock edit for {product_type}]")

if __name__ == '__main__':
    app = ApplicationBuilder().token(7652437692:AAETq862nXc7H-zqRDNixesAawjM3-0XKxk).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_polling()
