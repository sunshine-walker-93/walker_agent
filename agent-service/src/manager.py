from typing import Dict, List, Optional
import logging
from .agent import BaseAgent, ChatAgent

logger = logging.getLogger(__name__)

class AgentManager:
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self._initialize_default_agents()
    
    def _initialize_default_agents(self):
        """初始化默认的Agent"""
        chat_agent = ChatAgent(
            name="default",
            description="A general-purpose chat agent"
        )
        self.register_agent(chat_agent)
    
    def register_agent(self, agent: BaseAgent):
        """注册新的Agent"""
        self.agents[agent.name] = agent
        logger.info(f"Registered agent: {agent.name}")
    
    def get_agent(self, name: str) -> Optional[BaseAgent]:
        """获取指定的Agent"""
        return self.agents.get(name)
    
    def list_agents(self) -> List[Dict]:
        """列出所有Agent"""
        return [
            {
                "name": agent.name,
                "description": agent.description
            }
            for agent in self.agents.values()
        ]
    
    def clear_agent_memory(self, name: str) -> bool:
        """清空指定Agent的记忆"""
        agent = self.get_agent(name)
        if agent:
            agent.clear_memory()
            return True
        return False
    
    async def process_message(
        self,
        client_id: str,
        message: str,
        agent: str = "default",
        knowledge: Optional[Dict] = None,
        tools: Optional[List[Dict]] = None
    ) -> str:
        """处理消息"""
        target_agent = self.get_agent(agent)
        if not target_agent:
            return f"Agent {agent} not found"
        
        try:
            response = await target_agent.process_message(
                message=message,
                knowledge=knowledge,
                tools=tools
            )
            return response
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return f"Error: {str(e)}" 