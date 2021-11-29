export interface MenuItemData {
  text: string;
  href?: string;
  rel?: 'external';
}

export const menuItems: MenuItemData[] = [
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
    href: '/logout',
    rel: 'external',
  },
];
