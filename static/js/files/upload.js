let upload;
window.addEventListener("DOMContentLoaded",() => {
    upload = new UploadModal("#upload");
});

let ajax_url = "";
let max_filename_length_limit = -1;
let max_filesize_limit = -1;

class UploadModal {
    filename = "";
    isCopying = false;
    isUploading = false;
    progress = 0;
    state = 0;

    constructor(el) {
        this.el = document.querySelector(el);
        this.fileField = this.el?.querySelector("#id_file");

        this.el?.addEventListener("click",this.action.bind(this));
        this.fileField?.addEventListener("change",this.fileHandle.bind(this));
    }
    action(e) {
        this[e.target?.getAttribute("data-action")]?.();
        this.stateDisplay();
    }
    cancel() {
        this.isUploading = false;
        this.progress = 0;
        this.state = 0;
        this.stateDisplay();
        this.progressDisplay();
        this.object.abort();
        this.fileReset();
    }
    async copy() {
        const copyButton = this.el?.querySelector("[data-action='copy']");
        if (!this.isCopying && copyButton) {
            // disable
            this.isCopying = true;
            copyButton.style.width = `${copyButton.offsetWidth}px`;
            copyButton.disabled = true;
            copyButton.textContent = "Copied!";
            await navigator.clipboard.writeText(this._copy?this._copy:this.filename);
            await new Promise(res => setTimeout(res, 1000));
            // re-enable
            this.isCopying = false;
            copyButton.removeAttribute("style");
            copyButton.disabled = false;
            copyButton.textContent = "Copy Link";
        }
    }
    fail(message="Your file could not be uploaded due to an error. Try uploading it again?") {
        this.isUploading = false;
        this.progress = 0;
        this.state = 2;
        this.stateDisplay();
        this.el.querySelector("#error-message").innerText = message;
    }
    file() {
        this.fileField.click();
    }
    fileDisplay(name = "") {
        // update the name
        this.filename = name;

        const fileValue = this.el?.querySelector("[data-file]");
        if (fileValue) fileValue.textContent = this.filename;

        // show the file
        this.el?.setAttribute("data-ready", this.filename ? "true" : "false");
    }
    fileHandle(e) {
        return new Promise(() => {
            const { target } = e;
            if (target?.files.length) {
                let reader = new FileReader();
                reader.onload = e2 => {
                    this.fileDisplay(target.files[0].name);
                };
                reader.readAsDataURL(target.files[0]);
            }
        });
    }
    fileReset() {
        if (this.fileField) this.fileField.value = null;

        this.fileDisplay();
    }
    progressDisplay() {
        const progressValue = this.el?.querySelector("[data-progress-value]");
        const progressFill = this.el?.querySelector("[data-progress-fill]");
        const progressTimes100 = Math.floor(this.progress * 100);

        if (progressValue) progressValue.textContent = `${progressTimes100}%`;
        if (progressFill) progressFill.style.transform = `translateX(${progressTimes100}%)`;
    }
    progressUpdate(n) {
        this.progress = n;
        this.progressDisplay();
    }
    stateDisplay() {
        this.el?.setAttribute("data-state", `${this.state}`);
    }
    getRootPath = () => (window.document.location.href.substring(0, window.document.location.href.indexOf(window.document.location.pathname)));

    success(_copy="") {
        this.isUploading = false;
        this.state = 3;
        this._copy = _copy.trim()?this.getRootPath()+_copy:"";
        this.stateDisplay();
    }
    upload() {
        if (!this.isUploading) {
            this.isUploading = true;
            this.progress = 0;
            this.state = 1;
            this.object = new FileUploadObject();
        }
    }
}

class FileUploadObject {
    constructor() {
        this.form = new FormData(upload.el);
        if (this.verify()) {
            this.ajax = $.ajax({
                url: ajax_url,
                data: this.form,
                processData: false,
                contentType: false,
                method: "POST",
                xhr: function () {
                    const xhr = $.ajaxSettings.xhr();
                    if (xhr.upload) {
                        xhr.upload.addEventListener('progress', e => {
                                const {loaded, total} = e;
                                upload.progressUpdate(loaded / total);
                            }, false,
                        );
                        return xhr;
                    }
                },
                success: e => {
                    e.success ? upload.success(e.link) : upload.fail(e.error);
                },
                error: upload.fail,
            });
        }
    }

    verify() {
        let input = upload.fileField;
        if (!input.files[0]) {
            upload.fail("File is required");
            return false;
        }
        if (input.files[0].name.length > max_filename_length_limit) {
            upload.fail(`File name is too long > ${max_filename_length_limit} (${input.files[0].name.length})`);
            return false;
        }

        let size = getFileSize(input);
        if (size > max_filesize_limit) {
            upload.fail(`The file is too large > ${toFileSize(max_filesize_limit, 0, 0)}`);
            return false;
        }
        return true;
    }
    abort() {
        return this.ajax?this.ajax.abort():undefined;
    }
}
