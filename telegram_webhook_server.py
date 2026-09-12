"""
سيرفر بسيط يستقبل تنبيهات TradingView (Webhook) ويرسلها لتيليجرام تلقائيًا.

طريقة الاستخدام:
1. عدّل قيم BOT_TOKEN و CHAT_ID تحت بمعلوماتك.
2. ارفع هذا الملف على Render.com (الخطوات بشرح منفصل).
3. في TradingView، عند إنشاء Alert، حط رابط السيرفر (اللي بيعطيك ياه Render)
   داخل خانة "Webhook URL" مع إضافة /webhook في الآخر.
   مثال: https://your-app-name.onrender.com/webhook
"""

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ==== عدّل هذي القيم بمعلوماتك ====
BOT_TOKEN = "8862091427:AAGRZZHM0woVG1E_RZA_4NX0HtSrrWk2cSQ"
CHAT_ID = "5384040099"
# ===================================

TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


@app.route("/webhook", methods=["POST"])
def webhook():
    # TradingView يرسل نص التنبيه كـ raw text أو JSON حسب إعداداتك
    try:
        data = request.get_json(silent=True)
        if data and isinstance(data, dict) and "text" in data:
            message = data["text"]
        else:
            # لو مو JSON، ناخذ النص الخام مباشرة
            message = request.data.decode("utf-8")
    except Exception as e:
        message = f"⚠️ خطأ بقراءة التنبيه: {e}"

    if not message:
        message = "تنبيه وصل بدون نص!"

    # إرسال الرسالة لتيليجرام
    try:
        resp = requests.post(
            TELEGRAM_URL,
            json={"chat_id": CHAT_ID, "text": message},
            timeout=10,
        )
        telegram_ok = resp.status_code == 200
    except Exception as e:
        telegram_ok = False
        print(f"خطأ إرسال تيليجرام: {e}")

    return jsonify({"received": True, "telegram_sent": telegram_ok}), 200


@app.route("/", methods=["GET"])
def health_check():
    # صفحة بسيطة للتأكد إن السيرفر شغال (تفتحها بالمتصفح)
    return "السيرفر شغال ✅", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
