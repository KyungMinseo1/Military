from datetime import datetime
from typing import Optional, Tuple, Any, List

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
    
    def binary_search(self, target, start, end, find_insert_pos=False) -> Optional[Tuple[int, Any]]:
        '''
        이진 탐색 메소드
        '''
        if end < start:
            if find_insert_pos:
                return (start, None)  # 삽입 위치 반환
            return None
        mid = (start + end)//2
        mid_data = self.data[mid]
        if mid_data[0] == target:       # 찾으려는 학번과 일치한다면
            if find_insert_pos:
                return None
            return (mid, mid_data)      # 해당 데이터와 인덱스 번호 추출
        elif mid_data[0] > target:
            return self.binary_search(target, start, mid-1, find_insert_pos)
        elif mid_data[0] < target:
            return self.binary_search(target, mid+1, end, find_insert_pos)

    def init_create(self, student_data: dict, military_data: dict) -> None:
        '''
        학생정보와 군정보를 받아 첫 예비군 데이터를 생성하는 함수\n 
        학생정보와 군정보는 여러 학생 정보가 담긴 딕셔너리 형태  
        '''
        for s_num, s_data in student_data.items():

            temp_data = []                          # 정보저장을 위한 임시 리스트

            if s_data[2] == 1:                      # 학생이 여자이면 추가 X
                continue

            if s_num in self.s_list.keys():         # 학번을 통해 군번 연결 (학번에 해당하는 군번이 존재하지 않을 경우 건너뛰기)
                m_num = self.s_list[s_num]
                temp_data.append(s_num)             # 임시 데이터에 학번 추가
                temp_data.append(m_num)             # 임시 데이터에 군번 추가
                temp_data.append(s_data[0])             # 임시 데이터에 이름 추가
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
            temp_data.append(0)                     # 예비군 훈련 시간(처음 생성 시 0으로 초기화)
            temp_data.append(6)                     # 훈련 연기 가능 횟수(처음 생성 시 6으로 초기화)
            temp_data.append(0)                     # 조기 퇴소 횟수(처음 생성 시 0으로 초기화)

            self.data.append(temp_data)             # 임시 데이터를 최종 데이터에 추가
            self.data.sort(key = lambda x : x[0])   # 효율적인 검색/업데이트를 위한 정렬

    def create(self, student_data: dict, military_data: dict) -> Optional[List]:
        '''
        학생정보와 군정보를 받아 새로운 예비군 데이터를 생성하는 함수\n 
        학생정보와 군정보는 하나의 학생 정보가 담긴 딕셔너리 형태(개별 생성)  
        '''
        s_num, s_data = list(student_data.items())[0]
        m_num, m_data = list(military_data.items())[0]

        temp_data = []                          # 정보저장을 위한 임시 리스트

        if s_data[2] == 1:                      # 학생이 여자이면 추가 X
            return None

        temp_data.append(s_num)                 # 임시 데이터에 학번 추가
        temp_data.append(m_num)                 # 임시 데이터에 군번 추가
        temp_data.append(s_data[0])             # 임시 데이터에 이름 추가

        is_available = self.is_available(s_data[3], s_data[4], s_data[5])   # 예비군 훈련 가능여부 판단
        temp_data.append(is_available)          # 예비군 훈련 가능여부 추가

        out_date = m_data[4]                    # 전역일 데이터 추출
        out_year = int(out_date.split('-')[0])  # 전역년도 추출
        current_year = datetime.today().year    # 현재년도 추출
        reserve_year = current_year - out_year  # 예비군 복무연차 계산 (현재년도 - 전역년도)
        temp_data.append(reserve_year)          # 예비군 복무연차 추가

        temp_data.append(0)                     # 예비군 훈련 횟수(처음 생성 시 0으로 초기화)
        temp_data.append(0)                     # 예비군 훈련 시간(처음 생성 시 0으로 초기화)
        temp_data.append(6)                     # 훈련 연기 가능 횟수(처음 생성 시 6으로 초기화)
        temp_data.append(0)                     # 조기 퇴소 횟수(처음 생성 시 0으로 초기화)

        result = self.binary_search(s_num, 0, len(self.data)-1, find_insert_pos=True)
        if result:
            insert_pos, _ = result
        else:
            insert_pos = len(self.data)
            
        self.data.insert(insert_pos, temp_data) # 임시 데이터를 최종 데이터에 추가(정렬 형식에 맞추어서 추가)
       
        return [temp_data]

    def retrieve(self, value = None, is_filter = False) -> Optional[List]:
        '''
        데이터를 검색하기 위한 함수\n
        is_filter가 True이면 이번학기에 예비군 훈련이 가능한 학생 필터링\n
        is_filter가 False이면 학번으로 특정 학생의 예비군 정보 검색  
        '''
        found_data = []
        if is_filter:                               # 필터링 적용
            for data in self.data:
                if data[3] == 1:
                    found_data.append(data)
        else:                                       # 특정 학생 검색
            s_num = value
            result = self.binary_search(s_num, 0, len(self.data)-1)
            if result:
                _, data = result
            found_data.append(data)
        return found_data
    
    def update_after_train(self, update_list: list) -> Optional[List]:
        '''
        예비군 수료 정보 업데이트 함수\n
        업데이트 대상이 되는 예비군 수료 정보는\n
        [학번, 예비군 훈련 여부, 훈련 시간, 훈련 연기 여부, 조기퇴소 여부] 라고 가정\n
        이진 탐색으로 학번에 해당하는 데이터를 찾은 뒤, 정보 업데이트
        '''
        return_data = []
        for update_data in update_list:
            result = self.binary_search(update_data[0], 0, len(self.data)-1)
            if result:
                idx, data = result
            else:
                continue
            data[5] += update_data[1]               # 예비군 훈련 여부 업데이트
            data[6] += update_data[2]               # 예비군 훈련 시간 업데이트
            data[7] -= update_data[3]               # 예비군 훈련 연기 여부 업데이트
            data[8] += update_data[4]               # 예비군 조기퇴소 여부 업데이트
            self.data[idx] = data
            return_data.append(data)
        return return_data

    def update_is_available(self, student_data : dict) -> Optional[List]:
        '''
        학생정보가 수정되었을 때, 업데이트 함수\n
        교환/유학 여부 수정 시 업데이트\n
        학생정보는 동일하게 dict 형식으로 받음
        '''
        return_data = []
        for s_num, s_data in student_data.items():
            is_available = self.is_available(s_data[3], s_data[4], s_data[5])
            result = self.binary_search(s_num, 0, len(self.data)-1)
            if result:
                idx, data = result
            data[3] = is_available
            self.data[idx] = data
            return_data.append(data)
        return return_data