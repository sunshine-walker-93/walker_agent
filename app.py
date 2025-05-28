import os
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
    st.title("知识库管理")
    
    # 文件上传
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
        st.markdown(message["content"])
        if "intermediate_steps" in message:
            with st.expander("查看工具调用过程"):
                for step in message["intermediate_steps"]:
                    st.write(f"工具：{step[0].tool}")
                    st.write(f"输入：{step[0].tool_input}")
                    st.write(f"输出：{step[1]}")
                    st.write("---")

# 聊天输入
if prompt := st.chat_input("请输入您的问题"):
    # 添加用户消息到历史
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 获取 AI 响应
    with st.chat_message("assistant"):
        response = st.session_state.agent.chat(prompt)
        if response["success"]:
            st.markdown(response["output"])
            st.session_state.messages.append({
                "role": "assistant",
                "content": response["output"],
                "intermediate_steps": response.get("intermediate_steps", [])
            })
        else:
            st.error(response["output"]) 