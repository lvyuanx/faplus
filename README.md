# faplus
基于 FalstApi 的增强版本，能够实现类似于Django的框架逻辑

## 快速开始

### 1.安装
进入项目的根目录下执行：
```
pip install git+https://github.com/lvyuanx/faplus@<tag>
```
其中<tag>为版本号，如：v0.0.7 （0.0.7之前的版本存在问题，请勿使用）

### 2.初始化项目
进入项目的根目录下执行：
```
python -m faplus.management startproject
```

### 3.修复config.py中的配置
数据库和redis默认开启（可以关闭）

### 4.初始化数据库
```
python manage.py init_dbinit_db
```

### 5.启动项目
```
python manage.py runserver
```

只需简单的步骤，即可开始一个新的项目！
