import os
import json
import logging
from html import escape

from telegram import Update, KeyboardButton, WebAppInfo
from telegram.ext import ContextTypes


# =========================================================
# CONFIG
# =========================================================

LOG_GROUP_ID = int(
    os.getenv(
        "LOG_GROUP_ID",
        "-1001234567890"
    )
)

WEBAPP_URL = os.getenv(
    "WEBAPP_URL",
    "https://example.com/takhmin.html"
)


logger = logging.getLogger(__name__)


# =========================================================
# WEB APP BUTTON
# =========================================================

def get_takhmin_keyboard_button() -> KeyboardButton:
    """
    ساخت دکمه وب‌اپ تخمین تراز
    """

    return KeyboardButton(
        text="📊 تخمین تراز کنکور و نهایی",
        api_kwargs={
            "style": "success"
        },
        web_app=WebAppInfo(
            url=WEBAPP_URL
        )
    )


# =========================================================
# SAFE HELPERS
# =========================================================

def safe_value(
    value,
    default="—"
) -> str:

    if value is None or value == "":
        return default

    return escape(
        str(value)
    )


def get_taraz_range_text(
    data: dict
) -> str:

    taraz = data.get(
        "taraz"
    )

    if taraz not in (
        None,
        "",
        0,
        "0"
    ):
        return safe_value(
            taraz
        )


    taraz_min = data.get(
        "taraz_min"
    )

    taraz_max = data.get(
        "taraz_max"
    )


    if (
        taraz_min is not None
        and
        taraz_max is not None
    ):

        return (
            f"{safe_value(taraz_min)}"
            f" تا "
            f"{safe_value(taraz_max)}"
        )


    return "نامشخص"


# =========================================================
# WEB APP DATA HANDLER
# =========================================================

