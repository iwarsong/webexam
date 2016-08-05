# webexam v2.1

** 应付考试的客观题自由练习系统 **

### 1.依赖组件安装

+ python 2.7和pip
+ Flask 
+ Flask-Login 
+ Flask-SQLAlchemy 
+ xlrd
 
		在线安装：
		安装了python后，使用pip安装：
		pip install flask flask-login flask-sqlalchemy xlrd
		
		离线安装：
		在windows下可以使用离线包安装，运行 lib_offline_setup/setup_windows.cmd批处理。

### 2.使用

+ 在命令行窗口中，进入webexam目录，运行python runserver.py
+ 打开浏览器，输入http://localhost:5000
+ 前端页面使用了bootstrap，支持多种浏览器和手机端自适应
+ 目前只支持单选、多选和判断题的练习，可以将excel格式的试题进行导入。
