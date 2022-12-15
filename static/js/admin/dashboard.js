let ChartSocket;
let baseStamp = 0;
const Interval = 1000;

function initializeSiteRequest(ajax_url) {
    $.ajax({
        url: ajax_url,
        success: data => (updateSiteRequestChart(data)),
    })
}
initGithubRepositoryData("zmh-program", "Zh-Website");
function initializeWebsocket(url) {
    ChartSocket = new websocket(url, document.querySelector("#message-window"));
    baseStamp = Number(new Date());
    ChartSocket.get_websocket().onmessage = function(e) {
        const data = JSON.parse(e.data);
        let now = Number(new Date());
        let offset = now - baseStamp - Interval;
        baseStamp = now;

        wsProgressUpdate(offset.toFixed(1));
        roundProgressUpdate(cpu_progress_dom, data.cpu.toFixed(1));
        roundProgressUpdate(ram_progress_dom, data.ram.toFixed(1));
        roundProgressUpdate(rom_progress_dom, data.disk.toFixed(1));
        recv.update(data.recv);
        send.update(data.send);
        updateDynamicRequestChart(data.request);
        addTodayRequest(data.request);
    }
}
