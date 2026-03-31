import random
import string
import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from supabase import create_client, Client

# --- ТВОЇ ДАНІ (ЗАПОВНИ ТУТ) ---
TOKEN = "8242267315:AAGQ_92Ug-ett0NYreQ86VmxrpXHu5N0FUQ"
SUPABASE_URL = "https://tskdzdaafenzassocitb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRza2R6ZGFhZmVuemFzc29jaXRiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NDgxNjA0MywiZXhwIjoyMDkwMzkyMDQzfQ.KkA8c3r5gqdeTNk0dIXHfeLTQFMM95timBtiqWiViMk"
ADMIN_ID = 7069448924 # Встав свій ID сюди

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Генератор коду
def make_code():
    chars = string.ascii_uppercase + string.digits
    return f"DYM-{''.join(random.choices(chars, k=4))}-{''.join(random.choices(chars, k=4))}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return # Бот ігнорує чужих

    kbd = [['💎 +1 PRO Код', '💎 +5 PRO Кодів'], ['📋 Список вільних']]
    await update.message.reply_text(
        "⚡ DYM // OS Admin Panel\nОберіть дію:",
        reply_markup=ReplyKeyboardMarkup(kbd, resize_keyboard=True)
    )

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    
    cmd = update.message.text

    if cmd == '💎 +1 PRO Код' or cmd == '💎 +5 PRO Кодів':
        count = 1 if '1' in cmd else 5
        new_codes = [{"code": make_code()} for _ in range(count)]
        
        try:
            supabase.table("promocodes").insert(new_codes).execute()
            codes_text = "\n".join([f"`{c['code']}`" for c in new_codes])
            await update.message.reply_text(f"✅ Успішно додано:\n\n{codes_text}", parse_mode='MarkdownV2')
        except Exception as e:
            await update.message.reply_text(f"❌ Помилка: {e}")

    elif cmd == '📋 Список вільних':
        res = supabase.table("promocodes").select("code").eq("is_used", False).limit(20).execute()
        if res.data:
            msg = "🔑 **Доступні коди:**\n\n" + "\n".join([f"`{i['code']}`" for i in res.data])
            await update.message.reply_text(msg, parse_mode='MarkdownV2')
        else:
            await update.message.reply_text("📭 Немає вільних кодів.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    print("🤖 Бот увімкнений...")
    app.run_polling()

if __name__ == '__main__':
    main()