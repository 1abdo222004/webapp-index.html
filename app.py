from flask import Flask, request, jsonify, render_template

app = Flask(name)


saved_data = {}

@app.route('/') def index(): return render_template('index.html')

@app.route('/id', methods=['POST']) def receive_data(): data = request.get_json() init_data = data.get('initData')

# استخراج user id إن وجد من initData (بشكل مبسط)
user_id = None
if init_data:
    import re
    match = re.search(r'id%22%3A(\d+)', init_data)
    if match:
        user_id = match.group(1)
        saved_data[user_id] = {
            'initData': init_data
        }

return 'تم حفظ البيانات' if user_id else 'لم يتم العثور على user_id'

@app.route('/idinfo') def get_info(): user_id = request.args.get('id') if user_id in saved_data: return jsonify(saved_data[user_id]) return 'لا توجد بيانات لهذا المعرف', 404

if name == 'main': app.run(host='0.0.0.0', port=5000, debug=True)

