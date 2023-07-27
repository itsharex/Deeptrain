<script setup lang="ts">
import { reactive } from "vue";
import { username } from "@/assets/script/global";
import router from "@/router";
import axios from "axios";
import Mail from "@/components/icons/home/mail.vue";
import DateIcon from "@/components/icons/home/date.vue";
import Key from "@/components/icons/home/key.vue";
import ChangePasswordDialog from "@/views/dialog/ChangePasswordDialog.vue";
import ChangeEmailDialog from "@/views/dialog/ChangeEmailDialog.vue";
import Edit from "@/components/icons/home/edit.vue";
import { backend_url } from "@/config";
import { useI18n } from "vue-i18n";

function formatDate(time: string | Date, offset: boolean = true): string {
  const now = new Date(), date = typeof time == 'string' ? new Date(time) : time;
  const diff = (now.getTime() - date.getTime()) / 1000 + (offset ? 8 * 3600 : 0); // second

  if (diff < 0) {
    return t('time.none');
  } else if (diff < 60) {
    return t('time.justNow');
  } else if (diff < 3600) {
    const minutes = Math.floor(diff / 60);
    return t('time.minutesAgo', { minutes });
  } else if (diff < 86400) {
    const hours = Math.floor(diff / 3600);
    return t('time.hoursAgo', { hours });
  } else if (diff < 172800) {
    return t('time.yesterday', { time: `${padZero(date.getHours())}:${padZero(date.getMinutes())}` });
  } else if (diff < 259200) {
    return t('time.beforeYesterday', { time: `${padZero(date.getHours())}:${padZero(date.getMinutes())}` });
  } else if (diff < 604800) {
    const days = Math.floor(diff / 86400);
    return `${t('time.daysAgo', { days })} ${padZero(date.getHours())}:${padZero(date.getMinutes())}`;
  } else if (date.getFullYear() === now.getFullYear()) {
    return t('time.monthDay', {
      month: date.getMonth() + 1,
      day: date.getDate(),
      time: `${padZero(date.getHours())}:${padZero(date.getMinutes())}`
    });
  } else {
    return t('time.yearMonthDay', {
      year: date.getFullYear(),
      month: date.getMonth() + 1,
      day: date.getDate(),
      time: `${padZero(date.getHours())}:${padZero(date.getMinutes())}`
    });
  }
}

function padZero(n: number): string {
  return (n < 10 ? '0' : '') + n;
}

function contain(el: HTMLElement | null | undefined, target: HTMLElement | null): boolean {
  return (el && target) ? (el == target || el.contains(target)) : false;
}


const { t } = useI18n({
  messages: {
    en: {
      'time.none': 'none',
      'time.ago': 'ago',
      'time.justNow': 'just now',
      'time.minutesAgo': '{minutes} minutes ago',
      'time.hoursAgo': '{hours} hours ago',
      'time.yesterday': 'yesterday {time}',
      'time.beforeYesterday': 'before yesterday {time}',
      'time.daysAgo': '{days} days ago {time}',
      'time.monthDay': '{month}/{day} {time}',
      'time.yearMonthDay': '{year} {month}/{day} {time}'
    },
    zh: {
      'time.none': '无',
      'time.ago': '前',
      'time.justNow': '刚刚',
      'time.minutesAgo': '{minutes} 分钟前',
      'time.hoursAgo': '{hours} 小时前',
      'time.yesterday': '昨天 {time}',
      'time.beforeYesterday': '前天 {time}',
      'time.daysAgo': '{days} 天前 {time}',
      'time.monthDay': '{month}月{day}日 {time}',
      'time.yearMonthDay': '{year}年{month}月{day}日 {time}'
    }
  }
});

function logout() {
  router.push("/logout");
}

const form = reactive<Record<string, any>>({
  username: "",
  id: 0,
  email: "",
  created_at: "",
});

const dialog = reactive<Record<string, boolean>>({
  change: false,
  email: false,
});

function avatar() {
  const file = (document.getElementById("avatar") as HTMLInputElement).files?.[0];
  if (!file) return;
  if (file.size > 1024 * 1024 * 2) {
    ElNotification.error({
      title: t("avatar-update-failed"),
      message: t("avatar-update-failed-reason"),
      showClose: false,
    });
    return;
  }
  const formData = new FormData();
  formData.append("avatar", file);
  axios.post("avatar", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  }).then((res) => {
    if (res.data.status) {
      ElNotification.success({
        title: t("avatar-updated"),
        message: t("avatar-updated-successfully"),
        showClose: false,
      });
    } else {
      ElNotification.error({
        title: t("avatar-update-failed"),
        message: res.data.reason,
        showClose: false,
      });
    }
  });
}

