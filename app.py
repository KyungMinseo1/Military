from flask import Flask, render_template, request, redirect, url_for
from src.reserve import Reserve
import pickle

app = Flask(__name__)
app.secret_key = '19756451'

# 파일 불러오기
with open('data/student_data.pickle', 'rb') as fr:
    global_student_data = pickle.load(fr)
with open('data/military_data.pickle', 'rb') as fr:
    global_military_data = pickle.load(fr)
with open('data/s_list.pickle', 'rb') as fr:
    s_list = pickle.load(fr)

# 예비군 클래스 불러오기
reserve = Reserve(s_list)

# 예비군 데이터 자동 생성
reserve.init_create(global_student_data, global_military_data)

@app.route('/', methods = ['GET'])
def home():
    return render_template('home.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    data = 0
    if request.method == "POST":
        result = request.form.to_dict()
        s_result = {k: int(v) if isinstance(v, (int, str)) and str(v).isdigit() else v
                    for k, v in result.items() if k.startswith('s_')}
        m_result = {k: int(v) if isinstance(v, (int, str)) and str(v).isdigit() else v
                    for k, v in result.items() if k.startswith('m_')}
        student_data = {
            str(s_result['s_num']): list(s_result.values())[1:]
        }
        global_student_data[str(s_result['s_num'])] = list(s_result.values())[1:]
        military_data = {
            m_result['m_num']: list(m_result.values())[1:]
        }
        global_military_data[m_result['m_num']] = list(m_result.values())[1:]
        data = reserve.create(student_data, military_data)
        if data:
            return render_template('create.html', results=data)
    return render_template('create.html', results=data)

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
    return render_template('retrieve.html', results=data)

@app.route('/update', methods = ['GET', 'POST'])
def update():
    data = None
    if request.method == "POST":
        reset = request.form.get("action")
        if reset:
            return render_template('update.html', results=0, founds=0, error=0)
        form_type = request.form.get("form_type")
        if form_type == "military_update":
            # HTML에서 name="m_num", name="m_name" 등으로 전송된 데이터 처리
            s_nums = request.form.getlist("s_num")
            m_trains = request.form.getlist("m_train")
            m_times = request.form.getlist("m_time")
            m_delays = request.form.getlist("m_delay")
            m_leaves = request.form.getlist("m_leave")
            
            update_list = []
            # 모든 폼의 데이터를 순서대로 묶어서 처리
            for i in range(len(s_nums)):
                entry = [
                    s_nums[i], int(m_trains[i]), int(m_times[i]), int(m_delays[i]), int(m_leaves[i])
                    ]
                update_list.append(entry)
            data = reserve.update_after_train(update_list)
            return render_template('update.html', results=data, founds=0, error=0)
        
        elif form_type == "student":
            # 학번 리스트로 학생 정보 조회
            s_nums = request.form.getlist("s_num[]")
            found_students = []
            
            for s_num in s_nums:
                if s_num in global_student_data:
                    student_info = global_student_data[s_num]
                    # 학번을 포함한 학생 정보 추가 (업데이트 시 학번 식별용)
                    student_with_snum = [s_num] + list(student_info)
                    found_students.append(student_with_snum)
                else:
                    return render_template('update.html', results=0, founds=0, error=1)
            
            return render_template('update.html', results=0, founds=found_students, error=0)
        
        elif form_type == "student_update":
            total_str = request.form.get("total")
            if not total_str:
                return render_template('update.html', results=0, founds=0, error=1)
            
            total = int(total_str)
            update_dict = {}
            
            for i in range(total):
                # 각 학생의 학번을 키로 사용
                s_num = request.form.get(f"s_num_{i}")
                name = request.form.get(f"name_{i}")
                age_str = request.form.get(f"age_{i}")
                gender = request.form.get(f"gender_{i}")
                exchange_str = request.form.get(f"exchange_{i}")
                rest_str = request.form.get(f"rest_{i}")
                train_str = request.form.get(f"train_{i}")
                semester_str = request.form.get(f"semester_{i}")
                
                # None 체크 및 안전한 변환
                if not all([s_num, name, age_str, gender, exchange_str, rest_str, train_str, semester_str]):
                    continue  # 필수 데이터가 없으면 스킵
                
                try:
                    update_dict[s_num] = [
                        name, int(age_str), gender, int(exchange_str), int(rest_str), int(train_str), int(semester_str)
                        ]
                except (ValueError, TypeError):
                    continue  # 변환 실패 시 스킵
            
            # 학생 정보 업데이트
            if update_dict:
                result = reserve.update_is_available(update_dict)
            return render_template('update.html', results=result, founds=0, error=0)  # 성공 메시지 표시

    return render_template('update.html', results=data, founds=data, error=0)

@app.route('/delete', methods = ['GET', 'POST'])
def delete():
    data = None
    if request.method == "POST":
        reset = request.form.get("action")
        if reset:
            return render_template('delete.html', results=0, error=0)
        form_type = request.form.get("form_type")
        if form_type == "auto_delete":
            data = reserve.delete_auto(global_student_data)
            if data == []:
                return render_template('delete.html', results=0, error=1)
            else:
                return render_template('delete.html', results=data, error=0)
        
        elif form_type == "student":
            # 학번 리스트로 학생 정보 조회
            s_nums = request.form.getlist("s_num[]")
            data = reserve.delete_manual(s_nums)
            if data == []:
                return render_template('delete.html', results=0, error=1)
            else:
                return render_template('delete.html', results=data, error=0)
    return render_template('delete.html', results=data, error=0)

@app.route('/print', methods = ['GET', 'POST'])
def print():
    data = reserve.data
    return render_template('print.html', results=data)

if __name__ == "__main__":
    app.run(debug=True)

