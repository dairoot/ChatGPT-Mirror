<template>
  <div>
    <t-dialog
      :visible="tableVisible"
      header="请选择 ChatGPT 账号"
      :cancel-btn="null"
      :confirm-btn="null"
      :on-close="onClose"
      width="930px"
    >
      <t-loading :loading="tableLoading">
        <t-space break-line>
          <div
            v-for="item in tableData"
            :key="item.id"
            style="width: 160px; cursor: pointer"
            :class="{ 'is-disabled': !item.auth_status }"
            @click="onSelect(item.id)"
          >
            <div style="background: #f2f4f7; padding: 8px; border-radius: 5px">
              <t-space direction="vertical" style="width: 100%" :size="8">
                <div>
                  <div style="display: flex; justify-content: space-between">
                    <t-tag
                      size="small"
                      theme="primary"
                      variant="outline"
                      style="width: 35px"
                      :class="{ 'shiny-blue': item.plan_type !== 'free' }"
                      >{{ item.plan_type }}</t-tag
                    >
                    <span>{{ item.chatgpt_flag }} </span>
                  </div>
                </div>

                <div style="font-size: 12px; display: flex; justify-content: space-between">
                  <div>实时状态</div>
                  <div>
                    <span v-if="item.auth_status === false"> 已过期 </span>
                    <span v-else-if="getGPTUsePercent(item) < 40"> 空闲 </span>
                    <span v-else-if="getGPTUsePercent(item) < 80"> 忙碌 </span>
                    <span v-else> 繁忙 | 可用 </span>
                  </div>
                </div>

                <div>
                  <t-progress
                    v-if="getGPTUsePercent(item) < 40"
                    :percentage="getGPTUsePercent(item)"
                    status="success"
                    :label="false"
                  />
                  <t-progress
                    v-else-if="getGPTUsePercent(item) < 80"
                    :percentage="getGPTUsePercent(item)"
                    status="warning"
                    :label="false"
                  />
                  <t-progress v-else :percentage="getGPTUsePercent(item)" status="error" :label="false" />
                </div>

                <div></div>
              </t-space>
            </div>
          </div>
        </t-space>

        <!-- <t-list class="list-block" split>
          <t-list-item
            v-for="item in tableData"
            :key="item.id"
            @click="onSelect(item.id)"
            :class="{ 'is-disabled': !item.auth_status }"
          >
            <t-list-item-meta>
              <template #description>
                <t-space>
                  <t-tag theme="primary" variant="outline" style="width: 40px">{{ item.plan_type }}</t-tag>
                  {{ item.chatgpt_flag }}
                </t-space>
              </template>
            </t-list-item-meta>

            <template #action>
              <div>
                <t-tag v-if="item.auth_status === false" theme="danger" variant="light"> 已过期 </t-tag>
                <t-tag v-else-if="item.use_count.last_1h + item.use_count.last_2h + item.use_count.last_3h < 20" theme="success" variant="light"> 空闲 </t-tag>
                <t-tag v-else theme="warning" variant="light"> 繁忙 </t-tag>
              </div>
            </template>
          </t-list-item>
      </t-list> -->
      </t-loading>
    </t-dialog>
  </div>
</template>

<script setup lang="ts">
import dayjs from 'dayjs';
import Cookies from 'js-cookie';
import { MessagePlugin } from 'tdesign-vue-next';
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

import RequestApi from '@/api/request';

const tableLoading = ref(false);
const router = useRouter();
const tableVisible = ref(false);

interface TableData {
  id: number;
  chatgpt_flag: string;
  plan_type: string;
  auth_status: boolean;
  use_count: any;
}
const tableData = ref<TableData[]>([]);

onMounted(async () => {
  await getUserChatGPTAccountList();
});

const getGPTUsePercent = (item: any) => {
  const MaxLimitCount: number = item.plan_type === 'free' ? 20 : 80;
  return Math.min((item.use_count / MaxLimitCount) * 100 + 1, 99);
};
const getUserChatGPTAccountList = async () => {
  // 获取 用户 ChatGPT 账号列表
  tableLoading.value = true;
  const response = await RequestApi('/0x/user/chatgpt-list');

  const data = await response.json();
  tableLoading.value = false;
  if (data.results.length === 1 && data.results[0].auth_status) {
    onSelect(data.results[0].id);
  } else {
    tableVisible.value = true;
    tableData.value = data.results;
  }
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
.is-disabled {
  pointer-events: none;
  /* Prevent interaction */
  opacity: 0.5;
  /* Optional: Make the item look visually disabled */
}

.shiny-blue {
  box-shadow:
    0 0 1px rgba(0, 123, 255, 0.5),
    0 0 20px rgba(0, 123, 255, 0.3);
}
</style>
