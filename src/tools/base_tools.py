from typing import Any, Dict, List, Optional
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
import requests
from datetime import datetime
import json
import os
from src.knowledge_base.vector_store import KnowledgeBase

class SearchTool(BaseTool):
    name: str = "search_knowledge_base"
    description: str = "搜索知识库中的信息。输入应该是一个搜索查询。"
    knowledge_base: KnowledgeBase = Field(description="知识库实例")
    
    def __init__(self, knowledge_base: KnowledgeBase):
        super().__init__(knowledge_base=knowledge_base)
    
    def _run(self, query: str) -> str:
        """执行知识库搜索"""
        results = self.knowledge_base.search(query)
        if not results:
            return "在知识库中没有找到相关信息。"
        
        response = "找到以下相关信息：\n\n"
        for i, result in enumerate(results, 1):
            response += f"{i}. 内容：{result['content']}\n"
            response += f"   来源：{result['metadata'].get('source', '未知')}\n"
            response += f"   相关度：{result['score']:.2f}\n\n"
        return response
    
    async def _arun(self, query: str) -> str:
        """异步执行知识库搜索"""
        return self._run(query)

class CalculatorTool(BaseTool):
    name: str = "calculator"
    description: str = "执行数学计算。输入应该是一个数学表达式，例如：'2 + 2' 或 'sqrt(16)'。"
    
    def _run(self, expression: str) -> str:
        """执行数学计算"""
        try:
            # 使用更安全的计算方式
            allowed_names = {
                'abs': abs,
                'round': round,
                'min': min,
                'max': max,
                'sum': sum,
                'pow': pow,
            }
            # 创建安全的局部环境
            local_dict = {"__builtins__": {}, "abs": abs, "round": round}
            local_dict.update(allowed_names)
            result = eval(expression, {"__builtins__": {}}, local_dict)
            return f"计算结果: {result}"
        except Exception as e:
            return f"计算错误: {str(e)}"
    
    async def _arun(self, expression: str) -> str:
        """异步执行数学计算"""
        return self._run(expression)

class WeatherTool(BaseTool):
    name: str = "weather"
    description: str = "获取指定城市的天气信息。输入应该是城市名称，例如：'北京'。"
    
    def _run(self, city: str) -> str:
        """获取天气信息"""
        try:
            # 这里使用示例 API，实际使用时需要替换为真实的天气 API
            # 例如：和风天气、OpenWeatherMap 等
            api_key = os.getenv("WEATHER_API_KEY", "")
            if not api_key:
                return "未配置天气 API 密钥"
            
            url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&lang=zh"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                current = data["current"]
                location = data["location"]
                return f"""城市：{location['name']}
温度：{current['temp_c']}°C
天气：{current['condition']['text']}
湿度：{current['humidity']}%
风速：{current['wind_kph']} km/h"""
            else:
                return f"获取天气信息失败：{data.get('error', {}).get('message', '未知错误')}"
        except Exception as e:
            return f"获取天气信息时发生错误：{str(e)}"
    
    async def _arun(self, city: str) -> str:
        """异步获取天气信息"""
        return self._run(city)

class TimeTool(BaseTool):
    name: str = "current_time"
    description: str = "获取当前时间信息。不需要输入参数。"
    
    def _run(self, _: str = "") -> str:
        """获取当前时间"""
        now = datetime.now()
        return f"""当前时间：{now.strftime('%Y-%m-%d %H:%M:%S')}
星期：{['一', '二', '三', '四', '五', '六', '日'][now.weekday()]}"""

    async def _arun(self, _: str = "") -> str:
        """异步获取当前时间"""
        return self._run()

class HTTPRequestTool(BaseTool):
    name: str = "http_request"
    description: str = """发送 HTTP 请求到外部 API。输入应该是一个 JSON 字符串，包含以下字段：
    - url: API 的 URL
    - method: 请求方法（GET, POST, PUT, DELETE 等）
    - headers: 请求头（可选）
    - params: URL 参数（可选）
    - data: 请求体数据（可选）
    - json: JSON 格式的请求体数据（可选）
    示例输入：
    {{"url": "https://api.example.com/data", "method": "GET", "headers": {{"Authorization": "Bearer token"}}, "params": {{"key": "value"}}}}"""
    
    def _run(self, request_config: str) -> str:
        """执行 HTTP 请求"""
        try:
            # 解析请求配置
            config = json.loads(request_config)
            url = config.pop("url")
            method = config.pop("method", "GET").upper()
            
            # 发送请求
            response = requests.request(method, url, **config)
            
            # 尝试解析 JSON 响应
            try:
                result = response.json()
                return json.dumps(result, ensure_ascii=False, indent=2)
            except:
                # 如果不是 JSON，返回文本
                return response.text
                
        except json.JSONDecodeError:
            return "错误：输入必须是有效的 JSON 字符串"
        except requests.RequestException as e:
            return f"请求错误：{str(e)}"
        except Exception as e:
            return f"发生错误：{str(e)}"
    
    async def _arun(self, request_config: str) -> str:
        """异步执行 HTTP 请求"""
        return self._run(request_config)

def get_tools(knowledge_base=None) -> List[BaseTool]:
    """获取所有可用工具"""
    tools = [
        CalculatorTool(),
        TimeTool(),
        HTTPRequestTool(),  # 添加 HTTP 请求工具
    ]
    
    if knowledge_base:
        tools.append(SearchTool(knowledge_base))
    
    # 如果配置了天气 API 密钥，添加天气工具
    if os.getenv("WEATHER_API_KEY"):
        tools.append(WeatherTool())
    
    return tools 