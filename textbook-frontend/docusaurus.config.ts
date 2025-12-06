// docusaurus.config.ts
import { Config } from '@docusaurus/types';
import path from 'path';

const config: Config = {
  title: 'Physical AI & Humanoid Robotics Textbook',
  tagline: 'Embodied Intelligence for the Future',
  url: 'https://physical-ai-humanoid-robotics.vercel.app',
  baseUrl: '/',
  organizationName: 'SyedaFatimaNoor', // GitHub org/user name.
  projectName: 'Physical-AI-Humanoid-Robotics', // repo name.
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
          editUrl: 'https://github.com/SyedaFatimaNoor/Physical-AI-Humanoid-Robotics/edit/main/textbook-frontend/',
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
      links: [
        {
          title: 'Book',
          items: [
            {
              label: 'Introduction',
              to: '/docs/intro',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'Stack Overflow',
              href: 'https://stackoverflow.com/questions/tagged/docusaurus',
            },
            {
              label: 'Discord',
              href: 'https://discordapp.com/invite/docusaurus',
            },
            {
              label: 'X',
              href: 'https://x.com/docusaurus',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/SyedaFatimaNoor/Physical-AI-Humanoid-Robotics',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI Book. Built with Docusaurus.`,
    },
    colorMode: {
      defaultMode: 'light',
      disableSwitch: false,
      respectPrefersColorScheme: false,
    },
    // Custom CSS for gradients and micro‑animations will be added in src/css/custom.css
  },
  plugins: [],
};

export default config;
