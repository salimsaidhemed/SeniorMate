import "@mdi/font/css/materialdesignicons.css";
import "vuetify/styles";
import "./styles/main.css";

import { createApp } from "vue";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import { aliases, mdi } from "vuetify/iconsets/mdi";

import App from "./views/App.js";
import ChecklistSummary from "./components/ChecklistSummary.js";
import ConfirmDialog from "./components/ConfirmDialog.js";
import EmptyState from "./components/EmptyState.js";
import ErrorAlert from "./components/ErrorAlert.js";
import LoadingState from "./components/LoadingState.js";
import PageHeader from "./components/PageHeader.js";
import PrintField from "./components/PrintField.js";
import PrintPageLayout from "./components/PrintPageLayout.js";
import PrintSection from "./components/PrintSection.js";
import SectionCard from "./components/SectionCard.js";
import SignatureBlock from "./components/SignatureBlock.js";
import StatusChip from "./components/StatusChip.js";
import router from "./router.js";

const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: "mdi",
    aliases,
    sets: { mdi },
  },
  theme: {
    defaultTheme: "seniorMateLight",
    themes: {
      seniorMateLight: {
        dark: false,
        colors: {
          background: "#F4F7F7",
          surface: "#FFFFFF",
          primary: "#1F6F68",
          secondary: "#4D6D78",
          success: "#3E7D5A",
          info: "#3E7188",
          warning: "#9B6B23",
          error: "#B54747",
          "on-background": "#20302F",
          "on-surface": "#20302F",
        },
        variables: {
          "border-color": "#CBD7D5",
          "border-opacity": 0.72,
          "high-emphasis-opacity": 0.9,
          "medium-emphasis-opacity": 0.72,
        },
      },
    },
  },
  defaults: {
    VCard: {
      elevation: 0,
      border: true,
      rounded: "lg",
    },
    VBtn: {
      rounded: "lg",
    },
    VTextField: {
      variant: "outlined",
      density: "comfortable",
    },
    VSelect: {
      variant: "outlined",
      density: "comfortable",
    },
    VTextarea: {
      variant: "outlined",
      density: "comfortable",
    },
  },
});

createApp(App)
  .component("ChecklistSummary", ChecklistSummary)
  .component("ConfirmDialog", ConfirmDialog)
  .component("EmptyState", EmptyState)
  .component("ErrorAlert", ErrorAlert)
  .component("LoadingState", LoadingState)
  .component("PageHeader", PageHeader)
  .component("PrintField", PrintField)
  .component("PrintPageLayout", PrintPageLayout)
  .component("PrintSection", PrintSection)
  .component("SectionCard", SectionCard)
  .component("SignatureBlock", SignatureBlock)
  .component("StatusChip", StatusChip)
  .use(router)
  .use(vuetify)
  .mount("#app");
