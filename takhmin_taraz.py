import os
import json
import logging
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

async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    دریافت و پردازش داده‌های ارسالی از سمت مینی‌اپ
    """
    if not update.effective_message or not update.effective_message.web_app_data:
        return

    raw_data = update.effective_message.web_app_data.data
    user = update.effective_user

    try:
        data = json.loads(raw_data)
    except Exception as e:
        logger.error(f"Error parsing web_app_data: {e}")
        return

    action = data.get("action")
    phone = data.get("phone", "نامشخص")
    scores = data.get("scores", {})
    avg = data.get("weighted_avg", "0")
    taraz = data.get("taraz", "0")
    field = data.get("field", "tajrobi")
    
    field_title = "علوم تجربی" if field == "tajrobi" else field

    if action == "takhmin_konkur":
        # متن گزارش جهت ارسال به گروه مقصد برای کنکور
        report_text = (
            "🎯 <b>ثبت تخمین تراز کنکور جدید</b>\n\n"
            f"👤 <b>نام کاربر:</b> {user.full_name}\n"
            f"🆔 <b>آیدی عددی:</b> <code>{user.id}</code>\n"
            f"🔹 <b>یوزرنیم:</b> @{user.username if user.username else 'ندارد'}\n"
            f"📱 <b>شماره تماس:</b> <code>{phone}</code>\n"
            f"🧬 <b>رشته:</b> <b>{field_title}</b>\n"
            "━━━━━━━━━━━━━━\n"
            "📊 <b>درصدهای وارد شده:</b>\n"
            f"▫️ زیست (۱۲): <code>{scores.get('zist')}%</code>\n"
            f"▫️ شیمی (۹): <code>{scores.get('shimi')}%</code>\n"
            f"▫️ فیزیک (۷): <code>{scores.get('fizik')}%</code>\n"
            f"▫️ ریاضی (۷): <code>{scores.get('riazi')}%</code>\n"
            f"▫️ زمین (۱): <code>{scores.get('zamin')}%</code>\n"
            "━━━━━━━━━━━━━━\n"
            f"📈 <b>میانگین درصد وزنی:</b> <code>{avg}%</code>\n"
            f"🏆 <b>تراز تخمینی کنکور:</b> <b>{taraz}</b>"
        )

        user_receipt = (
            "✅ <b>کارنامه تخمین تراز کنکور شما ثبت شد.</b>\n\n"
            f"🏆 <b>تراز تخمینی کنکور شما:</b> <code>{taraz}</code>\n"
            f"📊 <b>میانگین درصد وزنی:</b> <code>{avg}%</code>\n\n"
            "مشاوران ما در اسرع وقت جهت بررسی شرایط با شما تماس خواهند گرفت."
        )

    elif action == "takhmin_nohaei":
        # متن گزارش جهت ارسال به گروه مقصد برای امتحانات نهایی
        report_text = (
            "📝 <b>ثبت تخمین تراز نهایی جدید</b>\n\n"
            f"👤 <b>نام کاربر:</b> {user.full_name}\n"
            f"🆔 <b>آیدی عددی:</b> <code>{user.id}</code>\n"
            f"🔹 <b>یوزرنیم:</b> @{user.username if user.username else 'ندارد'}\n"
            f"📱 <b>شماره تماس:</b> <code>{phone}</code>\n"
            f"🧬 <b>رشته:</b> <b>{field_title}</b>\n"
            "━━━━━━━━━━━━━━\n"
            "📊 <b>نمرات نهایی وارد شده:</b>\n"
            f"▫️ ادبیات فارسی (۱۱.۰۹): <code>{scores.get('farsi')}</code>\n"
            f"▫️ عربی زبان قرآن (۴.۶۴): <code>{scores.get('arabi')}</code>\n"
            f"▫️ دین و زندگی (۸.۴۷): <code>{scores.get('dini')}</code>\n"
            f"▫️ زبان انگلیسی (۶.۰۵): <code>{scores.get('zaban')}</code>\n"
            f"▫️ سلامت و بهداشت (۱.۷۶): <code>{scores.get('salamat')}</code>\n"
            f"▫️ علوم اجتماعی (۱.۳۱): <code>{scores.get('ejtemai')}</code>\n"
            f"▫️ زیست‌شناسی (۱۰.۶۶): <code>{scores.get('zist')}</code>\n"
            f"▫️ ریاضی (۱۰.۴): <code>{scores.get('riazi')}</code>\n"
            f"▫️ فیزیک (۹.۲۶): <code>{scores.get('fizik')}</code>\n"
            f"▫️ شیمی (۹.۱۹): <code>{scores.get('shimi')}</code>\n"
            "━━━━━━━━━━━━━━\n"
            f"📈 <b>معدل کتبی نهایی موزون:</b> <code>{avg}</code>\n"
            f"🏆 <b>تراز تخمینی نهایی:</b> <b>{taraz}</b>"
        )

        user_receipt = (
            "✅ <b>کارنامه تخمین تراز نهایی شما ثبت شد.</b>\n\n"
            f"🏆 <b>تراز تخمینی نهایی شما:</b> <code>{taraz}</code>\n"
            f"📊 <b>معدل کتبی نهایی موزون:</b> <code>{avg}</code>\n\n"
            "مشاوران ما در اسرع وقت جهت بررسی شرایط با شما تماس خواهند گرفت."
        )
    else:
        logger.error(f"Unknown webapp action received: {action}")
        return

    # ارسال گزارش جامع به گروه ادمین/مشاوران
    try:
        await context.bot.send_message(
            chat_id=LOG_GROUP_ID,
            text=report_text,
            parse_mode="HTML"
        )
    except Exception as ex:
        logger.error(f"Failed to forward report to group {LOG_GROUP_ID}: {ex}")

    # ارسال فیدبک و رسید به چت خود کاربر در ربات
    await update.effective_message.reply_text(user_receipt, parse_mode="HTML")
