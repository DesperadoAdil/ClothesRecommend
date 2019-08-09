# backend
后端部分

#### Python 3.6

#### 解压京东的数据库文件到 `backend/app/static/wqJD_20190120` 文件夹下

#### 修改 `backend/config.py`
  - 填写Mysql数据库的username，password，database

#### Mysql数据库
  - 创建数据库 database

#### 安装redis
  - 运行于localhost 6379端口，或者自己设计ip和端口，同时修改config.py中的配置

#### cmd进入 `backend`
  - 运行 `pip install -r requirements.txt` 安装依赖库
  - 运行 `celery -A app:celery worker -l info -P eventlet`
  - 运行 `python db.py` 创建数据表
  - 运行 `python run.py` 浏览器访问 `localhost` 演示demo
