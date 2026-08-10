document.addEventListener("DOMContentLoaded", () => {
    // API URL: Set to "" if frontend is served by the backend server,
    // or set to "http://127.0.0.1:8000" if deployed separately on Netlify/Vercel/S3.
    const API_BASE = "";

    // DOM Element References
    const statusBadge = document.getElementById("status-badge");
    const statusText = document.getElementById("status-text");
    const autoRefreshCheck = document.getElementById("auto-refresh-check");
    const refreshBtn = document.getElementById("refresh-btn");
    const exportPdfBtn = document.getElementById("export-pdf-btn");

    // KPI Elements
    const kpiPacketCount = document.getElementById("kpi-packet-count");
    const kpiTotalVolume = document.getElementById("kpi-total-volume");
    const kpiTopProto = document.getElementById("kpi-top-proto");
    const kpiConnCount = document.getElementById("kpi-conn-count");

    // Capture Form Elements
    const captureForm = document.getElementById("capture-form");
    const inputCount = document.getElementById("input-count");
    const inputProtocol = document.getElementById("input-protocol");
    const inputHost = document.getElementById("input-host");
    const inputPort = document.getElementById("input-port");
    const startCaptureBtn = document.getElementById("start-capture-btn");
    const btnText = document.getElementById("btn-text");
    const btnSpinner = document.getElementById("btn-spinner");
    const captureMessage = document.getElementById("capture-message");

    // Container Elements
    const protocolBarsContainer = document.getElementById("protocol-bars");
    const capturesListContainer = document.getElementById("captures-list");
    const topSrcIpsContainer = document.getElementById("top-src-ips");
    const topDstIpsContainer = document.getElementById("top-dst-ips");
    const topSrcPortsContainer = document.getElementById("top-src-ports");
    const topDstPortsContainer = document.getElementById("top-dst-ports");
    const connectionsTbody = document.getElementById("connections-tbody");

    // TCP Flag Elements
    const flagSyn = document.getElementById("flag-syn");
    const flagAck = document.getElementById("flag-ack");
    const flagFin = document.getElementById("flag-fin");
    const flagRst = document.getElementById("flag-rst");
    const flagPsh = document.getElementById("flag-psh");

    let isPolling = true;
    let pollInterval = null;

    // Fetch Traffic Statistics
    async function fetchStats() {
        try {
            const response = await fetch(`${API_BASE}/stats`);
            if (!response.ok) throw new Error("Failed to fetch stats");
            const data = await response.json();
            
            updateConnectionStatus("online", "Connected");
            renderDashboard(data);
        } catch (err) {
            console.error("Error fetching stats:", err);
            updateConnectionStatus("offline", "Disconnected");
        }
    }

    // Fetch PCAP Captures
    async function fetchCaptures() {
        try {
            const response = await fetch(`${API_BASE}/captures`);
            if (!response.ok) return;
            const data = await response.json();
            renderCaptures(data.files || []);
        } catch (err) {
            console.error("Error fetching captures:", err);
        }
    }

    // Update Status Badge
    function updateConnectionStatus(state, text) {
        statusBadge.className = `status-badge ${state}`;
        statusText.textContent = text;
    }

    // Render Stats Data into UI
    function renderDashboard(data) {
        // KPIs
        kpiPacketCount.textContent = (data.packet_count || 0).toLocaleString();
        kpiTotalVolume.textContent = `${data.total_kb || 0} KB`;
        
        const protocols = data.protocols || {};
        let topProto = "N/A";
        let maxProtoCount = 0;
        for (const [proto, count] of Object.entries(protocols)) {
            if (count > maxProtoCount) {
                maxProtoCount = count;
                topProto = proto;
            }
        }
        kpiTopProto.textContent = topProto;

        const connections = data.top_connections || [];
        kpiConnCount.textContent = connections.length;

        // Protocol Breakdown Bars
        renderProtocolBars(protocols, data.packet_count || 0);

        // TCP Flags
        const flags = data.tcp_flags || {};
        flagSyn.textContent = flags.SYN || 0;
        flagAck.textContent = flags.ACK || 0;
        flagFin.textContent = flags.FIN || 0;
        flagRst.textContent = flags.RST || 0;
        flagPsh.textContent = flags.PSH || 0;

        // Top Talkers
        renderStatList(topSrcIpsContainer, data.top_source_ips);
        renderStatList(topDstIpsContainer, data.top_destination_ips);
        renderStatList(topSrcPortsContainer, data.top_source_ports);
        renderStatList(topDstPortsContainer, data.top_destination_ports);

        // Connection Streams Table
        renderConnectionsTable(connections);
    }

    // Render Protocol Progress Bars
    function renderProtocolBars(protocols, totalPackets) {
        if (!protocols || Object.keys(protocols).length === 0 || totalPackets === 0) {
            protocolBarsContainer.innerHTML = `<div class="empty-state">No traffic captured yet.</div>`;
            return;
        }

        let html = "";
        for (const [proto, count] of Object.entries(protocols)) {
            const percent = totalPackets > 0 ? Math.round((count / totalPackets) * 100) : 0;
            const protoClass = proto.toLowerCase();
            html += `
                <div class="protocol-item ${protoClass}">
                    <div class="protocol-header">
                        <span><strong>${proto}</strong> (${count.toLocaleString()} packets)</span>
                        <span>${percent}%</span>
                    </div>
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill" style="width: ${percent}%;"></div>
                    </div>
                </div>
            `;
        }
        protocolBarsContainer.innerHTML = html;
    }

    // Render Stat List Items
    function renderStatList(container, statsDict) {
        if (!statsDict || Object.keys(statsDict).length === 0) {
            container.innerHTML = `<div class="empty-state">No data</div>`;
            return;
        }

        let html = "";
        for (const [key, count] of Object.entries(statsDict)) {
            html += `
                <div class="stat-list-item">
                    <span>${key}</span>
                    <span class="stat-count">${count}</span>
                </div>
            `;
        }
        container.innerHTML = html;
    }

    // Render Connection Streams Table
    function renderConnectionsTable(connections) {
        if (!connections || connections.length === 0) {
            connectionsTbody.innerHTML = `
                <tr>
                    <td colspan="5" class="table-empty">No connection streams captured yet.</td>
                </tr>
            `;
            return;
        }

        let html = "";
        for (const conn of connections) {
            html += `
                <tr>
                    <td>${conn.endpoint1}</td>
                    <td class="stream-direction">⇄</td>
                    <td>${conn.endpoint2}</td>
                    <td>${conn.packets}</td>
                    <td>${(conn.bytes / 1024).toFixed(2)} KB</td>
                </tr>
            `;
        }
        connectionsTbody.innerHTML = html;
    }

    // Render PCAP Files List with Download Button
    function renderCaptures(files) {
        if (!files || files.length === 0) {
            capturesListContainer.innerHTML = `<li class="empty-state">No capture files available.</li>`;
            return;
        }

        let html = "";
        for (const filename of files) {
            html += `
                <li>
                    <span class="capture-item-title">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
                        ${filename}
                    </span>
                    <div class="capture-actions">
                        <a href="${API_BASE}/captures/download/${filename}" class="btn btn-secondary btn-sm" download>
                            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                            Download
                        </a>
                    </div>
                </li>
            `;
        }
        capturesListContainer.innerHTML = html;
    }

    // Export PDF Report Event Handler
    if (exportPdfBtn) {
        exportPdfBtn.addEventListener("click", () => {
            window.print();
        });
    }

    // Trigger New Packet Capture
    captureForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const count = parseInt(inputCount.value) || 100;
        const protocol = inputProtocol.value || null;
        const host = inputHost.value.trim() || null;
        const port = inputPort.value ? parseInt(inputPort.value) : null;

        startCaptureBtn.disabled = true;
        btnText.textContent = "Capturing Packets...";
        btnSpinner.classList.remove("hidden");
        updateConnectionStatus("capturing", "Capturing...");

        captureMessage.classList.add("hidden");

        try {
            const response = await fetch(`${API_BASE}/capture`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ count, protocol, host, port })
            });

            if (!response.ok) throw new Error("Capture initiation failed");
            
            captureMessage.textContent = `Packet capture session initiated (${count} packets). Refreshing stats...`;
            captureMessage.classList.remove("hidden");

            setTimeout(() => {
                fetchStats();
                fetchCaptures();
            }, 2500);

        } catch (err) {
            console.error("Capture error:", err);
            captureMessage.textContent = "Failed to initiate packet capture session.";
            captureMessage.classList.remove("hidden");
        } finally {
            setTimeout(() => {
                startCaptureBtn.disabled = false;
                btnText.textContent = "Start Capture Session";
                btnSpinner.classList.add("hidden");
            }, 1000);
        }
    });

    // Auto Refresh Logic
    function startAutoRefresh() {
        if (pollInterval) clearInterval(pollInterval);
        pollInterval = setInterval(() => {
            if (isPolling) {
                fetchStats();
                fetchCaptures();
            }
        }, 3000);
    }

    autoRefreshCheck.addEventListener("change", (e) => {
        isPolling = e.target.checked;
    });

    refreshBtn.addEventListener("click", () => {
        fetchStats();
        fetchCaptures();
    });

    // Initial Load
    fetchStats();
    fetchCaptures();
    startAutoRefresh();
});