axios.get("info")
  .then((res) => {
    for (const key in res.data) {
      form[key] = res.data[key];
    }
    console.log(formatDate(form.created_at), form.created_at)
    form.created_at = formatDate(form.created_at);
  })
</script>
<template>
  <ChangePasswordDialog v-model="dialog.change" />
  <ChangeEmailDialog v-model="dialog.email" />
  <el-container>
    <el-main>
      <el-card class="card">
        <div class="header">
          <div class="logo">
            <img src="/favicon.ico" alt="" />
            <span>{{ t('title') }}</span>
          </div>
          <div class="grow" />
          <div class="username">{{ username }}</div>
          <div class="logout" @click="logout">{{ t('logout') }}</div>
        </div>
      </el-card>
      <el-card class="card">
        <div class="image">
          <img class="background" src="/home/background.jpg" alt="" loading="lazy">
          <div class="avatar">
            <input type="file" accept="image/*" style="display: none" id="avatar" @change="avatar" />
            <label class="before" for="avatar"><edit /></label>
            <img :src="`${backend_url}avatar/${username}`" alt="" loading="lazy">
          </div>
        </div>
        <div class="info">
          <div class="name">{{ form.username }}</div>
          <div class="id">{{ form.id }}</div>
        </div>
        <div class="setting">
          <div class="form general">
            <div class="title">
              <span>{{ t('general') }}</span>
            </div>
            <div class="item">
              <div class="label"><mail style="scale: 0.98; transform: translate(-2px, 7px)" /> {{ t('email') }}</div>
              <div class="grow" />
              <div class="value">
                <span>{{ form.email }}</span>
                <div class="button" @click="dialog.email = true">{{ t('change') }}</div>
              </div>
            </div>
            <div class="item">
              <div class="label"><key style="scale: 0.98; transform: translate(-2px, 6px)" /> {{ t('password') }}</div>
              <div class="grow" />
              <div class="value">
                <span>********</span>
                <div class="button" @click="dialog.change = true">{{ t('change') }}</div>
              </div>
            </div>
            <div class="item">
              <div class="label"><date-icon style="scale: 0.98; transform: translate(-2px, 6px)" /> {{ t('created_at') }}</div>
              <div class="grow" />
              <div class="value">{{ form.created_at }}</div>
            </div>
          </div>
        </div>
      </el-card>
    </el-main>
  </el-container>
</template>
<i18n>
{
  "en": {
    "title": "Deeptrain",
    "general": "General",
    "email": "Email",
    "password": "Password",
    "created_at": "Created At",
    "change": "Change",
    "logout": "Logout",
    "avatar": "Avatar",
    "avatar-update-failed": "Avatar update failed",
    "avatar-updated": "Avatar updated",
    "avatar-updated-successfully": "Your avatar has been updated successfully!",
    "avatar-update-failed-reason": "The file size should be less than 2MB"
  },
  "zh": {
    "title": "Deeptrain 账号管理",
    "general": "通用",
    "email": "邮箱",
    "password": "密码",
    "created_at": "注册时间",
    "change": "更改",
    "logout": "退出登录",
    "avatar": "头像",
    "avatar-update-failed": "头像更新失败",
    "avatar-updated": "头像更新成功",
    "avatar-updated-successfully": "您的头像已成功更新！",
    "avatar-update-failed-reason": "文件大小应小于 2MB"
  }
}
</i18n>
<style scoped>
.card {
  width: 100%;
  max-width: 820px;
  margin: 8px auto 12px;
}

.header {
  display: flex;
  flex-direction: row;
  align-items: center;
}

.logo {
  width: max-content;
  height: max-content;
  user-select: none;
  display: flex;
  align-items: center;
}

.logo img {
  width: 36px;
  height: 36px;
}

.logo span {
  font-size: 24px;
  font-weight: 600;
  margin-left: 16px;
  color: rgba(255, 255, 255, 0.9);
}

.image {
  width: calc(100% + 40px);
  height: 295px;
  overflow: hidden;
  position: relative;
  margin-right: 16px;
  border-radius: 4px 4px 0 0;
  transform: translate(-20px, -20px);
}

.image .background {
  width: 100%;
  height: 245px;
  object-fit: cover;
  object-position: center;
}

.image .avatar {
  position: absolute;
  bottom: 0;
  left: 50px;
  width: 100px;
  height: 100px;
  border-radius: 8px;
  padding: 2px;
  opacity: .9;
  backdrop-filter: blur(4px);
  background: rgba(0,0,0,.15);
  box-shadow: 0 0 8px 0 rgba(0, 0, 0, 0.2);
  object-fit: cover;
  object-position: center;
  transition: .5s;
  z-index: 64;
  user-select: none;
  cursor: pointer;
}

