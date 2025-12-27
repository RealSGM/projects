document.addEventListener("DOMContentLoaded", () => {
    const ctx = document.getElementById("fishChart").getContext("2d");

    function makeGradient(ctx, color1, color2) {
        const gradient = ctx.createLinearGradient(0, 0, 0, 300);
        gradient.addColorStop(0, color1);
        gradient.addColorStop(1, color2);
        return gradient;
    }

    function randomData(count) {
        return Array.from({ length: count }, () =>
            Math.floor(Math.random() * 150) + 20
        );
    }

    const datasets = {
        week: {
            labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            tuna: randomData(7),
            salmon: randomData(7),
            cod: randomData(7),
        },
        month: {
            labels: Array.from({ length: 30 }, (_, i) => `Day ${i + 1}`),
            tuna: randomData(30),
            salmon: randomData(30),
            cod: randomData(30),
        },
        year: {
            labels: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
            tuna: randomData(12),
            salmon: randomData(12),
            cod: randomData(12),
        }
    };

    function createChart(range) {
        return new Chart(ctx, {
            type: "line",
            data: {
                labels: datasets[range].labels,
                datasets: [
                    {
                        label: "Tuna",
                        data: datasets[range].tuna,
                        borderColor: "#ff6384",
                        backgroundColor: makeGradient(ctx, "rgba(255,99,132,0.35)", "rgba(255,99,132,0.05)"),
                        tension: 0.4,
                        fill: true,
                        borderWidth: 2.5,
                    },
                    {
                        label: "Salmon",
                        data: datasets[range].salmon,
                        borderColor: "#36a2eb",
                        backgroundColor: makeGradient(ctx, "rgba(54,162,235,0.35)", "rgba(54,162,235,0.05)"),
                        tension: 0.4,
                        fill: true,
                        borderWidth: 2.5,
                    },
                    {
                        label: "Cod",
                        data: datasets[range].cod,
                        borderColor: "#4bc0c0",
                        backgroundColor: makeGradient(ctx, "rgba(75,192,192,0.35)", "rgba(75,192,192,0.05)"),
                        tension: 0.4,
                        fill: true,
                        borderWidth: 2.5,
                    },
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: { mode: "nearest", intersect: false },
                plugins: {
                    legend: {
                        labels: {
                            usePointStyle: true,
                            pointStyle: "circle"
                        }
                    }
                },
                scales: {
                    y: {
                        ticks: { font: { size: 11 } },
                        grid: { color: "rgba(0,0,0,0.06)" }
                    },
                    x: {
                        ticks: { font: { size: 10 } },
                        grid: { display: false }
                    }
                }
            }
        });
    }

    let range = "week";
    let chart = createChart(range);

    document.querySelectorAll(".filter-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelector(".filter-btn.active")?.classList.remove("active");
            btn.classList.add("active");

            range = btn.dataset.range;

            chart.destroy();
            chart = createChart(range);
        });
    });
});
