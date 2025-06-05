function formatTimestampToLabel(isoString) {
    const date = new Date(isoString);
    date.setMinutes(0, 0, 0);
    const month = date.getMonth() + 1;
    const day = date.getDate();
    const hour = String(date.getHours()).padStart(2, '0');
    const dayOfWeek = ['일', '월', '화', '수', '목', '금', '토'][date.getDay()];
    return `${month}/${day}(${dayOfWeek}) ${hour}:00`;
}

function extractHourLabel(isoString) {
    const date = new Date(isoString);
    date.setMinutes(0, 0, 0);
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hour = String(date.getHours()).padStart(2, '0');
    return `${month}/${day} ${hour}:00 기준`;
}

async function drawMiniChart(file, elementId, rankSelector = null, updateTime = false) {
    const res = await fetch(`./js/data/${file}`);
    const json = await res.json();
    const history = json.history.slice(-24);

    const chartEl = document.querySelector(elementId);
    if (!chartEl) return;

    const chartWrapper = chartEl.closest(".chart");
    const chartNoneEl = chartWrapper?.querySelector(".chart_none");

    // ✅ song 타이틀 표시
    const title = json.title;
    if (title && chartWrapper) {
        const songTitleEl = chartWrapper.querySelector(".song");
        if (songTitleEl) {
            songTitleEl.textContent = title;
        }
    }

    if (!history.length) {
        chartEl.classList.add("hide");
        if (chartNoneEl) chartNoneEl.classList.remove("hide");
        return;
    }

    chartEl.classList.remove("hide");
    if (chartNoneEl) chartNoneEl.classList.add("hide");

    const labels = history.map(e => formatTimestampToLabel(e.timestamp));

    // ✅ 플랫폼별 chartLimit 설정
    let chartLimit = 100;
    if (file.includes("genie")) chartLimit = 200;
    if (file.includes("vibe")) chartLimit = 300;

    const series = history.map(e => {
        if (e.rank === null || e.rank > chartLimit) return null;
        return chartLimit + 1 - e.rank;
    });
    const visualSeries = series.map(v => v === null ? 0.5 : v);

    const latest = history[history.length - 1];
    const prev = history.length >= 2 ? history[history.length - 2] : null;

    let rankText = "", spanText = "", rankClass = "";
    const latestRank = latest.rank;
    const prevRank = prev?.rank ?? null;

    const isOut = latestRank === null || latestRank > chartLimit;
    const wasOut = prevRank === null || prevRank > chartLimit;

    if (isOut) {
        rankText = "";
        spanText = "차트아웃 ❌";
    } else {
        rankText = `${latestRank}위`;
        if (wasOut) {
            spanText = "🆕";
        } else {
            const diff = prevRank - latestRank;
            if (diff > 0) spanText = `🔺${diff}`;
            else if (diff < 0) spanText = `🔻${Math.abs(diff)}`;
        }
    }

    if (rankSelector) {
        const el = document.querySelector(rankSelector);
        if (el) {
            el.classList.remove("up", "down");
            if (rankClass) el.classList.add(rankClass);
            el.innerHTML = `${rankText}${spanText ? ` <span>${spanText}</span>` : ""}`;
        }
    }

    if (updateTime) {
        const timeEl = document.querySelector(".box.music_chart .time");
        if (timeEl) timeEl.textContent = extractHourLabel(latest.timestamp);
    }

    const options = {
        chart: { type: 'area', height: 80, toolbar: { show: false }, zoom: { enabled: false } },
        grid: { show: false },
        dataLabels: { enabled: false },
        colors: ["#5a81fa"],
        fill: {
            type: 'gradient',
            gradient: {
                shade: 'light',
                type: 'vertical',
                gradientToColors: ['#ffffff'],
                opacityFrom: 0.7,
                opacityTo: 0,
                stops: [0, 100]
            }
        },
        stroke: { curve: 'smooth', width: 2 },
        markers: { size: 0 },
        yaxis: { min: 0, max: chartLimit, show: false },
        xaxis: {
            categories: false,
            labels: { show: false },
            axisTicks: { show: false },
            axisBorder: { show: false }
        },
        tooltip: {
            custom: function ({ series, dataPointIndex }) {
                const raw = series[0][dataPointIndex];
                const actual = raw === 0.5 ? null : chartLimit + 1 - raw;
                const label = labels[dataPointIndex];
                return `
                    <div class="custom_tooltip">
                        <div class="date">${label}</div>
                        <div class="rank_count">${actual === null ? "차트아웃" : `${actual}위`}</div>
                    </div>`;
            }
        },
        series: [{
            name: "순위",
            data: visualSeries
        }]
    };

    const chart = new ApexCharts(chartEl, options);
    chart.render();
}

drawMiniChart("melon_top.json", "#melonTop100Chart", ".melon_top .rank", true);
drawMiniChart("melon_hot.json", "#melonHot100Chart", ".melon_hot .rank");
drawMiniChart("genie.json", "#genieChart", ".genie .rank");
drawMiniChart("bugs.json", "#bugsChart", ".bugs .rank");
drawMiniChart("vibe.json", "#vibeChart", ".vibe .rank");
drawMiniChart("flo.json", "#floChart", ".flo .rank");
drawMiniChart("melon_realtime.json", "#melonRealTimeChart", ".melon_realtime .rank");