import Cookies from 'js-cookie';
import { defineStore } from 'pinia';
import { MessagePlugin } from 'tdesign-vue-next';

import { usePermissionStore } from '@/store';
import type { UserInfo } from '@/types/interface';

const InitUserInfo: UserInfo = {
  name: '', // 用户名，用于展示在页面右上角头像处
  roles: [], // 前端权限模型使用 如果使用请配置modules/permission-fe.ts使用
};

export const useUserStore = defineStore('user', {
  state: () => ({
    token: 'main_token', // 默认token不走权限
    is_admin: false,
    userInfo: { ...InitUserInfo },
  }),
  getters: {
    roles: (state) => {
      return state.userInfo?.roles;
    },
  },
  actions: {
    async login(url: string, userInfo: Record<string, unknown>) {
      const response = await fetch(url, {
        method: 'POST',
        body: JSON.stringify(userInfo),
        headers: {
          'Content-Type': 'application/json',
        },
      });
      let data = null;
      if (response.status === 200) {
        data = await response.json();
        this.token = data.admin_token;
        this.is_admin = data.is_admin;
        Cookies.set('user_token', data.admin_token, { expires: 7 });
        MessagePlugin.success('登录成功');
      } else if (response.status === 400) {
        data = await response.json();
        MessagePlugin.error(JSON.stringify(Object.values(data)[0]));
      } else if (response.status === 502) {
        MessagePlugin.error('服务未正常启动');
        return new Response();
      } else if (response.status === 500) {
        MessagePlugin.error('系统异常，请稍后再试');
      }
      return data;
    },

    async logout() {
      this.token = '';
      this.userInfo = { ...InitUserInfo };
    },
  },
  persist: {
    afterRestore: () => {
      const permissionStore = usePermissionStore();
      permissionStore.initRoutes();
    },
    key: 'user',
    paths: ['token'],
  },
});