async def handle_webapp_data(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if (
        not update.effective_message
        or
        not update.effective_message.web_app_data
    ):
        return


    raw_data = (
        update
        .effective_message
        .web_app_data
        .data
    )


    user = update.effective_user


    # =====================================================
    # PARSE JSON
    # =====================================================

    try:

        data = json.loads(
            raw_data
        )

    except json.JSONDecodeError as error:

        logger.error(
            "Error parsing web_app_data JSON: %s",
            error
        )

        return

    except Exception as error:

        logger.exception(
            "Unexpected error while parsing web_app_data: %s",
            error
        )

        return


    # =====================================================
    # BASIC DATA
    # =====================================================

    action = data.get(
        "action"
    )


    phone = safe_value(
        data.get(
            "phone",
            "نامشخص"
        )
    )


    scores = (
        data.get(
            "scores",
            {}
        )
        or
        {}
    )


    avg = safe_value(
        data.get(
            "weighted_avg",
            "0"
        )
    )


    taraz_range = get_taraz_range_text(
        data
    )


    taraz_center = safe_value(
        data.get(
            "taraz_center",
            "—"
        )
    )


    taraz_min = safe_value(
        data.get(
            "taraz_min",
            "—"
        )
    )


    taraz_max = safe_value(
        data.get(
            "taraz_max",
            "—"
        )
    )


    field = data.get(
        "field",
        "tajrobi"
    )


    # =====================================================
    # FIELD TITLES
    # =====================================================

    field_titles = {

        "tajrobi":
            "علوم تجربی",

        "riazi":
            "ریاضی فیزیک"

    }


    field_title = field_titles.get(
        field,
        safe_value(field)
    )


    # =====================================================
    # USER INFO
    # =====================================================

    user_full_name = safe_value(
        user.full_name
        if user
        else
        "نامشخص"
    )


    user_id = (
        user.id
        if user
        else
        "نامشخص"
    )


    username = safe_value(
        (
            f"@{user.username}"
            if user and user.username
            else
            "ندارد"
        )
    )


    # =====================================================
    # KONKUR
    # =====================================================

    if action == "takhmin_konkur":


        # =================================================
        # KONKUR RIAZI
        # =================================================

        if field == "riazi":

            math_score = safe_value(
                scores.get(
                    "math"
                )
            )


            fizik_score = safe_value(
                scores.get(
                    "fizik"
                )
            )


            shimi_score = safe_value(
                scores.get(
                    "shimi"
                )
            )


            report_text = (

                "🎯 <b>ثبت تخمین تراز کنکور ریاضی جدید</b>\n\n"

                f"👤 <b>نام کاربر:</b> "
                f"{user_full_name}\n"

                f"🆔 <b>آیدی عددی:</b> "
                f"<code>{user_id}</code>\n"

                f"🔹 <b>یوزرنیم:</b> "
                f"{username}\n"

                f"📱 <b>شماره تماس:</b> "
                f"<code>{phone}</code>\n"

                f"📐 <b>رشته:</b> "
                f"<b>{field_title}</b>\n"

                "━━━━━━━━━━━━━━\n"

                "📊 <b>درصدهای واردشده:</b>\n"

                f"▫️ ریاضیات (۱۲): "
                f"<code>{math_score}%</code>\n"

                f"▫️ فیزیک (۹): "
                f"<code>{fizik_score}%</code>\n"

                f"▫️ شیمی (۷): "
                f"<code>{shimi_score}%</code>\n"

                "━━━━━━━━━━━━━━\n"

                f"📈 <b>میانگین درصد وزنی:</b> "
                f"<code>{avg}%</code>\n"

                f"🏆 <b>بازه تراز احتمالی کنکور:</b> "
                f"<b>{taraz_range}</b>\n"

                f"🎯 <b>تراز مرکزی محاسبه‌شده:</b> "
                f"<code>{taraz_center}</code>\n"

                f"↔️ <b>بازه خام:</b> "
                f"<code>{taraz_min}</code>"
                f" تا "
                f"<code>{taraz_max}</code>"

            )


            user_receipt = (

                "✅ <b>کارنامه تخمین تراز کنکور ریاضی شما ثبت شد.</b>\n\n"

                f"🏆 <b>بازه تراز احتمالی شما:</b>\n"
                f"<code>{taraz_range}</code>\n\n"

                f"📊 <b>میانگین درصد وزنی:</b> "
                f"<code>{avg}%</code>\n\n"

                "ℹ️ بازه نمایش‌داده‌شده "
                "با اختلاف ±۲۰۰ نسبت به "
                "تراز احتمالی محاسبه شده است.\n\n"

                "مشاوران ما در اسرع وقت "
                "جهت بررسی شرایط با شما تماس خواهند گرفت."

            )


        # =================================================
        # KONKUR TAJROBI
        # =================================================

        else:

            report_text = (

                "🎯 <b>ثبت تخمین تراز کنکور تجربی جدید</b>\n\n"

                f"👤 <b>نام کاربر:</b> "
                f"{user_full_name}\n"

                f"🆔 <b>آیدی عددی:</b> "
                f"<code>{user_id}</code>\n"

                f"🔹 <b>یوزرنیم:</b> "
                f"{username}\n"

                f"📱 <b>شماره تماس:</b> "
                f"<code>{phone}</code>\n"

                f"🧬 <b>رشته:</b> "
                f"<b>{field_title}</b>\n"

                "━━━━━━━━━━━━━━\n"

                "📊 <b>درصدهای واردشده:</b>\n"

                f"▫️ زیست‌شناسی (۱۲): "
                f"<code>{safe_value(scores.get('zist'))}%</code>\n"

                f"▫️ شیمی (۹): "
                f"<code>{safe_value(scores.get('shimi'))}%</code>\n"

                f"▫️ فیزیک (۷): "
                f"<code>{safe_value(scores.get('fizik'))}%</code>\n"

                f"▫️ ریاضی (۷): "
                f"<code>{safe_value(scores.get('riazi'))}%</code>\n"

                f"▫️ زمین‌شناسی (۱): "
                f"<code>{safe_value(scores.get('zamin'))}%</code>\n"

                "━━━━━━━━━━━━━━\n"

                f"📈 <b>میانگین درصد وزنی:</b> "
                f"<code>{avg}%</code>\n"

                f"🏆 <b>بازه تراز احتمالی کنکور:</b> "
                f"<b>{taraz_range}</b>\n"

                f"🎯 <b>تراز مرکزی محاسبه‌شده:</b> "
                f"<code>{taraz_center}</code>\n"

                f"↔️ <b>بازه خام:</b> "
                f"<code>{taraz_min}</code>"
                f" تا "
                f"<code>{taraz_max}</code>"

            )


            user_receipt = (

                "✅ <b>کارنامه تخمین تراز کنکور تجربی شما ثبت شد.</b>\n\n"

                f"🏆 <b>بازه تراز احتمالی شما:</b>\n"
                f"<code>{taraz_range}</code>\n\n"

                f"📊 <b>میانگین درصد وزنی:</b> "
                f"<code>{avg}%</code>\n\n"

                "ℹ️ بازه نمایش‌داده‌شده "
                "با اختلاف ±۲۰۰ نسبت به "
                "تراز احتمالی محاسبه شده است.\n\n"

                "مشاوران ما در اسرع وقت "
                "جهت بررسی شرایط با شما تماس خواهند گرفت."

            )


    # =====================================================
    # FINAL
    # =====================================================

    elif action == "takhmin_nohaei":


        # =================================================
        # FINAL RIAZI
        # =================================================

        if field == "riazi":

            subject_scores_text = (

                "📊 <b>نمرات نهایی واردشده:</b>\n"

                f"▫️ فارسی (۱۱.۰۹): "
                f"<code>{safe_value(scores.get('farsi'))}</code>\n"

                f"▫️ عربی (۴.۶۴): "
                f"<code>{safe_value(scores.get('arabi'))}</code>\n"

                f"▫️ دینی (۸.۴۷): "
                f"<code>{safe_value(scores.get('dini'))}</code>\n"

                f"▫️ زبان انگلیسی (۳.۰۵): "
                f"<code>{safe_value(scores.get('zaban'))}</code>\n"

                f"▫️ سلامت و بهداشت (۱.۷۶): "
                f"<code>{safe_value(scores.get('salamat'))}</code>\n"

                f"▫️ علوم اجتماعی (۱.۳۱): "
                f"<code>{safe_value(scores.get('ejtemai'))}</code>\n"

                f"▫️ حسابان (۸.۱۷): "
                f"<code>{safe_value(scores.get('hesaban'))}</code>\n"

                f"▫️ گسسته (۴.۷۱): "
                f"<code>{safe_value(scores.get('gosaste'))}</code>\n"

                f"▫️ هندسه (۵.۴۹): "
                f"<code>{safe_value(scores.get('hendese'))}</code>\n"

                f"▫️ فیزیک (۱۰.۷۰): "
                f"<code>{safe_value(scores.get('fizik'))}</code>\n"

                f"▫️ شیمی (۱۰.۷۰): "
                f"<code>{safe_value(scores.get('shimi'))}</code>\n"

            )


        # =================================================
        # FINAL TAJROBI
        # =================================================

        else:

            subject_scores_text = (

                "📊 <b>نمرات نهایی واردشده:</b>\n"

                f"▫️ فارسی (۱۱.۰۹): "
                f"<code>{safe_value(scores.get('farsi'))}</code>\n"

                f"▫️ عربی (۴.۶۴): "
                f"<code>{safe_value(scores.get('arabi'))}</code>\n"

                f"▫️ دین و زندگی (۸.۴۷): "
                f"<code>{safe_value(scores.get('dini'))}</code>\n"

                f"▫️ زبان انگلیسی (۶.۰۵): "
                f"<code>{safe_value(scores.get('zaban'))}</code>\n"

                f"▫️ سلامت و بهداشت (۱.۷۶): "
                f"<code>{safe_value(scores.get('salamat'))}</code>\n"

                f"▫️ علوم اجتماعی (۱.۳۱): "
                f"<code>{safe_value(scores.get('ejtemai'))}</code>\n"

                f"▫️ زیست‌شناسی (۱۰.۶۶): "
                f"<code>{safe_value(scores.get('zist'))}</code>\n"

                f"▫️ ریاضی (۱۰.۴۰): "
                f"<code>{safe_value(scores.get('riazi'))}</code>\n"

                f"▫️ فیزیک (۹.۲۶): "
                f"<code>{safe_value(scores.get('fizik'))}</code>\n"

                f"▫️ شیمی (۹.۱۹): "
                f"<code>{safe_value(scores.get('shimi'))}</code>\n"

            )


        # =================================================
        # REPORT
        # =================================================

        report_text = (

            "📝 <b>ثبت تخمین تراز نهایی جدید</b>\n\n"

            f"👤 <b>نام کاربر:</b> "
            f"{user_full_name}\n"

            f"🆔 <b>آیدی عددی:</b> "
            f"<code>{user_id}</code>\n"

            f"🔹 <b>یوزرنیم:</b> "
            f"{username}\n"

            f"📱 <b>شماره تماس:</b> "
            f"<code>{phone}</code>\n"

            f"🧬 <b>رشته:</b> "
            f"<b>{field_title}</b>\n"

            "━━━━━━━━━━━━━━\n"

            f"{subject_scores_text}"

            "━━━━━━━━━━━━━━\n"

            f"📈 <b>معدل کتبی نهایی موزون:</b> "
            f"<code>{avg}</code>\n"

            f"🏆 <b>بازه تراز احتمالی نهایی:</b> "
            f"<b>{taraz_range}</b>\n"

            f"🎯 <b>تراز مرکزی محاسبه‌شده:</b> "
            f"<code>{taraz_center}</code>\n"

            f"↔️ <b>بازه خام:</b> "
            f"<code>{taraz_min}</code>"
            f" تا "
            f"<code>{taraz_max}</code>"

        )


        user_receipt = (

            "✅ <b>کارنامه تخمین تراز نهایی شما ثبت شد.</b>\n\n"

            f"🏆 <b>بازه تراز احتمالی نهایی شما:</b>\n"
            f"<code>{taraz_range}</code>\n\n"

            f"📊 <b>معدل کتبی نهایی موزون:</b> "
            f"<code>{avg}</code>\n\n"

            "ℹ️ بازه نمایش‌داده‌شده "
            "با اختلاف ±۲۰۰ نسبت به "
            "تراز احتمالی محاسبه شده است.\n\n"

            "مشاوران ما در اسرع وقت "
            "جهت بررسی شرایط با شما تماس خواهند گرفت."

        )


    # =====================================================
    # UNKNOWN ACTION
    # =====================================================

    else:

        logger.error(
            "Unknown webapp action received: %s",
            action
        )

        return


    # =====================================================
    # SEND REPORT TO ADMIN GROUP
    # =====================================================

    try:

        await context.bot.send_message(
            chat_id=LOG_GROUP_ID,
            text=report_text,
            parse_mode="HTML"
        )

        logger.info(
            "Takhmin report successfully sent to LOG_GROUP_ID=%s "
            "for user_id=%s",
            LOG_GROUP_ID,
            user_id
        )

    except Exception as error:

        logger.exception(
            "FAILED TO SEND TAKHMIN REPORT TO ADMIN GROUP. "
            "LOG_GROUP_ID=%s | user_id=%s | error=%s",
            LOG_GROUP_ID,
            user_id,
            error
        )


    # =====================================================
    # SEND RECEIPT TO USER
    # =====================================================

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
