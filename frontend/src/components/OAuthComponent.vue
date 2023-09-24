<script setup lang="ts">
import { language, oauth } from "@/config";
import { useI18n } from "vue-i18n";
import Google from "@/components/icons/google.vue";
import Github from "@/components/icons/github.vue";
import OLink from "@/components/oauth/olink.vue";

const { t, locale } = useI18n();
locale.value = language.value;
</script>
<i18n>
{
  "en": {
    "continue-with": "Continue with {name}"
  },
  "zh": {
    "continue-with": "以 {name} 继续"
  }
}
</i18n>
<template>
  <div class="oauth">
    <o-link :uri="oauth.github_url">
      <github style="scale: 0.9" /> {{ t("continue-with", { name: "GitHub" }) }}
    </o-link>
    <o-link :uri="oauth.google_url">
      <google /> {{ t("continue-with", { name: "Google" }) }}
    </o-link>
  </div>
</template>

<style scoped>
@import "@/assets/style/user.css";
</style>
