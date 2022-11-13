class websocket {
    constructor(url, token, message_window) {
        this.socket = undefined;
        this.message_window = message_window;
        this.url = `ws://${window.location.host}/${ url }/${ token }/`;
        this.create();
    }
    create() {
        this.socket = new WebSocket(this.url);
        let dom = this.message_window;
        this.socket.onopen = function (e) {
            alerts(["alert-success", "message-data"], `服务器 ${window.location.host} 连接成功!`, dom);
        }
        this.socket.onclose = function(e) {
            alerts(["alert-danger", "message-data"], `服务器 ${window.location.host} 断开连接!`, dom);
        }
    }
    get_websocket(){
        return this.socket;
    }
}