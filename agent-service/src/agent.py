from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.memory = []
    
    @abstractmethod
    async def process_message(
        self,
        message: str,
        knowledge: Optional[Dict] = None,
        tools: Optional[List[Dict]] = None
    ) -> str:
        """处理消息"""
        pass
    
    def clear_memory(self):
        """清空记忆"""
        self.memory = []
        logger.info(f"Cleared memory for agent {self.name}")

class ChatAgent(BaseAgent):
    def __init__(self, name: str, description: str):
        super().__init__(name, description)
        self.conversation_history = []
    
    async def process_message(
        self,
        message: str,
        knowledge: Optional[Dict] = None,
        tools: Optional[List[Dict]] = None
    ) -> str:
        """处理聊天消息"""
        # 添加消息到历史记录
        self.conversation_history.append({"role": "user", "content": message})
        
        # 处理消息（这里应该调用实际的LLM）
        response = f"Echo: {message}"  # 示例响应
        
        # 添加响应到历史记录
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return response
    
    def clear_memory(self):
        """清空聊天历史"""
        super().clear_memory()
        self.conversation_history = []
        logger.info(f"Cleared conversation history for agent {self.name}") 