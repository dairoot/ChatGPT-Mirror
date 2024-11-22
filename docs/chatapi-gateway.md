## 自建网关 API

如果只需使用API，或希望重新开发管理后台，可选择仅部署网关服务。

```
docker run -p 50002:8787 dairoot/chatgpt-gateway:latest
```

## 环境变量

| 变量名| 类型	| 默认值	| 描述| 
| --- | --- | --- |--- |
| `ADMIN_PASSWORD` |	`String`	|`None`|	API请求秘钥 |
| `ENABLE_MIRROR_API` |	`Boolean`	|`true`	| 是否开启 API 访问|
| `MIRROR_API_PREFIX` |	`String`	|`None` |	API 访问前缀，建议配置|
| `HATD` |	`Boolean`	|`false`|	开启临时聊天（不保存聊天记录）|
| `PROXY_URL_POOL` |	`String`	|`None`|	代理池链接，多个代理用逗号分隔 <br> `http://username@password@ip:port,` <br> `socks5://username@password@ip:port`|
| `VOICE_PROXY_URL` | `String` | `None` | 语音代理地址 [点击自建](./docs/livekit.md)<br>若不配置，则用户需要翻墙才能使用语音功能|

## API

### 聊天 API
POST: /v1/chat/completions

- 请求头：
  | 字段 | 类型 | 默认值 | 必填 | 描述 |
  | --- | --- | --- |--- |--- |
  | `Authorization` | `string` | `None` | `是` |`Bearer ${`[Access Token](https://chatgpt.com/api/auth/session)`}` 或者<br>  `Bearer ${Mirror Token}` |
  | `Chatgpt-Account-Id` | `string` | `None` | `否` | Team 账号 ID |

- 提交参数：
  | 字段 | 类型 | 默认值 | 必填 | 描述 |
  | --- | --- | --- |--- |--- |
  | `model` | `string` | `None` | `是` |模型名称 <br> `gpt-4o-mini` `gpt-4o` `gpt-4` `gpt-4-mobile` <br> `o1-mini` `o1-preview`|
  | `messages` | `array` | `None` | `是` |消息内容 |
  | `stream` | `boolean` | `None` | `是` |是否流式返回 |
  | `conversation_id` | `string` |`自动匹配` | `否` | 会话 ID |
  | `parent_message_id` | `string` |`自动匹配` | `否` | 父消息 ID |
  | `hatd` | `boolean` |`默认同环境变量` | `否` | 开启临时聊天（不保存聊天记录）<br> 同上述环境变量的 `HATD` |


### 语音聊天
GET: /api/livekit

- 请求头：
  | 字段 | 类型 | 描述 |
  | ----- | ------ | ----------------------- |
  | `Authorization` | `string` | `Bearer ${环境变量的 ADMIN_PASSWORD}` |



### 登录 
参数详情请参考网关服务的 admin 登录页面

POST: /api/login

- 请求头：
  | 字段 | 类型 | 描述 |
  | ----- | ------ | ----------------------- |
  | `Authorization` | `string` | `Bearer ${环境变量的 ADMIN_PASSWORD}` |


- 请求参数
  | 字段 | 类型 | 描述 |
  | ----- | ------ | ----------------------- |
  | `access_token` | `string` | 仅支持 [Access Token](https://chatgpt.com/api/auth/session)  |
  | `limits` | `obj[]` | 模型限制 |
  | `user_name` | `string` | 用户名称 |
  | `isolated_session` | `bool` | 独立会话 |



### 获取长期有效 Mirror Token

`Mirror Token` 是一个固定值，不会发生变更，用于映射最新的 `Access Token` 以进行 API 访问。

因此，`Mirror Token` 本身不会过期，除非最新的 `Access Token` 失效。

POST: /api/get-mirror-token

- 请求头：
  | 字段 | 类型 | 描述 |
  | ----- | ------ | ----------------------- |
  | `Authorization` | `string` | `Bearer ${环境变量的 ADMIN_PASSWORD}` |

- 请求参数
  | 字段 | 类型 | 描述 |
  | ----- | ------ | ----------------------- |
  | `user_name` | `string` |  用户名称 |
  | `isolated_session` | `bool` | 独立会话 |
  | `limits` | `obj[]` | 模型限制 |
  | `chatgpt_list` | `string[]` | ChatGPT 登录邮箱列表 |


### 获取 ChatGPT 账号信息 

作用于 token 录入 和 刷新

POST: /api/get-user-info

- 请求头：
  | 字段 | 类型 | 描述 |
  | ----- | ------ | ----------------------- |
  | `Authorization` | `string` | `Bearer ${环境变量的 ADMIN_PASSWORD}` |


- 请求参数
  | 字段 | 类型 | 描述 |
  | ----- | ------ | ------------------------------------------------------------------------------ |
  | `chatgpt_token` | `string` | 支持的 token 类型 <br>- [Access Token](https://chatgpt.com/api/auth/session) <br>- [Session Token](https://www.bilibili.com/video/BV1fD421M7xP/?share_source=copy_web&vd_source=4c37761f5ba7612e942a84820f8099f6) <br>- Refresh Token |




### 获取用户使用次数
POST: /api/get-user-use-count
- 请求头：
  | 字段 | 类型 | 描述 |
  | ----- | ------ | ----------------------- |
  | `Authorization` | `string` | `Bearer ${环境变量的 ADMIN_PASSWORD}` |


- 请求参数
  | 字段 | 类型 | 描述 |
  | ----- | ------ | ----------------------- |
  | `username_list` | `string[]` | 用户列表 |



### 获取 ChatGPT 使用次数
POST: /api/get-chatgpt-use-count
- 请求头：
  | 字段 | 类型 | 描述 |
  | ----- | ------ | ----------------------- |
  | `Authorization` | `string` | `Bearer ${环境变量的 ADMIN_PASSWORD}` |


- 请求参数
  | 字段 | 类型 | 描述 |
  | ----- | ------ | ----------------------- |
  | `chatgpt_list` | `string[]` | ChatGPT 登录邮箱列表 |


### 免登地址
GET: /api/not-login?user_gateway_token=<mirror_token>




## 鸣谢
感谢 [rquest](https://github.com/penumbra-x/rquest/tree/main) 项目作者。
