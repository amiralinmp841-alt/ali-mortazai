import os
import json
import logging
from html import escape

from telegram import Update, KeyboardButton, WebAppInfo
from telegram.ext import ContextTypes


# شناسه گروه اختصاصی جهت ارسال گزارش‌ها
LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID", "-1001234567890"))

# آدرس دامنه/صفحه وب‌اپ شما (HTTPS اجباری تلگرام)
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://example.com/takhmin.html")

logger = logging.getLogger(__name__)


def get_takhmin_keyboard_button() -> KeyboardButton:
    """
    ساخت دکمه وب‌اپ برای قرار دادن در کیبورد اصلی ربات
    """
    return KeyboardButton(
        text="📊 تخمین تراز کنکور و نهایی",
        api_kwargs={"style": "success"},
        web_app=WebAppInfo(url=WEBAPP_URL)
    )


def safe_value(value, default="—") -> str:
    """
    تبدیل مقدار به متن امن برای استفاده در HTML تلگرام.
    """
    if value is None or value == "":
        return default

    return escape(str(value))


def get_taraz_range_text(data: dict) -> str:
    """
    دریافت بازه تراز از داده ارسالی وب‌اپ.
    """
    taraz = data.get("taraz")

    if taraz not in (None, "", 0, "0"):
        return safe_value(taraz)

    taraz_min = data.get("taraz_min")
    taraz_max = data.get("taraz_max")

    if taraz_min is not None and taraz_max is not None:
        return f"{safe_value(taraz_min)} تا {safe_value(taraz_max)}"

    return "نامشخص"


