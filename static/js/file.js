const isIE = /msie/i.test(navigator.userAgent) && !window.opera;

let fileUnits = Array("B", "KiB", "MiB", "GiB");
let fileUnitStride = 1024;

function getFileSize(target) {
    if (isIE && !target.files) {
        let sys = new ActiveXObject("Scripting.FileSystemObject");
        return sys.GetFile(target.value).Size;
    } else {
        return target.files[0].size;
    }
}

function toFileSize(size, idx=0, fixed){
    while (size > fileUnitStride && idx < fileUnits.length - 1){
        size /= fileUnitStride;
        idx ++;
    }
    return `${size.toFixed(fixed || 2)} ${fileUnits[idx]}`;
}