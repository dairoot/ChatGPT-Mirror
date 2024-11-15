<template>
  <t-table
    :data="tableChatgptDetailsData"
    :columns="columnsChatgptDetails"
    row-key="chatgpt_username"
    :loading="tableLoading"
    bordered
    hover
  >
    <template #auth_status="{ row }">
      <t-tag v-if="row.auth_status === false" theme="danger" variant="light"> 已过期 </t-tag>
      <t-tag v-if="row.auth_status === true" theme="success" variant="light"> 运行中 </t-tag>
    </template>

    <template #op="slotProps">
      <t-link theme="primary" @click="handleCopyUrl(slotProps.row.mirror_token)"> 复制</t-link>
    </template>
  </t-table>
</template>

<script setup lang="ts">
import { MessagePlugin, TableProps } from 'tdesign-vue-next';
import { ref } from 'vue';

import RequestApi from '@/api/request';

interface TableChatgptDetailsData {
  mirror_token: string;
  chatgpt_username: string;
  plan_type: string;
}

const tableLoading = ref(false);
const tableChatgptDetailsData = ref<TableChatgptDetailsData[]>([]);

const columnsChatgptDetails: TableProps['columns'] = [
  { colKey: 'chatgpt_username', title: 'ChatGPT', width: 80 },
  { colKey: 'plan_type', title: '类型', width: 30 },
  { colKey: 'auth_status', title: '状态', width: 30 },
  { colKey: 'mirror_token', title: 'Mirror Token (用于 API, 该token不会变更)', width: 100 },
  { colKey: 'op', title: '免登链接', width: 30 },
];

const getChatGPTDetails = async (user: any) => {
  tableLoading.value = true;
  const GptDetailsUri = `/0x/user/get-mirror-token?user_id=${user.id}`;
  const response = await RequestApi(GptDetailsUri);
  const data = await response.json();
  tableChatgptDetailsData.value = data;
  tableLoading.value = false;
  console.log(data);
};

const handleCopyUrl = (mirrorToken: string) => {
  const notLoginUrl = `${window.location.origin}/api/not-login?user_gateway_token=${mirrorToken}`;
  navigator.clipboard.writeText(notLoginUrl);
  MessagePlugin.success('复制成功');
};

defineExpose({
  getChatGPTDetails,
});
</script>
