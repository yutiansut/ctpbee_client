# ctpbee_client  
> 基于ctpbee界面端的后台服务

## 快速部署
```
# 安装依赖
pip install -r requriment.txt

```
根据实际部署情况修改 uwsig.ini
```
# supervisor
sudo apt install supervisor
cd /etc/supervisor/conf.d/ && sudo vim ctpbee_client_supervisor.conf
```
supervisor.conf
```
[program:ctpbee_client]
# 启动命令入口
command=/home/faith/GIT/ctpbee_client/venv/bin/uwsgi /home/faith/GIT/ctpbee_client/backend/uwsgi.ini

# 命令程序所在目录
directory=/home/faith/GIT/ctpbee_client/backend/
#运行命令的用户名
user=faith
        
autostart=true
autorestart=true
#日志地址
stdout_logfile=/home/faith/GIT/ctpbee_client/backend/uwsgi_supervisor.log    
```
根据实际部署情况修改 nginx.conf
```
# nginx
sudo apt install nginx
cd /etc/nginx/sites-available && sudo mv default default_bak
sudo vim default
```
default
```
server {
  listen  5000;
  server_name 10.40.25.15; #公网地址

  location / {
    include      uwsgi_params;
    uwsgi_pass   127.0.0.1:8001;  # 指向uwsgi 所应用的内部地址,所有请求将转发给uwsgi 处理
    uwsgi_param UWSGI_PYHOME /home/faith/GIT/ctpbee_client/venv; # 指向虚拟环境目录
    uwsgi_param UWSGI_CHDIR  /home/faith/GIT/ctpbee_client/backend; # 指向网站根目录
    uwsgi_param UWSGI_SCRIPT run:app; # 指定启动程序
  }
}
```
启动
```
sudo service supervisor start
sudo service nginx restart
```
如果表达的不清楚->[传送门](https://www.cnblogs.com/Ray-liang/p/4173923.html)

---
