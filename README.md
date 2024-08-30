<h1 align="center">ChatGPT Mirror</h1>

[![Docker](https://img.shields.io/docker/pulls/dairoot/chatgpt-mirror?label=ChatGPT-Mirror&logo=docker)](https://hub.docker.com/r/dairoot/chatgpt-mirror)
[![License](https://img.shields.io/github/license/dairoot/ChatGPT-Mirror)](https://github.com/dairoot/ChatGPT-Mirror/blob/main/LICENSE)

ChatGPT Mirror 后台是一个 ChatGPT 镜像站，允许多账号共享管理。实现多人同时使用 ChatGPT 服务。

## 特点

- 提供与官网同等的极致体验。
- 提供 ChatGPT 聊天接口 转 API `/v1/chat/completions`
- 用户无需翻墙，便可轻松访问并使用 ChatGPT 官方网站的所有功能。
- 通过在 `Mirror` 后台录入 `ChatGPT Token`，让团队成员每人拥有独立账号 (或共享同一个`ChatGPT Plus`账号)。
- 提供便捷的管理后台，帮助管理员高效管理账号。

## 在线体验

https://chatgpt.dairoot.cn

为了获得最佳体验，请先观看以下视频教程

https://github.com/user-attachments/assets/7b868672-cfaf-430c-9ec4-f1617a428225

<!--
<a href="https://www.bilibili.com/video/BV1fD421M7xP/" target="_blank">
  <img src="./docs/img/cover.jpeg"  alt="使用方法">
</a>
-->

## 部署

### 1. 本地运行

```bash
# 本地需要翻墙

docker pull dairoot/chatgpt-mirror

docker run -p 50001:50001 -p 443:443 \
   -e ADMIN_USERNAME=dairoot \
   -e ADMIN_PASSWORD=dairoot \
   dairoot/chatgpt-mirror

访问: https://localhost
```

### 2. 部署到服务器（海外 vps）

```bash
# 切换到 home 目录，并克隆 ChatGPT-Mirror 仓库
cd /home/ && git clone https://github.com/dairoot/ChatGPT-Mirror.git

cd ChatGPT-Mirror/

cp .env.example .env && vi .env # 修改管理后台账号密码

docker compose pull # 拉取镜像

docker compose up -d # 后台运行
```

若需要配置 ChatGPT 聊天页面，请点击查看[完整部署流程](./docs/deploy.md)

### 3. 使用 Zeabur 部署 （免服务器）

管理后台 默认账号密码为：dairoot

在 `Zeabur` 后台修改环境变量，即可更改 管理后台 账号密码

[![Deploy on Zeabur](https://zeabur.com/button.svg)](https://zeabur.com/templates/ZEUVRY?referralCode=dairoot)

---

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
    <td rowspan="3">管理后台</td>
    <td><code>ADMIN_USERNAME</code></td>
    <td><code>String</code></td>
    <td><code>None</code></td>
    <td>管理后台账号</td>
  </tr>
  <tr align="left">
    <td><code>ADMIN_PASSWORD</code></td>
    <td><code>String</code></td>
    <td><code>None</code></td>
    <td>管理后台密码</td>
  </tr>
    <tr align="left">
    <td><code>USE_SERVER_RENDER</code></td>
    <td><code>Boolean</code></td>
    <td><code>false</code></td>
    <td>服务端托管 Proofofwork</td>
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
    <td><code>String</code></td>
    <td><code>None</code></td>
    <td>API 访问前缀，建议配置</td>
  </tr>
  <tr align="left">
    <td><code>HATD</code></td>
    <td><code>Boolean</code></td>
    <td><code>false</code></td>
    <td>开启临时聊天（不保存聊天记录）</td>
  </tr>
   <tr align="left">
    <td rowspan="3">系统变量</td>
    <td><code>HTTP_PROXY</code></td>
    <td><code>String</code></td>
    <td><code>None</code></td>
    <td>http 代理地址</td>
  </tr>
  <tr align="left">
    <td><code>SOCKS5_PROXY</code></td>
    <td><code>String</code></td>
    <td><code>None</code></td>
    <td>socks5 代理地址</td>
  </tr>
</table>

## 聊天 API 接口

可搭配 [ChatGPT-Next-Web](https://app.nextchat.dev)、[Lobe-Chat](https://github.com/lobehub/lobe-chat) 使用

```
accessToken 获取地址：https://chatgpt.com/api/auth/session

API 地址为：https://你的域名/上述环境变量配置的MIRROR_API_PREFIX
```

参数详情
| 字段 | 类型 | 默认值 | 必填 | 描述 |
| --- | --- | --- |--- |--- |
| `model` | `string` | `None` | `是` |模型名称 <br> `gpt-4o-mini` `gpt-4o` `gpt-4` `gpt-4-mobile`|
| `messages` | `array` | `None` | `是` |消息内容 |
| `stream` | `boolean` | `None` | `是` |是否流式返回 |
| `conversation_id` | `string` |`自动匹配` | `否` | 会话 ID |
| `parent_message_id` | `string` |`自动匹配` | `否` | 父消息 ID |
| `hatd` | `boolean` |`默认同环境变量` | `否` | 同上述环境变量的 `HATD` |

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
     "stream": true,
     "conversation_id": null,
     "parent_message_id": null,
     "hatd": false
   }'
```

## FQA

[简体中文 > 常见问题](./docs/faq-cn.md)

## 加入群聊

[Telegram](https://t.me/+34aYksZdq5ZhMzhl)

## 捐赠

[Buy Me a Coffee](./docs/donation.md)

## Star History

![Star History Chart](https://api.star-history.com/svg?repos=dairoot/ChatGPT-Mirror&type=Timeline)
