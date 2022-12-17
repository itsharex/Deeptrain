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
function createCheckbox(cid, text="", parent) {
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
    return checkbox(input, label);
}

function validateUsername() {
    let textInput = document.getElementById("id_username");
    let checkbox = createCheckbox("username", "Please enter 3-12 user name");
    let validator = () => {
        let val = $(textInput).val().trim();
        let err;
        if (!val) {
            err = "User name field is required";
        } else {
            if (!(3<=val.length && val.length <=12)) {
                // err = `账户名不能${3 <= val ? "大于12":"小于3"}位, 请输入3~12位账户名`;
                err = "Please enter 3-12 user name";
            }
        }
        err?function (){checkbox.setText(err);checkbox.error()}():checkbox.success();
    }
    textInput.onkeyup = textInput.onkeydown = textInput.onchange = textInput.onfocusout = validator;
    validator();
    return validator;
}

validateUsername();