async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    دریافت و پردازش داده‌های ارسالی از سمت مینی‌اپ تخمین تراز
    """
    if not update.effective_message or not update.effective_message.web_app_data:
        return

    raw_data = update.effective_message.web_app_data.data
    user = update.effective_user

    try:
        data = json.loads(raw_data)
    except json.JSONDecodeError as error:
        logger.error("Error parsing web_app_data JSON: %s", error)
        return
    except Exception as error:
        logger.exception("Unexpected error while parsing web_app_data: %s", error)
        return

    action = data.get("action")
    phone = safe_value(data.get("phone", "نامشخص"))
    scores = data.get("scores", {}) or {}
    avg = safe_value(data.get("weighted_avg", "0"))
    taraz_range = get_taraz_range_text(data)

    taraz_center = safe_value(data.get("taraz_center", "—"))
    taraz_min = safe_value(data.get("taraz_min", "—"))
    taraz_max = safe_value(data.get("taraz_max", "—"))

    field = data.get("field", "tajrobi")

    field_titles = {
        "tajrobi": "علوم تجربی",
        "riazi": "ریاضی فیزیک",
    }

    field_title = field_titles.get(field, safe_value(field))

    user_full_name = safe_value(user.full_name if user else "نامشخص")
    user_id = user.id if user else "نامشخص"
    username = safe_value(
        f"@{user.username}" if user and user.username else "ندارد"
    )

    # ─────────────────────────────────────────────
    # گزارش کنکور تجربی و ریاضی
    # ─────────────────────────────────────────────
    if action == "takhmin_konkur":
        if field == "riazi":
            subject_scores_text = (
                f"▫️ ریاضیات (۱۲): <code>{safe_value(scores.get('riazi'))}%</code>\n"
                f"▫️ فیزیک (۹): <code>{safe_value(scores.get('fizik'))}%</code>\n"
                f"▫️ شیمی (۷): <code>{safe_value(scores.get('shimi'))}%</code>\n"
            )
        else:
            subject_scores_text = (
                f"▫️ زیست‌شناسی (۱۲): <code>{safe_value(scores.get('zist'))}%</code>\n"
                f"▫️ شیمی (۹): <code>{safe_value(scores.get('shimi'))}%</code>\n"
                f"▫️ فیزیک (۷): <code>{safe_value(scores.get('fizik'))}%</code>\n"
                f"▫️ ریاضی (۷): <code>{safe_value(scores.get('riazi'))}%</code>\n"
                f"▫️ زمین‌شناسی (۱): <code>{safe_value(scores.get('zamin'))}%</code>\n"
            )

        report_text = (
            "🎯 <b>ثبت تخمین تراز کنکور جدید</b>\n\n"
            f"👤 <b>نام کاربر:</b> {user_full_name}\n"
            f"🆔 <b>آیدی عددی:</b> <code>{user_id}</code>\n"
            f"🔹 <b>یوزرنیم:</b> {username}\n"
            f"📱 <b>شماره تماس:</b> <code>{phone}</code>\n"
            f"📐 <b>رشته:</b> <b>{field_title}</b>\n"
            "━━━━━━━━━━━━━━\n"
            "📊 <b>درصدهای واردشده:</b>\n"
            f"{subject_scores_text}"
            "━━━━━━━━━━━━━━\n"
            f"📈 <b>میانگین درصد وزنی:</b> <code>{avg}%</code>\n"
            f"🏆 <b>بازه تراز احتمالی کنکور:</b> <b>{taraz_range}</b>\n"
            f"🎯 <b>تراز مرکزی محاسبه‌شده:</b> <code>{taraz_center}</code>\n"
            f"↔️ <b>بازه خام:</b> <code>{taraz_min}</code> تا <code>{taraz_max}</code>"
        )

        user_receipt = (
            f"✅ <b>کارنامه تخمین تراز کنکور {field_title} شما ثبت شد.</b>\n\n"
            f"🏆 <b>بازه تراز احتمالی کنکور شما:</b>\n"
            f"<code>{taraz_range}</code>\n\n"
            f"📊 <b>میانگین درصد وزنی:</b> <code>{avg}%</code>\n\n"
            "ℹ️ بازهٔ نمایش‌داده‌شده با اختلاف ±۲۰۰ نسبت به تراز احتمالی محاسبه شده است.\n\n"
            "مشاوران ما در اسرع وقت جهت بررسی شرایط با شما تماس خواهند گرفت."
        )

    # ─────────────────────────────────────────────
    # گزارش نهایی تجربی و ریاضی
    # ─────────────────────────────────────────────
    elif action == "takhmin_nohaei":
        if field == "riazi":
            subject_scores_text = (
                "📊 <b>نمرات نهایی واردشده:</b>\n"
                f"▫️ فارسی (۱۱.۰۹): <code>{safe_value(scores.get('farsi'))}</code>\n"
                f"▫️ عربی (۴.۶۴): <code>{safe_value(scores.get('arabi'))}</code>\n"
                f"▫️ دینی (۸.۴۷): <code>{safe_value(scores.get('dini'))}</code>\n"
                f"▫️ زبان انگلیسی (۳.۰۵): <code>{safe_value(scores.get('zaban'))}</code>\n"
                f"▫️ سلامت و بهداشت (۱.۷۶): <code>{safe_value(scores.get('salamat'))}</code>\n"
                f"▫️ علوم اجتماعی (۱.۳۱): <code>{safe_value(scores.get('ejtemai'))}</code>\n"
                f"▫️ حسابان (۸.۱۷): <code>{safe_value(scores.get('hesaban'))}</code>\n"
                f"▫️ گسسته (۴.۷۱): <code>{safe_value(scores.get('gosaste'))}</code>\n"
                f"▫️ هندسه (۵.۴۹): <code>{safe_value(scores.get('hendese'))}</code>\n"
                f"▫️ فیزیک (۱۰.۷۰): <code>{safe_value(scores.get('fizik'))}</code>\n"
                f"▫️ شیمی (۱۰.۷۰): <code>{safe_value(scores.get('shimi'))}</code>\n"
            )
        else:
            subject_scores_text = (
                "📊 <b>نمرات نهایی واردشده:</b>\n"
                f"▫️ فارسی (۱۱.۰۹): <code>{safe_value(scores.get('farsi'))}</code>\n"
                f"▫️ عربی (۴.۶۴): <code>{safe_value(scores.get('arabi'))}</code>\n"
                f"▫️ دین و زندگی (۸.۴۷): <code>{safe_value(scores.get('dini'))}</code>\n"
                f"▫️ زبان انگلیسی (۶.۰۵): <code>{safe_value(scores.get('zaban'))}</code>\n"
                f"▫️ سلامت و بهداشت (۱.۷۶): <code>{safe_value(scores.get('salamat'))}</code>\n"
                f"▫️ علوم اجتماعی (۱.۳۱): <code>{safe_value(scores.get('ejtemai'))}</code>\n"
                f"▫️ زیست‌شناسی (۱۰.۶۶): <code>{safe_value(scores.get('zist'))}</code>\n"
                f"▫️ ریاضی (۱۰.۴۰): <code>{safe_value(scores.get('riazi'))}</code>\n"
                f"▫️ فیزیک (۹.۲۶): <code>{safe_value(scores.get('fizik'))}</code>\n"
                f"▫️ شیمی (۹.۱۹): <code>{safe_value(scores.get('shimi'))}</code>\n"
            )

        report_text = (
            "📝 <b>ثبت تخمین تراز نهایی جدید</b>\n\n"
            f"👤 <b>نام کاربر:</b> {user_full_name}\n"
            f"🆔 <b>آیدی عددی:</b> <code>{user_id}</code>\n"
            f"🔹 <b>یوزرنیم:</b> {username}\n"
            f"📱 <b>شماره تماس:</b> <code>{phone}</code>\n"
            f"🧬 <b>رشته:</b> <b>{field_title}</b>\n"
            "━━━━━━━━━━━━━━\n"
            f"{subject_scores_text}"
            "━━━━━━━━━━━━━━\n"
            f"📈 <b>معدل کتبی نهایی موزون:</b> <code>{avg}</code>\n"
            f"🏆 <b>بازه تراز احتمالی نهایی:</b> <b>{taraz_range}</b>\n"
            f"🎯 <b>تراز مرکزی محاسبه‌شده:</b> <code>{taraz_center}</code>\n"
            f"↔️ <b>بازه خام:</b> <code>{taraz_min}</code> تا <code>{taraz_max}</code>"
        )

        user_receipt = (
            f"✅ <b>کارنامه تخمین تراز نهایی {field_title} شما ثبت شد.</b>\n\n"
            f"🏆 <b>بازه تراز احتمالی نهایی شما:</b>\n"
            f"<code>{taraz_range}</code>\n\n"
            f"📊 <b>معدل کتبی نهایی موزون:</b> <code>{avg}</code>\n\n"
            "ℹ️ بازهٔ نمایش‌داده‌شده با اختلاف ±۲۰۰ نسبت به تراز احتمالی محاسبه شده است.\n\n"
            "مشاوران ما در اسرع وقت جهت بررسی شرایط با شما تماس خواهند گرفت."
        )

    else:
        logger.error("Unknown webapp action received: %s", action)
        return

    # ارسال گزارش جامع به گروه ادمین/مشاوران
    try:
        await context.bot.send_message(
            chat_id=LOG_GROUP_ID,
            text=report_text,
            parse_mode="HTML"
        )
    except Exception as error:
        logger.exception(
            "Failed to send report to group %s: %s",
            LOG_GROUP_ID,
            error
        )

    # ارسال رسید به چت کاربر
    try:
        await update.effective_message.reply_text(
            user_receipt,
            parse_mode="HTML"
        )
    except Exception as error:
        logger.exception(
            "Failed to send receipt to user %s: %s",
            user_id,
            error
        )
