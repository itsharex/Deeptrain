document.querySelector('.chat[data-chat=person1]').classList.add('active-chat');
document.querySelector('.person[data-chat=person1]').classList.add('active');
let last_stamp = 0;
const stride_stamp = 150;

let friends = {
        list: document.querySelector('ul.people'),
        all: document.querySelectorAll('.left .person'),
        name: '',
    },
    chat = {
        container: document.querySelector('.container .right'),
        current: null,
        person: null,
        name: document.querySelector('.container .right .top .name'),
    }

friends.all.forEach(f => {
    f.addEventListener('mousedown', () => {
        f.classList.contains('active') || setActiveChat(f);
    })
});

let input = document.getElementById('input');
let chatContainer = document.getElementById("chat-container");
let previewMessage = document.querySelector(".preview");
let timePreview = document.querySelector(".time");
let messageWindow = document.querySelector("#message-window");
let ChatSocket;
function initialize(token) {
    ChatSocket = new websocket("chat", token, messageWindow);
    ChatSocket.get_websocket().onmessage = function(e) {
        const data = JSON.parse(e.data);
        createMessage(
            data.username,
            data.id,
            data.image,
            data.content,
            data.self,
            data.html,
            data.identity,
            data.time,
        );
    };

    document.getElementById('send').onclick = () => {
        let val = input.value.trim().slice(0, 500), length=val.length;
        if (length < 1){alerts(["alert-info", "message-data"], "请输入内容!", messageWindow);}
        else {
            if (length > 500){alerts(["alert-warning", "message-data"], "最多输入500个字符!", messageWindow)}
            else {
                ChatSocket.get_websocket().send(JSON.stringify({'message': val}));
                $(input).val("");
            }
        }
    }
}
function setActiveChat(f) {
    friends.list.querySelector('.active').classList.remove('active');
    f.classList.add('active');
    chat.current = chat.container.querySelector('.active-chat');
    chat.person = f.getAttribute('data-chat');
    chat.current.classList.remove('active-chat');
    chat.container.querySelector('[data-chat="' + chat.person + '"]').classList.add('active-chat');
    friends.name = f.querySelector('.name').innerText;
    chat.name.innerHTML = friends.name;
}

function updateTime(time=new Date().getTime() / 1000) {
    let now = new Date(time * 1000).toLocaleTimeString();  /* python time-stamp (int) s -> ms */
    timePreview.innerText = now;
    if (last_stamp + stride_stamp <= time){
        last_stamp = time;
        const date = document.createElement("div");
        date.classList.add("time-line");
        date.innerHTML = `<span>${now}</span>`;
        chatContainer.appendChild(date);
    }
}

function createMessage(username, id, picture_url, message, is_self=true, is_html=false, identity=0, time) {
    updateTime(time);
    let dom = document.createElement('div');
    dom.classList.add("chat-element");
    dom.classList.add(is_self?"me":"you");
    dom.innerHTML = `<a href="/profile/id=${id}" target="_blank"><img src="${picture_url}" alt></a>
                     <div class="chat-content">
                        <div class="user"><img class="identity-image ${identity}" src alt><span class="username"></span></span>
                        <span class="bubble"></span>
                     </div>`;
    dom.querySelector(".username").innerText = username.toString();  // 防止XSS攻击, 因此不采用dom.innerHTML内填写, 单独存放.
    dom.querySelector(".bubble").innerText = message.toString();
    previewMessage.innerText = message;
    chatContainer.appendChild(dom);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}