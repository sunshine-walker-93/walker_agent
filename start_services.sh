#!/bin/bash

# 启动 MySQL（需要先安装）
# 如果没有安装 MySQL，请先安装：
# macOS: brew install mysql
# Ubuntu: sudo apt-get install mysql-server
# Windows: 从官网下载安装包

# 启动 MySQL
# macOS
# brew services start mysql
# Ubuntu
# sudo service mysql start

# 创建数据库和用户
mysql -u root -p123456 -e "CREATE DATABASE IF NOT EXISTS userdb;"
mysql -u root -p123456 -e "CREATE USER IF NOT EXISTS 'user'@'localhost' IDENTIFIED BY '123456';"
mysql -u root -p123456 -e "GRANT ALL PRIVILEGES ON userdb.* TO 'user'@'localhost';"
mysql -u root -p123456 -e "FLUSH PRIVILEGES;"

# 启动认证服务
cd auth-service
source venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --host 0.0.0.0 --port 8101 &
cd ..

# 启动用户服务
cd user-service
source venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --host 0.0.0.0 --port 8102 &
cd ..

# 启动知识库服务
cd knowledge-service
source venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --host 0.0.0.0 --port 8104 &
cd ..

# 启动智能助手服务
cd agent-service
source venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --host 0.0.0.0 --port 8103 &
cd ..

# 启动网关服务
cd gateway-service
source venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --host 0.0.0.0 --port 8100 &
cd ..

# 启动前端服务
cd frontend-service
# 确保没有遗留的 Node.js 进程
pkill -f "node.*vite" || true
npm install
npm run dev &
cd ..

echo "所有服务已启动"
echo "网关服务: http://localhost:8100"
echo "认证服务: http://localhost:8101"
echo "用户服务: http://localhost:8102"
echo "智能助手服务: http://localhost:8103"
echo "知识库服务: http://localhost:8104"
echo "前端服务: http://localhost:8105" 