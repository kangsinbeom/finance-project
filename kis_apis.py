import requests

# config.py가 같은 폴더에 있다고 가정
from config import KIS_APP_KEY, KIS_APP_SECRET, KIS_BASE_URL

def fetch_daily_price(access_token: str , code: str, date_1: str, date_2:str):
    '''
    fetch_daily_price의 Docstring
    기간 내의 시세를 가져오는 Fetch 함수
    '''
    
    url = f"{KIS_BASE_URL}/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
    
    headers = {
        'content-type': 'application/json; charset=utf-8',
        'authorization': access_token,
        'appkey': KIS_APP_KEY,
        'appsecret': KIS_APP_SECRET,
        'tr_id': 'FHKST03010100',
        'custtype': "P",
    }
    params = {
        "FID_COND_MRKT_DIV_CODE": "J",
        "FID_INPUT_ISCD": code,
        "FID_INPUT_DATE_1": date_1,
        "FID_INPUT_DATE_2": date_2,
        "FID_PERIOD_DIV_CODE": "D",
        "FID_ORG_ADJ_PRC": "1"
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()