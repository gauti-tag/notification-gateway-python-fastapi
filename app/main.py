from fastapi import FastAPI, BackgroundTasks, Request, Form
from fastapi.middleware.cors import CORSMiddleware 
from typing import Optional, Annotated
from pydantic import BaseModel
from httpx import AsyncClient, RequestError, TimeoutException
from starlette import status
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
from datetime import datetime


class NotificationRequest(BaseModel):
    url: str
    order_id: Optional[str] = None
    status_id: Optional[int] = None
    transaction_id: Optional[str] = None
    transaction_amount: Optional[str] = None
    currency: Optional[str] = None
    paid_transaction_amount: Optional[str] = None
    paid_currency: Optional[str] = None
    change_rate: Optional[float] = None
    conflictual_transaction_amount: Optional[str] = None
    conflictual_currency: Optional[str] = None
    wallet: Optional[str] = None
    phone_number: Optional[str] = None
    momo_reference_id: Optional[str] = None
    wallet_alias: Optional[str] = None
    wallet_name: Optional[str] = None
    receipt_generator_url: Optional[str] = None
    cancellation: bool

app = FastAPI()

origins = ["http://0.0.0.0:8080","http://localhost:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return JSONResponse(
            status_code = 404,
            content = {"detail": "Resource not found"},
        )
    return JSONResponse(
        status_code = exc.status_code,
        content = {"detail": exc.detail},
    )



async def send_notifiation(request: NotificationRequest):
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    url = request.url
    data = request.model_dump()
    data.pop('url')
    print(f"[{datetime.now()}] URL => {url} \n[{datetime.now()}] PARAMS SENT => {data} \n")
    
    try:
        async with AsyncClient(timeout=30.0) as client: 
            response = await client.post(url, headers = headers, data = data )
            print(f"[{datetime.now()}] RESPONSE => #{response.json()}")
    except TimeoutException:
        print(f"[{datetime.now()}] RESPONSE TO {url} TIMED OUT.")
    except RequestError as e:
        print(f"[{datetime.now()}] An error occurred while making the request: {e}")
    
    
@app.post("/", status_code = status.HTTP_202_ACCEPTED )
async def root(request: Annotated[NotificationRequest, Form()], background_tasks: BackgroundTasks):
    background_tasks.add_task(send_notifiation, request)
    return {"status": 200,"message": "Notification Sent"}
    
    