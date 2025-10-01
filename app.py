from flask import Flask,render_template

app = Flask(__name__)

# 只設定根目錄 "/"
@app.route("/")
def home():
    return render_template("index.html", title="首頁", message="Hello Flask!")

if __name__ == "__main__":
    app.run(debug=True)
