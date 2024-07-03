## 本地运行

```bash
# 本地需要翻墙
docker pull dairoot/chatgpt-mirror

docker run -p 50001:8787 \
   -e ADMIN_USERNAME=usernamexxx \
   -e ADMIN_PASSWORD=passwordxxx \
   -v ./admin/dist:/tmp/dist \
   dairoot/chatgpt-mirror

caddy run --config ./Caddyfile --watch

访问: https://localhost/
```

## 部署到服务器

需要境外 VPS

1. 运行

```bash
cd /home && git clone https://github.com/dairoot/ChatGPT-Mirror.git

cd ChatGPT-Mirror/

vi docker-compose.yml # 修改管理后台账号密码

docker compose pull # 拉取镜像

docker compose up -d # 后台运行
```

2. 配置 nginx （需要配置 https）

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
