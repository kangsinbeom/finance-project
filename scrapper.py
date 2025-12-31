import pandas as pd
import FinanceDataReader as fdr 
from datetime import datetime, timedelta
from kis_apis import fetch_daily_price
from time_cal import get_period_from_start

# KRX 상장 종목 코드 가져오기
def get_stock_code():
    '''
    KRX에 상장된 모든 종목의 코드를 가져와서 리스트로 반환하는 함수
    '''
    print('getting stock codes from KRX...')
    df_krx = fdr.StockListing('KRX')
    
    # 상장상태가 '정상'이고, 우리가 흔히 아는 KOSPI, KOSDAQ 종목만 필터링
    # (우선주나 특수 종목을 제외하고 싶을 때 유용)
    df_krx = df_krx[df_krx['Market'].isin(['KOSPI', 'KOSDAQ'])]
    
    codes = df_krx['Code'].tolist()
    print('종목 가져오기 끝')
    return codes


# 특정 종목의 가격 데이터를 데이터프레임으로 가져오는 함수
def get_stock_price_to_data_frame(code, period=90, access_token=""):
    '''
    특정 종목의 가격 데이터를 데이터프레임으로 가져오는 함수
    - end_date: 데이터를 가져올 끝 날짜. 기본값은 오늘(now).
    - period: end_date로부터 거꾸로 계산할 일수 (기본값 180일)
    '''
    date_1, date_2= get_period_from_start(period=90)
    
    res_data = fetch_daily_price(access_token, code, date_1, date_2)
    if "output2" in res_data and res_data["output2"]:
        df_price = pd.DataFrame(res_data["output2"])
        
        # 4. 컬럼명 변경 및 전처리 (fdr 형식과 일치시킴)
        # stck_bsop_date: 영업일자, stck_clpr: 주식 종가
        df_price = df_price[['stck_bsop_date', 'stck_clpr']].rename(columns={
            'stck_bsop_date': 'Date',
            'stck_clpr': 'Close'
        })
        
        # 5. 데이터 타입 변환 (문자열 -> 날짜/숫자)
        df_price['Date'] = pd.to_datetime(df_price['Date'])
        df_price['Close'] = pd.to_numeric(df_price['Close'])
        
        # 6. 정렬 (KIS는 최신순으로 주므로 과거순으로 정렬)
        df_price = df_price.sort_values(by='Date').reset_index(drop=True)
        
        return df_price[['Date', 'Close']]
    
    else:
        # 에러 메시지 출력 (KIS API가 반환한 에러 메시지 확인)
        msg = res_data.get('msg1', '데이터 없음')
        print(f'❌ 데이터 가져오기 실패: {msg}')
        return pd.DataFrame() # 빈 데이터프레임 반환

# 상관계수가 0.5 이상인 우상향 종목 필터링 함수
def filter_uptrend_stocks(codeList, aceess_token=""):
    '''
    상관관계 계수를 0.5이상 유지하고 있는 주식들을 필터링하는 함수
    에러가 발생하는 종목은 건너뜁니다.
    '''
    uptrend_stocks = []    
    
    print('Filtering uptrend stocks...')    
    
    for code in codeList:
        
        try:
            # 에러가 발생할 가능성이 있는 구간 시작
            df = get_stock_price_to_data_frame(code, access_token=aceess_token)
            
            if df is None or df.empty:
                continue
            
            df['Time'] = range(len(df))
            
            # 상관계수 계산
            correlation_matrix = df[['Time', 'Close']].corr()
            corr_value = correlation_matrix.loc['Time', 'Close']
            
            if corr_value >= 0.5:
                uptrend_stocks.append(code)
            # 에러가 발생할 가능성이 있는 구간 끝
            return
        except Exception as e:
            # 404 에러 등이 발생하면 이쪽으로 들어옵니다.
            print(f"⚠️ {code} 데이터를 가져올 수 없습니다. (건너뜀)")
            continue
            
    print('우상향 종목 필터링 완료.')
    return uptrend_stocks
