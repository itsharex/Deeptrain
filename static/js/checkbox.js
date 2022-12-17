const checkList = document.getElementById("checklist");
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
function createCheckbox(id, text, parent) {
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
    return checkbox(input, label);
}
