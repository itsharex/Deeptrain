type ElMessageOptions = {
  message: string;
  type?: string;
  title?: string;
  duration?: number;
  offset?: number;
  onClose?: () => any;
  center?: boolean;
  customClass?: string;
  showClose?: boolean;
  dangerouslyUseHTMLString?: boolean;
  appendTo?: string | HTMLElement;
  grouping?: boolean;
  repeatNum?: number;
};

function ElMessage(option: ElMessageOptions): void;

namespace ElNotification {
  type ElNotificationOptions = {
    title?: string;
    message: string;
    type?: string;
    iconClass?: string;
    customClass?: string;
    duration?: number;
    offset?: number;
    onClose?: () => any;
    showClose?: boolean;
    closeOnClick?: boolean;
    position?: string;
    dangerouslyUseHTMLString?: boolean;
  };

  function success(option: ElNotificationOptions): void;
  function warning(option: ElNotificationOptions): void;
  function info(option: ElNotificationOptions): void;
  function error(option: ElNotificationOptions): void;

  function closeAll(): void;
  function close(id: string): void;
}
function ElNotification(option: ElNotification.ElNotificationOptions): void;
