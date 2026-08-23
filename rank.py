import os
from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    WebAppInfo,
)


# --------------------------------------------------
# تنظیمات
# --------------------------------------------------

# آدرس عمومی سایت
# مثال:
WEBHOOK_URL = os.getenv("WEBHOOK_URL") 

# --------------------------------------------------
# دکمه ورود به تخمین رتبه
# --------------------------------------------------

def get_rank_keyboard_button():
    """
    دکمه WebApp مربوط به تخمین رتبه
    """

    return KeyboardButton(
        "تخمین رتبه 🎯",
        web_app=WebAppInfo(
            url=f"{WEBHOOK_URL}/rank"
        ),
        api_kwargs={"style": "success"}
    )


# --------------------------------------------------
# منوی تخمین رتبه
# --------------------------------------------------

def get_rank_menu_keyboard():
    """
    کیبورد صفحه تخمین رتبه
    """

    return ReplyKeyboardMarkup(
        [
            [
                get_rank_keyboard_button()
            ],
            [
                KeyboardButton(
                    "بازگشت",
                    api_kwargs={"style": "danger"}
                )
            ]
        ],
        resize_keyboard=True
    )


# --------------------------------------------------
# دریافت اطلاعات WebApp
# --------------------------------------------------

async def handle_webapp_data(update, context):
    """
    فعلاً فقط برای تست است.

    بعداً که منطق واقعی تخمین رتبه را اضافه کنیم،
    اطلاعات ارسال‌شده از rank.html اینجا پردازش می‌شود.
    """

    if not update.message or not update.message.web_app_data:
        return

    data = update.message.web_app_data.data

    print("================================")
    print("RANK WEBAPP DATA")
    print(data)
    print("================================")

    await update.message.reply_text(
        "✅ اطلاعات تخمین رتبه دریافت شد."
    )
