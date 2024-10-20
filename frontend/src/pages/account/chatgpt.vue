<template>
  <div>
    <t-card class="list-card-container">
      <t-row justify="space-between">
        <div class="left-operation-container">
          <t-button @click="showDialog = true">录入</t-button>

          <p v-if="!!selectedRowKeys.length" class="selected-count">
            {{ $t('pages.listBase.select') }} {{ selectedRowKeys.length }} {{ $t('pages.listBase.items') }}
          </p>
        </div>
      </t-row>
      <t-table
        :data="tableData"
        :columns="columns"
        row-key="chatgpt_username"
        :loading="tableLoading"
        :selected-row-keys="selectedRowKeys"
        bordered
        hover
        :pagination="pagination"
        @select-change="onSelectChange"
        @page-change="rehandlePageChange"
      >
        <template #auth_status="{ row }">
          <t-tag v-if="row.auth_status === false" theme="danger" variant="light"> 已过期 </t-tag>
          <t-tag v-if="row.auth_status === true" theme="success" variant="light"> 运行中 </t-tag>
        </template>

        <template #expires_at="{ row }">
          {{ TimestampToDate(row.expires_at) }}
        </template>

        <template #updated_at="{ row }">
          {{ TimestampToDate(row.updated_at) }}
        </template>

        <template #access_token_exp="{ row }">
          {{ TimestampToDate(row.access_token_exp * 1000) }}
        </template>

        <template #created_time="{ row }">
          {{ TimestampToDate(row.created_time * 1000) }}
        </template>

        <template #op="slotProps">
          <t-space>
            <!-- <t-link theme="primary" @click="handleUpdate(slotProps.row)">更新</t-link> -->
            <t-link theme="primary" @click="handleEdit(slotProps.row)">编辑</t-link>

            <t-link theme="danger" @click="handleClickDelete(slotProps.row)">删除</t-link>
          </t-space>
        </template>
      </t-table>

      <!-- 录入 Token dialog -->
      <t-dialog v-model:visible="showDialog" header="录入 ChatGPT Token" width="50%" :on-confirm="handleAdd">
        <t-form v-loading="loading" :data="newChat" :label-width="0">
          <t-form-item label="Token">
            <div style="display: flex; flex-direction: column; width: 100%">
              <t-textarea
                v-model="newChat.chatgpt_token"
                :autosize="{ minRows: 5, maxRows: 5 }"
                autofocus
                size="large"
                placeholder="请输入 Access Token 或 Session Token 或 Refresh Token。一行一串Token，多个Token请换行输入。"
              ></t-textarea>
              <span style="font-size: 12px; color: #888">
                <t-link target="_blank" theme="primary" size="small" href="https://chatgpt.com/api/auth/session">
                  Access Token</t-link
                >：有效期10天
              </span>
              <span style="font-size: 12px; color: #888">
                <t-link target="_blank" theme="primary" size="small" :href="ChatgptTokenTutorialUrl"
                  >Session Token</t-link
                >：有效期30天
                <!-- or
                <t-link target="_blank" theme="primary" size="small" :href="ChatgptTokenAuthUrl">自动获取</t-link> -->
              </span>
            </div>
          </t-form-item>
        </t-form>
      </t-dialog>

      <!-- 编辑 备注信息 -->
      <t-dialog v-model:visible="dialogVisibleEdit" header="编辑信息" width="50%" :on-confirm="handleEditConfirm">
        <t-form v-loading="loading" :data="editChatInfo" :label-width="120">
          <t-form-item label="备注信息">
            <t-input v-model="editChatInfo.remark" size="large" placeholder="备注信息"></t-input>
          </t-form-item>
        </t-form>
      </t-dialog>

      <!-- 确认删除 dialog -->
      <t-dialog
        v-model:visible="dialogVisibleDelete"
        header="确认删除该 ChatGPT token 吗"
        width="600"
        :on-confirm="handleDelete"
      >
      </t-dialog>
    </t-card>
  </div>
</template>

<script setup lang="ts">
import { MessagePlugin, TableProps } from 'tdesign-vue-next';
import { onMounted, ref } from 'vue';

import RequestApi from '@/api/request';
import { ChatgptTokenTutorialUrl } from '@/constants/index';
import { TimestampToDate } from '@/utils/date';

