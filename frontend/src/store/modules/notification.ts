import { defineStore } from 'pinia';

const readMsgIDList: any[] = [];

export const useNotificationStore = defineStore('notification', {
  state: () => ({
    readMsgIDList,
  }),
  getters: {
    getReadMsgIDList: (state) => state.readMsgIDList,
  },
  actions: {
    setReadMsgIDList(data: any) {
      this.readMsgIDList = data;
    },
  },
  persist: true,
});
