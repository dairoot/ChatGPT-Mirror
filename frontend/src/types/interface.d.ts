import type { TabValue } from 'tdesign-vue-next';
import { LocationQueryRaw, RouteRecordName } from 'vue-router';

export interface RouteMeta {
  title?: string | Record<string, string>;
  icon?: string;
  expanded?: boolean;
  orderNo?: number;
  hidden?: boolean;
  hiddenBreadcrumb?: boolean;
  single?: boolean;
  keepAlive?: boolean;
  frameSrc?: string;
  frameBlank?: boolean;
}

export interface MenuRoute {
  path: string;
  title?: string | Record<string, string>;
  name?: string;
  icon?:
    | string
    | {
        render: () => void;
      };
  redirect?: string;
  children: MenuRoute[];
  meta: RouteMeta;
}

export type ModeType = 'dark' | 'light';

export interface UserInfo {
  name: string;
  roles: string[];
}

export interface NotificationItem {
  id: string;
  content: string;
  type: string;
  status: boolean;
  collected: boolean;
  date: string;
  quality: string;
}

export interface TRouterInfo {
  path: string;
  query?: LocationQueryRaw;
  routeIdx?: number;
  title?: string;
  name?: RouteRecordName;
  isAlive?: boolean;
  isHome?: boolean;
  meta?: any;
}

export interface TTabRouterType {
  isRefreshing: boolean;
  tabRouterList: Array<TRouterInfo>;
}

export interface TTabRemoveOptions {
  value: TabValue;
  index: number;
  e: MouseEvent;
}
