<script setup lang="ts">
import { ref } from "vue";
import { getWithCache } from "@/assets/script/cache";
import { useI18n } from "vue-i18n";
import { syncLangRef } from "@/assets/script/utils";

const oauth = ref([]);
const { t, locale } = useI18n();
syncLangRef(locale);

getWithCache("oauth/list").then((resp) => {
  const data = resp.data;
  if (!data.status) ElMessage({
    type: "error",
    message: data.reason,
    showClose: false,
  });
  else oauth.value = data.data;
});
</script>

<template>
  <div class="form allauth">
    <div class="title"><span>{{ t("allauth") }}</span></div>
    <div class="oauth">


    </div>
  </div>
</template>
<i18n>
{
  "zh": {
    "allauth": "第三方账号"
  },
  "en": {
    "allauth": "Third-party account"
  }
}
</i18n>
<style scoped>
@import "@/assets/style/home.css";

</style>
