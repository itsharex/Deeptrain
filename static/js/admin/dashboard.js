let ChartSocket;
let baseStamp = 0;
const Interval = 1000;

function initializeSiteRequest(ajax_url) {
    $.ajax({
        url: ajax_url,
        success: data => (updateSiteRequestChart(data)),
    })
}

function initializeWebsocket(url) {
    ChartSocket = new websocket(url, document.querySelector("#message-window"));
    baseStamp = Number(new Date());
    ChartSocket.get_websocket().onmessage = function(e) {
        const data = JSON.parse(e.data);
        let now = Number(new Date());
        let offset = now - baseStamp - Interval;
        baseStamp = now;

        wsProgressUpdate(offset.toFixed(1));
        data.cpu?roundProgressUpdate(cpu_progress_dom, data.cpu.toFixed(1)):0;
        data.ram?roundProgressUpdate(ram_progress_dom, data.ram.toFixed(1)):0;
        data.disk?roundProgressUpdate(rom_progress_dom, data.disk.toFixed(1)):0;
        data.recv?recv.update(data.recv):0;
        data.send?send.update(data.send):0;
        data.request?updateDynamicRequestChart(data.request):0;
    }
}
