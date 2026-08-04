import os
import json
import asyncio
import threading
from flask import Flask, request
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove
)
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# ------------------ تنظیمات اصلی ------------------
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))
LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID", 0))
BACKUP_GROUP_ID = int(os.getenv("BACKUP_GROUP_ID", 0))
WEBHOOK_URL = os.getenv("WEBHOOK_URL") 

DB_FILE = "database.json"

app = Flask(__name__)
tg_app = ApplicationBuilder().token(TOKEN).build()
bot_loop = asyncio.new_event_loop()


# ------------------ توابع مدیریت دیتابیس ------------------
def load_db():
    if not os.path.exists(DB_FILE):
        data = {"monthly_plan": [], "free_analysis": []}
        save_db_sync(data)
        return data
    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return {"monthly_plan": [], "free_analysis": []}

def save_db_sync(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

async def save_db_and_backup(data):
    save_db_sync(data)
    try:
        await tg_app.bot.send_document(
            chat_id=BACKUP_GROUP_ID,
            document=open(DB_FILE, "rb"),
            caption="📦 نسخه پشتیبان دیتابیس بروزرسانی شد"
        )
    except Exception as e:
        print(f"Backup Error: {e}")

# ------------------ هندلرهای ربات ------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    context.user_data.clear() # ریست کردن وضعیت کاربر

    if user_id == ADMIN_ID:
        kb = [["دانش آموزان طرح ماهانه"], ["دانش آموزان طرح تماس رایگان و آنالیز تخصصی"]]
        await update.message.reply_text("خوش آمدید ادمین عزیز. پنل مدیریت:", 
                                       reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))
    else:
        kb = [["طرح ماهانه", "طرح تماس رایگان و آنالیز تخصصی", "ارتباط با پشتیبانی"]]
        await update.message.reply_text("سلام به ربات پشتیبانی رسانه کنکوری  بهشتی خوش اومدی رفیق😉\n\n آدرس کانال: @biologist_academy \n\n آدرس گروه: @biologistacademy ", 
                                       reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user = update.effective_user
    u_id = user.id
    username = f"@{user.username}" if user.username else "بدون یوزرنیم"

    # -------------------------
    # ادمین - منوی اصلی
    # -------------------------
    if u_id == ADMIN_ID:
        if text == "دانش آموزان طرح ماهانه":
            await show_admin_panel(update, "monthly_plan", "طرح ماهانه")
            return

        if text == "دانش آموزان طرح تماس رایگان و آنالیز تخصصی":
            await show_admin_panel(update, "free_analysis", "طرح تماس رایگان")
            return

    # -------------------------
    # بازگشت به صفحه اصلی (بررسی سراسری بازگشت)
    # -------------------------
    if text == "بازگشت":
        context.user_data.clear()
        kb = [["طرح ماهانه", "طرح تماس رایگان و آنالیز تخصصی", "ارتباط با پشتیبانی"]]
        await update.message.reply_text(
            "به صفحه اصلی برگشتید.",
            reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True)
        )
        return

    # -------------------------
    # انتخاب طرح
    # -------------------------
    if text in ["طرح تماس رایگان و آنالیز تخصصی"]:
        context.user_data["pending_plan"] = text

        kb = [["ثبت اطلاعات", "بازگشت"]]
        await update.message.reply_text(
            """<b>برای اینکه ما باهات تماس بگیریم، لطفاً اطلاعات زیر رو ارسال کن برامون که بدونیم کدوممون برات مناسب تریم😉</b>""",
            reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True), parse_mode="HTML"
        )
        return

    if text in ["طرح ماهانه"]:
        context.user_data["pending_plan"] = text

        kb = [["ثبت اطلاعات", "بازگشت"]]

        mahane_1 = """<blockquote>علی صمدی رتبه 46 کنکور و تراز 12400.کنکور پزشکی بهشتی 
محمد صدرا ولیان رتبه 129  و تراز 12300. کنکور پزشکی بهشتی 
هومن پارسی فر رتبه 138 کنکور و تراز 12000.  کنکور پزشکی بهشتی 
کسرا کلانتری رتبه 162 کنکور و تراز 11500.  کنکور پزشکی بهشتی
محمد حسن رحیم لو رتبه 179 کنکور و تراز 11900. کنکور پزشکی بهشتی 
امیر حسین خدامی رتبه 332 کنکور و تراز 11500.  کنکور پزشکی بهشتی
مسعود شیدایی نژاد رتبه 400 کنکور و تراز 10500.  پزشکی تهران</blockquote>"""

        mahane_2 = """<b>🚀 پلن‌های مشاوره آکادمی</b>

<blockquote> <b>🥈 طرح عادی</b>

📞 تماس تلفنی هر ۲ هفته یک‌بار
📝 برگزاری آزمون هر ۲ هفته یک‌بار
📊 پیگیری مستمر و ارائه گزارش روزانه
📚 ارائه برنامه مطالعاتی شخصی‌سازی‌شده به صورت هفتگی </blockquote>
<blockquote> <b>🥇 طرح VIP </b>

📞 تماس تلفنی هفته‌ای ۱ بار
📝 برگزاری آزمون هفته‌ای ۱ بار یا بیشتر
📊 پیگیری مستمر و ارائه گزارش روزانه
📚 ارائه برنامه مطالعاتی شخصی‌سازی‌شده به‌صورت هفتگی</blockquote>
<blockquote> <b>💎 مزایای مشترک هر دو طرح</b>

✅ مدت زمان تماس محدود نیست و تا رفع کامل سؤالات ادامه خواهد داشت.
✅ برنامه مطالعاتی کاملاً متناسب با شرایط، سطح و اهداف شما طراحی می‌شود.
✅ نظارت مستقیم بر روند پیشرفت و بررسی گزارش‌ها توسط علی مرتضایی (مدیر مجموعه).</blockquote>
<blockquote> <b>👥 نحوه همکاری</b>

شما در یک ساختار سه‌نفره فعالیت خواهید کرد:
👤 دانش آموز (شما)
👨🏻‍⚕️ مشاور
🕵🏻‍♂️ ناظر</blockquote>
<blockquote> <b>💰 هزینه‌ها</b>

🥈 طرح عادی :  1250 هزار تومان 
🥇 طرح وی آی پی :  1750 هزار تومان</blockquote>
<blockquote>🩺 تمامی اعضای تیم از دانشجویان پزشکی دانشگاه شهید بهشتی هستند.
✨ به‌زودی مشاوران سایر رشته‌ها نیز به مجموعه اضافه خواهند شد.</blockquote>

 با تلاش ، هر چیزی ممکن است👌..."""

        await update.message.reply_voice(
            voice="AwACAgQAAxkBAAPCanIkWyy8rY6BP-IefPbZwAVsi1kAAoIfAALgw5FQjlGS-9Yzk-g9BA"
        )
        await update.message.reply_text(mahane_1, parse_mode="HTML")
        await update.message.reply_text(mahane_2, parse_mode="HTML")
        await update.message.reply_text("طرح ماهانه فعال هست و افراد بالا ، تا الان ظرفیت دارند که با توجه به سبک و سطح درسی شما بهترین گزینه انتخاب خواهند شد .👌")

        await update.message.reply_text(
            "حله... برای ادامه، روی «ثبت اطلاعات» بزنید و بعد اطلاعات را در یک پیام بفرستید.",
            reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True)
        )
        return

    if text in ["ارتباط با پشتیبانی"]:
        await update.message.reply_text("آیدی پشتیبانی: @poshtibaniKL")
        return

    # -------------------------
    # کلیک روی ثبت اطلاعات
    # -------------------------
    if text == "ثبت اطلاعات" and context.user_data.get("pending_plan"):
        context.user_data["waiting_for_details"] = True
        information = """✨ اطلاعات زیر رو در قالب یک پیام، برای ما ارسال کنید:

نام و نام خانوادگی :
مقطع تحصیلی :
شماره تماس:
شماره تلفن منزل (درصورت داشتن):
نوع مدرسه:
استان و شهر :
سطح کیفی تحصیلی از نظر خودتون:
نقاط ضعف درسی:"""

        # کیبورد تک‌دکمه‌ای بازگشت برای انصراف از ارسال اطلاعات
        back_kb = [["بازگشت"]]
        await update.message.reply_text(
            information, 
            reply_markup=ReplyKeyboardMarkup(back_kb, resize_keyboard=True)
        )
        return

    # -------------------------
    # دریافت نهایی اطلاعات
    # -------------------------
    if context.user_data.get("waiting_for_details"):
        # اگر کاربر در این مرحله هم دکمه «بازگشت» را زد، فرآیند را لغو می‌کنیم
        if text == "بازگشت":
            context.user_data.clear()
            kb = [["طرح ماهانه", "طرح تماس رایگان و آنالیز تخصصی", "ارتباط با پشتیبانی"]]
            await update.message.reply_text(
                "ثبت اطلاعات لغو شد. به صفحه اصلی برگشتید.",
                reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True)
            )
            return

        plan_type = context.user_data.get("pending_plan")
        lines = text.splitlines()
        full_name = lines[0] if lines else "نامشخص"

        db = load_db()
        entry = {
            "id": u_id,
            "username": username,
            "name": full_name,
            "details": text,
            "plan": plan_type
        }

        key = "monthly_plan" if plan_type == "طرح ماهانه" else "free_analysis"
        db[key].append(entry)

        await save_db_and_backup(db)
        context.user_data.clear()

        kb = [["طرح ماهانه", "طرح تماس رایگان و آنالیز تخصصی", "ارتباط با پشتیبانی"]]
        await update.message.reply_text(
            """<b>درخواست مشاوره ثبت شد. برای پیگیری ثبت نام به آیدی پشتیبانی مراجعه کنید.</b>\n @poshtibaniKL""",
            reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True), parse_mode="HTML"
        )

        report = (
            f"👤 ثبت نام جدید: {plan_type}\n"
            f"نام: {full_name}\n"
            f"یوزرنیم: {username}\n"
            f"آیدی عددی: {u_id}\n\n"
            f"📝 اطلاعات ارسالی:\n{text}"
        )
        await context.bot.send_message(chat_id=LOG_GROUP_ID, text=report)
        return

