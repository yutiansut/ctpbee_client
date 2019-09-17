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
cd /etc/supervisor/conf.d/
sudo vim ctpbee_client_supervisor.conf
```
ctpbee_client_supervisor.conf
```
[program:ctpbee_client]
# 启动命令入口
command=/home/faith/GIT/ctpbee_client/backend/venv/bin/uwsgi /home/faith/GIT/ctpbee_client/backend/uwsgi.ini

# 命令程序所在目录
directory=/home/ctpbee_client/backend
#运行命令的用户名
user=faith
        
autostart=true
autorestart=true
#日志地址
stdout_logfile=/home/faith/GIT/ctpbee_client/backend/uwsgi_supervisor.log     
```
```
sudo service supervisor start
```
根据实际部署情况修改 nginx.conf
```
# nginx
sudo apt install nginx

```
