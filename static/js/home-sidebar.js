$(document).ready(function() {
    let action_id = 0;
    const actions = new Array(...document.querySelector("#menubar").children);
    const pages = new Array(... document.querySelector("#main").children);
    actions.forEach(action => (
        action.onclick = event => {
            let val = actions.indexOf(action);
            if (val === action_id) {
                return;
            }

            actions[action_id].querySelector(".card").classList.remove("active");
            action.querySelector(".card").classList.add("active");
            pages  [action_id].hidden = true;
            pages[val].hidden = false;
            action_id = val;
        }
    ));
});