## 服务器部署

#### 1. 运行

```bash
# 切换到 home 目录，并克隆 ChatGPT-Mirror 仓库
cd /home/ && git clone https://github.com/dairoot/ChatGPT-Mirror.git

cd ChatGPT-Mirror/

cp .env.example .env && vi .env # 修改管理后台账号密码

docker compose pull # 拉取镜像

docker compose up -d # 后台运行
```

#### 2. 配置 nginx （需要配置 https）

```bash
upstream chatgpt {
    server 127.0.0.1:50001;
    server 127.0.0.1:50002;
}

server {
    listen              443 ssl http2;
    listen              [::]:443 ssl http2;
    server_name         chatgpt.example.com;

    # SSL 文件
    ssl_certificate     /etc/nginx/ssl/chatgpt.example.com/fullchain.crt;
    ssl_certificate_key /etc/nginx/ssl/chatgpt.example.com/private.pem;


    # 日志文件
    # access_log /data/logs/ngx.chatgpt.access.log json_combined;
    access_log /data/logs/ngx.chatgpt.access.log;
    error_log /data/logs/ngx.chatgpt.error.log;


    # 静态文件
    location /fe {
       alias /home/ChatGPT-Mirror/admin/dist;
    }

    location / {
        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_pass http://chatgpt;
    }


}

# HTTP redirect
server {
    listen      80;
    listen      [::]:80;
    server_name chatgpt.example.com;
    return      301 https://chatgpt.example.com$request_uri;
}
```

- 小白用户可以使用宝塔面板进行部署，具体教程请参考：[如何安装 ChatGPT 镜像](https://dairoot.cn/2024/07/02/install-chatgpt-mirror/)。
