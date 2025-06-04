from datetime import datetime

class Reserve:
    def __init__(self, s_list: dict):
        '''
        학번과 군번이 서로 매핑된 데이터를 가지고 있다고 가정 (이를 통해 학생정보와 군정보를 연계)  
        '''
        self.data = []
        self.s_list = s_list  # {학번 : 군번}

    def is_available(self, x, y, z) -> int:
        '''
        군복무 가능여부를 판단하기 위한 함수  
        '''
        return x*y*z

    def create(self, student_data: dict, military_data: dict) -> None:
        '''
        학생정보와 군정보를 받아 예비군 데이터를 생성하는 함수\n 
        학생정보와 군정보는 여러 학생 정보가 담긴 딕셔너리 형태  
        '''
        for s_num, s_data in student_data.items():

            temp_data = []                          # 정보저장을 위한 임시 리스트

            if s_num in self.s_list.keys():         # 학번을 통해 군번 연결 (학번에 해당하는 군번이 존재하지 않을 경우 건너뛰기)
                m_num = self.s_list[s_num]
                temp_data.append(s_num)             # 임시 데이터에 학번 추가
                temp_data.append(m_num)             # 임시 데이터에 군번 추가
            else:
                continue

            is_available = self.is_available(s_data[3], s_data[4], s_data[5])   # 예비군 훈련 가능여부 판단
            temp_data.append(is_available)          # 예비군 훈련 가능여부 추가

            m_data = military_data[m_num]           # 연결된 군번에 해당하는 데이터 추출
            out_date = m_data[4]                    # 전역일 데이터 추출
            out_year = int(out_date.split('-')[0])  # 전역년도 추출
            current_year = datetime.today().year    # 현재년도 추출
            reserve_year = current_year - out_year  # 예비군 복무연차 계산 (현재년도 - 전역년도)
            temp_data.append(reserve_year)          # 예비군 복무연차 추가

            temp_data.append(0)                     # 예비군 훈련 횟수(처음 생성 시 0으로 초기화)
            temp_data.append(6)                     # 훈련 연기 가능 횟수(처음 생성 시 6으로 초기화)
            temp_data.append(0)                     # 조기 퇴소 횟수(처음 생성 시 0으로 초기화)

            self.data.append(temp_data)             # 임시 데이터를 최종 데이터에 추가

    def retrieve(self, value = None, is_filter = False) -> list:
        '''
        데이터를 검색하기 위한 함수\n
        is_filter가 True이면 이번학기에 예비군 훈련이 가능한 학생 필터링\n
        is_filter가 False이면 학번으로 특정 학생의 예비군 정보 검색  
        '''
        found_data = []
        if is_filter:                               # 필터링 적용
            for data in self.data:
                if data[2] == 1:
                    found_data.append(data)
        else:                                       # 특정 학생 검색
            s_num = value
            for data in self.data:
                if data[0] == s_num:
                    found_data.append(data)
                    break
        return found_data