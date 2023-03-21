const searchInput = document.getElementById("search");
const container = document.getElementById("file-container");

let timeout;
let before;
let search_last;

let active_page = 1;
let total_pages = 0;

let ajax_url = "<empty>";
let pagination = document.querySelector(".pagination").children[0];

const event = () => {
    let val = searchInput.value.trim();
    if (val === before) {
        return;
    }
    before = val;
    if (val.length < 35) {
        search(val);
    }
}
searchInput.onkeyup = _ => {
    clearTimeout(timeout);
    timeout = setTimeout(event, 800);
}
searchInput.onchange = event;

const asyncRedirect = (url, timeout) => (setTimeout(() => (window.location.href = url), timeout || 200));
function createFileCard(tag, filename, datetime, size, url, username) {
    let date = new Date(datetime).toDateString();
    let date_string = date.slice(date.split(" ")[0].length + 1);
    let html = `<div class='file__tags'><span class='task__tag task__tag--${tag}'>${tag}</span><button class='task__options'><i class="fas fa-ellipsis-h"></i></button></div>
        <p>${filename}</p>
        <div class='file__stats'>
            <span><time datetime="${datetime}"><i class="fas fa-flag">${date_string}</i></time></span>
            <span><i class="fas fa-comment"></i>${toFileSize(size)}</span>
            <span><i class="fas fa-paperclip"></i>${username}</span>
            <a href="${url}">
                <span class='task__owner'><svg xmlns="http://www.w3.org/2000/svg" aria-hidden="true" role="img" width="2em" height="2em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15V3m0 12l-4-4m4 4l4-4M2 17l.621 2.485A2 2 0 0 0 4.561 21h14.878a2 2 0 0 0 1.94-1.515L22 17"></path></svg></span>
            </a>
        </div>`

    let card = document.createElement("div");
    card.classList.add("file-card");
    card.innerHTML = html;
    container.appendChild(card);
    $(card).fadeIn(1000);
}

function clearFileCard() {
    container.innerHTML = "";
}

const search = content => (ajax(content));
const initialize = () => (ajax("", 1, true));

function ajax(content, page=1, initial=false) {
    if (!initial && !availablePage(page)) {
        return;
    }

    $.ajax({
        url: ajax_url,
        data: {
            name: content,
            page: page,
        },
        success: data => {
            clearFileCard();
            active_page = page;
            let objs = data.data;
            for (let i = 0; i < objs.length; i++) {
                let obj = objs[i];
                createFileCard(obj.tag, highlight(obj.name, content), obj.time, obj.size, obj.url, obj.user);
            }
            initializePages(data.total);
        }
    });
    search_last = content;
}

const availablePage = i => (1 <= i && i <= total_pages);
const getAvailablePage = i => (availablePage(i) ? i: undefined);

function changePageEvent () {
    let input, page = this.getAttribute("page");
    switch (page) {
        case "<":
            input = active_page - 1;
            break;
        case ">":
            input = active_page + 1;
            break;
        case "...":
            return;
        default:
            input = Number(page);
            break;
    }
    ajax(search_last, input);
}

function createPage(i) {
    let child = document.createElement("li");
    switch (true) {
        case i === active_page:
            child.classList.add("active");
            break;
        case i === "...":
            child.classList.add("more");
            break;
        default:
            break;
    }
    child.innerHTML = `<a>${i}</a>`;
    child.setAttribute("page", i.toString());
    child.onclick = changePageEvent;
    pagination.appendChild(child);
}
function initializePages(_total) {
    // if (_total === total_pages) {
    //     return;
    // } else {
    //     total_pages = _total;
    // }
    total_pages = _total;
    pagination.innerHTML = "";
    if (total_pages <= 5) {for (let i = 0; i < total_pages; i++) {createPage(i + 1)}}
    else {
        let list = [
            active_page !== 1 ? "<": undefined,
            getAvailablePage(active_page - 1), active_page, getAvailablePage(active_page + 1),
            ...(active_page !== total_pages ?
                [ ...(active_page + 1 !== total_pages ?["...", total_pages]:[undefined, ]), ">"]: [undefined, ]),
        ].filter(Boolean);
        for (let i = 0; i < list.length; i++){createPage(list[i])}
    }
}

function highlight(text, keyword) {
    let keywords = keyword.split(" ").sort((a, b) => b.length - a.length);
    return text.replace(new RegExp(`(${keywords.join('|')})`, 'gi'), "<span class='red'>$1</span>")
}