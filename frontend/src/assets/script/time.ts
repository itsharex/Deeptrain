import type { ComposerTranslation } from "vue-i18n";

export function formatDate(t: ComposerTranslation, time: string | Date, offset: boolean = true): string {
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

export function padZero(n: number): string {
  return (n < 10 ? '0' : '') + n;
}

export function contain(el: HTMLElement | null | undefined, target: HTMLElement | null): boolean {
  return (el && target) ? (el == target || el.contains(target)) : false;
}
