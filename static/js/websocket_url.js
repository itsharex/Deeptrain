class websocket {
    constructor(url, token, message_window) {
        this.socket = undefined;
        this.message_window = message_window;
        this.url = `ws://${window.location.host}/${ url }/${ token }/`;
        this.wss_url = `wss://${window.location.host}/${ url }/${ token }/`;
        this.create();
    }
    create() {
        try{
            this.socket = new WebSocket(this.url);
        }catch (DOMException) {
            this.socket = new WebSocket(this.wss_url);
        }
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