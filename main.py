from fastapi import FastAPI, HTTPException, Header
import json
from core.scrapper import get_stock_code, filter_uptrend_stocks
app = FastAPI()

@app.get("/stock/recommend")
async def get_recommend_stocks(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    print('추천 종목 뽑기 시작!!')
    # codes = get_stock_code()  # Assume this function is defined elsewhere
    filter_uptrend_stocks(['005930'], aceess_token=authorization)
    return {
        'status': "success",
        'data': {
            "recommend_stocks": 'asdf'
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
