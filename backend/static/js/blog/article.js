const article_data = document.querySelector(".js-article-data");
const article_id = Number(article_data.getAttribute("article-id"));
const article_title = article_data.getAttribute("title");
const csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

function cls_inner(dom, cls_) {
    let cls = cls_.split(" ");
    for (let i = 0; i < cls.length; i++) {
        dom.classList.add(cls[i])
    }
}
function to_top(dom, target) {
    target.insertBefore(dom, target.children[0]);
}

class SubmitNotify {
    constructor() {
        this.timeout = 0;
    }
    clear() {
        notify.destroyAll();
        clearTimeout(this.timeout);
    }
    success() {
        this.clear();
        notify.success("提交成功", "topRight");
    }
    error() {
        this.clear();
        notify.error("服务器连接失败, 请稍后重试", "topRight");
    }
    warning(reason) {
        this.clear();
        layer.open({
            title: '提交失败',
            content: reason,
        });
    }
    info(reason) {
        this.clear();
        notify.info(reason, "topRight");
    }
    loading() {
        let _this = this;
        this.timeout = setTimeout(function() {
            notify.loading("正在提交中...", "topRight");
        }, 200);
    }
}
class Like extends SubmitNotify {
    constructor() {
        super();
        this.button = document.getElementById("like");
        this.icon = document.getElementById("like-icon");
        this.nlike = document.getElementById("like-number");
        this.state = eval(article_data.getAttribute("like-state").toLowerCase());
        this.number = Number(article_data.getAttribute("likes"));
        this._await_loading = false;
        this.render();
        let _this = this;
        this.button.onclick = () => (_this.submit());
    }
    add(...classes) {
        for (let i = 0; i < classes.length; i++) {
            this.icon.classList.add(classes[i]);
        }
    }
    clear() {
        super.clear();
        this.render();
    }
    remove(...classes) {
        for (let i = 0; i < classes.length; i++) {
            this.icon.classList.remove(classes[i]);
        }
    }
    like() {
        this.add("layui-icon-heart-fill");
        this.remove("layui-icon-heart");
        this.remove("layui-icon-loading-1", "layui-anim", "layui-anim-rotate", "layui-anim-loop");
    }
    dislike() {
        this.add("layui-icon-heart");
        this.remove("layui-icon-heart-fill");
        this.remove("layui-icon-loading-1", "layui-anim", "layui-anim-rotate", "layui-anim-loop");
    }
    loading() {
        let _this = this;
        this.timeout = setTimeout(function() {
            if (!_this._await_loading) {
                return;
            }
            _this.add("layui-icon-loading-1", "layui-anim", "layui-anim-rotate", "layui-anim-loop");
            _this.remove("layui-icon-heart");
            _this.remove("layui-icon-heart-fill");
            notify.loading("正在提交中...", "topRight");
        }, 200);
    }
    render() {
        this.state?this.like():this.dislike();
        this.nlike.innerHTML = this.number.toString();
    }
    submit() {
        if (this._await_loading) {
            return;
        }
        this._await_loading = true;
        this.loading();

        let _this = this;
        $.ajax({
            url: `/blog/submit/like/${article_id}/`,
            method: "POST",
            dataType: "json",
            data : {
                "csrfmiddlewaretoken": csrf_token,
            },
            success: data => {
                if (data.success) {
                    _this.success();
                    _this.state = data.state;
                    _this.number = data.number;
                } else {
                    _this.warning(data.reason);
                }
                _this.render();
                _this._await_loading = false;
            },
            error: () => {
                _this.error();
                _this._await_loading = false;
            },
        })
    }
}

function prompt(title, callback) {
    layer.prompt({title: title, formType: 2, maxlength: 300}, function(text, index){
        layer.close(index);
        callback(text);
    });
}

