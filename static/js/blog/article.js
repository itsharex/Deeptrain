class Like {
    constructor(number=0, state=false, article_idx=0) {
        this.button = document.getElementById("like");
        this.icon = document.getElementById("like-icon");
        this.nlike = document.getElementById("like-number");
        this.state = state;
        this.number = number;
        this.article_idx = article_idx;

        let _this = this;
        this.button.onclick = () => (_this.submit());
        this.render();
    }
    clear() {
        notify.destroyAll();
        clearTimeout(this.timeout);
    }
    success(reason) {
        this.clear();
        notify.success(reason, "topRight");
    }
    error(reason) {
        this.clear();
        notify.error(reason, "topRight");
    }
    warning(reason) {
        this.clear();
        layer.open({
            title: '操作失败',
            content: reason,
        });
    }
    info(reason) {
        this.clear();
        notify.info(reason, "topRight");
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
            url: `/blog/submit/like/${this.article_idx}/`,
            method: "POST",
            dataType: "json",
            data : {
                "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            },
            success: data => {
                if (data.success) {
                    _this.success(data.reason);
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