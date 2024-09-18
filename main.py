import uvicorn

from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from CSV_FILES import CSV_FILES
from calculate_yield import calculate_yield

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# API routes
api_router = APIRouter()

class YieldParams(BaseModel):
    price_csv: str
    num_loans_per_day: int
    avg_initial_collateral_ratio: float
    min_collateral_ratio: float
    origination_fee_pct: float
    liquidation_spread_pct: float
    avg_repayment_days: int
    avg_slippage_pct: float
    avg_loan_amount: float

@api_router.get("/available_crypto")
async def get_available_crypto():
    """
    Returns a list of available cryptocurrencies that can be used for yield calculation.
    """
    return {
        "available_crypto": list(CSV_FILES.keys())
    }

@api_router.post("/calculate_yield")
async def api_calculate_yield(params: YieldParams):
    if params.price_csv not in CSV_FILES:
        raise HTTPException(status_code=400, detail="Invalid cryptocurrency choice")

    price_csv = CSV_FILES[params.price_csv]

    try:
        result = calculate_yield(
            price_csv,
            params.num_loans_per_day,
            params.avg_initial_collateral_ratio,
            params.min_collateral_ratio,
            params.origination_fee_pct,
            params.liquidation_spread_pct,
            params.avg_repayment_days,
            params.avg_slippage_pct,
            params.avg_loan_amount
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.include_router(api_router, prefix="/api")

@app.get("/")
@app.get("/index.html")
async def read_index():
    return FileResponse('static/index.html')

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
