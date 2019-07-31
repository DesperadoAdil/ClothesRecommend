# 服装推荐项目

### Web前后端
&emsp;&emsp;我们实现了简单的Web前后端来向用户提供推荐服务，用户输入景点地名，后端首先去马蜂窝网站上爬取相应景点的图片，然后建立异步任务进行模型的训练，最后将结果返回在前端。

#### 前端
- 采用Vue.js构建页面
- Axios实现异步API调用

#### 后端
- 采用Python Flask作为Web框架
- 采用Celery异步队列来构建训练任务
- 采用Mysql和Redis来存储数据

#### API
- GET `/api/task` 获取任务列表
  - 无参数
- POST `/api/task` 新建任务
  - **payload** `place` 景点地名
- GET `/api/task/<string:id>` 通过id获取任务详情
  - **param** `id` 任务id
- DELETE `/api/task/<string:id>` 通过id删除任务
  - **param** `id` 任务id

#### 部署
- redis
  `redis://localhost:6379/`

- celery
  在backend/目录下运行 `celery -A app:celery worker -l info -P eventlet`

- Flask
  在backend/目录下运行 `python run.py`，访问 `localhost` 即可

### 社交网络爬取图片
- [马蜂窝网](http://m.mafengwo.cn)游记中搜索地名获取相应图片
- Python requests 爬取网页
- Python BeautifulSoup 解析网页，提取图片
- 马蜂窝主域名(https://www.mafengwo.cn)的游记是有反爬虫保护的，但是在分析网页中注意到其分享功能所用的子域名(http://m.mafengwo.cn)是在主域名上的转发，而且没有反爬虫保护，可以通过这个域名绕过其保护机制

### 景点图片去除人物
- 采用Python opencv来去除图片中的人物
- 二值化：`cv.adaptiveThreshold` 采用局部阈值来进行图片二值化
- 根据二值化的轮廓确定人物的位置矩形
- 采用 `cv.grabCut` 方法来取出人物轮廓
- 将取走人物轮廓的图像作为mask与原图做 `cv.add` 操作得到除去人物的原图
