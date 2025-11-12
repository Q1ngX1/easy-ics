from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.api import router

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title="Easy ICS API",
    description="图片/文字生成 ICS 日历文件的 API 服务",
    version="0.1.0"
)

# 配置 CORS（允许前端跨域访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应设置具体的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def read_root():
    return {
        "message": "Easy ICS API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health"
    }


def main():
    pass


if __name__ == "__main__":
    main()
