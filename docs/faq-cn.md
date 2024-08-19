# 常见问题

## 一、 为什么首页会提示 403

```
chatgpt.com
正在验证您是否是真人。这可能需要几秒钟时间。
```

1. 更换服务器 IP 解决（简单方便）
2. 使用代理，配置环境变量（HTTP_PROXY、 SOCKS5_PROXY）

```bash
# 验证代理是否有效。启动程序后，核对返回的 ip 是否为代理 ip
curl -s http://127.0.0.1:50001/test?username=管理后台账号
```

3. 使用 warp 代理（不一定能成功）

- 全局模式：手动安装 warp 客户端
  [ygkkk/CFwarp](https://gitlab.com/rwkgyg/CFwarp) 或 [fscarmen/warp-sh](https://github.com/fscarmen/warp-sh)
- 局部模式：使用 docker 安装

```bash
docker compose -f docker-compose-warp.yml up
# 验证局部模式的 warp 是否安装成功，如果 warp=off 则 warp 安装失败
curl -s --socks5-hostname 127.0.0.1:1080 https://cloudflare.com/cdn-cgi/trace |grep warp

```

## 二、 为什么向 ChatGPT 提问时无法解析 URL 链接和文件，而官网可以

这是由于 IP 受到 ChatGPT 功能限制，可以通过更换 IP 解决。

## 三、 为什么向 ChatGPT 提问会出现验证码

- 验证码通常情况下只会出现一次。

- 使用付费的 [capsolver](https://dashboard.capsolver.com/passport/register?inviteCode=GT8NyMFVF0bG) 方案（待接入）
