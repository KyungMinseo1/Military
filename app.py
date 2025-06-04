from flask import Flask, render_template, request, redirect, url_for
from src.reserve import Reserve
import pickle

app = Flask(__name__)
app.secret_key = '19756451'

# 파일 불러오기
with open('data/student_data.pickle', 'rb') as fr:
    student_data = pickle.load(fr)
with open('data/military_data.pickle', 'rb') as fr:
    military_data = pickle.load(fr)
with open('data/s_list.pickle', 'rb') as fr:
    s_list = pickle.load(fr)

# 예비군 클래스 불러오기
reserve = Reserve(s_list)

# 예비군 데이터 자동 생성
reserve.create(student_data, military_data)

@app.route('/', methods = ['GET'])
def home():
    return render_template('home.html')

@app.route('/retrieve', methods = ['GET', 'POST'])
def retrieve():
    data = 0
    if request.method == "POST":
        retrieve_type = request.form.get("search_type")
        search_value = request.form.get("search_value")
        if retrieve_type == "s_info":
            data = reserve.retrieve(search_value, is_filter=False)
        elif retrieve_type == "filter":
            data = reserve.retrieve(is_filter=True)
    return render_template('retrieve.html', results=data)

@app.route('/update', methods = ['GET', 'POST'])
def update():
    return render_template('update.html')

@app.route('/delete', methods = ['GET', 'POST'])
def delete():
    return render_template('delete.html')

@app.route('/print', methods = ['GET', 'POST'])
def print():
    return render_template('print.html')

if __name__ == "__main__":
    app.run(debug=True)