.image .avatar img {
  width: 100%;
  height: 100%;
  border-radius: 8px;
}

.image .avatar .before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 8px;
  background: rgba(0,0,0,0);
  transition: .5s;
  z-index: 64;
}

.image .avatar:hover .before,
.image .avatar:active .before {
  background: rgba(0,0,0,.15);
}

.image .avatar svg {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 32px;
  height: 32px;
  background: rgba(0, 0, 0, 0);
  border-radius: 8px;
  padding: 4px;
  transform: translate(-50%, -50%);
  fill: rgba(0, 0, 0, 0);
  user-select: none;
  white-space: nowrap;
  flex-shrink: 1;
  z-index: 64;
  transition: .5s;
}

.image .avatar:hover svg,
.image .avatar:active svg {
  background: rgba(0, 0, 0, 0.5);
  fill: rgba(255, 255, 255, 0.9);
}

.info {
  width: 100%;
  height: 50px;
  transform: translateY(-12px);
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 0 16px;
  margin-bottom: 16px;
  user-select: none;
  white-space: nowrap;
}

.info .name {
  font-size: 1.25rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  margin-right: 16px;
  user-select: none;
  white-space: nowrap;
  font-family: ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica Neue,Arial,Noto Sans,sans-serif,Apple Color Emoji,Segoe UI Emoji,Segoe UI Symbol,Noto Color Emoji;
}

.info .id:before {
  content: "#";
  font-size: 16px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.6);
  user-select: none;
  white-space: nowrap;
}

.info .id {
  font-size: 24px;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.6);
  user-select: none;
  white-space: nowrap;
  transform: translateY(-2px);
}

.username {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.9);
  margin-right: 16px;
  user-select: none;
  white-space: nowrap;
}

.logout {
  font-size: 16px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  cursor: pointer;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 0 8px 0 rgba(0, 0, 0, 0.2);
  padding: 8px 16px;
  border-radius: 4px;
  transition: .5s;
  user-select: none;
  white-space: nowrap;
}

.logout:hover {
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.setting {
  display: flex;
  width: 100%;
  flex-direction: row;
  align-items: flex-start;
  padding: 6px;
  border-radius: 4px;
  background: rgba(0, 0, 0, 0.1);
  box-shadow: 0 0 8px 0 rgba(0, 0, 0, 0.2);
}

.form {
  width: 100%;
  margin: 0 16px;
}

.form .title {
  margin-bottom: 16px;
}

.form .title span {
  font-size: 24px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  user-select: none;
}

.form .title:before {
  content: "";
  display: inline-block;
  top: 4px;
  left: -2px;
  width: 4px;
  height: 24px;
  background: #409eff;
  margin-right: 8px;
  border-radius: 2px;
  user-select: none;
}

.form .item {
  display: flex;
  flex-direction: row;
  align-items: center;
  margin-bottom: 16px;
}

.form .item svg {
  width: 24px;
  height: 24px;
  transform: translateY(6px);
  fill: rgba(255, 255, 255, 0.85);
  user-select: none;
  white-space: nowrap;
  flex-shrink: 1;
}

.form .item .label {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.9);
  margin-right: 16px;
  width: 100px;
  user-select: none;
  white-space: nowrap;
}

.form .item .value {
  display: flex;
  flex-direction: row;
  font-size: 16px;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.75);
  user-select: none;
  white-space: nowrap;
}

.form .item .value span {
  margin-right: 16px;
  user-select: none;
  white-space: nowrap;
}

.form .item .value .button {
  font-size: 16px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  cursor: pointer;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 0 8px 0 rgba(0, 0, 0, 0.2);
  padding: 4px 8px;
  border-radius: 4px;
  transition: .5s;
  user-select: none;
  white-space: nowrap;
}

.form .item .value .button:hover {
  border: 1px solid rgba(255, 255, 255, 0.2);
}

@media (max-width: 620px) {
  .logo span {
    display: none;
  }

  .form .item {
    text-align: left;
    flex-direction: column;
    align-items: flex-start;
  }

  .form .item .label {
    margin-right: 0;
    text-align: left;
  }

  .form .item .value {
    margin-top: 4px;
    margin-left: 6px;
    text-align: left;
  }

  .image .avatar {
    width: 86px;
    height: 86px;
    left: 16px;
  }
}

@media (max-width: 540px) {
  .username {
    display: none;
  }
}
</style>
