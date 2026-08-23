import os
import json
import bisect

from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    WebAppInfo,
)


# =========================================================
# تنظیمات
# =========================================================

BASE_URL = os.getenv("BASE_URL", "").rstrip("/")
LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID", "0"))


# =========================================================
# داده‌های تخمین رتبه
#
# ساختار:
#
# تراز -> رتبه
# عدد بین دو نقطه -> حداکثر خطای تقریبی در آن نقطه
#
# مثال:
#
# 8000 -> 100
# 7000 -> 500
#
# خطای 8000 = ±50
# خطای 7000 = ±80
#
# برای نقاط بین این دو، خطا نیز به صورت خطی
# بین 50 و 80 تغییر می‌کند.
# =========================================================


RANK_DATA = {

    # -----------------------------------------------------
    # منطقه ۳
    # -----------------------------------------------------

    3: [
        (11100, 1, None),
        (11000, 20, 10),
        (10700, 100, 50),
        (10000, 400, 250),
        (9500, 1000, 250),
        (9200, 2000, 500),
        (9000, 3000, 500),
        (8700, 5000, 1000),
        (8000, 10000, 2000),
        (7300, 20000, 3000),
        (6300, 40000, 5000),
        (5500, 70000, 10000),
        (4900, 100000, None),
    ],


    # -----------------------------------------------------
    # منطقه ۱
    # -----------------------------------------------------

    1: [
        (11800, 1, None),
        (11000, 100, 50),
        (10500, 200, 100),
        (10000, 500, 250),
        (9400, 2000, 500),
        (8700, 5000, 1000),
        (8000, 10000, 2500),
        (6800, 20000, 2500),
        (6000, 30000, 5000),
        (5000, 45000, 5000),
        (4000, 60000, None),
    ],


    # -----------------------------------------------------
    # منطقه ۲
    # -----------------------------------------------------

    2: [
        (11700, 1, None),
        (11500, 20, 20),
        (11000, 100, 50),
        (10500, 300, 200),
        (10000, 1000, 300),
        (9500, 2000, 500),
        (9000, 5000, 1000),
        (8500, 10000, 2000),
        (7700, 20000, 2000),
        (7200, 30000, 4000),
        (6700, 40000, 5000),
        (5900, 60000, 8000),
        (5000, 90000, 10000),
        (4500, 110000, None),
    ],
}


# =========================================================
# دکمه WebApp
# =========================================================

def get_rank_keyboard_button():

    return KeyboardButton(
        "تخمین رتبه 🎯",

        web_app=WebAppInfo(
            url=f"{BASE_URL}/rank"
        ),

        api_kwargs={
            "style": "success"
        }
    )


# =========================================================
# منوی تخمین رتبه
# =========================================================

def get_rank_menu_keyboard():

    return ReplyKeyboardMarkup(
        [
            [
                get_rank_keyboard_button()
            ],
            [
                KeyboardButton(
                    "بازگشت",
                    api_kwargs={
                        "style": "danger"
                    }
                )
            ]
        ],

        resize_keyboard=True
    )


# =========================================================
# کیبورد منطقه
# =========================================================

def get_region_keyboard():

    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("منطقه ۱"),
                KeyboardButton("منطقه ۲"),
                KeyboardButton("منطقه ۳"),
            ]
        ],

        resize_keyboard=True,
        one_time_keyboard=True
    )


# =========================================================
# کیبورد ارسال شماره
# =========================================================

def get_phone_keyboard():

    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(
                    "📱 ارسال شماره موبایل",
                    request_contact=True
                )
            ]
        ],

        resize_keyboard=True,
        one_time_keyboard=True
    )


# =========================================================
# تبدیل متن منطقه به عدد
# =========================================================

def parse_region(text):

    if not text:
        return None

    text = text.strip()

    if text in ("منطقه ۱", "منطقه 1", "1"):
        return 1

    if text in ("منطقه ۲", "منطقه 2", "2"):
        return 2

    if text in ("منطقه ۳", "منطقه 3", "3"):
        return 3

    return None


# =========================================================
# محاسبه تراز میانگین
# =========================================================

def calculate_average_score(final_score, exam_score):

    return (
        float(final_score) * 0.60
        +
        float(exam_score) * 0.40
    )


# =========================================================
# محاسبه رتبه
# =========================================================

