#!/bin/bash

# 停止所有 Python 服务
pkill -f "uvicorn src.main:app"

# 停止 MySQL
# macOS
# brew services stop mysql
# Ubuntu
# sudo service mysql stop

echo "所有服务已停止" 