from datetime import datetime, timedelta

def get_period_from_start(start=None, period=90):
    '''
    기준일로부터 일정기간 전의 날짜를 반환하는 함수
    get_period_from_start의 Docstring
    
    :param star: 시작시간
    :param period: 기간
    '''

    if start is None:
        date_2_obj = datetime.now()
    else:
        date_2_obj = datetime.strptime(start, '%Y%m%d')
    date_1_obj= date_2_obj - timedelta(days=period)
    # 2. yyyyMMdd 형태의 '문자열'로 변환 (중요!)
    date_1 = date_1_obj.strftime('%Y%m%d')
    date_2 = date_2_obj.strftime('%Y%m%d')
    return date_1, date_2