def calculate_rank(score, region):

    data = RANK_DATA.get(region)

    if not data:
        raise ValueError("منطقه نامعتبر است.")

    score = float(score)

    # -----------------------------------------------------
    # داده‌ها از تراز بیشتر به کمتر هستند.
    # برای محاسبه راحت‌تر بر اساس تراز صعودی مرتب می‌کنیم.
    # -----------------------------------------------------

    points = sorted(
        data,
        key=lambda x: x[0]
    )

    # -----------------------------------------------------
    # بالاتر از بیشترین تراز
    # -----------------------------------------------------

    if score >= points[-1][0]:

        if score == points[-1][0]:
            rank = points[-1][1]
        else:
            rank = 1

        error = (
            points[-1][2]
            if points[-1][2] is not None
            else 0
        )

        return int(round(rank)), int(round(error))


    # -----------------------------------------------------
    # پایین‌تر از کمترین تراز
    # -----------------------------------------------------

    if score <= points[0][0]:

        rank = points[0][1]

        error = (
            points[0][2]
            if points[0][2] is not None
            else 0
        )

        return int(round(rank)), int(round(error))


    # -----------------------------------------------------
    # پیدا کردن دو نقطه‌ای که تراز بین آنهاست
    # -----------------------------------------------------

    for i in range(len(points) - 1):

        low_score, low_rank, low_error = points[i]

        high_score, high_rank, high_error = points[i + 1]

        if low_score <= score <= high_score:

            # -------------------------------------------------
            # چون تراز و رتبه رابطه معکوس دارند،
            # interpolation خطی انجام می‌دهیم.
            # -------------------------------------------------

            score_ratio = (
                (score - low_score)
                /
                (high_score - low_score)
            )

            rank = (
                low_rank
                +
                (high_rank - low_rank)
                *
                score_ratio
            )

            # -------------------------------------------------
            # محاسبه خطا
            # -------------------------------------------------

            if (
                low_error is not None
                and high_error is not None
            ):

                error = (
                    low_error
                    +
                    (high_error - low_error)
                    *
                    score_ratio
                )

            elif low_error is not None:

                error = low_error

            elif high_error is not None:

                error = high_error

            else:

                error = 0

            return (
                int(round(rank)),
                int(round(error))
            )

    # -----------------------------------------------------
    # حالت غیرمنتظره
    # -----------------------------------------------------

    return (
        int(points[-1][1]),
        int(points[-1][2] or 0)
    )


# =========================================================
# فرمت کردن رتبه
# =========================================================

def format_number(number):

    return f"{int(round(number)):,}"


# =========================================================
# دریافت اطلاعات WebApp
# =========================================================

async def handle_webapp_data(update, context):

    if (
        not update.message
        or not update.message.web_app_data
    ):
        return

    raw_data = update.message.web_app_data.data

    print("================================")
    print("RANK WEBAPP DATA")
    print(raw_data)
    print("================================")

    try:

        data = json.loads(raw_data)

    except Exception as e:

        print(f"Rank JSON error: {e}")

        await update.message.reply_text(
            "❌ اطلاعات ارسالی نامعتبر است."
        )

        return


    # فقط اطلاعات مربوط به rank

    if data.get("type") != "rank":

        return


    # رشته

    field = data.get("field")

    if field != "tajrobi":

        await update.message.reply_text(
            "❌ در حال حاضر فقط رشته تجربی فعال است."
        )

        return


    # ترازها

    try:

        final_score = float(
            data.get("final_score")
        )

        exam_score = float(
            data.get("exam_score")
        )

    except Exception:

        await update.message.reply_text(
            "❌ تراز واردشده صحیح نیست."
        )

        return


    # -----------------------------------------------------
    # اعتبارسنجی ترازها
    # -----------------------------------------------------

    if not (
        0 <= final_score <= 13000
        and
        0 <= exam_score <= 13000
    ):

        await update.message.reply_text(
            "❌ مقدار تراز باید بین ۰ تا ۱۳۰۰۰ باشد."
        )

        return


    # -----------------------------------------------------
    # محاسبه تراز میانگین
    # -----------------------------------------------------

    average_score = calculate_average_score(
        final_score,
        exam_score
    )


    # -----------------------------------------------------
    # ذخیره موقت اطلاعات در user_data
    # -----------------------------------------------------

    context.user_data["rank_data"] = {

        "field": "تجربی",

        "final_score": final_score,

        "exam_score": exam_score,

        "average_score": average_score,
    }


    # -----------------------------------------------------
    # مرحله بعد: منطقه
    # -----------------------------------------------------

    await update.message.reply_text(
        "📍 حالا لطفاً منطقه‌ات رو انتخاب کن:",
        reply_markup=get_region_keyboard()
    )


# =========================================================
# دریافت منطقه
# =========================================================

