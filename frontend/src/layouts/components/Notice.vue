<template>
  <t-popup expand-animation placement="bottom-right" trigger="click">
    <template #content>
      <div class="header-msg">
        <div class="header-msg-top">
          <p>{{ $t('layout.notice.title') }}</p>
          <!--           
          <t-button
            v-if="unreadMsg.length > 0"
            class="clear-btn"
            variant="text"
            theme="primary"
            @click="setRead('all')"
            >{{ $t('layout.notice.clear') }}
            </t-button> 
          -->
        </div>
        <t-list v-if="NotictList.length > 0" class="narrow-scrollbar" :split="false">
          <t-list-item
            v-for="(item, index) in NotictList"
            :key="index"
            :class="{ disabled: getReadMsgIDList.includes(item.id) }"
          >
            <div disabled>
              <p class="msg-content" v-html="item.content"></p>
              <p class="msg-type">{{ item.type }}</p>
            </div>
            <p class="msg-time">{{ item.date }}</p>
            <template #action>
              <t-button size="small" variant="outline" @click="setRead(item.id)">
                {{ $t('layout.notice.setRead') }}
              </t-button>
            </template>
          </t-list-item>
        </t-list>

        <div v-else class="empty-list">
          <img src="https://tdesign.gtimg.com/pro-template/personal/nothing.png" alt="空" />
          <p>{{ $t('layout.notice.empty') }}</p>
        </div>
      </div>
    </template>
    <t-badge :count="unreadMsgCount" :offset="[4, 4]">
      <t-button theme="default" shape="square" variant="text">
        <t-icon name="mail" />
      </t-button>
    </t-badge>
  </t-popup>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia';
import { computed, onMounted, ref } from 'vue';

import RequestApi from '@/api/request';
import { useNotificationStore } from '@/store';

const NotictList = ref([]);
const store = useNotificationStore();
const { getReadMsgIDList } = storeToRefs(store);

const readMsgIDList = new Set(getReadMsgIDList.value);

const unreadMsgCount = computed(() => {
  // 获取未读消息数量
  const unreadMsgIDList = [];
  NotictList.value.forEach((item) => {
    if (!getReadMsgIDList.value.includes(item.id)) {
      unreadMsgIDList.push(item.id);
    }
  });
  return unreadMsgIDList.length;
});

const getNoticeList = async () => {
  // 获取消息列表
  // const res1 = await RequestApi('/api/mirror-version');
  // const data1 = await res1.json();
  // console.log(data1.data1);

  const res2 = await fetch('https://notice.dairoot.cn/notice-list', {
    method: 'POST',
    body: JSON.stringify({}),
    headers: { 'Content-Type': 'application/json' },
  });
  const data2 = await res2.json();
  NotictList.value = data2;
};

onMounted(async () => {
  await getNoticeList();
});

const setRead = (msgId: Number) => {
  readMsgIDList.add(msgId);
  store.setReadMsgIDList(Array.from(readMsgIDList));
};
</script>

<style lang="less" scoped>
.disabled {
  pointer-events: none;
  opacity: 0.5;
}

.header-msg {
  width: 400px;
  // height: 440px;
  margin: calc(0px - var(--td-comp-paddingTB-xs)) calc(0px - var(--td-comp-paddingLR-s));

  .empty-list {
    // height: calc(100% - 120px);
    text-align: center;
    padding: var(--td-comp-paddingTB-xxl) 0;
    font: var(--td-font-body-medium);
    color: var(--td-text-color-secondary);

    img {
      width: var(--td-comp-size-xxxxl);
    }

    p {
      margin-top: var(--td-comp-margin-xs);
    }
  }

  &-top {
    position: relative;
    font: var(--td-font-title-medium);
    color: var(--td-text-color-primary);
    text-align: left;
    padding: var(--td-comp-paddingTB-l) var(--td-comp-paddingLR-xl) 0;
    display: flex;
    align-items: center;
    justify-content: space-between;

    .clear-btn {
      right: calc(var(--td-comp-paddingTB-l) - var(--td-comp-paddingLR-xl));
    }
  }

  &-bottom {
    align-items: center;
    display: flex;
    justify-content: center;
    padding: var(--td-comp-paddingTB-s) var(--td-comp-paddingLR-s);
    border-top: 1px solid var(--td-component-stroke);

    &-link {
      text-decoration: none;
      cursor: pointer;
      color: var(--td-text-color-placeholder);
    }
  }

  .t-list {
    height: calc(100% - 104px);
    padding: var(--td-comp-margin-s) var(--td-comp-margin-s);
  }

  .t-list-item {
    overflow: hidden;
    width: 100%;
    padding: var(--td-comp-paddingTB-l) var(--td-comp-paddingLR-l);
    border-radius: var(--td-radius-default);
    font: var(--td-font-body-medium);
    color: var(--td-text-color-primary);
    cursor: pointer;
    transition: background-color 0.2s linear;

    &:hover {
      background-color: var(--td-bg-color-container-hover);

      .msg-content {
        color: var(--td-brand-color);
      }

      .t-list-item__action {
        button {
          bottom: var(--td-comp-margin-l);
          opacity: 1;
        }
      }

      .msg-time {
        bottom: -6px;
        opacity: 0;
      }
    }

    .msg-content {
      margin-bottom: var(--td-comp-margin-s);
    }

    .msg-type {
      color: var(--td-text-color-secondary);
    }

    .t-list-item__action {
      button {
        opacity: 0;
        position: absolute;
        right: var(--td-comp-margin-xxl);
        bottom: -6px;
      }
    }

    .msg-time {
      transition: all 0.2s ease;
      opacity: 1;
      position: absolute;
      right: var(--td-comp-margin-xxl);
      bottom: var(--td-comp-margin-l);
      color: var(--td-text-color-secondary);
    }
  }
}
</style>
