import os
# 禁用字节码生成
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

import streamlit as st
from dotenv import load_dotenv
from src.tools.base_tools import get_tools
from src.knowledge_base.vector_store import KnowledgeBase
from src.agents.chat_agent import ChatAgent
import json
from datetime import datetime

# 加载环境变量
load_dotenv()

# 设置页面配置
st.set_page_config(
    page_title="智能助手",
    page_icon="🤖",
    layout="wide"
)

# 初始化 session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "knowledge_base" not in st.session_state:
    st.session_state.knowledge_base = KnowledgeBase()

if "agent" not in st.session_state:
    tools = get_tools(st.session_state.knowledge_base)
    st.session_state.agent = ChatAgent(tools=tools)

# 创建侧边栏
with st.sidebar:
    st.title("设置")
    
    # 模型选择
    model_type = st.radio(
        "选择模型类型",
        ["ollama", "api"],
        index=0,
        help="选择使用本地 Ollama 模型或 DeepSeek API"
    )
    
    # 如果选择了 API 模式，显示 API Key 输入
    if model_type == "api":
        api_key = st.text_input(
            "DeepSeek API Key",
            type="password",
            help="输入你的 DeepSeek API Key"
        )
        if api_key:
            os.environ["DEEPSEEK_API_KEY"] = api_key
    
    # 模型名称输入
    model_name = st.text_input(
        "模型名称",
        value="deepseek-r1:14b",
        help="输入模型名称（Ollama 模式）或 API 模型名称"
    )
    
    # 应用设置按钮
    if st.button("应用设置"):
        # 切换模型
        st.session_state.agent.switch_model(model_type, model_name)
        st.session_state.knowledge_base.switch_model(model_type)
        st.success("设置已更新！")
    
    # 文件上传
    st.title("知识库管理")
    uploaded_file = st.file_uploader(
        "上传文档到知识库",
        type=["txt", "md", "pdf", "docx"],
        help="支持的文件格式：TXT, MD, PDF, DOCX"
    )
    
    if uploaded_file is not None:
        # 保存上传的文件
        file_path = os.path.join("data/uploads", uploaded_file.name)
        os.makedirs("data/uploads", exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        
        # 添加到知识库
        result = st.session_state.knowledge_base.add_file(file_path)
        if result["success"]:
            st.success(result["message"])
        else:
            st.error(result["message"])
    
    # 知识库统计
    st.subheader("知识库统计")
    stats = st.session_state.knowledge_base.get_stats()
    st.write(f"总文档数：{stats['total_documents']}")
    if stats['sources']:
        st.write("文档来源：")
        for source in stats['sources']:
            st.write(f"- {source['source']}: {source['count']} 个文档")
    
    # 清空知识库
    if st.button("清空知识库"):
        st.session_state.knowledge_base.clear()
        st.success("知识库已清空！")
    
    # 清空对话历史
    if st.button("清空对话历史"):
        st.session_state.messages = []
        st.session_state.agent.clear_memory()
        st.success("对话历史已清空！")
    
    # 导出对话历史
    if st.button("导出对话历史"):
        history = st.session_state.agent.get_chat_history()
        if history:
            filename = f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
            st.success(f"对话历史已导出到：{filename}")
        else:
            st.info("没有对话历史可导出")

# 主界面
st.title("🤖 智能助手")

# 显示聊天历史
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # 使用不同的样式显示用户和助手的消息
        if message["role"] == "user":
            st.markdown(f"### 用户问题\n{message['content']}")
        else:
            # 使用不同的样式显示助手的回答
            st.markdown("### 助手回答")
            st.markdown(message["content"])
            
            # 显示工具调用过程
            if "intermediate_steps" in message:
                with st.expander("查看思考过程", expanded=False):
                    for step in message["intermediate_steps"]:
                        # 使用不同的背景色和样式显示思考过程
                        st.markdown("""
                        <style>
                        .thinking-box {
                            background-color: #f0f2f6;
                            padding: 1rem;
                            border-radius: 0.5rem;
                            margin: 1rem 0;
                        }
                        .result-box {
                            background-color: #e6f3ff;
                            padding: 1rem;
                            border-radius: 0.5rem;
                            margin: 1rem 0;
                        }
                        </style>
                        """, unsafe_allow_html=True)
                        
                        # 思考过程
                        st.markdown('<div class="thinking-box">', unsafe_allow_html=True)
                        st.markdown("#### 🤔 思考过程")
                        st.markdown(f"**使用的工具**: `{step['tool']}`")
                        st.markdown(f"**工具输入**:")
                        st.code(step['tool_input'], language="text")
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # 执行结果
                        st.markdown('<div class="result-box">', unsafe_allow_html=True)
                        st.markdown("#### ✨ 执行结果")
                        st.code(step['output'], language="text")
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        st.markdown("---")

# 聊天输入
if prompt := st.chat_input("请输入您的问题"):
    # 添加用户消息到历史
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"### 用户问题\n{prompt}")

    # 获取 AI 响应
    with st.chat_message("assistant"):
        try:
            response = st.session_state.agent.chat(prompt)
            if response["success"]:
                st.markdown("### 助手回答")
                st.markdown(response["output"])
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response["output"],
                    "intermediate_steps": response.get("intermediate_steps", [])
                })
            else:
                st.error(f"错误详情: {response.get('error', '未知错误')}")
                st.error(response["output"])
        except Exception as e:
            st.error(f"发生异常: {str(e)}")
            import traceback
            st.error(f"详细错误信息: {traceback.format_exc()}") 