import api from '$lib/shared/api';

export interface MenuItemData {
  text: string;
  href?: string;
  action?: () => void;
}

export default <MenuItemData[]>[
  {
    text: 'My cars',
    href: '/cars',
  },
  {
    text: 'Statistics',
    href: '/statistics',
  },
  {
    text: 'Log out',
    action: api.logOut,
  }
];