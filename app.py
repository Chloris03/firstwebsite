from flask import Flask, jsonify, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_folder="static", template_folder="templates")

# 用 dict 模擬資料庫
users = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username:
        return jsonify({"ok": False, "msg": "請輸入使用者名稱"}), 400
    if len(password) < 6:
        return jsonify({"ok": False, "msg": "密碼至少需 6 碼"}), 400
    if username in users:
        return jsonify({"ok": False, "msg": "使用者已存在"}), 409

    users[username] = {
        "password_hash": generate_password_hash(password),
        "failed": 0,
        "locked": False
    }
    return jsonify({"ok": True, "msg": "註冊成功"})

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    user = users.get(username)
    if not user:
        return jsonify({"ok": False, "msg": "帳號或密碼錯誤"}), 401

    if user["locked"]:
        return jsonify({"ok": False, "msg": "帳號已被鎖定"}), 423

    if check_password_hash(user["password_hash"], password):
        user["failed"] = 0
        return jsonify({"ok": True, "msg": "登入成功"})
    else:
        user["failed"] += 1
        if user["failed"] >= 3:
            user["locked"] = True
            return jsonify({"ok": False, "msg": "錯誤超過 3 次，帳號已鎖定"}), 423
        return jsonify({"ok": False, "msg": f"密碼錯誤，剩餘次數：{3 - user['failed']}"}), 401

if __name__ == "__main__":
    app.run(debug=True)

