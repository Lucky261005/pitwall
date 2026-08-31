import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "f1_telemetry.csv")

st.set_page_config(page_title="Pitwall — F1 Telemetry", page_icon="🏎️", layout="wide")

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root{
  --void:#050609; --panel:rgba(24,26,34,.55); --panel-hi:rgba(255,255,255,.05); --hairline:rgba(255,255,255,.09);
  --red:#e10600; --red-glow:#ff2a2a; --blue:#00c2ff;
  --text:#f5f6fa; --text-dim:#8e93a3; --green:#00e676; --amber:#ffb020;
}
[data-testid="stAppViewContainer"]{
  background:var(--void) !important;
  background-image:
    radial-gradient(ellipse 1100px 620px at 8% -14%, rgba(225,6,0,.20), transparent 60%),
    radial-gradient(ellipse 900px 620px at 108% -6%, rgba(0,194,255,.14), transparent 55%),
    radial-gradient(ellipse 800px 500px at 50% 115%, rgba(120,60,255,.10), transparent 60%) !important;
}
[data-testid="stAppViewContainer"] *:not([data-testid*="Icon" i]),
[data-testid="stSidebar"] *:not([data-testid*="Icon" i]){ font-family:'Inter',sans-serif; }
h1, h2, h3 { font-family:'Rajdhani',sans-serif !important; letter-spacing:.2px; color:var(--text) !important;}
[data-testid="stHeader"]{ background:transparent; }
[data-testid="stSidebar"]{
  background:linear-gradient(180deg,rgba(12,13,19,.92),rgba(5,6,9,.96)) !important;
  backdrop-filter:blur(18px);
  border-right:1px solid var(--hairline);
}
[data-testid="block-container"]{ padding-top:1.6rem; }

.pw-topbar{ display:flex; align-items:center; justify-content:space-between;
  background:linear-gradient(120deg, rgba(225,6,0,.16), rgba(0,194,255,.08));
  border:1px solid var(--hairline); border-radius:18px; padding:14px 22px; margin-bottom:22px;
  backdrop-filter:blur(14px); }
.pw-topbar .side{ display:flex; align-items:center; gap:22px; }
.pw-topbar-logo{ display:flex; align-items:center; gap:10px; }
.pw-topbar-logo .mk{ background:var(--red); color:#fff; font-family:'Rajdhani',sans-serif; font-weight:800;
  font-size:13px; padding:5px 9px; border-radius:6px; letter-spacing:.5px; box-shadow:0 0 18px rgba(225,6,0,.55);}
.pw-topbar-logo span{ font-family:'Rajdhani',sans-serif; font-weight:700; font-size:15px; letter-spacing:1.5px;
  text-transform:uppercase; color:var(--text-dim); }
.pw-topbar-logo b{ color:var(--text); }
.pw-navpill{ font-family:'Inter',sans-serif; font-size:12.5px; font-weight:600; color:var(--text-dim);
  letter-spacing:.2px; }
.pw-topbar-cta{ font-family:'JetBrains Mono',monospace; font-size:11px; letter-spacing:1px; color:var(--text);
  background:rgba(255,255,255,.08); border:1px solid var(--hairline); padding:7px 14px; border-radius:999px;
  display:inline-flex; align-items:center; gap:7px; }
.pw-topbar-cta::before{ content:""; width:7px; height:7px; border-radius:50%; background:var(--red-glow);
  box-shadow:0 0 8px var(--red-glow); display:inline-block; }

.pw-pillrow{ display:flex; gap:10px; flex-wrap:wrap; margin:2px 0 22px; }
.pw-pill{ display:flex; align-items:center; gap:8px; background:rgba(255,255,255,.05);
  border:1px solid var(--hairline); border-radius:999px; padding:8px 16px 8px 10px;
  font-family:'JetBrains Mono',monospace; font-size:11.5px; letter-spacing:.6px; color:var(--text); }
.pw-pill .dot{ width:8px; height:8px; border-radius:50%; display:inline-block; }

.pw-brand{ display:flex; align-items:center; gap:9px; padding:2px 0 16px; margin-bottom:10px;
  border-bottom:1px solid var(--hairline); }
.pw-mark{ background:var(--red); color:#fff; font-family:'Rajdhani',sans-serif; font-weight:700;
  font-size:13px; padding:4px 8px; border-radius:5px; letter-spacing:.4px; box-shadow:0 0 16px rgba(225,6,0,.5); }