# ------------------ پنل ادمین (اینلاین) ------------------

async def show_admin_panel(update: Update, key, title):
    kb = [
        [InlineKeyboardButton("مشاهده اسامی افراد", callback_data=f"list_{key}_0")],
        [InlineKeyboardButton("حذف دانش‌آموز خاص", callback_data=f"delselect_{key}_0")],
        [InlineKeyboardButton("حذف لیست ⚠️", callback_data=f"clearall_{key}")]
    ]
    await update.message.reply_text(f"مدیریت {title}:", reply_markup=InlineKeyboardMarkup(kb))

def parse_page_callback(data: str):
    """
    مثال:
    list_monthly_plan_0
    خروجی:
    mode = list
    key = monthly_plan
    page = 0
    """
    parts = data.split("_")

    if len(parts) < 3:
        raise ValueError(f"callback_data نامعتبر است: {data}")

    mode = parts[0]
    page = int(parts[-1])
    key = "_".join(parts[1:-1])

    return mode, key, page


def parse_index_callback(data: str):
    """
    مثال:
    info_monthly_plan_4
    خروجی:
    action = info
    key = monthly_plan
    index = 4
    """
    parts = data.split("_")

    if len(parts) < 3:
        raise ValueError(f"callback_data نامعتبر است: {data}")

    action = parts[0]
    index = int(parts[-1])
    key = "_".join(parts[1:-1])

    return action, key, index


