from fastapi import FastAPI ## FastAPI 앱 객체 생성. 
from app.routers import analyze

app = FastAPI(title="Job Agent")

app.include_router(analyze.router, prefix="/api") ## 라우터 등록


@app.get("/") ##  서버 주소 들어갔을 때 잘 돌아가는지 확인
def root():
    return {"status": "running"}