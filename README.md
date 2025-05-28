# Walker Agent - 智能对话助手

Walker Agent 是一个基于 LangChain 和 Streamlit 构建的智能对话助手，支持本地 Ollama 模型和 DeepSeek API 两种模式。它具备知识库管理、文档问答、工具调用等功能。

## 功能特点

- 🤖 支持本地 Ollama 模型和 DeepSeek API 两种模式
- 📚 知识库管理：支持上传和管理文档（TXT、PDF、DOCX、MD）
- 🔍 智能问答：基于知识库的问答功能
- 🛠️ 工具集成：内置搜索、计算器、天气、时间等工具
- 💬 对话历史：支持查看、导出对话历史
- 🔄 模型切换：支持在 Ollama 和 API 模式之间切换

## 系统要求

- Python 3.8+
- macOS/Linux/Windows
- 如果使用 Ollama 模式，需要安装 [Ollama](https://ollama.ai/)

## 安装步骤

1. 克隆项目并进入项目目录：
```bash
git clone <repository-url>
cd walker_agent
```

2. 创建并激活虚拟环境：
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
.\venv\Scripts\activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 如果使用 macOS，安装 libmagic：
```bash
brew install libmagic
```

5. 如果使用 Ollama 模式，安装并启动 Ollama：
```bash
# 安装 Ollama（如果尚未安装）
# 从 https://ollama.ai/ 下载并安装

# 拉取模型
ollama pull deepseek-coder
```

## 使用方法

1. 启动应用：
```bash
python -B app.py
```

2. 在浏览器中访问应用（默认地址：http://localhost:8501）

3. 配置设置：
   - 在侧边栏选择模型类型（Ollama 或 API）
   - 如果选择 API 模式，输入 DeepSeek API Key
   - 可以自定义模型名称
   - 点击"应用设置"保存配置

4. 知识库管理：
   - 在侧边栏上传文档（支持 TXT、PDF、DOCX、MD 格式）
   - 查看知识库统计信息
   - 可以清空知识库或导出对话历史

5. 开始对话：
   - 在输入框中输入问题
   - 系统会自动调用相关工具或搜索知识库
   - 查看对话历史和工具调用过程

## 项目结构

```
walker_agent/
├── app.py                 # Streamlit 应用主文件
├── requirements.txt       # 项目依赖
├── src/
│   ├── agents/           # 智能代理相关代码
│   │   └── chat_agent.py
│   ├── knowledge_base/   # 知识库相关代码
│   │   └── vector_store.py
│   └── tools/           # 工具相关代码
│       └── base_tools.py
└── data/                # 数据存储目录
    ├── chroma/         # 向量数据库
    └── uploads/        # 上传文件存储
```

## 注意事项

1. 确保在使用 API 模式时正确设置 API Key
2. 使用 Ollama 模式时需要确保 Ollama 服务正在运行
3. 上传文件大小可能受到系统限制
4. 建议定期备份重要的对话历史

## 常见问题

1. Q: 为什么上传 PDF 文件失败？
   A: 确保已安装所有必要的依赖，特别是 `unstructured` 和 `python-magic`。

2. Q: 如何切换模型？
   A: 在侧边栏的"设置"部分选择模型类型，输入必要的配置信息，然后点击"应用设置"。

3. Q: 对话历史保存在哪里？
   A: 对话历史保存在内存中，可以通过"导出对话历史"功能保存到本地文件。

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 许可证

[添加许可证信息] 