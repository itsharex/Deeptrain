const article_data = document.querySelector(".js-article-data");
const article_id = Number(article_data.getAttribute("article-id"));
const article_title = article_data.getAttribute("title");

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
        this.state = eval(article_data.getAttribute("like-state"));
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
                "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
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

class Comment extends SubmitNotify {
    constructor() {
        super();
        this.comments = document.querySelectorAll(".js-comment-btn");

        const _this = this;
        for (let i = 0; i < this.comments.length; i++) {
            this.comments[i].onclick = param => (_this.clicked(param));
        }
    }
    clicked(target) {
        let button = target.target.getAttribute("type")?target.target:target.target.parentNode;
        switch (button.getAttribute("comment-type")) {
            case "article":
                this.articlePrompt();
                break;
            case "user":
                let comment = button.parentNode;
                let data = comment.querySelector(".js-comment-data");
                let username = data.getAttribute("comment-user");
                let comment_id = Number(data.getAttribute("comment-id"));
                let root = eval(data.getAttribute("root").toLowerCase());
                this.userPrompt(username, comment_id, root);
                break;
        }
    }
    submit(content="", parent=undefined) {
        let _this = this;
        this.loading();
        $.ajax({
            url: `/blog/submit/comment/${article_id}/`,
            method: "POST",
            dataType: "json",
            data: {
                "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
                "content": content,
                "parent": parent,
            },
            success: function(data) {
                if (data.success) {
                    _this.success();
                } else {
                    _this.warning(data.reason);
                }
            },
            error: () => (_this.error()),
        });
    }
    articlePrompt() {
        let _this = this;
        prompt(`评论文章 <span class="layui-font-blue highlight-span"><i class="layui-icon layui-icon-read"></i> ${article_title}</span>`, content => (_this.submit(content)));
    }
    userPrompt(user, comment_id, root=true) {
        let _this = this;
        prompt(root?
            `评论用户 <span class="layui-font-blue"><i class="layui-icon layui-icon-friends"></i> ${user}</span>`:
            `回复用户 <span class="layui-font-blue"><i class="layui-icon layui-icon-username"></i> ${user}</span>`,
            content => (_this.submit(content, comment_id)));
    }
}
const like = new Like(), comment = new Comment();