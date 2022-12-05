const dom = document.getElementById('chart-container');
const mapChart = echarts.init(dom, null, {
    renderer: 'canvas',
    useDirtyRect: false
});
let option;
mapChart.showLoading();
function initialize(map_url, data_url) {
    $.get(map_url, function (map_json) {
        $.ajax({
            url: data_url,
            contentType: "json",
            success: function(data_json) {
                // let name_map = {};
                // for (let i = 0, object=Object(data_json.data); i < object.length; i++) {
                //     let obj = object[i];
                //     console.log(obj)
                //     name_map[obj.name] = obj.value;
                // }
                // console.log(name_map)
                mapChart.hideLoading();
                echarts.registerMap('World', map_json);
                mapChart.setOption(
                    (option = {
                        title: {
                            text: `Website Request (7 days)  - total ${data_json.total}`,
                            },
                        tooltip: {
                            trigger: 'item',
                            formatter: function (obj) {
                                return `${obj.name}<br/>${obj.value?obj.value:0} requests`
                            },
                        },
                        visualMap: {
                            min: 800,
                            max: 50000,
                            text: ['High', 'Low'],
                            realtime: false,
                            calculable: true,
                            inRange: {
                                color: ['lightskyblue', 'yellow', 'orangered']
                            }
                        },
                        series: [
                            {
                                name: 'SiteRequest',
                                type: 'map',
                                map: 'World',
                                label: {
                                    show: false,
                                },
                                data: data_json.data,
                            }
                        ]
                    })
                );
            }
        });
    });
}
window.addEventListener('resize', mapChart.resize);