import { defineConfig } from "vitepress";

export default defineConfig({
  title: "SeniorMate",
  description:
    "A modern caregiver and patient management platform for connected care operations.",
  base: "/SeniorMate/",
  cleanUrls: true,
  lastUpdated: true,
  head: [
    ["meta", { name: "theme-color", content: "#0C655F" }],
    ["meta", { property: "og:type", content: "website" }],
    ["meta", { property: "og:title", content: "SeniorMate v1.0.0" }],
    [
      "meta",
      {
        property: "og:description",
        content:
          "Patient management, clinical documentation, medical records, reporting, authentication, and care operations in one place."
      }
    ],
    ["link", { rel: "icon", href: "/SeniorMate/logo.svg", type: "image/svg+xml" }]
  ],
  themeConfig: {
    logo: "/logo.svg",
    siteTitle: false,
    nav: [
      { text: "Home", link: "/" },
      { text: "Features", link: "/features" },
      { text: "Screenshots", link: "/screenshots" },
      { text: "Architecture", link: "/architecture" },
      { text: "Documentation", link: "/documentation" },
      { text: "Roadmap", link: "/roadmap" },
      { text: "Contact", link: "/contact" }
    ],
    socialLinks: [
      {
        icon: "github",
        link: "https://github.com/salimsaidhemed/SeniorMate"
      }
    ],
    search: {
      provider: "local"
    },
    footer: {
      message: "Built for clear, connected care operations.",
      copyright: "SeniorMate v1.0.0"
    },
    outline: {
      level: [2, 3]
    }
  }
});
