from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, List
import json
import logging
import httpx
from .manager import AgentManager
from .websocket import ConnectionManager

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Agent Service")

# 初始化管理器
agent_manager = AgentManager()
connection_manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await connection_manager.connect(websocket, client_id)
    try:
        while True:
            # 接收消息
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # 处理消息
            target_agent = message.get("agent", "default")
            user_message = message.get("message")
            
            if not user_message:
                await connection_manager.send_message(
                    client_id,
                    {"type": "error", "content": "Message cannot be empty"}
                )
                continue
            
            # 获取知识库信息
            async with httpx.AsyncClient() as client:
                knowledge = await client.get(
                    f"http://knowledge-service/knowledge/search",
                    params={"query": user_message}
                )
            
            # 获取工具
            tools = []
            if "tools" in message:
                async with httpx.AsyncClient() as client:
                    for tool_name in message["tools"]:
                        tool = await client.get(
                            f"http://tool-service/tools/{tool_name}"
                        )
                        tools.append(tool.json())
            
            # 处理消息
            response = await agent_manager.process_message(
                client_id=client_id,
                message=user_message,
                agent=target_agent,
                knowledge=knowledge.json(),
                tools=tools
            )
            
            # 发送响应
            await connection_manager.send_message(
                client_id,
                {"type": "response", "content": response}
            )
            
    except WebSocketDisconnect:
        connection_manager.disconnect(client_id)
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        await connection_manager.send_message(
            client_id,
            {"type": "error", "content": f"Error: {str(e)}"}
        )
        connection_manager.disconnect(client_id)

@app.get("/agents")
async def list_agents():
    """获取所有可用的Agent"""
    return {
        "success": True,
        "agents": agent_manager.list_agents()
    }

@app.post("/agents/{agent_name}/clear")
async def clear_agent_memory(agent_name: str):
    """清空指定Agent的记忆"""
    success = agent_manager.clear_agent_memory(agent_name)
    if not success:
        return {"success": False, "error": "Agent not found"}
    return {"success": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003) 