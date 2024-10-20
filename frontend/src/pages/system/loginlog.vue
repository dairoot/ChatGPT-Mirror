<template>
  <div>
    <t-card class="list-card-container">
      <t-table
        :data="tableData"
        :columns="columns"
        rowKey="id"
        :loading="tableLoading"
        :pagination="pagination"
        @page-change="rehandlePageChange"
      >
        <template #created_at="{ row }">
          {{ TimestampToDate(row.created_at * 1000) }}
        </template>
        <template #user_agent="{ row }">
          {{ parseUserAgent(row.user_agent) }}
        </template>
      </t-table>
    </t-card>
  </div>
</template>

<script setup lang="ts">
// eslint-disable-next-line import/no-duplicates

import { TableProps } from 'tdesign-vue-next';
import UAParser from 'ua-parser-js';
import { onMounted, ref } from 'vue';

import RequestApi from '@/api/request';
import { TimestampToDate } from '@/utils/date';

interface TableData {
  username: string;
  ip: string;
  country: string;
  created_at: number;
  user_agent: string;
}
const pagination = {
  defaultPageSize: 20,
  total: 0,
  defaultCurrent: 1,
};

const tableLoading = ref(false);
const tableData = ref<TableData[]>([]);
const columns: TableProps['columns'] = [
  { colKey: 'username', title: '用户名', width: 200 },
  { colKey: 'chatgpt_username', title: 'ChatGPT', width: 200 },
  { colKey: 'ip', title: 'IP', width: 200 },
  // { colKey: 'country', title: '国家/地区', width: 100 },
  { colKey: 'log_type', title: '操作类型', width: 200 },
  { colKey: 'created_at', title: '操作时间', width: 200 },
  { colKey: 'user_agent', title: '操作设备', width: 250 },
];
const VisitLogUri = '/0x/user/visit-log';

onMounted(async () => {
  await getVisitList();
});

const parseUserAgent = (userAgent: string) => {
  const parser = new UAParser();
  parser.setUA(userAgent);
  const u: any = parser.getResult();

  const deviceInfo = `${u.browser.name}  ${u.os.name.replace(/\s+/g, '')} ${u.os.version}`;

  return deviceInfo;
};
const rehandlePageChange = (curr: any) => {
  pagination.defaultCurrent = curr.current;
  pagination.defaultPageSize = curr.pageSize;
  getVisitList();
};

const getVisitList = async () => {
  tableLoading.value = true;
  const params: any = {
    page: pagination.defaultCurrent,
    page_size: pagination.defaultPageSize,
  };

  const queryString = new URLSearchParams(params).toString();
  const response = await RequestApi(`${VisitLogUri}?${queryString}`);

  const data = await response.json();
  pagination.total = data.count;
  tableData.value = data.results;
  tableLoading.value = false;
};
</script>
<style scoped></style>
