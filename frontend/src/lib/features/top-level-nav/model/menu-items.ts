import { goto } from "$app/navigation";

export interface MenuItemData {
  text: string;
  href?: string;
  action?: () => void;
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
    async action(): Promise<void> {
      await fetch('/logout');
      await goto('/');
    },
  },
];
