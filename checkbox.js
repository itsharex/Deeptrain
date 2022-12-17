checkbox = (selector, label) => (
    {
        target: selector,
        label: label,
        setText: text => {
            label.innerText = text;
        },
        success: () => {
            selector.checked = true;
            selector.indeterminate = false;
        },
        normal: () => {
            selector.checked = false;
            selector.indeterminate = false;
        },
        error: () => {
            selector.checked = false;
            selector.indeterminate = true;
        },
        isChecked : () => (selector.checked),
        isError: () => (selector.indeterminate),
    }
)

function createCheckbox(id) {
    document.createElement("input");
}