.pw-brand-name{ font-family:'Rajdhani',sans-serif; font-weight:700; font-size:15px; letter-spacing:1px;
  text-transform:uppercase; color:var(--text-dim); }
.pw-brand-name b{ color:var(--text); }
.pw-eyebrow{ font-family:'JetBrains Mono',monospace !important; font-size:11px; letter-spacing:2.2px;
  color:var(--red-glow); text-transform:uppercase; margin:0 0 5px; }
.pw-hero h1{ font-weight:700; font-size:34px; letter-spacing:.2px; text-transform:uppercase;
  margin:0; line-height:1.1; color:var(--text); }
.pw-hero p{ color:var(--text-dim); font-size:14px; margin:8px 0 0; max-width:680px; }

div[class*="st-key-pwcard_"][data-testid="stVerticalBlock"]{
  background:var(--panel) !important; border:1px solid var(--hairline) !important;
  border-radius:18px !important; backdrop-filter:blur(16px);
  box-shadow:0 12px 32px rgba(0,0,0,.35); margin-bottom:16px; padding:20px 22px !important;
}
.pw-card-title{ font-family:'Rajdhani',sans-serif; font-size:15px; font-weight:700; letter-spacing:.3px;
  color:var(--blue); text-transform:uppercase; margin:0 0 12px; }
[data-testid="stExpander"]{ background:rgba(0,0,0,.25) !important; border:1px solid var(--hairline) !important;
  border-radius:12px !important; margin-top:10px; }
[data-testid="stExpander"] summary{ font-family:'JetBrains Mono',monospace !important; font-size:11.5px !important;
  color:var(--text-dim) !important; }
.pw-metric-row{ display:flex; gap:14px; flex-wrap:wrap; }
.pw-metric{ background:var(--panel-hi); border:1px solid var(--hairline); border-radius:14px;
  padding:14px 18px; min-width:150px; flex:1; }
.pw-metric .lbl{ font-family:'JetBrains Mono',monospace; font-size:10px; letter-spacing:1.5px;
  color:var(--text-dim); text-transform:uppercase; }
.pw-metric .val{ font-family:'Rajdhani',sans-serif; font-size:27px; font-weight:700; color:var(--text); }
.pw-metric .val.red{ color:var(--red-glow); } .pw-metric .val.blue{ color:var(--blue); }
.pw-metric .val.green{ color:var(--green); } .pw-metric .val.amber{ color:var(--amber); }
.pw-tag{ display:inline-block; font-family:'JetBrains Mono',monospace; font-size:10px;
  letter-spacing:1px; padding:3px 9px; border-radius:5px; background:var(--panel-hi);
  border:1px solid var(--hairline); color:var(--text-dim); margin-right:6px; }

.pw-standing{ display:flex; align-items:center; gap:14px; padding:9px 4px;
  border-bottom:1px solid var(--hairline); }
.pw-standing:last-child{ border-bottom:none; }
.pw-standing .pos{ font-family:'Rajdhani',sans-serif; font-weight:800; font-size:19px;
  color:var(--red-glow); width:30px; }
.pw-standing .who b{ display:block; font-size:14px; color:var(--text); font-weight:600; }
.pw-standing .who small{ font-family:'JetBrains Mono',monospace; font-size:10.5px; color:var(--text-dim); }
.pw-standing .gap{ margin-left:auto; font-family:'JetBrains Mono',monospace; font-size:13px;
  color:var(--text); font-weight:600; }
.pw-standing .swatch{ width:6px; height:34px; border-radius:4px; }

.pw-digitrow{ display:flex; gap:10px; }
.pw-digit{ flex:1; text-align:center; background:rgba(0,0,0,.35); border:1px solid var(--hairline);
  border-radius:12px; padding:10px 6px; }
.pw-digit .v{ font-family:'JetBrains Mono',monospace; font-size:22px; font-weight:600; color:var(--blue); }
.pw-digit .l{ font-family:'JetBrains Mono',monospace; font-size:9px; letter-spacing:1.2px;
  color:var(--text-dim); text-transform:uppercase; margin-top:2px; }

