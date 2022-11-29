let input;
let area = document.querySelector("#area");
let description = document.querySelector("#desc");
let msg = document.querySelector(".message-line");
let max_size;
let max_name;
let ajax_url;
let commit_button = document.getElementById("commit");
let commit_button_width = `${commit_button.offsetWidth} px`;

let loading = false;
let commit_span = $(document.getElementById("commit-span"));
let loading_animation = $(document.getElementById("loading"));

let timeout;

const canSubmit = () => {
    return updateInput() && !loading;
}

function init(selector, _max_size, max_name_length, url) {
    input = document.querySelector(selector);
    max_size = _max_size || 1024;
    max_name = max_name_length;
    ajax_url = url;

    setLoadingState(false);
    commit_button.style.width = `${commit_button.offsetWidth} px`;
}

document.getElementById("cancel-file").onclick = () => {
    $(input).val("");
    area.innerText = "Drag a file here to upload.";
    description.innerHTML = "Alternatively, you can select a file by <br><strong>clicking here</strong>";
    add_messages([]);
};

function updateInput() {
    {
        let errs = [];
        if (!input.files[0]) {
            errs.push(["error", `File is required`]);
            add_messages(errs);
            return false;
        }
        if (input.files[0].name.length > max_name) {
            errs.push(["error", `File name is too long > ${max_name} (${input.files[0].name.length})`]);
        }
        let size = getFileSize(input);
        if (size > max_size) {
            errs.push(["error", `The file is too large > ${toFileSize(max_size, 0, 0)}`]);
        }
        area.innerText = input.files[0].name;
        description.innerHTML = `<strong>${toFileSize(size)}</strong>`;
        add_messages(errs);
        return $.isEmptyObject(errs);
    }
}

function _add_message(type, content) {
    let dom;
    switch (type) {
        case "error":
            dom = document.createElement("div");
            dom.classList.add("error");
            dom.innerHTML = `<i class="fa fa-solid fa-circle-xmark"></i>&nbsp;${content}`;
            break;
        case "success":
            dom = document.createElement("div");
            dom.classList.add("success");
            dom.innerHTML = `<i class="fa fa-solid fa-circle-check"></i>&nbsp;Successfully upload file ${content}`
            break;
        case "link":
            dom = document.createElement("a");
            dom.href = content;
            dom.classList.add("link");
            dom.innerHTML = '<i class="fa fa-solid fa-circle-chevron-right"></i>&nbsp; Download the submitted file';
            break;
    }
    msg.appendChild(dom);
}

function add_messages(arguments) {
    msg.innerHTML = "";
    for (let i = 0; i < arguments.length; i++) {
        _add_message(...arguments[i]);
    }
}

function setLoadingState(state){
    loading = state;
    // switch (state) {
    //     case true:
    //         commit_span.hide();
    //         loading_animation.show();
    //         break;
    //     case false:
    //         commit_span.show();
    //         loading_animation.hide();
    //         break;
    // }
    clearTimeout(timeout);
    timeout = setTimeout(function() {
            [commit_span, loading_animation][Number(state)].show();
            [commit_span, loading_animation][Number(!state)].hide();
            commit_button.style.width = `${commit_button.offsetWidth} px`;
    }, 100);  // 延迟响应, 设置延迟的等待最小限制 (<100ms 不显示等待动画)
}

commit_button.onclick = () => {
    let form = new FormData(document.querySelector("#fileform"));
    if (!canSubmit()){
        return;
    }
    setLoadingState(true);
    $.ajax({
        url: ajax_url,
        method: "POST",
        processData: false,
        contentType: false,
        data: form,
        success: data => {
            switch (data.success){
                case true:
                    add_messages([
                        ["success", data.name],
                        ["link", data.link],
                    ]);
                    break;
                case false:
                    add_messages([
                        ["error", data.error],
                    ]);
                    break;
            }
            setLoadingState(false);
        },
        error: err => {
            add_messages([["error", "Connection Error"], ]);
            setLoadingState(false);
        }
    })
}