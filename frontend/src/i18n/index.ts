import { createI18n } from "vue-i18n";
import { language } from "@/config";

const i18n = createI18n({
  legacy: false,
  locale: language.value,
  messages: {},
});

export default i18n;
