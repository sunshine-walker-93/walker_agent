# 个人信息管理系统

一个集成了智能助手的个人信息管理系统，提供用户认证、个人信息管理、智能对话等功能。

## 功能特点

- 用户认证和授权
- 个人信息管理
- 智能助手对话
- 系统设置
- 实时通知
- 多语言支持
- 主题切换

## 技术栈

- 后端：FastAPI
- 前端：HTML, Tailwind CSS, JavaScript
- 数据库：内存存储（可扩展为持久化存储）
- 认证：JWT
- 实时通信：WebSocket
- AI：LangChain, OpenAI

## 安装

1. 克隆仓库：
```bash
git clone <repository-url>
cd <repository-name>
```

2. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置环境变量：
创建 `.env` 文件并添加以下配置：
```
OPENAI_API_KEY=your-api-key
SECRET_KEY=your-secret-key
```

## 运行

1. 启动服务器：
```bash
python src/app.py
```

2. 访问系统：
打开浏览器访问 `http://localhost:8000`

## 使用指南

### 注册和登录

1. 访问登录页面
2. 点击"注册"创建新账号
3. 填写必要信息并提交
4. 使用注册的账号登录系统

### 个人信息管理

1. 在侧边栏点击"个人信息"
2. 查看和编辑个人资料
3. 修改密码
4. 更新邮箱和姓名

### 智能助手

1. 在侧边栏点击"智能助手"
2. 在输入框中输入问题或消息
3. 等待助手回复
4. 可以继续对话或开始新的话题

### 系统设置

1. 在侧边栏点击"系统设置"
2. 配置通知偏好
3. 选择界面主题
4. 设置语言
5. 管理隐私选项

## API文档

启动服务器后，访问 `http://localhost:8000/docs` 查看完整的API文档。

### 主要API端点

- POST `/token` - 获取访问令牌
- POST `/api/auth/register` - 注册新用户
- GET `/api/user/profile` - 获取用户信息
- PUT `/api/user/profile` - 更新用户信息
- PUT `/api/user/password` - 修改密码
- GET `/api/user/settings` - 获取用户设置
- PUT `/api/user/settings` - 更新用户设置
- DELETE `/api/user/data` - 清除用户数据
- DELETE `/api/user/account` - 删除用户账号
- WebSocket `/ws/{client_id}` - 实时通信

## 开发指南

### 项目结构

```
.
├── src/
│   ├── agents/         # 智能代理
│   ├── core/          # 核心功能
│   ├── static/        # 静态文件
│   └── app.py         # 主应用
├── data/              # 数据存储
├── requirements.txt   # 依赖列表
└── README.md         # 项目文档
```

### 添加新功能

1. 创建新的代理：
   - 在 `src/agents/` 目录下创建新的代理类
   - 继承 `BaseAgent` 类
   - 实现必要的方法

2. 添加新的API端点：
   - 在 `src/app.py` 中添加新的路由
   - 实现相应的处理函数
   - 更新API文档

3. 修改前端界面：
   - 在 `src/static/` 目录下修改或添加HTML文件
   - 更新JavaScript代码
   - 调整样式

## 贡献

欢迎提交问题和改进建议。请遵循以下步骤：

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License

## 本地开发环境设置

### 前置要求
1. Python 3.9+
2. PostgreSQL 13+

### 安装 PostgreSQL
- macOS:
  ```bash
  brew install postgresql
  ```
- Ubuntu:
  ```bash
  sudo apt-get install postgresql
  ```
- Windows:
  从 [PostgreSQL 官网](https://www.postgresql.org/download/windows/) 下载安装包

### 启动服务
1. 确保 PostgreSQL 已安装并运行
2. 运行启动脚本：
   ```bash
   ./start_services.sh
   ```
   这将启动所有服务：
   - 网关服务 (http://localhost:8100)
   - 认证服务 (http://localhost:8101)
   - 用户服务 (http://localhost:8102)
   - 智能助手服务 (http://localhost:8103)
   - 知识库服务 (http://localhost:8104)

### 停止服务
运行停止脚本：
```bash
./stop_services.sh
```

## 服务说明

### 网关服务
- 端口：8100
- 功能：API 网关，路由请求到各个微服务

### 认证服务
- 端口：8101
- 功能：用户认证和授权

### 用户服务
- 端口：8102
- 功能：用户管理

### 智能助手服务
- 端口：8103
- 功能：智能对话和任务处理

### 知识库服务
- 端口：8104
- 功能：知识库管理和检索

## 开发指南

### 添加新服务
1. 创建新的服务目录
2. 创建虚拟环境：`python -m venv venv`
3. 添加 requirements.txt
4. 在 start_services.sh 中添加启动命令

### 修改服务
1. 激活对应服务的虚拟环境：`source venv/bin/activate`
2. 修改代码
3. 重启服务：`pkill -f "uvicorn src.main:app" && uvicorn src.main:app --host 0.0.0.0 --port <端口号>`