class CommentObject {
    constructor(opt) {
        this.avatar = opt.avatar;
        this.username = opt.username;
        this.id = opt.id;
        this.url = opt.url;
        this.content = opt.content;
        this.root = opt.root;
        if (!this.root) {
            this.reply_name = opt.replyName || "";
            this.reply_url = opt.replyUrl || "";
        }
    }
    toHtml() {
        let reply_html = this.reply_name?`<i class="layui-icon layui-icon-right arrow"></i><a href="${this.reply_url}" target="_blank">&nbsp;${this.reply_name}</a>`:"";
        return `<img class="avatar" src="${this.avatar}" alt>
                <div class="comment-content">
                    <div class="js-comment-data" comment-id="${this.id}" root="${this.root}" comment-user="${this.username}" hidden></div>
                    <a href="${this.url}" target="_blank">${this.username}</a>
                    ${reply_html}
                    <div class="content js-inner-content"></div>
                    <button type="button" comment-type="user" class="layui-btn layui-btn-primary layui-btn-sm comment-btn js-comment-btn"><i class="layui-icon layui-icon-reply-fill"></i></button>
                        <div class="children"></div>
                </div>`;
    }
    toNode() {
        let dom = document.createElement("div");
        cls_inner(dom, "layui-panel comment layui-anim layui-anim-downbit");
        dom.innerHTML = this.toHtml();
        dom.querySelector(".js-inner-content").innerText = this.content;
        return dom;
    }
    innerNode(node) {
        let dom = this.toNode();
        if (this.root) {
            to_top(dom, document.querySelector("#comments"));
        } else {
            if (this.reply_name) {
                to_top(dom, node.parentNode.parentNode);
            } else {
                to_top(dom, node.querySelector(".children"));
            }
        }
        return dom.querySelector(".js-comment-btn");
    }
}
class Comment extends SubmitNotify {
    constructor() {
        super();
        this.comments = document.querySelectorAll(".js-comment-btn");
        this.number = Number(article_data.getAttribute("comments"));
        this.number_dom = document.querySelector("#comment-number");

        const _this = this;
        for (let i = 0; i < this.comments.length; i++) {
            this.comments[i].onclick = param => (_this.clicked(param));
        }
    }
    clicked(target) {
        let button = target.target.getAttribute("type")?target.target:target.target.parentNode;
        let comment = button.parentNode;
        let _this = this;

        switch (button.getAttribute("comment-type")) {
            case "article":
                prompt(
                    `评论文章 <span class="layui-font-blue highlight-span"><i class="layui-icon layui-icon-read"></i> ${article_title}</span>`,
                    content => (_this.submit(content, comment)),
                );
                break;
            case "user":
                let data = comment.querySelector(".js-comment-data").attributes;
                let username = data["comment-user"].value;
                let comment_id = Number(data["comment-id"].value);
                let root = eval(data.root.value.toLowerCase());

                prompt(
                    root?
                    `评论用户 <span class="layui-font-blue"><i class="layui-icon layui-icon-friends"></i> ${username}</span>`:
                    `回复用户 <span class="layui-font-blue"><i class="layui-icon layui-icon-username"></i> ${username}</span>`,
                content => (_this.submit(content, comment, comment_id)),
                );
                break;
        }
    }
    submit(content, parentNode, parent_id=undefined) {
        let _this = this;
        this.loading();
        $.ajax({
            url: `/blog/submit/comment/${article_id}/`,
            method: "POST",
            dataType: "json",
            data: {
                "csrfmiddlewaretoken": csrf_token,
                "content": content,
                "parent": parent_id,
            },
            success: function(data) {
                if (data.success) {
                    _this.success();
                    let el = new CommentObject(
                        {
                            ...data,
                            "content": content,
                        }
                    );
                    el.innerNode(parentNode).onclick = param => (_this.clicked(param));
                    _this.number += 1;
                    _this.number_dom.innerText = _this.number.toString();
                } else {
                    _this.warning(data.reason);
                }
            },
            error: () => (_this.error()),
        });
    }
}
const like = new Like(), comment = new Comment();