async def handle_region(update, context):

    if not update.message:
        return False

    text = update.message.text

    region = parse_region(text)

    if region is None:
        return False


    # بررسی اینکه کاربر از مسیر رتبه آمده

    rank_data = context.user_data.get("rank_data")

    if not rank_data:
        return False


    rank_data["region"] = region


    # -----------------------------------------------------
    # مرحله بعد: شماره موبایل
    # -----------------------------------------------------

    await update.message.reply_text(
        "📱 برای ادامه، لطفاً شماره موبایلت رو با دکمه زیر ارسال کن:",
        reply_markup=get_phone_keyboard()
    )

    return True


# =========================================================
# دریافت شماره و محاسبه نهایی
# =========================================================

async def handle_phone(update, context):

    if not update.message:
        return False

    if not update.message.contact:
        return False


    rank_data = context.user_data.get("rank_data")

    if not rank_data:
        return False


    contact = update.message.contact

    # -----------------------------------------------------
    # امنیت:
    # فقط شماره‌ای که خود کاربر ارسال کرده قبول شود.
    # -----------------------------------------------------

    if (
        contact.user_id is not None
        and
        contact.user_id != update.effective_user.id
    ):

        await update.message.reply_text(
            "❌ لطفاً شماره موبایل خودت را ارسال کن."
        )

        return True


    phone_number = contact.phone_number

    region = rank_data["region"]

    average_score = rank_data["average_score"]

    final_score = rank_data["final_score"]

    exam_score = rank_data["exam_score"]


    # -----------------------------------------------------
    # محاسبه رتبه
    # -----------------------------------------------------

    estimated_rank, error = calculate_rank(
        average_score,
        region
    )


    lower_rank = max(
        1,
        estimated_rank - error
    )

    upper_rank = (
        estimated_rank + error
    )


    # -----------------------------------------------------
    # پیام نتیجه
    # -----------------------------------------------------

    result_text = (
        "🎯 <b>نتیجه تخمین رتبه</b>\n\n"

        f"📚 رشته: <b>تجربی</b>\n"
        f"📍 منطقه: <b>{region}</b>\n\n"

        f"📖 تراز نهایی: "
        f"<b>{format_number(final_score)}</b>\n"

        f"📝 تراز کنکور: "
        f"<b>{format_number(exam_score)}</b>\n\n"

        f"📊 تراز میانگین: "
        f"<b>{format_number(average_score)}</b>\n\n"

        f"🏆 رتبه تخمینی: "
        f"<b>{format_number(estimated_rank)}</b>\n\n"

        f"📌 بازه تقریبی رتبه:\n"
        f"<b>{format_number(lower_rank)}</b>"
        f" تا "
        f"<b>{format_number(upper_rank)}</b>\n\n"

        "⚠️ این رتبه تخمینی است و نتیجه قطعی کنکور محسوب نمی‌شود."
    )


    await update.message.reply_text(
        result_text,
        parse_mode="HTML",
        reply_markup=get_rank_menu_keyboard()
    )


    # =====================================================
    # ارسال گزارش به گروه لاگ
    # =====================================================

    try:

        user = update.effective_user

        full_name = user.full_name or "بدون نام"

        username = (
            f"@{user.username}"
            if user.username
            else "بدون یوزرنیم"
        )

        user_id = user.id


        log_text = (
            "🎯 <b>تخمین رتبه جدید</b>\n\n"

            "👤 <b>اطلاعات کاربر</b>\n"
            f"نام: {full_name}\n"
            f"یوزرنیم: {username}\n"
            f"آیدی: <code>{user_id}</code>\n"
            f"📱 شماره: <code>{phone_number}</code>\n\n"

            "📚 <b>اطلاعات آزمون</b>\n"
            f"رشته: تجربی\n"
            f"منطقه: {region}\n\n"

            f"تراز نهایی: {format_number(final_score)}\n"
            f"تراز کنکور: {format_number(exam_score)}\n"
            f"تراز میانگین: {format_number(average_score)}\n\n"

            f"🏆 رتبه تخمینی: {format_number(estimated_rank)}\n"
            f"📌 بازه: "
            f"{format_number(lower_rank)}"
            f" تا "
            f"{format_number(upper_rank)}"
        )


        if LOG_GROUP_ID:

            await context.bot.send_message(
                chat_id=LOG_GROUP_ID,
                text=log_text,
                parse_mode="HTML"
            )


    except Exception as e:

        print(
            f"Rank log error: {e}"
        )


    # -----------------------------------------------------
    # پاک کردن اطلاعات موقت
    # -----------------------------------------------------

    context.user_data.pop(
        "rank_data",
        None
    )

    return True
