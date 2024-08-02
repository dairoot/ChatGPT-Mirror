# 常见问题

## 1. 部署好了，访问首页跳转到 `/fe/#/login` ，但页面显示空白

- 请检查反向代理配置，是否正确映射前端目录 `admin/dist` 路径

- 查看该站点的访问日志，根据错误信息进行更改。

- 如果使用 Docker 部署 NGINX，请确保将前端目录正确映射到 Docker 容器内。

- 小白用户可以使用宝塔面板进行部署，具体教程请参考：[如何安装 ChatGPT 镜像](https://dairoot.cn/2024/07/02/install-chatgpt-mirror/)。

## 2. 为什么首页会提示 403

```
正在验证您是否是真人。这可能需要几秒钟时间
验证所用的时间比预期时间长。如果问题仍然存在，请检查您的 Intemnet 连接并刷新页面
```

- 更换服务器 IP 解决
- 使用代理
- 使用 warp

## 3. 为什么向 ChatGPT 提问时无法解析 URL 链接和文件，而官网可以

这是由于 IP 受到 ChatGPT 功能限制，可以通过更换服务器 IP 解决，或者切换本地代理。

## 4. 为什么向 ChatGPT 提问会出现验证码

- 验证码通常情况下只会出现一次。

- 使用付费的 [capsolver](https://dashboard.capsolver.com/passport/register?inviteCode=GT8NyMFVF0bG) 方案（待接入）
