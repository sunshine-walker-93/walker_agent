from typing import List, Optional, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_core.tools import BaseTool
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import json

class ChatAgent:
    def __init__(
        self,
        tools: List[BaseTool],
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.7
    ):
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            streaming=True,
            callbacks=[StreamingStdOutCallbackHandler()]
        )
        self.tools = tools
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="output"
        )
        self._initialize_agent()
    
    def _initialize_agent(self):
        """初始化 Agent"""
        system_prompt = """你是一个智能助手，可以帮助用户回答问题。
你的主要职责是：
1. 理解用户的问题并提供准确的回答
2. 在需要时使用工具来获取信息或执行计算
3. 保持对话的连贯性和上下文理解
4. 提供清晰、专业的回答

你可以使用的工具包括：
{}

使用工具的规则：
1. 如果用户的问题需要搜索知识库，使用 search_knowledge_base 工具
2. 如果用户的问题涉及数学计算，使用 calculator 工具
3. 如果用户询问天气，使用 weather 工具
4. 如果用户询问时间，使用 current_time 工具

回答要求：
1. 始终用中文回答
2. 回答要简洁明了
3. 如果使用了工具，要解释工具的结果
4. 如果无法回答，要诚实地说明
5. 保持礼貌和专业的语气"""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt.format(
                "\n".join([f"- {tool.name}: {tool.description}" for tool in self.tools])
            )),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        self.agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=3
        )
    
    def chat(self, message: str) -> Dict[str, Any]:
        """与 Agent 对话"""
        try:
            response = self.agent_executor.invoke({"input": message})
            return {
                "success": True,
                "output": response["output"],
                "intermediate_steps": response.get("intermediate_steps", [])
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": "抱歉，处理您的问题时出现了错误。请稍后重试。"
            }
    
    def clear_memory(self):
        """清空对话历史"""
        self.memory.clear()
    
    def get_chat_history(self) -> List[Dict[str, str]]:
        """获取对话历史"""
        history = []
        for message in self.memory.chat_memory.messages:
            history.append({
                "role": message.type,
                "content": message.content
            })
        return history 