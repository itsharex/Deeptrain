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
                mapChart.hideLoading();

                let country_values = [];
                data_json.data.forEach(n => (country_values.push(n.value)));
                let min = Math.min(country_values), max = Math.max(country_values);

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
                            min: 0,
                            max: max,
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