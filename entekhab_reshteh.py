import os

from flask import send_from_directory

from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    WebAppInfo,
)


# =========================================================
# تنظیمات
# =========================================================

BASE_URL = os.getenv("BASE_URL", "").rstrip("/")


# =========================================================
# مسیر Mini App
# =========================================================

MINIAPP_URL = f"{BASE_URL}/reshteh"


# =========================================================
# منوی انتخاب رشته
# =========================================================

def get_selection_menu_keyboard():

    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(
                    "طرح های انتخاب رشته",
                    api_kwargs={
                        "style": "primary"
                    }
                ),

                KeyboardButton(
                    "معرفی رشته ها 📚",

                    web_app=WebAppInfo(
                        url=MINIAPP_URL
                    ),

                    api_kwargs={
                        "style": "success"
                    }
                )
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
# ورود به منوی انتخاب رشته
# =========================================================

async def handle_selection_menu(update, context):

    user_id = update.effective_user.id

    # اگر می‌خواهی همان محدودیت عضویت فعلی حفظ شود،
    # check_member از main.py به این تابع داده می‌شود.
    check_member = context.bot_data.get("check_member_function")

    if (
        user_id != context.bot_data.get("admin_id")
        and check_member
    ):
        allowed = await check_member(update, context)

        if not allowed:
            return True

    await update.message.reply_text(
        "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=get_selection_menu_keyboard()
    )

    return True


# =========================================================
# طرح های انتخاب رشته
# =========================================================

async def handle_selection_plans(update, context):

    user_id = update.effective_user.id

    check_member = context.bot_data.get("check_member_function")

    if (
        user_id != context.bot_data.get("admin_id")
        and check_member
    ):
        allowed = await check_member(update, context)

        if not allowed:
            return True

    # -----------------------------------------------------
    # طرح اول
    # -----------------------------------------------------

    await update.message.reply_voice(
        voice="AwACAgQAAxkBAALWo2qpjtFZF0RcjikPM04colK4ilMKAALXIAACbLRJUawNoLiIz0eEPQQ",

        caption="""**طرح اول**

**مشاوره انتخاب رشته**

مناسب کسی که خودش کد رشته هارو استخراج می‌کنه و میخواد راجب رشته ها دوره و هر چیزی که نیازه بدونه و چینشش رو تعیین کنه.

یا میخواد انتخاب رشته ای که جایی دیگه انجام داده چک بشه.

1 تماس کامل تا جایی که سوالی باشد""",

        parse_mode="Markdown"
    )

    # -----------------------------------------------------
    # طرح دوم
    # -----------------------------------------------------

    await update.message.reply_voice(
        voice="AwACAgQAAxkBAALW0mqpkQJilxMCvxpkApzf2xHLRMbWAALeIAACbLRJUZ0bW3M24ih4PQQ",

        caption="""**طرح دوم**

**انجام انتخاب رشته کامل**

بررسی انتخاب ۱ تا ۱۵۰ انتخاب رشته

دریافت فرم ۱۵۰ تایی انتخاب رشته با دریافت شانس قبولی در هر کد رشته

تعداد تماس بر اساس زمانی که تکمیل بشه انتخاب رشته شما تعیین میشه

تماس با والدین در صورت تمایل""",

        parse_mode="Markdown"
    )

    # -----------------------------------------------------
    # طرح سوم
    # -----------------------------------------------------

    await update.message.reply_voice(
        voice="AwACAgQAAxkBAALW12qpkQl7q7_HkmlvkmGQ0D4kTHk8AALfIAACbLRJUcmAz9z18OBQPQQ",

        caption="""**طرح سوم**

**تماس جهت مشاوره انتخاب رشته**

و ارسال فرم ۱۵۰ تایی انتخاب رشته براساس اولویت ها

**۱ تماس تا جایی که سوالی باشد**""",

        parse_mode="Markdown"
    )

    # -----------------------------------------------------
    # قیمت‌ها
    # -----------------------------------------------------

    await update.message.reply_text(
        """قیمت ها

طرح اول
1650

طرح دوم
4450

طرح سوم
2450

طرح دوم قسطی میشود"""
    )

    # -----------------------------------------------------
    # اطلاعات موردنیاز
    # -----------------------------------------------------

    await update.message.reply_text(
        """✨ اطلاعات زیر رو در قالب یک پیام، به آیدی پشتیبانی ارسال کنید:

نام و نام خانوادگی :
شماره تماس :
مقطع تحصیلی :
شماره تلفن منزل (درصورت داشتن) :
تراز میانگین تخمینی یا رتبه کنکور :
نوع مدرسه :
رشته های مورد علاقه :
هر موضوعی که نیازه ما از شما بدونیم :
استان و شهر :
سطح مالی :
نوع طرح انتخابی :"""
    )

    # -----------------------------------------------------
    # پشتیبانی
    # -----------------------------------------------------

    await update.message.reply_text(
        """فرم ثبت نام رو به آیدی پشتیبانی ارسال کنید.
@poshtibaniKL"""
    )

    return True


# =========================================================
# Route مربوط به Mini App
# =========================================================

def register_selection_routes(app):

    @app.route("/reshteh", methods=["GET"])
    def reshteh_page():

        return send_from_directory(
            "static",
            "reshteh.html"
        )
