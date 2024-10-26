<template>
  <div>
    <t-dialog :visible="true" header="请选择 ChatGPT 账号" :cancel-btn="null" :confirm-btn="null" :on-close="onClose">
      <t-list class="list-block" split>
        <t-loading :loading="tableLoading">
          <t-list-item v-for="item in tableData" :key="item.id" @click="onSelect(item.id)">
            <t-list-item-meta>
              <template #description>
                <t-space>
                  <t-tag theme="primary" variant="outline">{{ item.plan_type }}</t-tag>
                  <span>{{ item.chatgpt_flag }}</span>
                </t-space>
              </template>
            </t-list-item-meta>
          </t-list-item>
        </t-loading>
      </t-list>
    </t-dialog>
  </div>
</template>

<script setup lang="ts">
import Cookies from 'js-cookie';
import { MessagePlugin } from 'tdesign-vue-next';
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

import RequestApi from '@/api/request';

const tableLoading = ref(false);
const router = useRouter();

interface TableData {
  id: number;
  chatgpt_flag: string;
  plan_type: string;
}
const tableData = ref<TableData[]>([]);

onMounted(async () => {
  await getUserChatGPTAccountList();
});

const getUserChatGPTAccountList = async () => {
  // 获取 用户 ChatGPT 账号列表
  tableLoading.value = true;

  const response = await RequestApi('/0x/user/chatgpt-list');

  const data = await response.json();
  tableData.value = data.results;

  tableLoading.value = false;
};

const onClose = () => {
  router.push({ name: 'login' });
};
const onSelect = async (chatgptId: number) => {
  console.log(chatgptId);
  tableLoading.value = true;
  const response = await RequestApi('/0x/chatgpt/login', 'POST', { chatgpt_id: chatgptId });
  tableLoading.value = false;

  const data = await response.json();
  if (response.status !== 200) {
    MessagePlugin.error(JSON.stringify(Object.values(data)[0]));
  } else {
    Cookies.set('user-gateway-token', data['user-gateway-token'], { expires: 7 });
    MessagePlugin.success('登录成功');
    window.location.href = '/'; // 跳转到首页
  }
};
</script>

<style lang="less" scoped>
.list-block {
  border: 1px solid var(--td-border-level-1-color);
  border-bottom: none;

  .t-list-item:hover {
    background: var(--td-gray-color-2);
    cursor: pointer;
  }
}
</style>
