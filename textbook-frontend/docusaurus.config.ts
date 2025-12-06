// docusaurus.config.ts
import { Config } from '@docusaurus/types';
import path from 'path';

const config: Config = {
  title: 'Physical AI & Humanoid Robotics Textbook',
  tagline: 'Embodied Intelligence for the Future',
  url: 'https://your-username.github.io', // replace with actual repo URL
  baseUrl: '/',
  organizationName: 'your-username', // GitHub org/user name.
  projectName: 'physical-ai-humanoid-robotics-textbook', // repo name.
  favicon: 'img/favicon.ico',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  i18n: {
    defaultLocale: 'en',
    locales: ['en'], // , 'ur'
  },
  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/your-username/physical-ai-humanoid-robotics-textbook/edit/main/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],
  themeConfig: {
    navbar: {
      title: 'Physical AI',
      logo: {
        alt: 'Logo',
        src: 'img/logo.svg',
      },
      items: [
        { to: '/docs/intro', label: 'Book', position: 'left' },
        { href: 'https://github.com/SyedaFatimaNoor/Physical-AI-Humanoid-Robotics', label: 'GitHub', position: 'right' },
      ],
    },
    footer: {
      style: 'dark',
      links: [],
      copyright: `© ${new Date().getFullYear()} Physical AI`,
    },
    colorMode: {
      defaultMode: 'dark',
      disableSwitch: false,
      respectPrefersColorScheme: false,
    },
    // Custom CSS for gradients and micro‑animations will be added in src/css/custom.css
  },
  plugins: [],
};

export default config;
