# 常见问题
--- 
## 一、 为什么录入 Token 会显示403

```
chatgpt.com
正在验证您是否是真人。这可能需要几秒钟时间。
```

### 以下四个方案，多试试，总有一个方案适合你

### 方案一. 更换服务器 IP 解决（简单方便）
[腾讯云](https://curl.qcloud.com/0JAXkoF1) 选择欧美区域

### 方案二. 使用 warp 代理（不一定能成功）

centos 7 可能无法安装 warp，请使用更高级系统版本

##### 安装并启动 warp

```bash
docker compose -f docker-compose-warp.yml up
# 验证局部模式的 warp 是否安装成功，如果 warp=off 则 warp 安装失败
curl -s --socks5-hostname 127.0.0.1:1080 https://cloudflare.com/cdn-cgi/trace |grep warp
```

##### 设置warp代理，并启动程序
```bash
vi .env

PROXY_URL_POOL=socks5://warp:1080

./deploy.sh
```
查看代理配置是否有效

```bash
curl  http://127.0.0.1:50002/api/check-proxy?admin_password=环境变量中的ADMIN_PASSWORD

```

如果代理状态为200，则为成功


### 方案三. 使用代理池
```bash
vi .env

# 多个代理地址，用逗号隔开

PROXY_URL_POOL=http://username@password@ip:port,socks5://username@password@ip:port

./deploy.sh
```
查看代理配置是否有效（同warp验证流程）

### 方案四. 脚本过盾
```bash
docker compose -f docker-compose-cf5s.yml up
```


--- 

## 二、 为什么向 ChatGPT 提问时无法解析 URL 链接和文件，而官网可以

这是由于 IP 受到 ChatGPT 降智，可以通过更换 IP 解决。或者尝试发送一张照片，激活chatgpt功能。

--- 

## 三、 为什么向 ChatGPT 提问会出现验证码

- 验证码通常情况下只会出现一次。

- 使用付费的 [capsolver](https://dashboard.capsolver.com/passport/register?inviteCode=GT8NyMFVF0bG) 方案（待接入）