interface TableData {
  username: string;
  status: number;
  plan_type: string;
  // expires_at: number;
  updated_at: number;
  access_token_exp: number;
}
const selectedRowKeys = ref<TableProps['selectedRowKeys']>([]);
const loading = ref(false);
const tableLoading = ref(false);
const tableData = ref<TableData[]>([]);

const pagination = {
  defaultPageSize: 20,
  total: 0,
  defaultCurrent: 1,
};

const rehandlePageChange = (curr: any) => {
  pagination.defaultCurrent = curr.current;
  pagination.defaultPageSize = curr.pageSize;
  getChatGPTList();
};

const columns: TableProps['columns'] = [
  { colKey: 'row-select', type: 'multiple' },
  { colKey: 'chatgpt_username', title: 'ChatGPT 账号', width: 220 },
  { colKey: 'auth_status', title: '状态', width: 100 },
  { colKey: 'plan_type', title: '类型', width: 100 },
  { colKey: 'access_token_exp', title: 'Access Token 过期时间', width: 200 },
  { colKey: 'created_time', title: '创建时间', width: 200 },
  // { colKey: 'updated_at', title: '最近更新时间', width: 200 },
  { colKey: 'remark', title: '备注' },
  { width: 200, colKey: 'op', title: '操作' },
];
const showDialog = ref(false);
const dialogVisibleDelete = ref(false);
const usernameDelete = ref('');
const dialogVisibleEdit = ref(false);

const newChat = ref({ chatgpt_token: '', remark: '' });
const editChatInfo = ref({ remark: '', chatgpt_username: '' });

const ChatgptTokenUrl = '/0x/chatgpt/';

onMounted(async () => {
  await getChatGPTList();
});

const getChatGPTList = async () => {
  // 发送请求获取 Token 列表
  tableLoading.value = true;
  const params: any = {
    page: pagination.defaultCurrent,
    page_size: pagination.defaultPageSize,
  };

  const queryString = new URLSearchParams(params).toString();
  const response = await RequestApi(`${ChatgptTokenUrl}?${queryString}`);

  const data = await response.json();
  // console.log('results', data.results);
  tableData.value = data.results;
  pagination.total = data.count;

  tableLoading.value = false;
};

const addChatToken = async () => {
  // 发送请求添加 Token
  loading.value = true;

  const response = await RequestApi(ChatgptTokenUrl, 'POST', {
    chatgpt_token_list: newChat.value.chatgpt_token.split('\n'),
  });

  const data = await response.json();
  loading.value = false;

  if (response.status !== 200) {
    MessagePlugin.error(JSON.stringify(Object.values(data)[0]));

    if (data.message.includes('status: 403')) {
      window.location.href = '/';
    }
  } else {
    showDialog.value = false;
    await getChatGPTList();
    newChat.value.chatgpt_token = '';
    MessagePlugin.success('新增成功');
  }
};

const handleEdit = (row: any) => {
  console.log('row', row.remark);
  editChatInfo.value = { ...row };

  dialogVisibleEdit.value = true;
};

const handleClickDelete = (row: any) => {
  usernameDelete.value = row.chatgpt_username;
  dialogVisibleDelete.value = true;
};

const handleDelete = async () => {
  const response = await RequestApi(ChatgptTokenUrl, 'DELETE', { chatgpt_username: usernameDelete.value });

  const data = await response.json();
  dialogVisibleDelete.value = false;
  usernameDelete.value = '';

  if (response.status !== 200) {
    MessagePlugin.error(JSON.stringify(Object.values(data)[0]));
  } else {
    await getChatGPTList();
    MessagePlugin.success('删除成功');
  }
};

const handleAdd = () => {
  if (newChat.value.chatgpt_token.trim() === '') {
    MessagePlugin.error('Token 不能为空');
  } else {
    addChatToken();
  }
};

const onSelectChange: TableProps['onSelectChange'] = (value, _) => {
  selectedRowKeys.value = value;
  // console.log(value, ctx);
};

const handleEditConfirm = async () => {
  await RequestApi(ChatgptTokenUrl, 'PUT', {
    remark: editChatInfo.value.remark,
    chatgpt_username: editChatInfo.value.chatgpt_username,
  });
  await getChatGPTList();
  MessagePlugin.success('修改成功');
  dialogVisibleEdit.value = false;
};
</script>

<style lang="less" scoped>
.left-operation-container {
  padding: 6px 0;
  margin-bottom: 16px;

  .selected-count {
    display: inline-block;
    margin-left: 8px;
    color: var(--td-text-color-secondary);
  }
}
</style>
