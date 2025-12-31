from fastapi import FastAPI, HTTPException, Header
from scrapper import get_stock_code, filter_uptrend_stocks

app = FastAPI()

@app.get("/stock/recommend")
async def get_recommend_stocks(authorization: str = Header(None)):
    
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    codes = get_stock_code()  # Assume this function is defined elsewhere
    respose = filter_uptrend_stocks(codes, aceess_token=authorization)
    return {
        'status': "success",
        'data': {
            "recommend_stocks": respose
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
