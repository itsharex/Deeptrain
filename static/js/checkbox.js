const checkList = document.getElementById("checklist");
let redirect = () => (document.location.href="/home/");
const checkbox = (selector, label) => (
    {
        target: selector,
        label: label,
        setText: text => {
            label.innerText = text;
        },
        success: () => {
            selector.checked = true;
            selector.indeterminate = false;
            return true;
        },
        normal: () => {
            selector.checked = false;
            selector.indeterminate = false;
            return false;
        },
        error: () => {
            selector.checked = false;
            selector.indeterminate = true;
            return false;
        },
        hidden: () => {
            selector.style.display = "none";  // 已设置display属性, hidden不可用
            label.style.display = "none";
        },
        display: () => {
            selector.style.display = "grid";
            label.style.display = "grid";
        },
        setVisible: function(visible=false) {
            visible?this.display():this.hidden();
        },
        isSuccess: () => (selector.checked),
        isError: () => (selector.indeterminate),
    }
)
function createCheckbox(cid, text="", visible=true, parent) {
    let id = `checkbox-${cid}`;
    let input = document.createElement("input");
    input.id = id;
    input.type = "checkbox";
    input.disabled = true;
    
    let label = document.createElement("label");
    label.for = id;
    label.innerText = text;
    let node = parent || checkList;
    node.appendChild(input);
    node.appendChild(label);
    let object = checkbox(input, label);
    object.setVisible(visible);
    return object;
}

function usernameValidator() {
    let textInput = document.getElementById("id_username");
    let checkbox = createCheckbox("username", "Please enter 3 to 12 username");
    let validator = () => {
        let length = $(textInput).val().trim().length;
        return (3 > length || length > 12)? checkbox.error(): checkbox.success();
    }
    textInput.onkeyup = textInput.onkeydown = textInput.onchange = textInput.onfocusout = ()=>{validator()}; //  使validator不返回值, 造成校验错误时输入框输入不动
    return validator;
}

function textAreaValidator() {
    let textInput = document.getElementById("id_textarea");
    let checkbox = createCheckbox("username", "Please enter 1 to 200 profile");
    let validator = () => {
        let length = $(textInput).val().trim().length;
        return (1 > length || length > 200)? checkbox.error(): checkbox.success();
    }
    textInput.onkeyup = textInput.onkeydown = textInput.onchange = textInput.onfocusout = ()=>{validator()}; //  使validator不返回值, 造成校验错误时输入框输入不动
    return validator;
}

function passwordValidator() {
    let textInput = document.getElementById("id_password");
    let checkbox = createCheckbox("password", "Please enter 6 to 14 password");
    let validator = () => {
        let length = $(textInput).val().trim().length;
        return (6 > length || length > 14)? checkbox.error(): checkbox.success();
    }
    textInput.validator = validator;
    textInput.onkeyup = textInput.onkeydown = textInput.onchange = textInput.onfocusout = ()=>{validator()};
    return validator;
}

function repasswordValidator() {
    let textInput = document.getElementById("id_re_password");
    let targetInput = document.getElementById("id_password");
    let checkbox = createCheckbox("re_password", "Enter the password again");
    let validator = () => {
        return ($(textInput).val().trim() !== $(targetInput).val().trim())? checkbox.error(): checkbox.success();
    }
    textInput.onkeyup = textInput.onkeydown = textInput.onchange = textInput.onfocusout = ()=>{validator()};
    targetInput.onkeyup = targetInput.onkeydown = targetInput.onchange = targetInput.onfocusout = () => {textInput.value.trim()?validator():0;targetInput.validator();}
    return validator;
}

function oldPasswordValidator() {
    let textInput = document.getElementById("id_old_password");
    let checkbox = createCheckbox("old_password", "Please enter the old password");
    let validator = () => {
        let length = $(textInput).val().trim().length;
        return (6 > length || length > 14)? checkbox.error(): checkbox.success();
    }
    textInput.onkeyup = textInput.onkeydown = textInput.onchange = textInput.onfocusout = ()=>{validator()};
    return validator;
}

function hCaptchaValidator() {
    // hCaptcha.com 引入稍慢, 因此等iframe引入后运行
    // 异步, 不阻塞线程
    let captchaInput;
    let checkbox = createCheckbox("captcha", "Please enter the Captcha");
    let isSuccess = false;
    let validator = () => {
        return !isSuccess? checkbox.error(): checkbox.success();
    }
    let interval = setInterval(function() {
        if (!!document.getElementById("id_captcha").children[0]) {
            clearTimeout(interval);
            captchaInput = document.getElementById("id_captcha").children[0];
            // captchaInput.onclick = captchaInput.onfocusout = ()=>{validator()};
            let captchaInterval = setInterval(function() {
                isSuccess = !!captchaInput.getAttribute("data-hcaptcha-response");
                if (isSuccess) {clearTimeout(captchaInterval);validator()}
            }, 200);
        }
    }, 500);

    return validator;
}

function TurnstileValidator() {
    // turnstile 引入稍慢, 因此等iframe引入后运行
    // 异步, 不阻塞线程
    let captchaInput;
    let checkbox = createCheckbox("captcha", "Please enter the Captcha");
    let isSuccess = false;
    let validator = () => {
        return !isSuccess? checkbox.error(): checkbox.success();
    }
    let interval = setInterval(function() {
        if (!!document.getElementById("id_captcha").children[0]) {
            clearTimeout(interval);
            captchaInput = document.getElementById("id_captcha").children[1];
            let captchaInterval = setInterval(function() {
                isSuccess = !!captchaInput.getAttribute("value");
                if (isSuccess) {clearTimeout(captchaInterval);validator()}
            }, 200);
        }
    }, 500);

    return validator;
}

let userForm = {
    defaultText: "Waiting for the reply...",
    checkbox: createCheckbox("error", this.defaultText, false),
    success: function() {
        this.checkbox.success();
        this.checkbox.hidden();
        setTimeout(redirect, 500);
    },
    error: function(msg="") {
        this.checkbox.error();
        this.checkbox.display();
        this.checkbox.setText(msg);
    },
    form: document.getElementById("user-form"),
    submit: function () {
        $.ajax({
            data: new FormData(this.form),
            url: this.form.getAttribute("ajax"),
            method: "POST",
            processData: false,
            contentType: false,
            dataType: "json",
            success: data => (data.success ? this.success(): this.error(data.reason)),
            error: () => (this.error("Website connection error! Please try again later")),
        });
        this.checkbox.display();
        this.checkbox.normal();
        this.checkbox.setText(this.defaultText);
    },
}

function $validate(validators) {
    let validate = function () {
        (validators.every(
            validator => validator()
        ))?userForm.submit():0;
    };
    validate();
    document.getElementById("submit-box").onclick = validate;
}