def parse_key_callback(data: str):
    """
    مثال:
    clearall_monthly_plan
    خروجی:
    action = clearall
    key = monthly_plan
    """
    action, key = data.split("_", 1)
    return action, key


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if query.from_user.id != ADMIN_ID:
        await query.answer("شما اجازه دسترسی به این بخش را ندارید.", show_alert=True)
        return

    await query.answer()

    data = query.data
    db = load_db()

    # --------------------------------------------------
    # نمایش لیست افراد یا منوی حذف افراد
    # --------------------------------------------------
    if data.startswith("list_") or data.startswith("delselect_"):
        try:
            mode, key, page = parse_page_callback(data)
        except (ValueError, IndexError):
            await query.edit_message_text("خطا در اطلاعات دکمه.")
            return

        users = db.get(key, [])

        if not users:
            await query.edit_message_text("لیست خالی است.")
            return

        page_size = 20
        start_idx = page * page_size
        end_idx = start_idx + page_size
        batch = users[start_idx:end_idx]

        buttons = []

        for i, user in enumerate(batch):
            real_index = start_idx + i
            name = user.get("name", "بدون نام")

            if mode == "list":
                callback_data = f"info_{key}_{real_index}"
            else:
                callback_data = f"askdel_{key}_{real_index}"

            buttons.append([
                InlineKeyboardButton(
                    name,
                    callback_data=callback_data
                )
            ])

        navigation = []

        if page > 0:
            navigation.append(
                InlineKeyboardButton(
                    "⬅️ صفحه قبل",
                    callback_data=f"{mode}_{key}_{page - 1}"
                )
            )

        if end_idx < len(users):
            navigation.append(
                InlineKeyboardButton(
                    "صفحه بعد ➡️",
                    callback_data=f"{mode}_{key}_{page + 1}"
                )
            )

        if navigation:
            buttons.append(navigation)

        title = "اسامی دانش‌آموزان" if mode == "list" else "دانش‌آموز موردنظر برای حذف را انتخاب کنید"

        await query.edit_message_text(
            title,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return

    # --------------------------------------------------
    # نمایش مشخصات یک فرد
    # --------------------------------------------------
    if data.startswith("info_"):
        try:
            action, key, index = parse_index_callback(data)
        except (ValueError, IndexError):
            await query.answer("اطلاعات دکمه نامعتبر است.", show_alert=True)
            return

        users = db.get(key, [])

        if index < 0 or index >= len(users):
            await query.answer("این دانش‌آموز دیگر وجود ندارد.", show_alert=True)
            return

        user = users[index]

        details = user.get("details", "بدون اطلاعات")
        name = user.get("name", "بدون نام")
        username = user.get("username", "بدون یوزرنیم")
        telegram_id = user.get("id", "نامشخص")
        plan = user.get("plan", "نامشخص")

        message = (
            f"👤 نام و نام خانوادگی:\n{name}\n\n"
            f"🔗 یوزرنیم تلگرام:\n{username}\n\n"
            f"🆔 آیدی عددی:\n{telegram_id}\n\n"
            f"📋 طرح انتخابی:\n{plan}\n\n"
            f"📝 اطلاعات کامل ارسالی:\n{details}"
        )

        await query.message.reply_text(message)
        return

    # --------------------------------------------------
    # تأیید اولیه حذف دانش‌آموز
    # --------------------------------------------------
    if data.startswith("askdel_"):
        try:
            action, key, index = parse_index_callback(data)
        except (ValueError, IndexError):
            await query.edit_message_text("اطلاعات حذف نامعتبر است.")
            return

        users = db.get(key, [])

        if index < 0 or index >= len(users):
            await query.edit_message_text("این دانش‌آموز دیگر وجود ندارد.")
            return

        user = users[index]
        name = user.get("name", "بدون نام")

        keyboard = [
            [
                InlineKeyboardButton(
                    "✅ بله، حذف کن",
                    callback_data=f"confirmdel_{key}_{index}"
                ),
                InlineKeyboardButton(
                    "❌ خیر",
                    callback_data="cancel"
                )
            ]
        ]

        await query.edit_message_text(
            f"آیا مطمئنی دانش‌آموز «{name}» حذف شود؟",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    # --------------------------------------------------
    # حذف قطعی یک دانش‌آموز
    # --------------------------------------------------
    if data.startswith("confirmdel_"):
        try:
            action, key, index = parse_index_callback(data)
        except (ValueError, IndexError):
            await query.edit_message_text("اطلاعات حذف نامعتبر است.")
            return

        users = db.get(key, [])

        if index < 0 or index >= len(users):
            await query.edit_message_text("این دانش‌آموز دیگر وجود ندارد.")
            return

        deleted_user = users.pop(index)
        db[key] = users

        await save_db_and_backup(db)

        # اطلاع‌رسانی حذف به صورت پاپ‌آپ (اختیاری)
        await query.answer(f"✅ «{deleted_user.get('name')}» حذف شد.", show_alert=True)

        # تعیین عنوان فارسی برای منو
        title_fa = "طرح ماهانه" if key == "monthly_plan" else "طرح تماس رایگان"

        # بازگشت به پنل مدیریت همان بخش
        kb = [
            [InlineKeyboardButton("مشاهده اسامی افراد", callback_data=f"list_{key}_0")],
            [InlineKeyboardButton("حذف دانش‌آموز خاص", callback_data=f"delselect_{key}_0")],
            [InlineKeyboardButton("حذف لیست ⚠️", callback_data=f"clearall_{key}")]
        ]
        
        await query.edit_message_text(
            f"✅ حذف انجام شد.\nمدیریت {title_fa}:", 
            reply_markup=InlineKeyboardMarkup(kb)
        )
        return

    # --------------------------------------------------
    # درخواست حذف کل لیست
    # --------------------------------------------------
    if data.startswith("clearall_"):
        try:
            action, key = parse_key_callback(data)
        except ValueError:
            await query.edit_message_text("اطلاعات حذف لیست نامعتبر است.")
            return

        title = (
            "طرح ماهانه"
            if key == "monthly_plan"
            else "طرح تماس رایگان و آنالیز تخصصی"
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    "✅ بله، کل لیست حذف شود",
                    callback_data=f"doclear_{key}"
                ),
                InlineKeyboardButton(
                    "❌ خیر",
                    callback_data="cancel"
                )
            ]
        ]

        await query.edit_message_text(
            f"⚠️ آیا مطمئنی تمام افراد ثبت‌نام‌شده در «{title}» حذف شوند؟",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    # --------------------------------------------------
    # حذف کل لیست
    # --------------------------------------------------
    if data.startswith("doclear_"):
        try:
            action, key = parse_key_callback(data)
        except ValueError:
            await query.edit_message_text("اطلاعات حذف لیست نامعتبر است.")
            return

        if key not in db:
            await query.edit_message_text("این طرح در دیتابیس وجود ندارد.")
            return

        db[key] = []

        await save_db_and_backup(db)

        await query.edit_message_text(
            "✅ کل لیست این طرح با موفقیت حذف شد."
        )
        return

    # --------------------------------------------------
    # لغو عملیات
    # --------------------------------------------------
    if data == "cancel":
        await query.edit_message_text("❌ عملیات لغو شد.")
        return

async def handle_db_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not update.message.document:
        return

    if update.message.document.file_name != DB_FILE:
        await update.message.reply_text(f"❌ فقط فایل {DB_FILE} قابل قبول است.")
        return

    try:
        f = await update.message.document.get_file()
        await f.download_to_drive(DB_FILE)

        # خواندن دیتابیس جدید
        db = load_db()

        # ذخیره و ارسال بکاپ
        await save_db_and_backup(db)

        # پیام به ادمین
        await update.message.reply_text("✅ دیتابیس جایگزین شد و بکاپ جدید ارسال شد.")

        # گزارش به گروه لاگ
        admin_user = update.effective_user
        admin_name = admin_user.full_name
        admin_username = f"@{admin_user.username}" if admin_user.username else "بدون یوزرنیم"

        monthly_count = len(db.get("monthly_plan", []))
        free_count = len(db.get("free_analysis", []))

        log_text = (
            f"🗂 دیتابیس توسط ادمین جایگزین شد.\n\n"
            f"👤 نام ادمین: {admin_name}\n"
            f"🔗 یوزرنیم: {admin_username}\n"
            f"🆔 آیدی: {admin_user.id}\n\n"
            f"📊 آمار فعلی دیتابیس:\n"
            f"طرح ماهانه: {monthly_count}\n"
            f"طرح تماس رایگان و آنالیز تخصصی: {free_count}"
        )

        await context.bot.send_message(chat_id=LOG_GROUP_ID, text=log_text)

    except Exception as e:
        print(f"DB upload error: {e}")
        await update.message.reply_text("❌ خطا در جایگزینی دیتابیس.")

# ===== get file id ===== ===== ===== =====
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.voice:
        file_id = update.message.voice.file_id
        await update.message.reply_text(
            f"🎤 فایل‌آیدی این وویس:\n\n<code>{file_id}</code>",
            parse_mode="HTML"
        )

# ------------------ تنظیمات WEBHOOK و FLASK ------------------

@app.route("/webhook", methods=["POST"])
def webhook_handler():
    update = Update.de_json(request.get_json(force=True), tg_app.bot)
    asyncio.run_coroutine_threadsafe(
        tg_app.process_update(update),
        bot_loop
    )
    return "OK", 200

def run_flask():
    app.run(host="0.0.0.0", port=5000)

async def setup_bot():
    await tg_app.initialize()
    await tg_app.start()
    await tg_app.bot.set_webhook(WEBHOOK_URL)

def start_bot_loop():
    asyncio.set_event_loop(bot_loop)
    bot_loop.run_until_complete(setup_bot())
    bot_loop.run_forever()

if __name__ == "__main__":
    tg_app.add_handler(CommandHandler("start", start))
    # tg_app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    tg_app.add_handler(MessageHandler(filters.Document.ALL, handle_db_upload))
    tg_app.add_handler(CallbackQueryHandler(callback_handler))

    if not TOKEN:
        raise ValueError("BOT_TOKEN تنظیم نشده است.")
    if not WEBHOOK_URL:
        raise ValueError("WEBHOOK_URL تنظیم نشده است.")

    print("Bot is running with webhook...")

    bot_thread = threading.Thread(target=start_bot_loop, daemon=True)
    bot_thread.start()

    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

