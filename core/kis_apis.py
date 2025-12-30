import requests
from config import KIS_APP_KEY, KIS_APP_SECRET, KIS_BASE_URL


def fetch_daily_price(access_token: str,code: str, date_1: str, date_2: str):
    '''KIS API를 통해서 특정 종목의 일별 가격 데이터를 가져오는 함수'''
    url = f"{KIS_BASE_URL}/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
    print(access_token, ';;;;', code, date_1, date_2,'종료일')
    
    headers = {
        'Content-type': 'application/json; charset=utf-8',
        'authorization': access_token,
        'appkey': KIS_APP_KEY,
        'appsecret': KIS_APP_SECRET,
        'tr_id': 'FHKST03010100',
        'custtype': "P", # 개인: 'P', 법인: 'B'
    }
    
    params = {
        "FID_COND_SCR_DIV_CODE": "J",  # 업종/종목 구분 (보통 J)
        "FID_INPUT_ISCD": code,        # 종목코드 (예: "005930")
        "FID_INPUT_DATE_1": date_1,    # 시작일 (YYYYMMDD)
        "FID_INPUT_DATE_2": date_2,    # 종료일 (YYYYMMDD)
        "FID_PERIOD_DIV_CODE": "D",    # D:일, W:주, M:월
        "FID_ORG_ADJ_PRC": "1"         # 0:수정주가 미반영, 1:수정주가 반영
    }

    try: 
        response = requests.get(url, headers=headers, params=params)
    except Exception as e:
        print(f"Error fetching data for {code}: {e}")
        return None
    print(response.json())
    
    return response.json()
    