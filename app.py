from flask import Flask, render_template

app = Flask(__name__)  # 如果你用的是 statics 資料夾，見下方第 3 點的設定

@app.route("/")
def home():
    returndex.html",
        title="簡約灰色系網站",
        heading="歡迎來到我的網站",
        content= render_template(
        "in"這是一個簡約但有內容的灰色系設計。"
    )

if __name__ == "__main__":
    app.run(debug=True)
