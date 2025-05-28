from typing import List, Optional, Dict, Any
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_core.tools import BaseTool
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import json
import os

class ChatAgent:
    def __init__(
        self,
        tools: List[BaseTool],
        model_type: str = "ollama",  # "ollama" 或 "api"
        model_name: str = "deepseek-r1:14b",
        temperature: float = 0.7
    ):
        self.model_type = model_type
        self.model_name = model_name
        self.temperature = temperature
        self.tools = tools
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="output"
        )
        self._initialize_llm()
        self._initialize_agent()
    
    def _initialize_llm(self):
        """初始化语言模型"""
        if self.model_type == "ollama":
            self.llm = ChatOllama(
                model=self.model_name,
                temperature=self.temperature,
                streaming=True,
                callbacks=[StreamingStdOutCallbackHandler()]
            )
        else:  # api mode
            self.llm = ChatOpenAI(
                model=self.model_name,
                temperature=self.temperature,
                streaming=True,
                callbacks=[StreamingStdOutCallbackHandler()]
            )
    
    def switch_model(self, model_type: str, model_name: Optional[str] = None):
        """切换模型类型和名称"""
        self.model_type = model_type
        if model_name:
            self.model_name = model_name
        self._initialize_llm()
        self._initialize_agent()  # 重新初始化 agent 以使用新的模型
    
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
            print(f"开始处理消息: {message}")  # 调试日志
            response = self.agent_executor.invoke({"input": message})
            print(f"Agent 响应: {response}")  # 调试日志
            
            # 格式化工具调用过程
            formatted_steps = []
            for step in response.get("intermediate_steps", []):
                formatted_steps.append({
                    "tool": step[0].tool,
                    "tool_input": step[0].tool_input,
                    "output": step[1]
                })
            
            return {
                "success": True,
                "output": response["output"],
                "intermediate_steps": formatted_steps
            }
        except Exception as e:
            import traceback
            error_msg = f"错误类型: {type(e).__name__}\n错误信息: {str(e)}\n{traceback.format_exc()}"
            print(f"发生错误: {error_msg}")  # 调试日志
            return {
                "success": False,
                "error": error_msg,
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