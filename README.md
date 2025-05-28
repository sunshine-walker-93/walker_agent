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

### 后端
- FastAPI (微服务架构)
- MySQL 数据库
- JWT 认证
- WebSocket 实时通信
- LangChain + OpenAI AI 集成

### 前端
- Vue 3 + TypeScript
- Vite 构建工具
- Pinia 状态管理
- Vue Router 路由管理
- Element Plus UI 框架
- Axios HTTP 客户端

## 系统架构

系统采用微服务架构，包含以下服务：

- 网关服务 (8100): API 网关，路由请求到各个微服务
- 认证服务 (8101): 用户认证和授权
- 用户服务 (8102): 用户管理
- 智能助手服务 (8103): 智能对话和任务处理
- 知识库服务 (8104): 知识库管理和检索
- 前端服务 (8105): Vue.js 单页应用

## 开发环境设置

### 前置要求
1. Python 3.9+
2. Node.js 16+
3. MySQL 8.0+

### 安装 MySQL
- macOS:
  ```bash
  brew install mysql
  ```
- Ubuntu:
  ```bash
  sudo apt-get install mysql-server
  ```
- Windows:
  从 [MySQL 官网](https://dev.mysql.com/downloads/mysql/) 下载安装包

### 安装 Node.js
- macOS:
  ```bash
  brew install node
  ```
- Ubuntu:
  ```bash
  curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
  sudo apt-get install -y nodejs
  ```
- Windows:
  从 [Node.js 官网](https://nodejs.org/) 下载安装包

### 克隆和设置项目
1. 克隆仓库：
```bash
git clone <repository-url>
cd <repository-name>
```

2. 设置后端服务：
```bash
# 为每个服务创建虚拟环境
for service in gateway-service auth-service user-service agent-service knowledge-service; do
  cd $service
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  cd ..
done
```

3. 设置前端服务：
```bash
cd frontend-service
npm install
```

### 配置环境变量
1. 后端服务配置：
   - 在每个服务目录下创建 `.env` 文件
   - 配置必要的环境变量（数据库连接、密钥等）

2. 前端服务配置：
   - 在 `frontend-service` 目录下创建 `.env` 文件
   - 配置 API 地址等环境变量

### 启动服务
运行启动脚本：
```bash
./start_services.sh
```

这将启动所有服务：
- 网关服务: http://localhost:8100
- 认证服务: http://localhost:8101
- 用户服务: http://localhost:8102
- 智能助手服务: http://localhost:8103
- 知识库服务: http://localhost:8104
- 前端服务: http://localhost:8105

### 停止服务
运行停止脚本：
```bash
./stop_services.sh
```

## 开发指南

### 后端开发
1. 添加新的服务：
   - 创建新的服务目录
   - 创建虚拟环境
   - 添加 requirements.txt
   - 在 start_services.sh 中添加启动命令

2. 添加新的API端点：
   - 在对应服务的 `src/main.py` 中添加新的路由
   - 实现相应的处理函数
   - 更新API文档

### 前端开发
1. 开发模式：
```bash
cd frontend-service
npm run dev
```

2. 构建生产版本：
```bash
cd frontend-service
npm run build
```

3. 添加新功能：
   - 创建新的 Vue 组件
   - 添加新的路由
   - 创建新的 API 调用
   - 更新状态管理

4. 目录结构：
```
frontend-service/
├── src/
│   ├── api/          # API 调用
│   ├── components/   # Vue 组件
│   ├── router/       # 路由配置
│   ├── stores/       # Pinia 状态管理
│   ├── types/        # TypeScript 类型定义
│   ├── views/        # 页面组件
│   ├── App.vue       # 根组件
│   └── main.ts       # 入口文件
├── public/           # 静态资源
└── package.json      # 项目配置
```

## API文档

启动服务后，访问以下地址查看API文档：
- 网关服务: http://localhost:8100/docs
- 认证服务: http://localhost:8101/docs
- 用户服务: http://localhost:8102/docs
- 智能助手服务: http://localhost:8103/docs
- 知识库服务: http://localhost:8104/docs

## 贡献

欢迎提交问题和改进建议。请遵循以下步骤：

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License