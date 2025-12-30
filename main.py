import pandas as pd
import FinanceDataReader as fdr 
from datetime import datetime, timedelta

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
    return codes


# 특정 종목의 가격 데이터를 데이터프레임으로 가져오는 함수
def get_stock_price_frame(code, end_date=None, period=180):
    '''
    특정 종목의 가격 데이터를 데이터프레임으로 가져오는 함수
    - end_date: 데이터를 가져올 끝 날짜. 기본값은 오늘(now).
    - period: end_date로부터 거꾸로 계산할 일수 (기본값 180일)
    '''
    
    if end_date is None:
        end_obj = datetime.now()
    else:
        end_obj = datetime.strptime(end_date, '%Y-%m-%d')    
    start_obj = end_obj - timedelta(days=period)

    final_end = end_obj.strftime('%Y-%m-%d')
    final_start = start_obj.strftime('%Y-%m-%d')

    print(f'🚀 {code} 수집 기간: {final_start} ~ {final_end} ({period}일간)')
    df_price = fdr.DataReader(code, start=final_start, end=final_end)

    # 데이터프레임이 비어있지 않으면 날짜와 종가 컬럼만 반환
    if not df_price.empty:
        return df_price.reset_index()[['Date', 'Close']]
    print('데이터 프레임 가져오기 완료')
    return df_price

# 상관계수가 0.5 이상인 우상향 종목 필터링 함수
def filter_uptrend_stocks(codeList):
    '''
    상관관계 계수를 0.5이상 유지하고 있는 주식들을 필터링하는 함수
    에러가 발생하는 종목은 건너뜁니다.
    '''
    uptrend_stocks = []    
    
    print('Filtering uptrend stocks...')    
    for code in codeList:
        try:
            # 에러가 발생할 가능성이 있는 구간 시작
            df = get_stock_price_frame(code)
            
            if df is None or df.empty:
                continue
            
            df['Time'] = range(len(df))
            
            # 상관계수 계산
            correlation_matrix = df[['Time', 'Close']].corr()
            corr_value = correlation_matrix.loc['Time', 'Close']
            
            print(f"📈 {code}의 상관계수: {corr_value:.4f}")
            
            if corr_value >= 0.5:
                print(f"✅ {code}는 우상향 종목입니다!")
                uptrend_stocks.append(code)
            # 에러가 발생할 가능성이 있는 구간 끝

        except Exception as e:
            # 404 에러 등이 발생하면 이쪽으로 들어옵니다.
            print(f"⚠️ {code} 데이터를 가져올 수 없습니다. (건너뜀)")
            continue
            
    print('우상향 종목 필터링 완료.')
    return uptrend_stocks


codeList = get_stock_code()
uptend_stock = filter_uptrend_stocks(codeList)
print('우상향 종목 리스트:', uptend_stock)