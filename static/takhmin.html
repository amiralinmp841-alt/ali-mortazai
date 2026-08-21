<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>تخمین تراز کنکور و نهایی</title>

  <script src="https://telegram.org/js/telegram-web-app.js"></script>

  <style>
    :root {
      --bg-color: var(--tg-theme-bg-color, #0b0f1f);
      --card-bg: var(--tg-theme-secondary-bg-color, #161b2e);
      --text-color: var(--tg-theme-text-color, #fdf2f8);
      --hint-color: var(--tg-theme-hint-color, #b9a0c4);
      --btn-color: var(--tg-theme-button-color, #f472b6);
      --btn-text: var(--tg-theme-button-text-color, #1c1020);
      --border-color: rgba(244, 114, 182, 0.18);
      --primary: #f472b6;
      --primary-2: #a78bfa;
      --success: #34d399;
      --shadow: rgba(244, 114, 182, 0.12);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    body {
      background: linear-gradient(160deg, #0b0f1f 0%, #131a38 55%, #1e1440 100%);
      background-color: var(--bg-color);
      color: var(--text-color);
      padding: 16px;
      line-height: 1.5;
      min-height: 100vh;
    }

    .container {
      max-width: 480px;
      margin: 0 auto;
    }

    .header {
      text-align: center;
      margin-bottom: 20px;
    }

    .brand-name {
      font-size: 1.8rem;
      font-weight: 900;
      color: var(--text-color);
      margin-bottom: 4px;
      letter-spacing: -0.5px;
      background: linear-gradient(135deg, #f472b6, #a78bfa);
      -webkit-background-clip: text;
      background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .brand-tagline {
      font-size: 0.82rem;
      color: var(--hint-color);
      margin-bottom: 14px;
    }

    .header-logo {
      width: 100%;
      max-width: 140px;
      height: auto;
      max-height: 90px;
      object-fit: contain;
      display: block;
      margin: 0 auto 12px auto;
      filter: drop-shadow(0 4px 12px var(--shadow));
      border-radius: 10px;
    }

    .header h1 {
      font-size: 1.2rem;
      font-weight: 800;
      color: var(--primary);
      margin-top: 8px;
    }

    .header p {
      font-size: 0.8rem;
      color: var(--hint-color);
      margin-top: 4px;
    }

    .card {
      background: linear-gradient(145deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
      background-color: var(--card-bg);
      border-radius: 18px;
      padding: 18px;
      border: 1px solid var(--border-color);
      box-shadow:
        0 14px 32px -10px rgba(0, 0, 0, 0.55),
        inset 0 1px 0 rgba(255,255,255,0.05);
      margin-bottom: 16px;
    }

    .btn {
      width: 100%;
      padding: 13px;
      border-radius: 12px;
      border: none;
      font-weight: 700;
      font-size: 0.95rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: all 0.2s ease;
      margin-top: 10px;
    }

    .btn-primary {
      background: linear-gradient(135deg, #f472b6 0%, #a78bfa 100%);
      background-color: var(--btn-color);
      color: var(--btn-text);
      box-shadow: 0 8px 20px -8px var(--shadow);
    }

    .btn-primary:active {
      transform: scale(0.98);
      filter: brightness(0.92);
    }

    .btn-secondary {
      background: rgba(244, 114, 182, 0.08);
      color: var(--text-color);
      border: 1px solid var(--border-color);
    }

    .btn-secondary:active {
      background: rgba(244, 114, 182, 0.16);
    }

    .grid-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-bottom: 12px;
    }

    .form-group {
      margin-bottom: 12px;
    }

    .form-group label {
      display: block;
      font-size: 0.8rem;
      color: var(--hint-color);
      margin-bottom: 6px;
    }

    .input-control {
      width: 100%;
      padding: 11px 14px;
      border-radius: 10px;
      background: rgba(0, 0, 0, 0.35);
      border: 1px solid var(--border-color);
      color: var(--text-color);
      font-size: 1rem;
      text-align: center;
      outline: none;
      transition: border-color 0.2s, box-shadow 0.2s;
    }

    .input-control:focus {
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(244, 114, 182, 0.15);
    }

    .hidden {
      display: none !important;
    }

    .modal-overlay {
      position: fixed;
      inset: 0;
      background: rgba(10, 5, 20, 0.85);
      backdrop-filter: blur(6px);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 16px;
      z-index: 100;
    }

    .result-box {
      text-align: center;
      padding: 20px;
      border-radius: 16px;
      background: linear-gradient(
        135deg,
        rgba(244, 114, 182, 0.22),
        rgba(167, 139, 250, 0.22),
        rgba(52, 211, 153, 0.15)
      );
      border: 1px solid var(--primary);
      box-shadow: 0 0 26px -6px var(--shadow);
      margin-bottom: 16px;
    }

    .result-box .taraz-val {
      font-size: 1.55rem;
      font-weight: 800;
      background: linear-gradient(135deg, #f472b6, #a78bfa, #34d399);
      -webkit-background-clip: text;
      background-clip: text;
      -webkit-text-fill-color: transparent;
      margin: 10px 0;
      line-height: 1.8;
    }

    .badge {
      display: inline-block;
      padding: 4px 10px;
      background: rgba(244, 114, 182, 0.14);
      border: 1px solid var(--border-color);
      border-radius: 20px;
      font-size: 0.75rem;
      color: var(--primary);
    }
  </style>
</head>

<body>
  <div class="container">

    <div class="header">
      <div class="brand-name">بیولوژیست</div>
      <img src="logo.png" alt="لوگو" class="header-logo">
      <div class="brand-tagline">تنها رسانه کنکوری دانشجویان بهشتی</div>
      <h1>📊 سامانه هوشمند تخمین تراز</h1>
      <p>محاسبه تراز کنکور و نهایی بر اساس آخرین متدولوژی</p>
    </div>

    <!-- مرحله ۱: انتخاب نوع آزمون -->
    <div id="section-menu" class="card">
      <p style="margin-bottom:14px; text-align:center; font-size:0.9rem;">
        بخش مورد نظر را انتخاب کنید:
      </p>

      <button class="btn btn-primary" onclick="selectType('konkur')">
        🎯 ۱۴۰۵ تخمین تراز کنکور
      </button>

      <button class="btn btn-primary" onclick="selectType('nohaei')">
        📝 ۱۴۰۵ تخمین تراز نهایی
      </button>
    </div>

    <!-- مرحله ۱.۵: انتخاب رشته -->
    <div id="section-field" class="card hidden">
      <p style="margin-bottom:14px; text-align:center; font-size:0.9rem;">
        رشته تحصیلی خود را انتخاب کنید:
      </p>

      <button class="btn btn-primary" onclick="selectField('tajrobi')">
        🧬 تجربی
      </button>

      <button class="btn btn-primary" onclick="selectRiaziField()">
        📐 ریاضی
      </button>

      <button class="btn btn-secondary" onclick="showInactiveField('انسانی')">
        📚 انسانی (غیرفعال)
      </button>

      <button class="btn btn-secondary" onclick="backToMenu()">
        بازگشت به منوی قبل
      </button>
    </div>

    <!-- فرم درصدهای کنکور تجربی -->
    <div id="section-konkur" class="card hidden">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
        <span style="font-weight:700; font-size:0.95rem;">
          درصدهای دروس کنکور تجربی
        </span>

        <span class="badge">ضرایب رسمی</span>
      </div>

      <div class="grid-2">
        <div class="form-group">
          <label>زیست‌شناسی (ضریب ۱۲)</label>
          <input type="number" id="p_zist" class="input-control" placeholder="٪" min="0" max="100" step="0.01">
        </div>

        <div class="form-group">
          <label>شیمی (ضریب ۹)</label>
          <input type="number" id="p_shimi" class="input-control" placeholder="٪" min="0" max="100" step="0.01">
        </div>
      </div>

      <div class="grid-2">
        <div class="form-group">
          <label>فیزیک (ضریب ۷)</label>
          <input type="number" id="p_fizik" class="input-control" placeholder="٪" min="0" max="100" step="0.01">
        </div>

        <div class="form-group">
          <label>ریاضی (ضریب ۷)</label>
          <input type="number" id="p_riazi" class="input-control" placeholder="٪" min="0" max="100" step="0.01">
        </div>
      </div>

      <div class="form-group">
        <label>زمین‌شناسی (ضریب ۱)</label>
        <input type="number" id="p_zamin" class="input-control" placeholder="٪" min="0" max="100" step="0.01">
      </div>

      <button class="btn btn-primary" onclick="openPhoneModal()">
        ⚡ محاسبه بازه تراز کنکور
      </button>

      <button class="btn btn-secondary" onclick="backToFields()">
        بازگشت
      </button>
    </div>

    <!-- فرم درصدهای کنکور ریاضی -->
    <div id="section-konkur-riazi" class="card hidden">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
        <span style="font-weight:700; font-size:0.95rem;">
          درصدهای دروس کنکور ریاضی
        </span>

        <span class="badge">ضرایب رسمی ریاضی</span>
      </div>

      <div class="grid-2">
        <div class="form-group">
          <label>ریاضیات (ضریب ۱۲)</label>
          <input type="number" id="pr_riazi" class="input-control" placeholder="٪" min="0" max="100" step="0.01">
        </div>

        <div class="form-group">
          <label>فیزیک (ضریب ۹)</label>
          <input type="number" id="pr_fizik" class="input-control" placeholder="٪" min="0" max="100" step="0.01">
        </div>
      </div>

      <div class="form-group">
        <label>شیمی (ضریب ۷)</label>
        <input type="number" id="pr_shimi" class="input-control" placeholder="٪" min="0" max="100" step="0.01">
      </div>

      <button class="btn btn-primary" onclick="openPhoneModal()">
        ⚡ محاسبه بازه تراز کنکور
      </button>

      <button class="btn btn-secondary" onclick="backToFields()">
        بازگشت
      </button>
    </div>

    <!-- فرم نمرات نهایی -->
    <div id="section-nohaei" class="card hidden">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
        <span id="nohaei-form-title" style="font-weight:700; font-size:0.95rem;">
          نمرات نهایی تجربی
        </span>

        <span class="badge">ضرایب نهایی مصوب</span>
      </div>

      <!-- دروس عمومی مشترک -->
      <div class="grid-2">
        <div class="form-group">
          <label>فارسی (ضریب ۱۱.۰۹)</label>
          <input type="number" id="n_farsi" class="input-control" placeholder="۰ تا ۲۰" min="0" max="20" step="0.25">
        </div>

        <div class="form-group">
          <label>عربی (ضریب ۴.۶۴)</label>
          <input type="number" id="n_arabi" class="input-control" placeholder="۰ تا ۲۰" min="0" max="20" step="0.25">
        </div>
      </div>

      <div class="grid-2">
        <div class="form-group">
          <label>دینی (ضریب ۸.۴۷)</label>
          <input type="number" id="n_dini" class="input-control" placeholder="۰ تا ۲۰" min="0" max="20" step="0.25">
        </div>

        <div class="form-group">
          <label id="label-zaban">زبان انگلیسی (ضریب ۶.۰۵)</label>
          <input type="number" id="n_zaban" class="input-control" placeholder="۰ تا ۲۰" min="0" max="20" step="0.25">
        </div>
      </div>

      <div class="grid-2">
        <div class="form-group">
          <label>سلامت و بهداشت (ضریب ۱.۷۶)</label>
          <input type="number" id="n_salamat" class="input-control" placeholder="۰ تا ۲۰" min="0" max="20" step="0.25">
        </div>

        <div class="form-group">
          <label>علوم اجتماعی (ضریب ۱.۳۱)</label>
          <input type="number" id="n_ejtemai" class="input-control" placeholder="۰ تا ۲۰" min="0" max="20" step="0.25">
        </div>
      </div>

      <!-- دروس اختصاصی تجربی -->
      <div id="nohaei-tajrobi-fields">
        <div class="grid-2">
          <div class="form-group">
            <label>زیست‌شناسی (ضریب ۱۰.۶۶)</label>
            <input type="number" id="n_zist" class="input-control" placeholder="۰ تا ۲۰" min="0" max="20" step="0.25">
          </div>

          <div class="form-group">
            <label>ریاضی (ضریب ۱۰.۴۰)</label>
            <input type="number" id="n_riazi" class="input-control" placeholder="۰ تا ۲۰" min="0" max="20" step="0.25">
          </div>
        </div>

        <div class="grid-2">
          <div class="form-group">
            <label>فیزیک (ضریب ۹.۲۶)</label>
            <input type="number" id="n_fizik" class="input-control" placeholder="۰ تا ۲۰" min="0" max="20" step="0.25">
          </div>

          <div class="form-group">
            <label>شیمی (ضریب ۹.۱۹)</label>
            <input type="number" id="n_shimi" class="input-control" placeholder="۰ تا ۲۰" min="0" max="20" step="0.25">
          </div>
        </div>
      </div>

      <!-- دروس اختصاصی ریاضی -->
      <div id="nohaei-riazi-fields" class="hidden">
        <div class="grid-2">
          <div class="form-group">
            <label>حسابان (ضریب ۸.۱۷)</label>
            <input type="number" id="n_hesaban" class="input-control" placeholder="۰ تا ۲۰" min="0" max="20" step="0.25">
          </div>

          <div class="form-group">
            <label>هندسه (ضریب ۵.۴۹)</label>
            <input type="number" id="n_hendese" class="input-control" placeholder="۰ تا ۲۰" min="0" max="20" step="0.25">
          </div>
        </div>

        <div class="grid-2">
          <div class="form-group">
            <label>گسسته (ضریب ۴.۷۱)</label>
            <input type="number" id="n_gosaste" class="input-control" placeholder="۰ تا ۲۰" min="0" max="20" step="0.25">
          </div>

          <div class="form-group">
            <label>فیزیک (ضریب ۱۰.۷۰)</label>
            <input type="number" id="n_fizik_riazi" class="input-control" placeholder="۰ تا ۲۰" min="0" max="20" step="0.25">
          </div>
        </div>

        <div class="form-group">
          <label>شیمی (ضریب ۱۰.۷۰)</label>
          <input type="number" id="n_shimi_riazi" class="input-control" placeholder="۰ تا ۲۰" min="0" max="20" step="0.25">
        </div>
      </div>

      <button class="btn btn-primary" onclick="openPhoneModal()">
        ⚡ محاسبه بازه تراز نهایی
      </button>

      <button class="btn btn-secondary" onclick="backToFields()">
        بازگشت
      </button>
    </div>

    <!-- پاپ‌آپ شماره تماس -->
    <div id="modal-phone" class="modal-overlay hidden">
      <div class="card" style="width:100%; max-width:380px;">
        <h3 style="font-size:1.1rem; margin-bottom:8px;">
          📱 دریافت کارنامه تراز
        </h3>

        <p style="font-size:0.8rem; color:var(--hint-color); margin-bottom:14px;">
          برای مشاهده گزارش، لطفاً شماره موبایل خود را وارد نمایید:
        </p>

        <div class="form-group">
          <input
            type="tel"
            id="user_phone"
            class="input-control"
            placeholder="مثال: 09123456789"
            style="letter-spacing:2px;"
          >
        </div>

        <button class="btn btn-primary" onclick="processAndCalculate()">
          تأیید و مشاهده نتیجه
        </button>

        <button class="btn btn-secondary" onclick="closePhoneModal()">
          انصراف
        </button>
      </div>
    </div>

    <!-- نتیجه -->
    <div id="section-result" class="card hidden">
      <div class="result-box">
        <p style="font-size:0.85rem; color:var(--hint-color);" id="res-title">
          بازه تراز تخمینی شما
        </p>

        <div class="taraz-val" id="res-taraz">----</div>

        <p style="font-size:0.85rem;" id="res-avg-container">
          میانگین وزنی: <b id="res-avg">0</b>
        </p>
      </div>

      <p style="font-size:0.75rem; color:var(--hint-color); text-align:center; margin-bottom:14px;">
        بازهٔ تراز با اختلاف ±۲۰۰ نسبت به تراز احتمالی محاسبه شده است.
        اطلاعات برای مشاور ارسال گردید.
      </p>

      <button class="btn btn-primary" onclick="closeApp()">
        بستن و بازگشت به ربات
      </button>
    </div>
  </div>

  <script>
    const tg = window.Telegram?.WebApp;

    if (tg) {
      tg.ready();
      tg.expand();
    }

    let selectedAction = "";
    let selectedField = "";

    function showMessage(message) {
      if (tg) {
        tg.showAlert(message);
      } else {
        alert(message);
      }
    }

    function selectType(type) {
      selectedAction = type;
      selectedField = "";

      document.getElementById("section-menu").classList.add("hidden");
      document.getElementById("section-field").classList.remove("hidden");
    }

    function selectField(field) {
      selectedField = field;

      document.getElementById("section-field").classList.add("hidden");

      if (selectedAction === "konkur") {
        if (field === "riazi") {
          document.getElementById("section-konkur-riazi").classList.remove("hidden");
        } else {
          document.getElementById("section-konkur").classList.remove("hidden");
        }
        return;
      }

      setNohaeiFormByField();
      document.getElementById("section-nohaei").classList.remove("hidden");
    }

    function selectRiaziField() {
      selectField("riazi");
    }

    function showInactiveField(fieldName) {
      showMessage(`${fieldName} در حال حاضر فعال نیست.`);
    }

    function setNohaeiFormByField() {
      const isRiazi = selectedField === "riazi";

      document.getElementById("nohaei-form-title").innerText = isRiazi
        ? "نمرات نهایی ریاضی"
        : "نمرات نهایی تجربی";

      document.getElementById("label-zaban").innerText = isRiazi
        ? "زبان انگلیسی (ضریب ۳.۰۵)"
        : "زبان انگلیسی (ضریب ۶.۰۵)";

      document
        .getElementById("nohaei-tajrobi-fields")
        .classList.toggle("hidden", isRiazi);

      document
        .getElementById("nohaei-riazi-fields")
        .classList.toggle("hidden", !isRiazi);
    }

    function backToMenu() {
      document.getElementById("section-field").classList.add("hidden");
      document.getElementById("section-menu").classList.remove("hidden");
    }

    function backToFields() {
      document.getElementById("section-konkur").classList.add("hidden");
      document.getElementById("section-konkur-riazi").classList.add("hidden");
      document.getElementById("section-nohaei").classList.add("hidden");
      document.getElementById("section-field").classList.remove("hidden");
    }

    function openPhoneModal() {
      if (selectedAction === "konkur") {
        const ids = selectedField === "riazi"
          ? ["pr_riazi", "pr_fizik", "pr_shimi"]
          : ["p_zist", "p_shimi", "p_fizik", "p_riazi", "p_zamin"];

        for (const id of ids) {
          const value = document.getElementById(id).value;

          if (value === "" || isNaN(value)) {
            showMessage("لطفاً درصد تمام دروس کنکور را وارد کنید.");
            return;
          }

          const score = parseFloat(value);

          if (score < 0 || score > 100) {
            showMessage("درصد هر درس باید بین ۰ تا ۱۰۰ باشد. درصد منفی پذیرفته نمی‌شود.");
            return;
          }
        }
      } else {
        const commonIds = [
          "n_farsi",
          "n_arabi",
          "n_dini",
          "n_zaban",
          "n_salamat",
          "n_ejtemai"
        ];

        const tajrobiIds = [
          "n_zist",
          "n_riazi",
          "n_fizik",
          "n_shimi"
        ];

        const riaziIds = [
          "n_hesaban",
          "n_gosaste",
          "n_hendese",
          "n_fizik_riazi",
          "n_shimi_riazi"
        ];

        const ids = selectedField === "riazi"
          ? [...commonIds, ...riaziIds]
          : [...commonIds, ...tajrobiIds];

        for (const id of ids) {
          const value = document.getElementById(id).value;

          if (value === "" || isNaN(value)) {
            showMessage("لطفاً نمره تمام دروس نهایی را وارد کنید.");
            return;
          }

          const score = parseFloat(value);

          if (score < 0 || score > 20) {
            showMessage("نمرات نهایی باید بین بازه ۰ تا ۲۰ باشند.");
            return;
          }
        }
      }

      document.getElementById("modal-phone").classList.remove("hidden");
    }

    function closePhoneModal() {
      document.getElementById("modal-phone").classList.add("hidden");
    }

    function interpolate(value, points) {
      if (value <= points[0].x) {
        return points[0].y;
      }

      if (value >= points[points.length - 1].x) {
        return points[points.length - 1].y;
      }

      for (let i = 0; i < points.length - 1; i++) {
        const p1 = points[i];
        const p2 = points[i + 1];

        if (value >= p1.x && value <= p2.x) {
          const result =
            p1.y +
            ((value - p1.x) / (p2.x - p1.x)) * (p2.y - p1.y);

          return Math.round(result);
        }
      }

      return points[points.length - 1].y;
    }

    function calculateKonkurTaraz(avg) {
      const points = [
        { x: 0, y: 4000 },
        { x: 5, y: 5900 },
        { x: 10, y: 6600 },
        { x: 20, y: 7500 },
        { x: 30, y: 8300 },
        { x: 40, y: 9300 },
        { x: 50, y: 10000 },
        { x: 60, y: 10900 },
        { x: 70, y: 11800 },
        { x: 80, y: 12800 },
        { x: 90, y: 14000 },
        { x: 100, y: 15000 }
      ];

      return interpolate(avg, points);
    }

    function calculateKonkurRiaziTaraz(avg) {
      const points = [
        { x: 0, y: 4300 },
        { x: 10, y: 6300 },
        { x: 20, y: 7600 },
        { x: 30, y: 8600 },
        { x: 40, y: 9500 },
        { x: 50, y: 10000 },
        { x: 60, y: 10800 },
        { x: 70, y: 11600 },
        { x: 80, y: 12400 },
        { x: 90, y: 13500 },
        { x: 100, y: 14500 }
      ];

      return interpolate(avg, points);
    }

    function calculateNohaeiTajrobiTaraz(avg) {
      const points = [
        { x: 10, y: 4400 },
        { x: 11, y: 4800 },
        { x: 12, y: 5200 },
        { x: 13, y: 5800 },
        { x: 14, y: 6200 },
        { x: 15, y: 6500 },
        { x: 16, y: 6900 },
        { x: 16.5, y: 7100 },
        { x: 17, y: 7400 },
        { x: 17.5, y: 7700 },
        { x: 18, y: 8100 },
        { x: 18.5, y: 8600 },
        { x: 19, y: 9200 },
        { x: 19.5, y: 10000 },
        { x: 19.75, y: 10700 },
        { x: 20, y: 12000 }
      ];

      return interpolate(avg, points);
    }

    function calculateNohaeiRiaziTaraz(avg) {
      const points = [
        { x: 10, y: 4800 },
        { x: 11, y: 5300 },
        { x: 12, y: 5600 },
        { x: 13, y: 6000 },
        { x: 14, y: 6400 },
        { x: 15, y: 6800 },
        { x: 16, y: 7200 },
        { x: 17, y: 7700 },
        { x: 18, y: 8400 },
        { x: 18.5, y: 9000 },
        { x: 19, y: 9600 },
        { x: 19.5, y: 10200 },
        { x: 19.75, y: 10600 },
        { x: 20, y: 12000 }
      ];

      return interpolate(avg, points);
    }

    function createTarazRange(centerTaraz) {
      const minTaraz = centerTaraz - 200;
      const maxTaraz = centerTaraz + 200;

      return {
        center: centerTaraz,
        min: minTaraz,
        max: maxTaraz,
        text: `${minTaraz.toLocaleString("fa-IR")} تا ${maxTaraz.toLocaleString("fa-IR")}`
      };
    }

    function processAndCalculate() {
      const phone = document.getElementById("user_phone").value.trim();
      const phoneRegex = /^(\+98|0)?9\d{9}$/;

      if (!phoneRegex.test(phone)) {
        showMessage("لطفاً یک شماره موبایل معتبر ۱۱ رقمی وارد کنید.");
        return;
      }

      let calculatedTaraz = 0;
      let calculatedAvg = 0;

      const payload = {
        action: selectedAction === "konkur"
          ? "takhmin_konkur"
          : "takhmin_nohaei",
        phone: phone,
        field: selectedField,
        scores: {},
        weighted_avg: "0",
        taraz: "",
        taraz_center: 0,
        taraz_min: 0,
        taraz_max: 0
      };

      if (selectedAction === "konkur") {
        if (selectedField === "riazi") {
          const riazi = parseFloat(document.getElementById("pr_riazi").value);
          const fizik = parseFloat(document.getElementById("pr_fizik").value);
          const shimi = parseFloat(document.getElementById("pr_shimi").value);

          const weightedSum =
            (riazi * 12) +
            (fizik * 9) +
            (shimi * 7);

          const totalWeight = 28;

          calculatedAvg = weightedSum / totalWeight;
          calculatedTaraz = calculateKonkurRiaziTaraz(calculatedAvg);

          payload.scores = {
            riazi,
            fizik,
            shimi
          };
        } else {
          const zist = parseFloat(document.getElementById("p_zist").value);
          const shimi = parseFloat(document.getElementById("p_shimi").value);
          const fizik = parseFloat(document.getElementById("p_fizik").value);
          const riazi = parseFloat(document.getElementById("p_riazi").value);
          const zamin = parseFloat(document.getElementById("p_zamin").value);

          const weightedSum =
            (zist * 12) +
            (shimi * 9) +
            (fizik * 7) +
            (riazi * 7) +
            (zamin * 1);

          const totalWeight = 36;

          calculatedAvg = weightedSum / totalWeight;
          calculatedTaraz = calculateKonkurTaraz(calculatedAvg);

          payload.scores = {
            zist,
            shimi,
            fizik,
            riazi,
            zamin
          };
        }
      } else {
        const farsi = parseFloat(document.getElementById("n_farsi").value);
        const arabi = parseFloat(document.getElementById("n_arabi").value);
        const dini = parseFloat(document.getElementById("n_dini").value);
        const zaban = parseFloat(document.getElementById("n_zaban").value);
        const salamat = parseFloat(document.getElementById("n_salamat").value);
        const ejtemai = parseFloat(document.getElementById("n_ejtemai").value);

        if (selectedField === "riazi") {
          const hesaban = parseFloat(document.getElementById("n_hesaban").value);
          const gosaste = parseFloat(document.getElementById("n_gosaste").value);
          const hendese = parseFloat(document.getElementById("n_hendese").value);
          const fizik = parseFloat(document.getElementById("n_fizik_riazi").value);
          const shimi = parseFloat(document.getElementById("n_shimi_riazi").value);

          const weightedSum =
            (farsi * 11.09) +
            (arabi * 4.64) +
            (dini * 8.47) +
            (zaban * 3.05) +
            (salamat * 1.76) +
            (ejtemai * 1.31) +
            (hesaban * 8.17) +
            (gosaste * 4.71) +
            (hendese * 5.49) +
            (shimi * 10.70) +
            (fizik * 10.70);

          const totalWeight = 70.09;

          calculatedAvg = weightedSum / totalWeight;
          calculatedTaraz = calculateNohaeiRiaziTaraz(calculatedAvg);

          payload.scores = {
            farsi,
            arabi,
            dini,
            zaban,
            salamat,
            ejtemai,
            hesaban,
            gosaste,
            hendese,
            fizik,
            shimi
          };
        } else {
          const zist = parseFloat(document.getElementById("n_zist").value);
          const riazi = parseFloat(document.getElementById("n_riazi").value);
          const fizik = parseFloat(document.getElementById("n_fizik").value);
          const shimi = parseFloat(document.getElementById("n_shimi").value);

          const weightedSum =
            (farsi * 11.09) +
            (arabi * 4.64) +
            (dini * 8.47) +
            (zaban * 6.05) +
            (salamat * 1.76) +
            (ejtemai * 1.31) +
            (zist * 10.66) +
            (riazi * 10.40) +
            (fizik * 9.26) +
            (shimi * 9.19);

          const totalWeight = 72.83;

          calculatedAvg = weightedSum / totalWeight;
          calculatedTaraz = calculateNohaeiTajrobiTaraz(calculatedAvg);

          payload.scores = {
            farsi,
            arabi,
            dini,
            zaban,
            salamat,
            ejtemai,
            zist,
            riazi,
            fizik,
            shimi
          };
        }
      }

      const tarazRange = createTarazRange(calculatedTaraz);

      payload.weighted_avg = calculatedAvg.toFixed(2);
      payload.taraz = tarazRange.text;
      payload.taraz_center = tarazRange.center;
      payload.taraz_min = tarazRange.min;
      payload.taraz_max = tarazRange.max;

      if (tg) {
        tg.sendData(JSON.stringify(payload));
      }

      closePhoneModal();

      document.getElementById("section-konkur").classList.add("hidden");
      document.getElementById("section-konkur-riazi").classList.add("hidden");
      document.getElementById("section-nohaei").classList.add("hidden");
      document.getElementById("section-result").classList.remove("hidden");

      const fieldName = selectedField === "riazi" ? "ریاضی" : "تجربی";

      if (selectedAction === "konkur") {
        document.getElementById("res-title").innerText =
          `🏆 بازه تراز تخمینی کنکور ${fieldName} شما`;

        document.getElementById("res-avg-container").innerHTML =
          `میانگین درصد وزنی: <b>${calculatedAvg.toFixed(2)}٪</b>`;
      } else {
        document.getElementById("res-title").innerText =
          `🏆 بازه تراز تخمینی امتحانات نهایی ${fieldName} شما`;

        document.getElementById("res-avg-container").innerHTML =
          `معدل کتبی موزون: <b>${calculatedAvg.toFixed(2)}</b>`;
      }

      document.getElementById("res-taraz").innerText = tarazRange.text;
    }

    function closeApp() {
      if (tg) {
        tg.close();
      }
    }
  </script>
</body>
</html>
