# LangChain Agent Demo

这是一个基于 LangChain 和 Streamlit 构建的智能助手应用，支持聊天对话、工具调用和知识库查询功能。

## 功能特点

- 基于 Streamlit 的现代化聊天界面
- 使用 LangChain 构建的智能 Agent
- 支持工具调用
- 支持知识库查询
- 对话历史记录

## 安装步骤

1. 克隆项目到本地
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 创建 `.env` 文件并添加 OpenAI API 密钥：
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## 运行应用

```bash
streamlit run app.py
```

## 项目结构

- `app.py`: 主应用文件
- `requirements.txt`: 项目依赖
- `.env`: 环境变量配置文件（需要自行创建）

## 使用说明

1. 启动应用后，在浏览器中打开显示的地址
2. 在聊天输入框中输入问题
3. Agent 将使用可用的工具和知识库来回答您的问题

## 注意事项

- 确保已正确设置 OpenAI API 密钥
- 首次运行时需要下载相关模型，可能需要一些时间 