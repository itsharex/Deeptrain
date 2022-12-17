let errorFrame = document.querySelector("#error-frame");
let form = document.getElementById("user-form");
document.getElementById("submit-box").onclick = () => {
    let url = form.getAttribute("ajax");
    $.ajax({
        data: new FormData(form),
        url: form.getAttribute("ajax"),
        method: "POST",
        processData: false,
        contentType: false,
        dataType : "json",
        success: data => {
            console.log(data)
            if (!data.success) {
                errorFrame.style.display = "inherit";
                document.querySelector("#error").innerText = data.reason;
            } else {
                errorFrame.style.display = "none";
                document.location.href = "/home/";
            }
        },
        error : () => {
            errorFrame.style.display = "inherit";
            document.querySelector("#error").innerText = "网站连接错误! 请稍后重试";
        }
    })
}
