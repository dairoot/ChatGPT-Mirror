## 服务器部署

服务器推荐：[腾讯云](https://curl.qcloud.com/0JAXkoF1) 选择欧美区域


#### 1. 运行

```bash
# 切换到 home 目录，并克隆 ChatGPT-Mirror 仓库
cd /home/ && git clone https://github.com/dairoot/ChatGPT-Mirror.git

cd ChatGPT-Mirror/

# 修改管理后台账号密码
cp .env.example .env && vi .env

# 启动
./deploy.sh
```

- 具体教程请参考：[如何安装 ChatGPT 镜像](https://dairoot.cn/2024/07/02/install-chatgpt-mirror/)。


2. #### 配置 nginx (可以不配置 https， 但推荐配置)
   ⚠️ 记得将 `chatgpt.example.com` 替换为自己域名，总有人忘记

```
# 创建缓存目录
mkdir -p /etc/nginx/cache/newchat

cd /etc/nginx/conf.d/ && vi chatgpt.conf (贴以下配置)
# 校验配置是否正确，并加载配置
nginx -t
nginx -s reload
```

##### 配置一

```nginx

server {
    listen              443 ssl http2;
    listen              [::]:443 ssl http2;
    server_name         chatgpt.example.com;

    # SSL 文件 START
    ssl_certificate     /etc/nginx/ssl/chatgpt.example.com/fullchain.crt;
    ssl_certificate_key /etc/nginx/ssl/chatgpt.example.com/private.pem;
    # SSL 文件 END


    # 日志文件 START
    # access_log /data/logs/ngx.chatgpt.access.log json_combined;
    access_log /data/logs/ngx.chatgpt.access.log;
    error_log /data/logs/ngx.chatgpt.error.log;
    # 日志文件 END

    # 屏蔽无效文件 START
    location ~* \.js\.map$ {
        return 404;
    }
    # 屏蔽无效文件 END


    client_header_buffer_size 4k;
    large_client_header_buffers 8 16k;


    location / {
        proxy_redirect off;
        proxy_buffering off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $http_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $http_x_forwarded_proto;

        proxy_pass http://127.0.0.1:50002;
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

##### 配置二、 使用 `cloudflare` 小黄云代理，则无需 https。

```nginx

server {
    listen              80;
    server_name         chatgpt.example.com;

    # 日志文件 START
    # access_log /data/logs/ngx.chatgpt.access.log json_combined;
    access_log /data/logs/ngx.chatgpt.access.log;
    error_log /data/logs/ngx.chatgpt.error.log;
    # 日志文件 END

    client_header_buffer_size 4k;
    large_client_header_buffers 8 16k;


    location / {
        proxy_redirect off;
        proxy_buffering off;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $http_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $http_x_forwarded_proto;

        proxy_pass http://127.0.0.1:50002;
    }
}
```

3. #### 配置 nginx 缓存（该步骤非必需）

```nginx
proxy_cache_path /etc/nginx/cache/newchat levels=1:2 keys_zone=newchat_cache:20m inactive=1d max_size=5g;

server {
    ..... 省略上述配置


    # GLOBAL-CACHE START
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff|woff2|ttf|otf|eot|svg|mp4|webm|ogg|ogv|zip|pdf)$ {
        proxy_cache newchat_cache;
        proxy_cache_valid 200 60m;   # 对状态码200的响应缓存60分钟

        # 设置静态文件的缓存控制，浏览器缓存控制
        expires 7d;

        # 添加响应头部
        add_header X-Cache-Status $upstream_cache_status;

        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_pass http://127.0.0.1:50002;
    }
    # GLOBAL-CACHE END


}
```
