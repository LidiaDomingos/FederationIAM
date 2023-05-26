import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  base: "/FederationIAM",
  title: "IAM",
  description: "Centro de Federação de Usuários",
  themeConfig: {
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Roteiro', link: '/Objetivo' }
    ],

    sidebar: [
      {
        text: '',
        items: [
          { text: 'Objetivo', link: '/Objetivo' },
          { text: 'Pré-requisitos', link: '/Requisitos' },
          { text: 'Terraform', link: '/Terraform' },
          { text: 'Python', link: '/Python' }
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/LidiaDomingos/FederationIAM' }
    ]
  }
})
