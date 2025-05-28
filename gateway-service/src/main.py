from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
import logging
from typing import Dict

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="API Gateway")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 服务路由配置
SERVICE_ROUTES: Dict[str, str] = {
    "auth": "http://localhost:8101",
    "user": "http://localhost:8102",
    "agent": "http://localhost:8103",
    "knowledge": "http://localhost:8104",
    "frontend": "http://localhost:8105"
}

@app.middleware("http")
async def route_middleware(request: Request, call_next):
    path = request.url.path
    service = path.split("/")[1] if len(path.split("/")) > 1 else "frontend"
    
    if service in SERVICE_ROUTES:
        target_url = f"{SERVICE_ROUTES[service]}{path}"
        logger.info(f"Routing request to {target_url}")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method=request.method,
                    url=target_url,
                    headers=dict(request.headers),
                    content=await request.body()
                )
                return response
        except Exception as e:
            logger.error(f"Error routing request to {service}: {str(e)}")
            return {"error": f"Service {service} is not available"}
    
    return await call_next(request)

@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy"}

@app.get("/")
async def root():
    """根路径重定向到API文档"""
    return {"message": "Welcome to the API Gateway", "docs_url": "/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8100) 