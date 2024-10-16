## 服务器部署

#### 1. 运行

```bash
# 切换到 home 目录，并克隆 ChatGPT-Mirror 仓库
cd /home/ && git clone https://github.com/dairoot/ChatGPT-Mirror.git

cd ChatGPT-Mirror/

cp .env.example .env && vi .env # 修改管理后台账号密码

./deploy.sh
```

#### 2.1 配置 nginx （需要配置 https）
⚠️ 记得将 `chatgpt.example.com` 替换为自己域名，总有人忘记

```conf
proxy_cache_path /etc/nginx/cache/chatgpt levels=1:2 keys_zone=chatgpt_cache:20m inactive=1d max_size=5g;

upstream chatgpt {
    server 127.0.0.1:50001;
    # server 127.0.0.1:50002;
}

server {
    listen              443 ssl http2;
    listen              [::]:443 ssl http2;
    server_name         chatgpt.example.com;

    # SSL 文件 START
    ssl_certificate     /etc/nginx/ssl/chatgpt.example.com/fullchain.crt;
    ssl_certificate_key /etc/nginx/ssl/chatgpt.example.com/private.pem;
    # SSL 文件 END

    # GLOBAL-CACHE START
    location ~* \.(js|css)$ {
        proxy_cache chatgpt_cache;
        proxy_cache_valid 200 60m;   # 对状态码200的响应缓存60分钟

        # 设置静态文件的缓存控制，浏览器缓存控制
        expires 7d;

        # 添加响应头部
        add_header X-Cache-Status $upstream_cache_status;

        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_pass http://chatgpt;
    }
    # GLOBAL-CACHE END


    # 日志文件 START
    # access_log /data/logs/ngx.chatgpt.access.log json_combined;
    access_log /data/logs/ngx.chatgpt.access.log;
    error_log /data/logs/ngx.chatgpt.error.log;
    # 日志文件 END


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

#### 2.2 如果使用 `cloudflare` 小黄云代理，则无需 https。nginx 配置如下

```bash
proxy_cache_path /etc/nginx/cache/chatgpt levels=1:2 keys_zone=chatgpt_cache:20m inactive=1d max_size=5g;

upstream chatgpt {
    server 127.0.0.1:50001;
    # server 127.0.0.1:50002;
}

server {
    listen              80;
    server_name         chatgpt.example.com;

    # GLOBAL-CACHE START
    location ~* \.(js|css)$ {
        proxy_cache chatgpt_cache;
        proxy_cache_valid 200 60m;   # 对状态码200的响应缓存60分钟

        # 设置静态文件的缓存控制，浏览器缓存控制
        expires 7d;

        # 添加响应头部
        add_header X-Cache-Status $upstream_cache_status;

        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_pass http://chatgpt;
    }
    # GLOBAL-CACHE END


    # 日志文件 START
    # access_log /data/logs/ngx.chatgpt.access.log json_combined;
    access_log /data/logs/ngx.chatgpt.access.log;
    error_log /data/logs/ngx.chatgpt.error.log;
    # 日志文件 END


    location / {
        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_pass http://chatgpt;
    }
}
```

- 小白用户可以使用宝塔面板进行部署，具体教程请参考：[如何安装 ChatGPT 镜像](https://dairoot.cn/2024/07/02/install-chatgpt-mirror/)。
