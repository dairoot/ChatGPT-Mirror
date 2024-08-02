<h1 align="center">ChatGPT Mirror</h1>

[![Docker](https://img.shields.io/docker/pulls/dairoot/chatgpt-mirror?label=ChatGPT-Mirror&logo=docker)](https://hub.docker.com/r/dairoot/chatgpt-mirror)
[![License](https://img.shields.io/github/license/dairoot/ChatGPT-Mirror)](https://github.com/dairoot/ChatGPT-Mirror/blob/main/LICENSE)

ChatGPT Mirror 后台是一个 ChatGPT 镜像网站，允许多账号共享管理。实现多人同时使用 ChatGPT 服务。

## 特点

- 提供与官网同等的极致体验。
- 提供 ChatGPT 聊天接口 转 API `/v1/chat/completions`
- 用户无需翻墙，便可轻松访问并使用 ChatGPT 官方网站的所有功能。
- 通过在 `Mirror` 后台录入 `ChatGPT Token`，让团队成员每人拥有独立账号 (或共享同一个`ChatGPT Plus`账号)。
- 提供便捷的管理后台，帮助管理员高效管理账号。

## 在线体验

https://chatgpt.dairoot.cn

- 账号：dairoot
- 密码：dairoot

为了获得最佳体验，请先观看以下视频教程

https://github.com/user-attachments/assets/7b868672-cfaf-430c-9ec4-f1617a428225

<!--
<a href="https://www.bilibili.com/video/BV1fD421M7xP/" target="_blank">
  <img src="./docs/img/cover.jpeg"  alt="使用方法">
</a>
-->

## 本地运行

```bash
# 本地需要翻墙
git clone https://github.com/dairoot/ChatGPT-Mirror.git

cd ChatGPT-Mirror/

docker pull dairoot/chatgpt-mirror

docker run -p 50001:50001 \
   -e ADMIN_USERNAME=usernamexxx \
   -e ADMIN_PASSWORD=passwordxxx \
   -v ./admin/dist:/tmp/dist \
   dairoot/chatgpt-mirror

caddy run --config ./Caddyfile --watch

访问: https://localhost/
```

## 部署到服务器（海外 vps）

#### 1. 运行

```bash
# 切换到 home 目录，并克隆 ChatGPT-Mirror 仓库
cd /home/ && git clone https://github.com/dairoot/ChatGPT-Mirror.git

cd ChatGPT-Mirror/

cp .env.example .env && vi .env # 修改管理后台账号密码

docker compose pull # 拉取镜像

docker compose up -d # 后台运行
```

#### 2. 若需要配置 ChatGPT 聊天页面，请点击查看[完整部署流程](./docs/deploy.md)

## 环境变量

<table>
  <tr align="left">
    <th>分类</th>
    <th>变量名</th>
    <th>类型</th>
    <th>默认值</th>
    <th>描述</th>
  </tr>
  <tr align="left">
    <td rowspan="2">管理后台</td>
    <td><code>ADMIN_USERNAME</code></td>
    <td><code>string</code></td>
    <td><code>None</code></td>
    <td>管理后台账号</td>
  </tr>
  <tr align="left">
    <td><code>ADMIN_PASSWORD</code></td>
    <td><code>string</code></td>
    <td><code>None</code></td>
    <td>管理后台密码</td>
  </tr>
  <tr align="left">
    <td rowspan="3">API 相关</td>
    <td><code>ENABLE_MIRROR_API</code></td>
    <td><code>Boolean</code></td>
    <td><code>true</code></td>
    <td>是否开启 API 访问</td>
  </tr>
  <tr align="left">
    <td><code>MIRROR_API_PREFIX</code></td>
    <td><code>string</code></td>
    <td><code>None</code></td>
    <td>API 访问秘钥，建议配置避免他人利用</td>
  </tr>
  <tr align="left">
    <td><code>ENABLE_CONTEXT</code></td>
    <td><code>Boolean</code></td>
    <td><code>false</code></td>
    <td>是否开启上下文，生成环境建议开启</td>
  </tr>
</table>

## 聊天 API 接口

| API 模型        | 描述                       |
| --------------- | -------------------------- |
| `gpt-4o-mini`   | ChatGPT 4o mini (推荐使用) |
| `gpt-4o`        | ChatGPT 4o                 |
| `gpt-4`         | ChatGPT 4                  |
| `gpt-4-mobile`  | ChatGPT 手机版本模型       |
| `gpt-3.5-turbo` | ChatGPT 3.5 (即将下线)     |

可搭配 [ChatGPT-Next-Web](https://app.nextchat.dev)、[Lobe-Chat](https://github.com/lobehub/lobe-chat) 使用

```
accessToken 获取地址：https://chatgpt.com/api/auth/session

API 地址为：https://你的域名/上述环境变量配置的MIRROR_API_PREFIX
```

聊天接口请求示例：

```bash
export accessToken=XXXXX  # 获取地址：https://chatgpt.com/api/auth/session
export yourUrl=http://127.0.0.1:50001/上述环境变量配置的MIRROR_API_PREFIX


curl --location "${yourUrl}/v1/chat/completions" \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer ${accessToken}" \
--data '{
     "model": "gpt-4o-mini",
     "messages": [{"role": "user", "content": "你好呀!"}],
     "stream": true
   }'
```

若需指定会话，需要在请求中添加 `conversation_id` 和 `parent_message_id` 字段：

```json
{
  "model": "gpt-4o-mini",
  "messages": [{ "role": "user", "content": "你好呀!" }],
  "stream": true,
  "conversation_id": "5ca8838d-ab10-4e41-90b8-2c7ed546ed44",
  "parent_message_id": "ae10397c-f90d-4ca8-9a4d-0002994e6c31"
}
```

## FQA

[简体中文 > 常见问题](./docs/faq-cn.md)

## 加入群聊

[Telegram](https://t.me/+34aYksZdq5ZhMzhl)

## 捐赠

[Buy Me a Coffee](./docs/donation.md)

## Star History

![Star History Chart](https://api.star-history.com/svg?repos=dairoot/ChatGPT-Mirror&type=Timeline)
