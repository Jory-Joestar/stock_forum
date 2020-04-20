# stock_forum
软件工程课的团队项目

# Change Log
v0.0.0 (2020/4/19 20:30)
·项目框架及最初版本上线
·用户注册、登陆、登出
·查看、创建论坛板块
·发表论坛文章
·发表、回复、删除评论
·按股票名称查询某天的股票价格

# 环境依赖
环境配置：Python3
依赖的外部库：
django==3.0.4
django-bootstrap3==12.0.3
pandas==1.0.3
pyecharts==0.5.11
pyecharts-snapshot==0.2.0
tushare==1.2.54

# 安装
配置好上述环境和依赖库之后，将本项目移植到本地，在控制台中打开项目目录
输入python manage.py migrate迁移数据库
输入python manage.py runserver 如果运行成功，访问localhost:8000即可正常使用
输入python manage.py createsuperuser 创建超级管理员
超级管理员可登陆localhost:8000/admin管理所有数据

# 目录结构
/stock_forum：项目配置目录
    /settings.py:项目的setting文件，在里面注册安装的应用，文件的路径等等
    /urls.py：定义url模式，将访问定向到应用或视图函数
    /wsgi.py:本地运行不需要改动，django自带文件
    /asgi.py:同上
/forum：django项目应用，论坛功能实现
    /migrations:有关数据库的设定，用于迁移数据库
    /templates/forum:HTML模板文件夹
    /admin.py：用于注册可管理的数据模型
    /apps.py:django自带，没动
    /forms.py：定义表单类，用于获取用户输入的数据
    /models.py:定义模型类，操作数据库数据
    /test.py:测试模块，没动
    /urls.py:定义url模式，将访问定向到视图函数
    /views.py：定义视图函数，处理用户的访问和请求
/users:django项目应用，实现用户管理
    /migrations:有关数据库的设定，用于迁移数据库
    /templates/forum:HTML模板文件夹
    /admin.py：用于注册可管理的数据模型
    /apps.py:django自带，没动
    /forms.py：定义表单类，用于获取用户输入的数据
    /models.py:定义模型类，操作数据库数据
    /test.py:测试模块，没动
    /urls.py:定义url模式，将访问定向到视图函数
    /views.py：定义视图函数，处理用户的访问和请求
/extends:拓展功能模块
    /data：数据源模块
        /stock_basic.py：从API获得股票价格数据，生产数据集，k线图
    /get_price.py：获得股票价格，供forum应用中的视图函数调用
/manage.py:django项目控制模块，没动