[data-testid="stSidebar"] .stRadio label{ color:var(--text) !important; }
[data-testid="stSlider"] [data-baseweb="slider"] div{ background:var(--blue) !important; }
code, .stCode { font-family:'JetBrains Mono',monospace !important; }
hr{ border-color:var(--hairline) !important; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

VOID, PANEL, HAIR = "#08080c", "#121218", "#242430"
RED, RED_GLOW, BLUE = "#e10600", "#ff2a2a", "#00c2ff"
GREEN, AMBER, TEXT, TEXT_DIM = "#00e676", "#ffb020", "#f2f2f6", "#8f8f9c"
COMPOUND_COLOR = {"Soft": RED_GLOW, "Medium": AMBER, "Hard": TEXT}
TEAM_COLOR = {
    "Red Bull Racing": "#3671C6", "Mercedes": "#27F4D2", "Ferrari": "#E8002D",
    "McLaren": "#FF8000", "Aston Martin": "#229971", "Alpine": "#FF87BC",
    "Williams": "#64C4FF", "RB": "#6692FF", "Sauber": "#00E701", "Haas": "#B6BABD",
}

plt.rcParams.update({
    "figure.facecolor": PANEL, "axes.facecolor": PANEL,
    "axes.edgecolor": HAIR, "axes.labelcolor": TEXT_DIM,
    "xtick.color": TEXT_DIM, "ytick.color": TEXT_DIM,
    "text.color": TEXT, "grid.color": HAIR, "grid.linestyle": "--",
    "grid.linewidth": 0.6, "font.family": "sans-serif",
    "axes.titlecolor": TEXT, "legend.facecolor": PANEL,
    "legend.edgecolor": HAIR, "legend.labelcolor": TEXT,
})


def styled_ax(ax, title=""):
    ax.set_title(title, fontsize=12, fontweight="bold", loc="left", pad=10)
    ax.grid(True, alpha=0.5)
    for spine in ax.spines.values():
        spine.set_color(HAIR)
    return ax


@st.cache_data
def load_data():
    if not os.path.exists(CSV_PATH):
        st.error(f"Dataset not found at `{CSV_PATH}`. Run `generate_dataset.py` first to build it.")
        st.stop()
    return pd.read_csv(CSV_PATH)


df = load_data()

drivers_all = df["driver"].to_numpy()
teams_all = df["team"].to_numpy()
laps = df["lap"].to_numpy()
lap_times = df["lap_time_sec"].to_numpy()
sectors = df[["sector1_sec", "sector2_sec", "sector3_sec"]].to_numpy()
speed_trap = df["speed_trap_kmh"].to_numpy()
compound = df["tyre_compound"].to_numpy()
tyre_age = df["tyre_age_laps"].to_numpy()
pit_stop = df["pit_stop"].to_numpy().astype(bool)
fuel = df["fuel_load_kg"].to_numpy()
driver_codes = np.unique(drivers_all)

st.sidebar.markdown(
    '<div class="pw-brand"><span class="pw-mark">PW</span>'
    '<span class="pw-brand-name"><b>Pitwall</b></span></div>',
    unsafe_allow_html=True,
)
SECTIONS = [
    "Overview",
    "Pace & Speed",
    "Race Statistics",
    "Field Analysis",
    "Grid Filters",
    "Fastest Laps",
    "Rankings",
    "Visualizations",
    "Head to Head",
]
choice = st.sidebar.radio("MENU", SECTIONS, label_visibility="visible")
st.sidebar.markdown("<hr/>", unsafe_allow_html=True)
st.sidebar.markdown(
    f'<span class="pw-tag">rows: {len(df)}</span>'
    f'<span class="pw-tag">drivers: {driver_codes.size}</span>'
    f'<span class="pw-tag">laps: {int(laps.max())}</span>',
    unsafe_allow_html=True,
)


def hero(eyebrow, title, sub):
    st.markdown(
        f'<div class="pw-hero"><p class="pw-eyebrow">{eyebrow}</p>'
        f'<h1>{title}</h1><p>{sub}</p></div><br/>',
        unsafe_allow_html=True,
    )


def metric_row(items):
    html = '<div class="pw-metric-row">'
    for lbl, val, cls in items:
        html += (f'<div class="pw-metric"><div class="lbl">{lbl}</div>'
                  f'<div class="val {cls}">{val}</div></div>')
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


_card_stack = []
_card_counter = [0]


def card_open(title=None):
    _card_counter[0] += 1
    c = st.container(border=True, key=f"pwcard_{_card_counter[0]}")
    c.__enter__()
    _card_stack.append(c)
    if title:
        st.markdown(f'<div class="pw-card-title">{title}</div>', unsafe_allow_html=True)


def card_close():
    _card_stack.pop().__exit__(None, None, None)


def circuit_shape(n=500):
    theta = np.linspace(0, 2 * np.pi, n, endpoint=False)
    r = 1 + 0.20 * np.sin(3 * theta + 0.4) + 0.11 * np.cos(5 * theta) + 0.07 * np.sin(7 * theta - 1.0)
    x = r * np.cos(theta)
    y = r * np.sin(theta) * 0.72
    return x, y


TRACK_X, TRACK_Y = circuit_shape()
N_TRACK_PTS = TRACK_X.size


def draw_trackmap(sel_lap):
    cum_times = np.array([lap_times[(drivers_all == d) & (laps <= sel_lap)].sum() for d in driver_codes])
    order = np.argsort(cum_times)
    leader_time = cum_times[order[0]]
    gaps = cum_times - leader_time
    avg_lap = lap_times[laps <= sel_lap].mean()
    frac = np.clip(gaps / avg_lap, 0, 0.97)
    idx = (frac * N_TRACK_PTS).astype(int) % N_TRACK_PTS
    xs, ys = TRACK_X[idx], TRACK_Y[idx]

    fig, ax = plt.subplots(figsize=(6.4, 5.4))
    ax.plot(np.append(TRACK_X, TRACK_X[0]), np.append(TRACK_Y, TRACK_Y[0]),
            color=TEXT_DIM, linewidth=2.2, alpha=0.55, zorder=1)
    ax.plot([TRACK_X[0]], [TRACK_Y[0]], marker="_", color=TEXT, markersize=18,
            markeredgewidth=3, zorder=2)

    for rank, di in enumerate(order):
        d = driver_codes[di]
        team = teams_all[drivers_all == d][0]
        col = TEAM_COLOR.get(team, BLUE)
        is_leader = rank == 0
        ax.scatter(xs[di], ys[di], s=210 if is_leader else 150, color=col,
                   edgecolor="white" if is_leader else VOID, linewidth=1.6, zorder=3)
        ax.annotate(d, (xs[di], ys[di]), textcoords="offset points", xytext=(0, 11),
                    fontsize=8.5, fontweight="bold", color=TEXT, ha="center", zorder=4)

    ax.set_xlim(-1.45, 1.45); ax.set_ylim(-1.15, 1.15)
    ax.set_aspect("equal"); ax.axis("off")
    fig.patch.set_alpha(0)
    return fig, order, cum_times, gaps


def standings_html(order, cum_times, gaps):
    rows = ""
    for rank, di in enumerate(order):
        d = driver_codes[di]
        team = teams_all[drivers_all == d][0]
        col = TEAM_COLOR.get(team, BLUE)
        gap_txt = "LEADER" if rank == 0 else f"+{gaps[di]:.2f}s"
        rows += (
            f'<div class="pw-standing"><span class="swatch" style="background:{col}"></span>'
            f'<span class="pos">P{rank+1}</span>'
            f'<span class="who"><b>{d}</b><small>{team}</small></span>'
            f'<span class="gap">{gap_txt}</span></div>'
        )
    return rows


st.markdown(
    '<div class="pw-topbar"><div class="side">'
    '<div class="pw-topbar-logo"><span class="mk">PW</span>'
    '<span><b>Pitwall</b></span></div>'
    '<span class="pw-navpill">Race</span>'
    '<span class="pw-navpill">Trackmap</span>'
    '<span class="pw-navpill">Statistics</span>'
    '<span class="pw-navpill">Visualization</span>'
    '</div><span class="pw-topbar-cta">LIVE</span></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="pw-pillrow">'
    '<span class="pw-pill"><span class="dot" style="background:#e10600"></span>Bahrain Grand Prix</span>'
    '<span class="pw-pill"><span class="dot" style="background:#00c2ff"></span>2025 Season · Race</span>'
    '<span class="pw-pill"><span class="dot" style="background:#00e676"></span>20 Drivers · 57 Laps</span>'
    "</div>",
    unsafe_allow_html=True,
)

if choice == "Overview":
    hero("RACE WEEKEND", "Bahrain Grand Prix — Telemetry Dashboard",
         "Lap-by-lap telemetry for the 2025 Bahrain Grand Prix: 20 drivers, 57 laps, "
         "sector splits, tyre strategy and pit stops.")

    metric_row([
        ("TOTAL LAPS LOGGED", f"{len(df):,}", "blue"),
        ("FASTEST LAP", f"{lap_times.min():.3f}s", "red"),
        ("MEAN LAP TIME", f"{lap_times.mean():.3f}s", ""),
        ("STD DEV (LAP TIME)", f"{lap_times.std():.3f}s", "amber"),
        ("PIT STOPS", f"{int(pit_stop.sum())}", "green"),
    ])
    st.write("")

    trk_col, stand_col = st.columns([1.3, 1])
    with trk_col:
        card_open("Live Trackmap")
        sel_lap = st.slider("Race lap", 1, int(laps.max()), int(laps.max()), key="trackmap_lap")
        fig, order, cum_times, gaps = draw_trackmap(sel_lap)
        st.pyplot(fig, use_container_width=True)
        card_close()
    with stand_col:
        card_open(f"Standings at Lap {sel_lap}")
        st.markdown(standings_html(order, cum_times, gaps), unsafe_allow_html=True)
        card_close()

        leader_di = order[0]
        card_open("Race digits")
        st.markdown(
            '<div class="pw-digitrow">'
            f'<div class="pw-digit"><div class="v">{sel_lap}</div><div class="l">Lap</div></div>'
            f'<div class="pw-digit"><div class="v">{int(laps.max()) - sel_lap}</div><div class="l">Laps left</div></div>'
            f'<div class="pw-digit"><div class="v">{gaps[order[-1]]:.1f}s</div><div class="l">Front-to-back</div></div>'
            "</div>",
            unsafe_allow_html=True,
        )
        card_close()

    card_open("Session Data")
    st.dataframe(df.head(25), use_container_width=True, height=340)
    st.download_button(
        "Download full dataset (CSV)",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="f1_telemetry.csv",
        mime="text/csv",
    )
    card_close()

    card_open("Data Fields")
    st.markdown("""
- `lap` — lap number (1–57) &nbsp;·&nbsp; `driver` / `team` — entrant codes
- `lap_time_sec`, `sector1_sec`, `sector2_sec`, `sector3_sec` — timing splits (seconds)
- `speed_trap_kmh` — top speed through the speed trap
- `tyre_compound`, `tyre_age_laps` — strategy data &nbsp;·&nbsp; `pit_stop` — 1 on an in-lap
- `fuel_load_kg`, `track_temp_c` — car/track state
""")
    card_close()

elif choice == "Pace & Speed":
    hero("PACE", "Pace & Speed", "Speed conversions, sector splits and pace delta across the full session.")

    card_open("Session Snapshot")
    c1, c2 = st.columns(2)
    c1.write(f"Lap records: **{lap_times.shape[0]}**")
    c2.write(f"Sector columns: **{sectors.shape[1]}**")
    card_close()

    card_open("Speed & Pace Metrics")
    speed_ms = speed_trap / 3.6
    sector_sum = sectors.sum(axis=1)
    resid = lap_times - sector_sum
    pace_delta = np.abs(lap_times - lap_times.min())

    metric_row([
        ("AVG SPEED (M/S)", f"{speed_ms.mean():.2f}", "blue"),
        ("MAX SECTOR-SUM RESIDUAL", f"{np.abs(resid).max():.4f}s", "amber"),
        ("MEDIAN PACE DELTA TO FASTEST", f"{np.median(pace_delta):.3f}s", "red"),
    ])
    card_close()

elif choice == "Race Statistics":
    hero("STATS", "Race Statistics", "Field-wide and per-driver summary statistics for the session.")

    card_open("Field Summary")
    p25, p50, p75, p90 = np.percentile(lap_times, [25, 50, 75, 90])
    metric_row([
        ("SUM", f"{lap_times.sum():,.1f}s", ""),
        ("MEAN", f"{lap_times.mean():.3f}s", "blue"),
        ("MEDIAN", f"{p50:.3f}s", "blue"),
        ("STD DEV", f"{lap_times.std():.3f}s", "amber"),
        ("MIN / MAX", f"{lap_times.min():.2f} / {lap_times.max():.2f}", "red"),
    ])
    st.write(f"25th / 75th / 90th percentile: **{p25:.3f}s / {p75:.3f}s / {p90:.3f}s**")
    card_close()

    card_open("Per-Driver Averages")
    means = np.array([lap_times[drivers_all == d].mean() for d in driver_codes])
    best = np.array([lap_times[drivers_all == d].min() for d in driver_codes])
    order = np.argsort(means)
    table = pd.DataFrame({
        "driver": driver_codes[order],
        "mean_lap_sec": means[order].round(3),
        "best_lap_sec": best[order].round(3),
    })
    st.dataframe(table, use_container_width=True, height=300)
    card_close()

elif choice == "Field Analysis":
    hero("FIELD", "Field Analysis", "Every driver's pace measured against the leader and the field's best sector times.")

    card_open("Pace Delta to Leader")
    grid = np.array([lap_times[drivers_all == d].mean() for d in driver_codes])
    delta_to_fastest = grid - grid.min()
    z_scores = (grid - grid.mean()) / grid.std()

    fig, ax = plt.subplots(figsize=(9, 4.2))
    order = np.argsort(delta_to_fastest)
    ax.bar(driver_codes[order], delta_to_fastest[order], color=BLUE, edgecolor=VOID)
    styled_ax(ax, "Average-pace delta to the fastest driver")
    ax.set_ylabel("Delta (s)")
    plt.xticks(rotation=60)
    st.pyplot(fig, use_container_width=True)
    card_close()

    card_open("Sector Time Loss")
    sector_best = sectors.min(axis=0)
    sector_delta = sectors - sector_best
    st.write(f"Field-best sector times: **S1 {sector_best[0]:.3f}s · S2 {sector_best[1]:.3f}s · S3 {sector_best[2]:.3f}s**")
    st.write(f"Mean time lost per sector across the whole field: "
              f"**S1 {sector_delta[:,0].mean():.3f}s · S2 {sector_delta[:,1].mean():.3f}s · S3 {sector_delta[:,2].mean():.3f}s**")
    card_close()

elif choice == "Grid Filters":
    hero("FILTERS", "Grid Filters", "Filtering the field by pace, tyre strategy and track conditions.")

    card_open("Fast Lap Filter")
    fast_mask = lap_times < np.percentile(lap_times, 10)
    metric_row([
        ("LAPS IN FASTEST 10%", f"{fast_mask.sum()}", "red"),
        ("ANY PIT STOP LOGGED", f"{bool(np.any(pit_stop))}", "green"),
        ("ALL TYRE-AGE > 0", f"{bool(np.all(tyre_age > 0))}", "blue"),
    ])
    card_close()

    card_open("Compound Strategy Filter")
    quick_on_softs = (compound == "Soft") & (lap_times < np.percentile(lap_times, 20))
    not_pitting = ~pit_stop
    metric_row([
        ("FAST LAPS ON SOFTS", f"{int(quick_on_softs.sum())}", "red"),
        ("NON-PIT LAPS", f"{int(not_pitting.sum())}", ""),
        ("SOFT-TYRE SHARE OF FIELD", f"{(compound == 'Soft').mean()*100:.1f}%", "amber"),
    ])
    st.write("Laps matching the fast-on-softs filter:")
    st.dataframe(df.loc[quick_on_softs, ["lap", "driver", "lap_time_sec", "tyre_compound"]].head(10),
                 use_container_width=True)
    card_close()

elif choice == "Fastest Laps":
    hero("FASTEST", "Fastest Laps", "The quickest drivers and laps of the session.")

    card_open("Selected Drivers")
    pick = np.array(["VER", "HAM", "LEC", "NOR", "ALO"])
    mask = np.isin(drivers_all, pick)
    st.write(f"Rows selected: **{int(mask.sum())}**")
    st.dataframe(df.loc[mask, ["lap", "driver", "team", "lap_time_sec"]].head(10),
                 use_container_width=True)
    card_close()

    card_open("Top 10 Fastest Laps of the Race")
    top_idx = np.argsort(lap_times)[:10]
    st.dataframe(df.iloc[top_idx][["lap", "driver", "team", "lap_time_sec", "tyre_compound"]]
                 .reset_index(drop=True), use_container_width=True)
    card_close()

    card_open("Sector Splits — Top 10")
    cols = ["sector1_sec", "sector3_sec"]
    s1_s3 = df[cols].to_numpy()[top_idx]
    st.write("S1 & S3 for the 10 fastest laps:")
    st.dataframe(pd.DataFrame(s1_s3, columns=cols).round(3), use_container_width=True)
    card_close()

elif choice == "Rankings":
    hero("RANKINGS", "Rankings", "The grid ranked by best lap time, with the fastest laps of the race isolated.")

    card_open("Driver Rankings")
    best_per_driver = np.array([lap_times[drivers_all == d].min() for d in driver_codes])
    order = np.argsort(best_per_driver)
    ranked = pd.DataFrame({
        "position": np.arange(1, len(order) + 1),
        "driver": driver_codes[order],
        "best_lap_sec": best_per_driver[order].round(3),
    })
    st.dataframe(ranked, use_container_width=True, height=300)
    card_close()

    card_open("Fastest 5 Laps of the Race")
    k = 5
    part_idx = np.argpartition(lap_times, k)[:k]
    fastest5 = np.sort(lap_times[part_idx])
    st.write("Fastest 5 lap times of the entire race: " + ", ".join(f"{t:.3f}s" for t in fastest5))
    card_close()

    card_open("Best Sector 1 Times")
    order2 = np.argsort(sectors[:, 0])
    sectors_sorted = sectors[order2]
    st.write("First 5 rows once sorted by Sector 1 time (fastest sector-1 laps first):")
    st.dataframe(pd.DataFrame(sectors_sorted[:5], columns=["sector1_sec", "sector2_sec", "sector3_sec"]).round(3),
                 use_container_width=True)
    card_close()

elif choice == "Visualizations":
    hero("CHARTS", "Visualizations", "Six views of the same session data.")

    row1c1, row1c2 = st.columns(2)
    with row1c1:
        card_open("Lap Time Trend — Top 5")
        fig, ax = plt.subplots(figsize=(6, 4.2))
        top5 = ranked_top5 = driver_codes[np.argsort(
            np.array([lap_times[drivers_all == d].mean() for d in driver_codes]))[:5]]
        for i, d in enumerate(top5):
            m = drivers_all == d
            ax.plot(laps[m], lap_times[m], label=d, linewidth=1.6,
                    color=[RED_GLOW, BLUE, GREEN, AMBER, "#c792ea"][i])
        styled_ax(ax, "Lap time per lap")
        ax.set_xlabel("Lap"); ax.set_ylabel("Lap time (s)")
        ax.legend(fontsize=8, ncol=5, loc="upper center", bbox_to_anchor=(0.5, -0.18))
        st.pyplot(fig, use_container_width=True)
        card_close()

    with row1c2:
        card_open("Average Pace by Team")
        fig, ax = plt.subplots(figsize=(6, 4.2))
        team_codes = np.unique(teams_all)
        team_means = np.array([lap_times[teams_all == t].mean() for t in team_codes])
        o = np.argsort(team_means)
        ax.barh(team_codes[o], team_means[o], color=BLUE, edgecolor=VOID)
        styled_ax(ax, "Mean lap time by team")
        ax.set_xlabel("Seconds")
        st.pyplot(fig, use_container_width=True)
        card_close()

    row2c1, row2c2 = st.columns(2)
    with row2c1:
        card_open("Tyre Degradation")
        fig, ax = plt.subplots(figsize=(6, 4.2))
        for comp, col in COMPOUND_COLOR.items():
            m = compound == comp
            ax.scatter(tyre_age[m], lap_times[m], s=10, alpha=0.6, color=col, label=comp)
        styled_ax(ax, "Tyre degradation")
        ax.set_xlabel("Tyre age (laps)"); ax.set_ylabel("Lap time (s)")
        ax.legend(fontsize=9)
        st.pyplot(fig, use_container_width=True)
        card_close()

    with row2c2:
        card_open("Lap Time Distribution")
        fig, ax = plt.subplots(figsize=(6, 4.2))
        ax.hist(lap_times, bins=30, color=RED_GLOW, edgecolor=VOID, alpha=0.9)
        ax.axvline(lap_times.mean(), color=BLUE, linestyle="--", linewidth=1.3, label=f"mean {lap_times.mean():.2f}s")
        styled_ax(ax, "Distribution of all lap times")
        ax.set_xlabel("Lap time (s)"); ax.set_ylabel("Count")
        ax.legend(fontsize=9)
        st.pyplot(fig, use_container_width=True)
        card_close()

    row3c1, row3c2 = st.columns(2)
    with row3c1:
        card_open("Pace Spread by Compound")
        fig, ax = plt.subplots(figsize=(6, 4.2))
        data = [lap_times[compound == c] for c in ["Soft", "Medium", "Hard"]]
        bp = ax.boxplot(data, tick_labels=["Soft", "Medium", "Hard"], patch_artist=True,
                         medianprops=dict(color=VOID, linewidth=1.5))
        for patch, c in zip(bp["boxes"], [RED_GLOW, AMBER, TEXT]):
            patch.set_facecolor(c); patch.set_alpha(0.75)
        styled_ax(ax, "Lap time by compound")
        ax.set_ylabel("Lap time (s)")
        st.pyplot(fig, use_container_width=True)
        card_close()

    with row3c2:
        card_open("Sector Time Heatmap")
        fig, ax = plt.subplots(figsize=(6, 6.5))
        heat = np.array([[sectors[drivers_all == d, j].mean() for j in range(3)] for d in driver_codes])
        im = ax.imshow(heat, aspect="auto", cmap="magma")
        ax.set_yticks(range(len(driver_codes))); ax.set_yticklabels(driver_codes, fontsize=7)
        ax.set_xticks(range(3)); ax.set_xticklabels(["S1", "S2", "S3"])
        styled_ax(ax, "Mean sector time per driver")
        fig.colorbar(im, ax=ax, shrink=0.8, label="seconds")
        st.pyplot(fig, use_container_width=True)
        card_close()

elif choice == "Head to Head":
    hero("HEAD TO HEAD", "Driver Comparison", "Pick two drivers to compare pace, consistency and race-long gap evolution.")

    dcol1, dcol2 = st.columns(2)
    with dcol1:
        driver_a = st.selectbox("Driver A", driver_codes, index=0, key="cmp_a")
    with dcol2:
        default_b_idx = 1 if driver_codes.size > 1 else 0
        driver_b = st.selectbox("Driver B", driver_codes, index=default_b_idx, key="cmp_b")

    if driver_a == driver_b:
        st.warning("Pick two different drivers to compare.")
    else:
        mask_a = drivers_all == driver_a
        mask_b = drivers_all == driver_b
        order_a = np.argsort(laps[mask_a])
        order_b = np.argsort(laps[mask_b])
        laps_a, times_a = laps[mask_a][order_a], lap_times[mask_a][order_a]
        laps_b, times_b = laps[mask_b][order_b], lap_times[mask_b][order_b]
        team_a = teams_all[mask_a][0]
        team_b = teams_all[mask_b][0]

        card_open(f"{driver_a} ({team_a})  vs  {driver_b} ({team_b})")
        summary = pd.DataFrame({
            "metric": ["Best lap (s)", "Average lap (s)", "Consistency — std dev (s)",
                       "Average speed trap (km/h)", "Pit stops"],
            driver_a: [
                times_a.min().round(3), times_a.mean().round(3), times_a.std().round(3),
                speed_trap[mask_a].mean().round(1), int(pit_stop[mask_a].sum()),
            ],
            driver_b: [
                times_b.min().round(3), times_b.mean().round(3), times_b.std().round(3),
                speed_trap[mask_b].mean().round(1), int(pit_stop[mask_b].sum()),
            ],
        })
        st.dataframe(summary, use_container_width=True, hide_index=True)
        card_close()

        col_a, col_b = st.columns(2)
        with col_a:
            card_open("Lap time evolution")
            fig, ax = plt.subplots(figsize=(6.4, 4.2))
            ax.plot(laps_a, times_a, label=driver_a, color=TEAM_COLOR.get(team_a, RED_GLOW), linewidth=1.8)
            ax.plot(laps_b, times_b, label=driver_b, color=TEAM_COLOR.get(team_b, BLUE), linewidth=1.8)
            styled_ax(ax, f"{driver_a} vs {driver_b} — lap time per lap")
            ax.set_xlabel("Lap"); ax.set_ylabel("Lap time (s)")
            ax.legend(fontsize=9)
            st.pyplot(fig, use_container_width=True)
            card_close()

        with col_b:
            card_open("Race gap evolution")
            common_n = min(times_a.size, times_b.size)
            cum_a = np.cumsum(times_a[:common_n])
            cum_b = np.cumsum(times_b[:common_n])
            gap = cum_b - cum_a
            lap_axis = np.arange(1, common_n + 1)

            fig, ax = plt.subplots(figsize=(6.4, 4.2))
            ax.axhline(0, color=TEXT_DIM, linewidth=1, alpha=0.6)
            ax.fill_between(lap_axis, gap, 0, where=gap >= 0, color=TEAM_COLOR.get(team_a, RED_GLOW), alpha=0.35)
            ax.fill_between(lap_axis, gap, 0, where=gap < 0, color=TEAM_COLOR.get(team_b, BLUE), alpha=0.35)
            ax.plot(lap_axis, gap, color=TEXT, linewidth=1.4)
            styled_ax(ax, f"Cumulative gap (positive = {driver_a} ahead)")
            ax.set_xlabel("Lap"); ax.set_ylabel("Gap (s)")
            st.pyplot(fig, use_container_width=True)
            card_close()
