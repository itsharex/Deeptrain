const articleData = document.querySelector(".js-article-data");

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
    error(reason) {
        this.clear();
        notify.error(reason, "topRight");
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
}
class Like extends SubmitNotify {
    constructor() {
        super();
        this.button = document.getElementById("like");
        this.icon = document.getElementById("like-icon");
        this.nlike = document.getElementById("like-number");
        this.state = eval(articleData.getAttribute("like-state"));
        this.number = Number(articleData.getAttribute("likes"));
        this.article_id = Number(articleData.getAttribute("article-id"));
        this.render();
        let _this = this;
        this.button.onclick = () => (_this.submit());
    }
    add(...classes) {
        for (let i = 0; i < classes.length; i++) {
            this.icon.classList.add(classes[i]);
        }
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
            _this.add("layui-icon-loading-1", "layui-anim", "layui-anim-rotate", "layui-anim-loop");
            _this.remove("layui-icon-heart");
            _this.remove("layui-icon-heart-fill");
            notify.loading("正在提交中...", "topRight");
        }, 500)
    }
    render() {
        this.state?this.like():this.dislike();
        this.nlike.innerHTML = this.number.toString();
    }
    submit() {
        this.loading();

        let _this = this;
        $.ajax({
            url: `/blog/submit/like/${this.article_id}/`,
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
            },
            error: () => (_this.error("服务器连接失败, 请稍后重试")),
        })
    }
}

function prompt(title, callback) {
    layer.prompt({title: title, formType: 2}, function(text, index){
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
        let comment = button.parentNode;
        let data = comment.querySelector(".js-comment-data");
        switch (button.getAttribute("comment-type")) {
            case "article":
                break;
            case "user":
                break;
        }
    }
    articlePrompt(title, callback) {
        prompt(`评论文章 <span class="layui-font-blue"><i class="layui-icon layui-icon-read"></i> ${title}</span>`, callback)
    }
    userPrompt(user, callback) {
        prompt(`评论用户 <span class="layui-font-blue"><i class="layui-icon layui-icon-friends"></i> ${user}</span>`, callback)
    }
    replyPrompt(user, callback) {
        prompt(`回复用户 <span class="layui-font-blue"><i class="layui-icon layui-icon-username"></i> ${user}</span>`, callback)
    }
}
const like = new Like(), comment = new Comment();