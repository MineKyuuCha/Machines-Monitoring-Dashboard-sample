
import streamlit as st
from datetime import datetime, timedelta
import random
import textwrap
import plotly.graph_objects as go

# ============================================================
# WELDING MACHINE MONITORING SYSTEM
# Visual prototype
#
# IMPORTANT:
# This version is still using DEMO DATA.
# Later, replace get_demo_data() with database.py / machines.db.
# ============================================================

st.set_page_config(
    page_title="Welding Machine Monitoring System",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------
# DEMO DATA
# ------------------------------------------------------------

now = datetime.now()

machines = [
    {
        "id": "Machine 01",
        "status": "ON",
        "since": now - timedelta(hours=6, minutes=19, seconds=43),
        "last_off": now - timedelta(days=1, hours=21, minutes=25, seconds=17),
        "total_on": timedelta(hours=6, minutes=19, seconds=43),
        "total_off": timedelta(hours=1, minutes=40, seconds=37),
    },
    {
        "id": "Machine 02",
        "status": "OFF",
        "since": now - timedelta(hours=4, minutes=6, seconds=27),
        "last_on": now - timedelta(hours=4, minutes=6, seconds=27),
        "total_on": timedelta(hours=2, minutes=22, seconds=29),
        "total_off": timedelta(hours=5, minutes=7, seconds=31),
    },
    {
        "id": "Machine 03",
        "status": "ON",
        "since": now - timedelta(hours=6, minutes=36, seconds=58),
        "last_off": now - timedelta(days=1, hours=22, minutes=17, seconds=50),
        "total_on": timedelta(hours=6, minutes=36, seconds=58),
        "total_off": timedelta(hours=1, minutes=23, seconds=2),
    },
    {
        "id": "Machine 04",
        "status": "OFF",
        "since": now - timedelta(hours=2, minutes=16, seconds=12),
        "last_on": now - timedelta(hours=8, minutes=1, seconds=12),
        "total_on": timedelta(hours=5, minutes=44, seconds=48),
        "total_off": timedelta(hours=2, minutes=15, seconds=12),
    },
]

# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------

def html(value):
    """Remove Python indentation so Streamlit doesn't interpret
    indented HTML as a Markdown code block."""
    return textwrap.dedent(value).strip()


def fmt_td(value):
    total = max(0, int(value.total_seconds()))
    h = total // 3600
    m = (total % 3600) // 60
    s = total % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


def fmt_time(dt):
    return dt.strftime("%H:%M:%S")


def fmt_date_time(dt):
    return dt.strftime("%d %b %Y %H:%M:%S")


def utilization(machine):
    total = machine["total_on"] + machine["total_off"]
    if total.total_seconds() == 0:
        return 0
    return machine["total_on"].total_seconds() / total.total_seconds() * 100


# ------------------------------------------------------------
# CSS
# ------------------------------------------------------------

st.markdown(
    html("""
    <style>
    /* ================= APP ================= */

    .stApp {
        background:
            radial-gradient(circle at 82% 8%, rgba(24,103,185,.10), transparent 28%),
            radial-gradient(circle at 15% 90%, rgba(15,70,120,.10), transparent 30%),
            #071019;
        color: #edf4fb;
    }

    section.main > div {
        max-width: none !important;
    }

    .block-container {
        max-width: none !important;
        width: 100% !important;
        padding: 0.5rem 1.4rem 1rem 1.4rem !important;
    }

    /* Hide Streamlit decoration */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background: transparent !important;}

    /* ================= SIDEBAR ================= */

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b1620 0%, #08121b 100%);
        border-right: 1px solid #1d2c39;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.2rem;
    }

    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 0 8px 20px 8px;
    }

    .sidebar-logo {
        width: 42px;
        height: 42px;
        border: 1px solid #344757;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #101f2c;
        font-size: 22px;
    }

    .sidebar-title {
        font-size: 15px;
        font-weight: 800;
        letter-spacing: .4px;
    }

    .sidebar-subtitle {
        color: #81909f;
        font-size: 10px;
        margin-top: 2px;
    }

    .nav-item {
        height: 46px;
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 0 15px;
        margin: 5px 0;
        border-radius: 7px;
        color: #c8d2dc;
        font-size: 15px;
    }

    .nav-active {
        background: linear-gradient(90deg, #1169cf, #0957b0);
        color: white;
        box-shadow: inset 0 0 0 1px rgba(73,160,255,.18);
    }

    .nav-icon {
        width: 22px;
        text-align: center;
        font-size: 17px;
    }

    .sidebar-divider {
        height: 1px;
        background: #263541;
        margin: 30px 8px 16px;
    }

    .system-info-title {
        color: #298cff;
        font-size: 13px;
        font-weight: 800;
        letter-spacing: .6px;
        margin: 0 8px 12px;
    }

    .system-row {
        display: flex;
        justify-content: space-between;
        color: #c6d0da;
        font-size: 12px;
        padding: 5px 8px;
    }

    .system-row span:last-child {
        color: #edf4fb;
    }

    /* ================= HEADER ================= */

    .top-header {
        min-height: 80px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #1a2935;
        margin-bottom: 16px;
    }

    .header-left {
        display: flex;
        align-items: center;
        gap: 13px;
    }

    .header-logo {
        font-size: 38px;
        line-height: 1;
        filter: grayscale(1) brightness(1.7);
    }

    .header-title {
        font-size: 25px;
        font-weight: 850;
        letter-spacing: .5px;
    }

    .header-subtitle {
        color: #9aa9b8;
        font-size: 14px;
        margin-top: 3px;
    }

    .header-right {
        text-align: right;
    }

    .header-date {
        color: #bdc7d1;
        font-size: 14px;
        margin-bottom: 8px;
    }

    .online {
        color: #43dc50;
        font-size: 13px;
        font-weight: 700;
    }

    .online-dot {
        display: inline-block;
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background: #43dc50;
        box-shadow: 0 0 10px rgba(67,220,80,.65);
        margin-right: 8px;
    }

    /* ================= SECTION ================= */

    .section-title {
        color: #278cff;
        font-size: 17px;
        font-weight: 850;
        letter-spacing: .5px;
        margin: 6px 0 10px 3px;
    }

    /* ================= SUMMARY ================= */

    .summary-card {
        min-height: 115px;
        background: linear-gradient(145deg, #101c27, #0b151e);
        border: 1px solid #253541;
        border-radius: 8px;
        box-shadow: 0 8px 20px rgba(0,0,0,.18);
        padding: 17px 19px;
        position: relative;
        overflow: hidden;
    }

    .summary-label {
        font-size: 13px;
        font-weight: 700;
        color: #d5dde5;
    }

    .summary-value {
        font-size: 30px;
        font-weight: 850;
        margin-top: 13px;
    }

    .summary-small {
        color: #a6b2be;
        font-size: 13px;
    }

    .summary-icon {
        position: absolute;
        right: 18px;
        top: 27px;
        width: 57px;
        height: 57px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 27px;
        background: rgba(20,70,120,.35);
        border: 1px solid rgba(60,130,210,.18);
    }

    .blue { color: #4aa3ff; }
    .green { color: #39d94c; }
    .red { color: #ff414b; }
    .yellow { color: #ffc21a; }

    /* ================= MACHINE CARD ================= */

    .machine-card {
        min-height: 315px;
        background: linear-gradient(145deg, #101b25, #0b151e);
        border-radius: 7px;
        padding: 14px 17px;
        border: 1px solid #2a3b48;
        box-shadow: 0 7px 18px rgba(0,0,0,.20);
    }

    .machine-on {
        border-color: #23783b;
        box-shadow:
            inset 0 0 0 1px rgba(40,210,70,.05),
            0 7px 18px rgba(0,0,0,.20);
    }

    .machine-off {
        border-color: #71313a;
    }

    .machine-head {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
    }

    .machine-name {
        font-size: 14px;
        font-weight: 850;
    }

    .machine-dot {
        display: inline-block;
        width: 9px;
        height: 9px;
        border-radius: 50%;
        margin-right: 7px;
        vertical-align: middle;
    }

    .dot-on {
        background: #3bd84d;
        box-shadow: 0 0 8px rgba(59,216,77,.65);
    }

    .dot-off {
        background: #f03643;
        box-shadow: 0 0 8px rgba(240,54,67,.35);
    }

    .status-pill {
        font-size: 12px;
        font-weight: 800;
        padding: 4px 15px;
        border-radius: 5px;
    }

    .pill-on {
        color: #42dc50;
        background: rgba(40,190,60,.15);
        border: 1px solid #278b3a;
    }

    .pill-off {
        color: #ff4751;
        background: rgba(220,40,50,.13);
        border: 1px solid #8b3039;
    }

    .machine-body {
        display: flex;
        align-items: center;
        gap: 19px;
        min-height: 145px;
    }

    .power {
        width: 70px;
        text-align: center;
        font-size: 53px;
        line-height: 1;
        font-family: Arial, sans-serif;
        font-weight: 200;
    }

    .power-on {
        color: #39dc4b;
        text-shadow: 0 0 13px rgba(57,220,75,.20);
    }

    .power-off {
        color: #ff3944;
        text-shadow: 0 0 13px rgba(255,57,68,.12);
    }

    .machine-details {
        flex: 1;
    }

    .detail-row {
        display: flex;
        align-items: center;
        margin: 9px 0;
        font-size: 12px;
    }

    .detail-label {
        width: 86px;
        color: #b8c3cd;
    }

    .detail-value {
        color: #edf4fb;
        font-size: 13px;
        font-weight: 650;
    }

    .detail-status-on { color: #3bd84d; }
    .detail-status-off { color: #ff3d47; }

    .machine-separator {
        height: 1px;
        background: #2a3a47;
        margin: 8px 0 10px;
    }

    .machine-footer {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        font-size: 11px;
    }

    .machine-footer-label {
        color: #bac4cd;
        margin-right: 7px;
    }

    .machine-footer-value {
        color: #edf4fb;
    }

    /* ================= PANELS ================= */

    .panel {
        background: linear-gradient(145deg, #0f1a24, #0a141d);
        border: 1px solid #22323f;
        border-radius: 7px;
        box-shadow: 0 7px 18px rgba(0,0,0,.18);
        padding: 14px 16px;
    }

    .panel-title {
        color: #278cff;
        font-size: 16px;
        font-weight: 850;
        margin-bottom: 4px;
    }

    /* ================= EVENTS ================= */

    .event-row {
        display: grid;
        grid-template-columns: 90px 14px 1fr 45px;
        align-items: center;
        min-height: 39px;
        border-bottom: 1px solid #243440;
        font-size: 12px;
    }

    .event-time {
        color: #d5dee7;
    }

    .event-machine {
        color: #eef4fa;
        font-weight: 650;
    }

    .event-status-on {
        color: #3bd84d;
        font-weight: 800;
        text-align: right;
    }

    .event-status-off {
        color: #ff414b;
        font-weight: 800;
        text-align: right;
    }

    /* ================= TABLE ================= */

    .summary-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 12px;
    }

    .summary-table th {
        text-align: left;
        color: #bdc9d3;
        background: #15232f;
        font-weight: 650;
        padding: 10px 11px;
        border-right: 1px solid #263743;
    }

    .summary-table td {
        padding: 10px 11px;
        border-top: 1px solid #243440;
        color: #e3ebf2;
    }

    .progress-track {
        width: 150px;
        height: 8px;
        background: #172630;
        border-radius: 2px;
        display: inline-block;
        margin-right: 8px;
        vertical-align: middle;
    }

    .progress-fill {
        height: 8px;
        border-radius: 2px;
        display: block;
    }

    .util-green { background: #36d24a; }
    .util-red { background: #f03a45; }
    .util-blue { background: #3584dc; }
    .util-yellow { background: #e8b414; }

    .util-text-green { color: #42dc50; }
    .util-text-red { color: #ff424c; }
    .util-text-blue { color: #4a96f2; }
    .util-text-yellow { color: #f1c225; }

    .footer {
        text-align: center;
        color: #9aa7b3;
        font-size: 12px;
        padding: 12px 0 0;
    }

    /* ================= RESPONSIVE ================= */

    @media (max-width: 1100px) {
        .header-title { font-size: 20px; }
        .machine-card { min-height: 300px; }
    }
    </style>
    """),
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------

with st.sidebar:
    st.markdown(
        html("""
        <div class="sidebar-brand">
            <div class="sidebar-logo">⚙</div>
            <div>
                <div class="sidebar-title">WELDING MONITOR</div>
                <div class="sidebar-subtitle">Industrial IoT System</div>
            </div>
        </div>
        """),
        unsafe_allow_html=True,
    )

    st.markdown(
        html('<div class="nav-item nav-active"><span class="nav-icon">▣</span>Dashboard</div>'),
        unsafe_allow_html=True,
    )
    st.markdown(
        html('<div class="nav-item"><span class="nav-icon">⚙</span>Machines</div>'),
        unsafe_allow_html=True,
    )
    st.markdown(
        html('<div class="nav-item"><span class="nav-icon">▤</span>History</div>'),
        unsafe_allow_html=True,
    )
    st.markdown(
        html('<div class="nav-item"><span class="nav-icon">▤</span>Reports</div>'),
        unsafe_allow_html=True,
    )
    st.markdown(
        html('<div class="nav-item"><span class="nav-icon">⚙</span>Settings</div>'),
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="system-info-title">SYSTEM INFO</div>', unsafe_allow_html=True)

    online_count = len(machines)
    offline_count = 0

    st.markdown(
        html(f"""
        <div class="system-row"><span>Connected Nodes</span><span>{len(machines)}</span></div>
        <div class="system-row"><span>Online</span><span>{online_count}</span></div>
        <div class="system-row"><span>Offline</span><span>{offline_count}</span></div>
        <div class="system-row"><span>Last Update</span><span>{now.strftime("%H:%M:%S")}</span></div>
        """),
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------
# HEADER
# ------------------------------------------------------------

st.markdown(
    html(f"""
    <div class="top-header">
        <div class="header-left">
            <div class="header-logo">⚒</div>
            <div>
                <div class="header-title">WELDING MACHINE MONITORING SYSTEM</div>
                <div class="header-subtitle">Real-time Status Monitoring</div>
            </div>
        </div>
        <div class="header-right">
            <div class="header-date">{now.strftime("%d %B %Y")} &nbsp; | &nbsp; ◷ {now.strftime("%H:%M:%S")}</div>
            <div class="online"><span class="online-dot"></span>System Online</div>
        </div>
    </div>
    """),
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# OVERVIEW
# ------------------------------------------------------------

st.markdown('<div class="section-title">OVERVIEW</div>', unsafe_allow_html=True)

on_count = sum(1 for m in machines if m["status"] == "ON")
off_count = len(machines) - on_count
total_on = sum((m["total_on"] for m in machines), timedelta())
on_percent = (on_count / len(machines) * 100) if machines else 0

c1, c2, c3, c4 = st.columns(4, gap="small")

with c1:
    st.markdown(
        html(f"""
        <div class="summary-card">
            <div class="summary-label">TOTAL MACHINES</div>
            <div class="summary-value blue">{len(machines)}</div>
            <div class="summary-small">All Connected</div>
            <div class="summary-icon blue">⚙</div>
        </div>
        """),
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        html(f"""
        <div class="summary-card">
            <div class="summary-label">MACHINES ON</div>
            <div class="summary-value green">{on_count}</div>
            <div class="summary-small">{on_percent:.0f}%</div>
            <div class="summary-icon green">⏻</div>
        </div>
        """),
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        html(f"""
        <div class="summary-card">
            <div class="summary-label">MACHINES OFF</div>
            <div class="summary-value red">{off_count}</div>
            <div class="summary-small">{100-on_percent:.0f}%</div>
            <div class="summary-icon red">⏻</div>
        </div>
        """),
        unsafe_allow_html=True,
    )

with c4:
    st.markdown(
        html(f"""
        <div class="summary-card">
            <div class="summary-label">TOTAL ON TIME (TODAY)</div>
            <div class="summary-value yellow">{fmt_td(total_on)}</div>
            <div class="summary-small">hh:mm:ss</div>
            <div class="summary-icon yellow">◷</div>
        </div>
        """),
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------
# MACHINE STATUS
# ------------------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-title">MACHINE STATUS</div>', unsafe_allow_html=True)

cols = st.columns(4, gap="small")

for col, m in zip(cols, machines):
    with col:
        is_on = m["status"] == "ON"

        card_class = "machine-on" if is_on else "machine-off"
        dot_class = "dot-on" if is_on else "dot-off"
        pill_class = "pill-on" if is_on else "pill-off"
        power_class = "power-on" if is_on else "power-off"
        detail_status = "detail-status-on" if is_on else "detail-status-off"

        if is_on:
            since_text = fmt_time(m["since"])
            footer_label = "Last OFF"
            footer_value = fmt_date_time(m["last_off"])
            runtime = fmt_td(now - m["since"])
        else:
            since_text = fmt_time(m["since"])
            footer_label = "Last ON"
            footer_value = fmt_date_time(m["last_on"])
            runtime = fmt_td(m["total_on"])

        st.markdown(
            html(f"""
            <div class="machine-card {card_class}">
                <div class="machine-head">
                    <div class="machine-name">
                        <span class="machine-dot {dot_class}"></span>{m["id"].upper()}
                    </div>
                    <div class="status-pill {pill_class}">{m["status"]}</div>
                </div>

                <div class="machine-body">
                    <div class="power {power_class}">⏻</div>

                    <div class="machine-details">
                        <div class="detail-row">
                            <span class="detail-label">Status</span>
                            <span class="detail-value {detail_status}">{m["status"]}</span>
                        </div>

                        <div class="detail-row">
                            <span class="detail-label">Since</span>
                            <span class="detail-value">{since_text}</span>
                        </div>

                        <div class="detail-row">
                            <span class="detail-label">Running Time</span>
                            <span class="detail-value">{runtime}</span>
                        </div>
                    </div>
                </div>

                <div class="machine-separator"></div>

                <div class="machine-footer">
                    <span class="machine-footer-label">{footer_label}</span>
                    <span class="machine-footer-value">{footer_value}</span>
                </div>
            </div>
            """),
            unsafe_allow_html=True,
        )

# ------------------------------------------------------------
# CHART + RECENT EVENTS
# ------------------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)

chart_col, event_col = st.columns([1.65, 0.9], gap="small")

with chart_col:
    st.markdown(
        '<div class="panel"><div class="panel-title">ON TIME CHART (TODAY)</div>',
        unsafe_allow_html=True,
    )

    # Stable demo curves so they do not jump every Streamlit rerun.
    random.seed(42)

    x = list(range(25))
    chart_colors = ["#39dc4b", "#ff3d47", "#368ee8", "#e8b414"]

    fig = go.Figure()

    for idx, m in enumerate(machines):
        cumulative = []
        value = idx * 0.15

        for hour in x:
            if hour >= 7 + idx:
                value += [0.0, 0.08, 0.15, 0.25][(hour + idx) % 4]
            elif hour >= 2 + idx:
                value += 0.35

            cumulative.append(min(value, 10))

        fig.add_trace(
            go.Scatter(
                x=x,
                y=cumulative,
                mode="lines",
                name=m["id"],
                line=dict(
                    color=chart_colors[idx],
                    width=2.2,
                    shape="hv",
                ),
                hovertemplate=(
                    f"{m['id']}<br>"
                    "Hour: %{x}<br>"
                    "ON time: %{y:.1f} h"
                    "<extra></extra>"
                ),
            )
        )

    fig.update_layout(
        height=245,
        margin=dict(l=35, r=10, t=8, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#dbe4ec", size=11),
        legend=dict(
            orientation="h",
            y=1.13,
            x=0.5,
            xanchor="center",
            font=dict(size=11),
        ),
        xaxis=dict(
            tickmode="array",
            tickvals=[0, 4, 8, 12, 16, 20, 24],
            ticktext=["00:00", "04:00", "08:00", "12:00", "16:00", "20:00", "24:00"],
            gridcolor="#1d2d3a",
            zeroline=False,
            color="#d2dce5",
        ),
        yaxis=dict(
            title="Hours",
            range=[0, 10],
            dtick=2,
            gridcolor="#1d2d3a",
            zeroline=False,
            color="#d2dce5",
        ),
        hovermode="x unified",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False},
    )

    st.markdown("</div>", unsafe_allow_html=True)

with event_col:
    st.markdown(
        '<div class="panel"><div class="panel-title">RECENT EVENTS</div>',
        unsafe_allow_html=True,
    )

    demo_events = [
        (now - timedelta(seconds=20), "Machine 03", "ON"),
        (now - timedelta(minutes=3), "Machine 04", "OFF"),
        (now - timedelta(hours=3, minutes=36), "Machine 02", "OFF"),
        (now - timedelta(hours=6, minutes=19), "Machine 01", "ON"),
        (now - timedelta(hours=6, minutes=36), "Machine 03", "ON"),
    ]

    for event_time, machine_name, status in demo_events:
        status_class = "event-status-on" if status == "ON" else "event-status-off"
        dot = "dot-on" if status == "ON" else "dot-off"

        st.markdown(
            html(f"""
            <div class="event-row">
                <span class="event-time">{event_time.strftime("%H:%M:%S")}</span>
                <span class="machine-dot {dot}"></span>
                <span class="event-machine">{machine_name}</span>
                <span class="{status_class}">{status}</span>
            </div>
            """),
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div style="text-align:right;color:#278cff;font-size:12px;font-weight:700;padding-top:12px;">View All Events →</div>',
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# TODAY'S SUMMARY
# ------------------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-title">TODAY\'S SUMMARY</div>', unsafe_allow_html=True)

rows = ""

for i, m in enumerate(machines):
    util = utilization(m)

    status_class = (
        "util-text-green"
        if m["status"] == "ON"
        else "util-text-red"
    )

    if i == 2:
        bar_class = "util-blue"
    elif i == 3:
        bar_class = "util-yellow"
    elif m["status"] == "ON":
        bar_class = "util-green"
    else:
        bar_class = "util-red"

    rows += f"""
    <tr>
        <td>{m["id"]}</td>
        <td>
            <span class="machine-dot {'dot-on' if m['status'] == 'ON' else 'dot-off'}"></span>
            <span class="{status_class}">{m["status"]}</span>
        </td>
        <td>{fmt_time(m["since"])}</td>
        <td>{fmt_td(m["total_on"])}</td>
        <td>{fmt_td(m["total_off"])}</td>
        <td>
            <span class="progress-track">
                <span class="progress-fill {bar_class}" style="width:{min(util,100):.1f}%"></span>
            </span>
            <span class="{status_class}">{util:.1f}%</span>
        </td>
    </tr>
    """

st.markdown(
    html(f"""
    <div class="panel">
        <table class="summary-table">
            <thead>
                <tr>
                    <th>Machine</th>
                    <th>Status</th>
                    <th>First ON</th>
                    <th>Total ON Time</th>
                    <th>OFF Time</th>
                    <th>Utilization</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
    </div>
    """),
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------

st.markdown(
    '<div class="footer">Welding Machine Monitoring System © 2026</div>',
    unsafe_allow_html=True,
)
