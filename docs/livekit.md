使用 nginx搭建 语音聊天代理地址
```
cd /etc/nginx/conf.d/ && vi webrtc.conf (贴以下配置)
```

使用 cloudflare 小黄云代理，则无需 https。

```
server {
    listen              80;
    server_name webrtc.example.cn; // 替换自己域名


    location / {
        proxy_pass https://webrtc.chatgpt.com;
        proxy_set_header Host webrtc.chatgpt.com;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header REMOTE-HOST $remote_addr;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        add_header X-Cache $upstream_cache_status;
        add_header Cache-Control no-cache;
        proxy_ssl_server_name on;
    }
}
```

## 配置环境变量

```bash
$ vi .env

VOICE_PROXY_URL=webrtc.example.cn # 替换自己域名
```
