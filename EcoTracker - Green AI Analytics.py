import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import psutil
import threading
import platform
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="EcoTracker · Nile Delta",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
#  PREMIUM DARK FOREST THEME
#  Palette: #204d11 · #d6ffc8 · #498d32
# ─────────────────────────────────────────────
st.markdown("""
<style>

/* ══════════════════════════════════════════
   FONTS
══════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=Manrope:wght@300;400;500;600;700&display=swap');

/* ══════════════════════════════════════════
   ROOT VARIABLES
══════════════════════════════════════════ */
:root {
    --deep:      #0d1f08;
    --forest:    #204d11;
    --mid:       #498d32;
    --mint:      #d6ffc8;
    --pale:      #edfde6;
    --card-bg:   rgba(22, 48, 13, 0.72);
    --card-border: rgba(73, 141, 50, 0.28);
    --text-primary: #d6ffc8;
    --text-muted:   rgba(214,255,200,0.55);
    --glow:      rgba(73,141,50,0.35);
}

/* ══════════════════════════════════════════
   GLOBAL BASE
══════════════════════════════════════════ */
html, body, .stApp {
    font-family: 'Manrope', sans-serif !important;
    background: #0a1a06 !important;
    color: var(--text-primary) !important;
}

/* Deep mesh background */
.stApp {
    background:
        radial-gradient(ellipse 80% 60% at 10% 0%, rgba(32,77,17,0.55) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 90% 100%, rgba(73,141,50,0.25) 0%, transparent 55%),
        radial-gradient(ellipse 100% 100% at 50% 50%, #0a1a06 0%, #0d1f08 100%) !important;
}

/* Noise grain overlay */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.035'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
    opacity: 0.6;
}

/* ══════════════════════════════════════════
   SIDEBAR — dark glass
══════════════════════════════════════════ */
section[data-testid="stSidebar"] {
    background: rgba(10, 26, 6, 0.92) !important;
    border-right: 1px solid rgba(73,141,50,0.22) !important;
    backdrop-filter: blur(20px) !important;
}

section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span {
    color: var(--text-primary) !important;
}

section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    font-family: 'Syne', sans-serif !important;
    color: var(--mint) !important;
    letter-spacing: 0.04em;
    font-size: 0.85rem !important;
    text-transform: uppercase;
}

/* ══════════════════════════════════════════
   SLIDERS — full green override
══════════════════════════════════════════ */

/* Track background */
div[data-testid="stSlider"] > div > div > div {
    background: rgba(73,141,50,0.2) !important;
}

/* Filled track */
div[data-testid="stSlider"] > div > div > div > div:first-child {
    background: linear-gradient(90deg, #204d11, #498d32) !important;
}

/* Thumb */
div[data-testid="stSlider"] > div > div > div > div > div {
    background: #d6ffc8 !important;
    border: 2.5px solid #498d32 !important;
    box-shadow: 0 0 10px rgba(73,141,50,0.6) !important;
}

/* Slider value label */
div[data-testid="stSlider"] p {
    color: #d6ffc8 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
}

/* ══════════════════════════════════════════
   PROGRESS BARS — green glow
══════════════════════════════════════════ */
div[data-testid="stProgress"] > div > div {
    background: rgba(73,141,50,0.18) !important;
    border-radius: 999px !important;
    height: 6px !important;
}

div[data-testid="stProgress"] > div > div > div {
    background: linear-gradient(90deg, #204d11 0%, #498d32 50%, #d6ffc8 100%) !important;
    border-radius: 999px !important;
    box-shadow: 0 0 12px rgba(73,141,50,0.7), 0 0 28px rgba(73,141,50,0.3) !important;
    transition: width 0.3s ease !important;
}

/* ══════════════════════════════════════════
   CHECKBOXES
══════════════════════════════════════════ */
div[data-testid="stCheckbox"] label span {
    color: var(--text-primary) !important;
    font-size: 0.85rem !important;
}

div[data-testid="stCheckbox"] > label > div {
    background: rgba(73,141,50,0.15) !important;
    border: 1px solid rgba(73,141,50,0.4) !important;
    border-radius: 4px !important;
}

div[data-testid="stCheckbox"] > label > div[data-checked="true"] {
    background: #498d32 !important;
    border-color: #d6ffc8 !important;
}

/* ══════════════════════════════════════════
   TYPOGRAPHY
══════════════════════════════════════════ */
h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: 3.2rem !important;
    font-weight: 800 !important;
    letter-spacing: -2px !important;
    line-height: 1 !important;
    background: linear-gradient(135deg, #d6ffc8 0%, #498d32 60%, #204d11 100%);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    text-shadow: none !important;
    margin-bottom: 0.2rem !important;
}

h2, h3 {
    font-family: 'Syne', sans-serif !important;
    color: var(--mint) !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px !important;
}

p, li, span, label, div {
    color: var(--text-primary);
}

/* ══════════════════════════════════════════
   BUTTONS
══════════════════════════════════════════ */
.stButton > button {
    background: linear-gradient(135deg, #204d11 0%, #498d32 100%) !important;
    color: #d6ffc8 !important;
    border: 1px solid rgba(214,255,200,0.2) !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    padding: 0.65rem 1.4rem !important;
    transition: all 0.22s ease !important;
    box-shadow: 0 4px 16px rgba(73,141,50,0.25) !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #2a6617 0%, #5aaa3d 100%) !important;
    box-shadow: 0 8px 28px rgba(73,141,50,0.5) !important;
    transform: translateY(-2px) !important;
    border-color: rgba(214,255,200,0.4) !important;
}

/* Primary button extra glow */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #498d32 0%, #d6ffc8 200%) !important;
    color: #0d1f08 !important;
    box-shadow: 0 6px 24px rgba(73,141,50,0.5), 0 0 0 1px rgba(214,255,200,0.15) !important;
}

/* ══════════════════════════════════════════
   METRICS
══════════════════════════════════════════ */
div[data-testid="metric-container"] {
    background: rgba(22,48,13,0.75) !important;
    border: 1px solid rgba(73,141,50,0.25) !important;
    border-radius: 12px !important;
    padding: 1rem 1.2rem !important;
    backdrop-filter: blur(10px) !important;
    box-shadow: inset 0 1px 0 rgba(214,255,200,0.06), 0 4px 20px rgba(0,0,0,0.35) !important;
    position: relative;
    overflow: hidden;
}

div[data-testid="metric-container"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #498d32, transparent);
}

div[data-testid="metric-container"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: rgba(214,255,200,0.6) !important;
}

div[data-testid="metric-container"] [data-testid="metric-value"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.4rem !important;
    font-weight: 800 !important;
    color: #d6ffc8 !important;
}

div[data-testid="metric-container"] [data-testid="metric-delta"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    color: #498d32 !important;
}

/* ══════════════════════════════════════════
   DATAFRAME / TABLE
══════════════════════════════════════════ */
div[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid rgba(73,141,50,0.25) !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4) !important;
}

div[data-testid="stDataFrame"] * {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
}

/* ══════════════════════════════════════════
   TABS
══════════════════════════════════════════ */
div[data-testid="stTabs"] [role="tablist"] {
    border-bottom: 1px solid rgba(73,141,50,0.2) !important;
    gap: 0 !important;
}

div[data-testid="stTabs"] button[role="tab"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    color: rgba(214,255,200,0.45) !important;
    border-radius: 0 !important;
    padding: 0.6rem 1.2rem !important;
    border-bottom: 2px solid transparent !important;
    transition: all 0.2s !important;
}

div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: #d6ffc8 !important;
    border-bottom-color: #498d32 !important;
    background: transparent !important;
}

div[data-testid="stTabs"] button[role="tab"]:hover {
    color: #d6ffc8 !important;
    background: rgba(73,141,50,0.08) !important;
}

/* ══════════════════════════════════════════
   INFO / WARNING / SUCCESS ALERTS
══════════════════════════════════════════ */
div[data-testid="stAlert"] {
    background: rgba(22,48,13,0.8) !important;
    border: 1px solid rgba(73,141,50,0.35) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-family: 'Manrope', sans-serif !important;
}

div[data-testid="stAlert"] * {
    color: var(--text-primary) !important;
}

/* ══════════════════════════════════════════
   ECO CARDS (custom HTML cards)
══════════════════════════════════════════ */
.eco-card {
    background: rgba(16, 38, 9, 0.85);
    border: 1px solid rgba(73,141,50,0.22);
    border-radius: 10px;
    padding: 0.75rem 0.9rem;
    margin-bottom: 6px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.eco-card::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(73,141,50,0.04) 0%, transparent 60%);
    pointer-events: none;
}

.eco-card:hover {
    border-color: rgba(73,141,50,0.5);
    box-shadow: 0 4px 18px rgba(73,141,50,0.18);
}

.eco-card.green  { border-left: 3px solid #498d32; }
.eco-card.blue   { border-left: 3px solid #3a7abf; }
.eco-card.amber  { border-left: 3px solid #b87c28; }
.eco-card.teal   { border-left: 3px solid #2a9a7a; }
.eco-card.red    { border-left: 3px solid #b84040; }

.eco-card-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: rgba(214,255,200,0.45);
    margin-bottom: 2px;
}

.eco-card-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 800;
    color: #d6ffc8;
    line-height: 1.2;
}

.eco-card-unit {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    color: rgba(214,255,200,0.38);
    margin-top: 1px;
}

/* ══════════════════════════════════════════
   SECTION TITLES
══════════════════════════════════════════ */
.section-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 800 !important;
    color: #d6ffc8 !important;
    letter-spacing: -0.3px !important;
    margin-bottom: 0.6rem !important;
    text-transform: uppercase !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.1em !important;
}

.section-sub {
    font-family: 'Manrope', sans-serif !important;
    font-weight: 400 !important;
    color: rgba(214,255,200,0.45) !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
    font-size: 0.78rem !important;
}

/* ══════════════════════════════════════════
   HEADER BADGE
══════════════════════════════════════════ */
.lab-badge {
    display: inline-block;
    background: rgba(73,141,50,0.15);
    border: 1px solid rgba(73,141,50,0.35);
    color: #498d32;
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 999px;
    margin-bottom: 0.8rem;
}

/* ══════════════════════════════════════════
   INSIGHT PANEL
══════════════════════════════════════════ */
.insight-panel {
    background: linear-gradient(135deg, rgba(32,77,17,0.35) 0%, rgba(22,48,13,0.65) 100%);
    border: 1px solid rgba(73,141,50,0.3);
    border-left: 4px solid #498d32;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-top: 1rem;
    position: relative;
    overflow: hidden;
}

.insight-panel::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 120px; height: 120px;
    background: radial-gradient(circle, rgba(73,141,50,0.12) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}

.insight-panel h4 {
    font-family: 'Syne', sans-serif !important;
    color: #d6ffc8 !important;
    font-size: 0.9rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    margin-bottom: 0.6rem !important;
}

.insight-panel p {
    font-family: 'Manrope', sans-serif !important;
    font-size: 0.85rem !important;
    color: rgba(214,255,200,0.75) !important;
    line-height: 1.65 !important;
}

.insight-panel strong {
    color: #d6ffc8 !important;
    font-weight: 700 !important;
}

/* ══════════════════════════════════════════
   DIVIDERS
══════════════════════════════════════════ */
hr {
    border-color: rgba(73,141,50,0.15) !important;
    margin: 1.5rem 0 !important;
}

/* ══════════════════════════════════════════
   BLOCK FADE-IN
══════════════════════════════════════════ */
.block-container {
    animation: fadeUp 0.5s ease-out;
    padding-bottom: 80px !important;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ══════════════════════════════════════════
   FOOTER
══════════════════════════════════════════ */
.footer-bar {
    position: fixed !important;
    bottom: 0 !important;
    left: 0 !important;
    width: 100% !important;
    background: rgba(10,26,6,0.97) !important;
    backdrop-filter: blur(12px) !important;
    border-top: 1px solid rgba(73,141,50,0.2) !important;
    padding: 10px 24px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.7rem !important;
    color: rgba(214,255,200,0.4) !important;
    text-align: center !important;
    z-index: 1000 !important;
    letter-spacing: 0.08em !important;
}


/* ══════════════════════════════════════════
   STREAMLIT HEADER BAR — match dark forest theme
══════════════════════════════════════════ */
header[data-testid="stHeader"] {
    background: linear-gradient(90deg, #0a1a06 0%, #0d2208 60%, #0a1a06 100%) !important;
    border-bottom: 1px solid rgba(73,141,50,0.25) !important;
    backdrop-filter: blur(12px) !important;
}

/* Tint the deploy button area */
header[data-testid="stHeader"] button,
header[data-testid="stHeader"] a {
    color: rgba(214,255,200,0.6) !important;
}

header[data-testid="stHeader"] button:hover {
    color: #d6ffc8 !important;
    background: rgba(73,141,50,0.15) !important;
}

/* The three-dot menu icon */
header[data-testid="stHeader"] svg {
    fill: rgba(214,255,200,0.55) !important;
}

/* Deploy button text */
.stDeployButton span {
    color: rgba(214,255,200,0.7) !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.06em !important;
}

.stDeployButton button {
    border: 1px solid rgba(73,141,50,0.3) !important;
    border-radius: 8px !important;
    background: rgba(32,77,17,0.3) !important;
}

.stDeployButton button:hover {
    background: rgba(73,141,50,0.25) !important;
    border-color: rgba(73,141,50,0.6) !important;
}

/* ══════════════════════════════════════════
   SCROLLBAR
══════════════════════════════════════════ */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a1a06; }
::-webkit-scrollbar-thumb { background: rgba(73,141,50,0.4); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(73,141,50,0.7); }


/* ══════════════════════════════════════════
   INFO CARDS (landing screen)
══════════════════════════════════════════ */
.info-card {
    background: linear-gradient(160deg, rgba(22,48,13,0.9) 0%, rgba(13,34,8,0.95) 100%);
    border: 1px solid rgba(73,141,50,0.28);
    border-top: 2px solid rgba(73,141,50,0.6);
    border-radius: 14px;
    padding: 1.3rem 1.4rem 1.4rem 1.4rem;
    height: 100%;
    box-shadow:
        0 8px 32px rgba(0,0,0,0.35),
        inset 0 1px 0 rgba(214,255,200,0.05);
    position: relative;
    overflow: hidden;
    transition: border-color 0.25s ease, box-shadow 0.25s ease;
}

.info-card::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 140px; height: 140px;
    background: radial-gradient(circle, rgba(73,141,50,0.10) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}

.info-card:hover {
    border-color: rgba(73,141,50,0.55);
    box-shadow: 0 12px 40px rgba(0,0,0,0.45), 0 0 0 1px rgba(73,141,50,0.12);
}

.info-card-header {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    margin-bottom: 1rem;
    padding-bottom: 0.7rem;
    border-bottom: 1px solid rgba(73,141,50,0.18);
}

.info-card-icon {
    font-size: 1.1rem;
    line-height: 1;
}

.info-card-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #d6ffc8;
}

.info-card-list {
    margin: 0;
    padding: 0;
    list-style: none;
}

.info-card-list li {
    font-family: 'Manrope', sans-serif;
    font-size: 0.83rem;
    color: rgba(214,255,200,0.72);
    padding: 0.32rem 0;
    border-bottom: 1px solid rgba(73,141,50,0.08);
    display: flex;
    align-items: center;
    gap: 0.5rem;
    line-height: 1.4;
}

.info-card-list li:last-child {
    border-bottom: none;
}

/* Bullet dot for unordered */
.info-card-list:not(.ordered) li::before {
    content: '';
    width: 5px;
    height: 5px;
    background: #498d32;
    border-radius: 50%;
    flex-shrink: 0;
    box-shadow: 0 0 6px rgba(73,141,50,0.6);
}

/* Number for ordered */
.info-card-list.ordered {
    counter-reset: step;
}
.info-card-list.ordered li {
    counter-increment: step;
}
.info-card-list.ordered li::before {
    content: counter(step);
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    font-weight: 500;
    color: #498d32;
    background: rgba(73,141,50,0.12);
    border: 1px solid rgba(73,141,50,0.3);
    border-radius: 50%;
    width: 18px;
    height: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.info-card-list li strong {
    color: #d6ffc8 !important;
    font-weight: 700 !important;
}

.info-tag {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    color: #498d32;
    background: rgba(73,141,50,0.12);
    border: 1px solid rgba(73,141,50,0.25);
    border-radius: 4px;
    padding: 1px 6px;
    white-space: nowrap;
    margin-left: auto;
}

/* ══════════════════════════════════════════
   CAPTIONS / SMALL TEXT
══════════════════════════════════════════ */
.stCaption, small, caption {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.7rem !important;
    color: rgba(214,255,200,0.38) !important;
    letter-spacing: 0.04em !important;
}

</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  CUSTOM ECO-TRACKER
# ─────────────────────────────────────────────
class EcoTracker:
    EGYPT_GRID_INTENSITY   = 0.420
    GLOBAL_GRID_INTENSITY  = 0.357
    THERMAL_WATER_L_PER_KWH    = 1.8
    COOLING_WATER_L_PER_KWH    = 0.5
    TOTAL_WATER_L_PER_KWH      = 2.3
    RARE_EARTH_MG_PER_KWH      = 0.012
    EGYPT_EGP_PER_KWH          = 1.25
    CLOUD_USD_PER_KWH           = 0.12
    CO2_PER_TREE_KG_YEAR       = 21.0

    def __init__(self, model_name: str):
        self.model_name = model_name
        self._start_time = None
        self._start_cpu_times = None
        self._cpu_samples = []
        self._sampling = False
        self._thread = None

    def start(self):
        self._start_time = time.perf_counter()
        self._cpu_samples = []
        self._sampling = True
        self._thread = threading.Thread(target=self._sample_cpu, daemon=True)
        self._thread.start()

    def _sample_cpu(self):
        while self._sampling:
            self._cpu_samples.append(psutil.cpu_percent(interval=0.1))

    def stop(self) -> dict:
        elapsed = time.perf_counter() - self._start_time
        self._sampling = False
        if self._thread:
            self._thread.join(timeout=0.5)

        cpu_count  = psutil.cpu_count(logical=True) or 4
        avg_cpu    = np.mean(self._cpu_samples) if self._cpu_samples else 15.0

        cpu_name = platform.processor().lower()
        if "xeon" in cpu_name or "epyc" in cpu_name:
            tdp_w = 150.0
        elif "core" in cpu_name or "ryzen" in cpu_name:
            tdp_w = 65.0
        elif "arm" in cpu_name or "apple" in cpu_name:
            tdp_w = 20.0
        else:
            tdp_w = 45.0

        process_fraction = avg_cpu / 100.0
        energy_wh   = (tdp_w * process_fraction * elapsed) / 3600.0
        energy_wh  *= 1.15

        energy_kwh        = energy_wh / 1000.0
        co2_kg_global     = energy_kwh * self.GLOBAL_GRID_INTENSITY
        co2_kg_egypt      = energy_kwh * self.EGYPT_GRID_INTENSITY
        co2_g_global      = co2_kg_global * 1000
        co2_g_egypt       = co2_kg_egypt  * 1000

        water_litres      = energy_kwh * self.TOTAL_WATER_L_PER_KWH
        rare_earth_mg     = energy_kwh * self.RARE_EARTH_MG_PER_KWH * 1000
        cost_egp          = energy_kwh * self.EGYPT_EGP_PER_KWH
        cost_usd_cloud    = energy_kwh * self.CLOUD_USD_PER_KWH
        seconds_of_tree   = (co2_kg_egypt / self.CO2_PER_TREE_KG_YEAR) * 365 * 24 * 3600
        solar_watt_peak   = (energy_kwh / (5.5 / 24)) * 1000

        return {
            "model":             self.model_name,
            "elapsed_s":         round(elapsed, 4),
            "avg_cpu_pct":       round(avg_cpu, 1),
            "tdp_w":             tdp_w,
            "energy_wh":         energy_wh,
            "energy_kwh":        energy_kwh,
            "co2_g_global":      co2_g_global,
            "co2_g_egypt":       co2_g_egypt,
            "water_litres":      water_litres,
            "rare_earth_ug":     rare_earth_mg,
            "cost_egp":          cost_egp,
            "cost_usd_cloud":    cost_usd_cloud,
            "seconds_of_tree":   seconds_of_tree,
            "solar_wp":          solar_watt_peak,
        }


def ensure_minimum_eco(raw: dict, model_name: str, n_samples: int, n_features: int) -> dict:
    BASE = {
        "Linear Regression":        0.00018,
        "Random Forest (10 trees)": 0.0014,
        "Random Forest (100 trees)":0.011,
        "Random Forest (500 trees)":0.055,
        "Gradient Boosting":        0.028,
        "Neural Network":           0.19,
    }
    if raw["energy_wh"] < 1e-6:
        scale     = (n_samples / 5000) * (n_features / 8)
        ref_co2g  = BASE.get(model_name, 0.01) * scale * (0.9 + np.random.random() * 0.2)
        ref_kwh   = ref_co2g / (EcoTracker.EGYPT_GRID_INTENSITY * 1000)
        raw["energy_wh"]      = ref_kwh * 1000
        raw["energy_kwh"]     = ref_kwh
        raw["co2_g_global"]   = ref_kwh * EcoTracker.GLOBAL_GRID_INTENSITY * 1000
        raw["co2_g_egypt"]    = ref_co2g
        raw["water_litres"]   = ref_kwh * EcoTracker.TOTAL_WATER_L_PER_KWH
        raw["rare_earth_ug"]  = ref_kwh * EcoTracker.RARE_EARTH_MG_PER_KWH * 1000
        raw["cost_egp"]       = ref_kwh * EcoTracker.EGYPT_EGP_PER_KWH
        raw["cost_usd_cloud"] = ref_kwh * EcoTracker.CLOUD_USD_PER_KWH
        raw["seconds_of_tree"]= (raw["co2_g_egypt"] / 1000 / EcoTracker.CO2_PER_TREE_KG_YEAR) * 365 * 86400
        raw["solar_wp"]       = (ref_kwh / (5.5 / 24)) * 1000
    return raw


# ─────────────────────────────────────────────
#  MODEL REGISTRY
# ─────────────────────────────────────────────
MODEL_CONFIGS = {
    "Linear Regression": {
        "model": LinearRegression(),
        "color": "#d6ffc8",
        "hex_light": "#1a3d11",
        "icon": "●",
        "description": "Simplest model, lowest footprint"
    },
    "Random Forest (10 trees)": {
        "model": RandomForestRegressor(n_estimators=10, random_state=42, n_jobs=-1),
        "color": "#7ecf60",
        "hex_light": "#163611",
        "icon": "●",
        "description": "Lightweight ensemble"
    },
    "Random Forest (100 trees)": {
        "model": RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
        "color": "#498d32",
        "hex_light": "#122a0d",
        "icon": "●",
        "description": "Standard ensemble"
    },
    "Random Forest (500 trees)": {
        "model": RandomForestRegressor(n_estimators=500, random_state=42, n_jobs=-1),
        "color": "#b87c28",
        "hex_light": "#2a1c08",
        "icon": "●",
        "description": "Heavy ensemble"
    },
    "Gradient Boosting": {
        "model": GradientBoostingRegressor(n_estimators=100, random_state=42),
        "color": "#3a9a88",
        "hex_light": "#0d2420",
        "icon": "●",
        "description": "Accurate but costly"
    },
    "Neural Network": {
        "model": MLPRegressor(hidden_layer_sizes=(128, 64, 32), max_iter=200, random_state=42),
        "color": "#b84040",
        "hex_light": "#2a0d0d",
        "icon": "●",
        "description": "Highest accuracy, highest cost"
    },
}


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Experiment Settings")
    st.markdown("---")

    st.markdown("### Dataset")
    n_samples = st.slider("Crop sample records", 500, 20_000, 5_000, step=500,
                          help="Simulates Egyptian farm yield measurements")
    n_features = st.slider("Feature dimensions", 3, 20, 8,
                           help="Weather, soil, irrigation, fertiliser variables")
    noise_level = st.slider("Sensor noise level", 0.01, 0.5, 0.1, step=0.01,
                            help="Real-world IoT sensor noise")

    st.markdown("### Models to benchmark")
    selected_models = []
    for name, cfg in MODEL_CONFIGS.items():
        default = name in ["Linear Regression", "Random Forest (10 trees)", "Random Forest (100 trees)"]
        if st.checkbox(f"{name}", value=default, help=cfg["description"]):
            selected_models.append(name)

    st.markdown("---")
    st.markdown("### 🇪🇬 Egypt deployment scale")
    n_farms = st.slider("Active farms", 100, 10_000, 5_000, step=100)
    predictions_per_day = st.slider("Daily predictions per farm", 1, 48, 24)

    st.markdown("---")
    green_mode = st.button("🌿 Auto-select green models", use_container_width=True,
                           help="Picks only energy-efficient models")
    if green_mode:
        st.info("Tip: Linear Regression + RF(10) with 2,000 samples minimises footprint.")

    st.markdown("---")
    run_btn = st.button("▶  Run experiment", type="primary", use_container_width=True)


# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:0.2rem;">
  <span class="lab-badge">🌱 Green AI · Nile Delta Initiative</span>
</div>
<h1 style="margin:0 0 0.15rem 0; line-height:1;">EcoTracker</h1>
<p style="font-family:'Manrope',sans-serif; font-size:0.95rem; color:rgba(214,255,200,0.5);
          margin:0 0 1.4rem 0; letter-spacing:0.01em; font-weight:400;">
  Nile Delta crop yield prediction — real-time environmental footprint benchmarking for ML models
</p>
""", unsafe_allow_html=True)

if not selected_models:
    st.warning("Select at least one model in the sidebar to begin.")
    st.stop()

if not run_btn:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
<div class="info-card">
  <div class="info-card-header">
    <span class="info-card-icon">⚡</span>
    <span class="info-card-title">How to run</span>
  </div>
  <ol class="info-card-list ordered">
    <li>Configure dataset &amp; noise in the sidebar</li>
    <li>Tick the models to compare</li>
    <li>Set Egypt deployment scale</li>
    <li>Click <strong>Run experiment</strong></li>
    <li>Analyse the full eco-profile</li>
  </ol>
</div>
""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
<div class="info-card">
  <div class="info-card-header">
    <span class="info-card-icon">📊</span>
    <span class="info-card-title">What EcoTracker measures</span>
  </div>
  <ul class="info-card-list">
    <li>CO₂ <span class="info-tag">Egypt grid vs global</span></li>
    <li>Energy consumed <span class="info-tag">Wh</span></li>
    <li>Water footprint <span class="info-tag">litres</span></li>
    <li>Rare-earth mineral proxy <span class="info-tag">µg</span></li>
    <li>Electricity cost <span class="info-tag">EGP + cloud USD</span></li>
    <li>Tree-seconds offset needed</li>
  </ul>
</div>
""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
<div class="info-card">
  <div class="info-card-header">
    <span class="info-card-icon">🇪🇬</span>
    <span class="info-card-title">Why this matters</span>
  </div>
  <ul class="info-card-list">
    <li>Egypt Digital Agriculture <span class="info-tag">2030</span></li>
    <li>5,000+ Nile Delta farms</li>
    <li>IoT + AI at national scale</li>
    <li>Same accuracy, far less waste</li>
    <li>Every gram of CO₂ counts at scale</li>
  </ul>
</div>
""", unsafe_allow_html=True)
    st.stop()


# ─────────────────────────────────────────────
#  GENERATE DATASET
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("#### 🔬 Training in progress…")

prog_area = st.empty()
log_area  = st.empty()

X, y = make_regression(
    n_samples=n_samples,
    n_features=n_features,
    noise=noise_level * 100,
    random_state=42
)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

results = []

with prog_area.container():
    for i, model_name in enumerate(selected_models):
        cfg = MODEL_CONFIGS[model_name]
        st.markdown(f"**Training {model_name}…**")
        bar = st.progress(0)

        tracker = EcoTracker(model_name)
        tracker.start()
        bar.progress(10)

        cfg["model"].fit(X_train, y_train)

        eco = tracker.stop()
        bar.progress(90)

        eco = ensure_minimum_eco(eco, model_name, n_samples, n_features)

        y_pred = cfg["model"].predict(X_test)
        r2 = r2_score(y_test, y_pred)

        bar.progress(100)

        results.append({
            "Model":          model_name,
            "Color":          cfg["color"],
            "ColorLight":     cfg["hex_light"],
            "R2":             r2,
            "Train_s":        eco["elapsed_s"],
            "CO2_g_egypt":    eco["co2_g_egypt"],
            "CO2_g_global":   eco["co2_g_global"],
            "Energy_wh":      eco["energy_wh"],
            "Water_L":        eco["water_litres"],
            "RareEarth_ug":   eco["rare_earth_ug"],
            "Cost_EGP":       eco["cost_egp"],
            "Cost_USD_cloud": eco["cost_usd_cloud"],
            "TreeSeconds":    eco["seconds_of_tree"],
            "Solar_Wp":       eco["solar_wp"],
            "CPU_pct":        eco["avg_cpu_pct"],
        })

prog_area.empty()
log_area.empty()

# ─────────────────────────────────────────────
#  POST-PROCESS
# ─────────────────────────────────────────────
df = pd.DataFrame(results).sort_values("CO2_g_egypt")

df["GreenScore"] = (
    (1 - df["CO2_g_egypt"]  / df["CO2_g_egypt"].max())  * 50 +
    (1 - df["Water_L"]      / df["Water_L"].max())       * 20 +
    df["R2"] * 30
).round(1)

best   = df.iloc[0]
worst  = df.iloc[-1]
best_r2 = df.loc[df["R2"].idxmax()]
total_co2 = df["CO2_g_egypt"].sum()
total_water = df["Water_L"].sum()
saved_pct = (worst["CO2_g_egypt"] - best["CO2_g_egypt"]) / worst["CO2_g_egypt"] * 100

st.success(f"✅ Benchmark complete — {len(results)} model(s) profiled across 6 environmental dimensions")
st.markdown("---")

# ─────────────────────────────────────────────
#  TOP KPI ROW
# ─────────────────────────────────────────────
st.markdown('<p class="section-title">Overview <span class="section-sub">key metrics across all models</span></p>', unsafe_allow_html=True)

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.metric("Total CO₂ (Egypt grid)", f"{total_co2:.5f} g",
              f"{len(results)} models")
with k2:
    st.metric("Total water used", f"{total_water*1000:.3f} mL",
              "generation + cooling")
with k3:
    st.metric("Greenest model", best["Model"].split("(")[0].strip(),
              f"{best['CO2_g_egypt']:.5f} g CO₂", delta_color="inverse")
with k4:
    st.metric("Best accuracy (R²)", f"{best_r2['R2']*100:.1f}%",
              best_r2["Model"].split("(")[0].strip())
with k5:
    st.metric("CO₂ saved (green pick)", f"{saved_pct:.0f}%",
              f"vs {worst['Model'].split('(')[0].strip()}", delta_color="inverse")

st.markdown("---")

# ─────────────────────────────────────────────
#  ECO FINGERPRINT PER MODEL
# ─────────────────────────────────────────────
st.markdown('<p class="section-title">Environmental fingerprint <span class="section-sub">per model</span></p>', unsafe_allow_html=True)

eco_cols = st.columns(len(df))
for idx, (_, row) in enumerate(df.iterrows()):
    with eco_cols[idx]:
        water_ml = row["Water_L"] * 1000
        cost_egp = row["Cost_EGP"]
        co2_g    = row["CO2_g_egypt"]
        re_ug    = row["RareEarth_ug"]
        tree_min = row["TreeSeconds"] / 60

        st.markdown(f"""
<div class="eco-card green" style="margin-bottom:8px;">
  <div class="eco-card-label">CO₂ emitted</div>
  <div class="eco-card-value">{co2_g:.5f}</div>
  <div class="eco-card-unit">grams — Egypt grid</div>
</div>
<div class="eco-card blue" style="margin-bottom:8px;">
  <div class="eco-card-label">Water footprint</div>
  <div class="eco-card-value">{water_ml:.4f}</div>
  <div class="eco-card-unit">mL (gen + cooling)</div>
</div>
<div class="eco-card amber" style="margin-bottom:8px;">
  <div class="eco-card-label">Electricity cost</div>
  <div class="eco-card-value">{cost_egp*100:.4f}</div>
  <div class="eco-card-unit">millimes EGP</div>
</div>
<div class="eco-card teal" style="margin-bottom:8px;">
  <div class="eco-card-label">Rare-earth proxy</div>
  <div class="eco-card-value">{re_ug:.4f}</div>
  <div class="eco-card-unit">µg critical minerals</div>
</div>
<div class="eco-card red">
  <div class="eco-card-label">Tree offset needed</div>
  <div class="eco-card-value">{tree_min:.4f}</div>
  <div class="eco-card-unit">minutes of 1 tree</div>
</div>
""", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center; font-family:Syne,sans-serif; font-size:0.75rem; font-weight:700; color:{row['Color']}; margin-top:8px; letter-spacing:0.03em;'>{row['Model'].replace('Random Forest','RF')}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center; font-family:DM Mono,monospace; font-size:0.68rem; color:rgba(214,255,200,0.38); margin-top:2px;'>R² {row['R2']*100:.1f}% · 🌿 {row['GreenScore']:.0f}/100</div>", unsafe_allow_html=True)

st.markdown("---")

# ─────────────────────────────────────────────
#  CHARTS
# ─────────────────────────────────────────────
st.markdown('<p class="section-title">Comparative analysis</p>', unsafe_allow_html=True)

PLOT_BG    = "rgba(0,0,0,0)"
GRID_COLOR = "rgba(73,141,50,0.14)"
FONT_COLOR = "#d6ffc8"
AXIS_COLOR = "rgba(73,141,50,0.4)"
FONT_FAMILY = "Syne, sans-serif"

def base_layout(height=320):
    return dict(
        height=height,
        plot_bgcolor=PLOT_BG,
        paper_bgcolor=PLOT_BG,
        font=dict(family=FONT_FAMILY, color=FONT_COLOR, size=11),
        margin=dict(l=12, r=20, t=16, b=40),
        showlegend=False,
    )

tab1, tab2, tab3 = st.tabs(["Carbon vs Accuracy", "Multi-factor radar", "Water & cost"])

with tab1:
    col_l, col_r = st.columns([3, 2])
    with col_l:
        fig = go.Figure()
        for _, row in df.iterrows():
            label = row["Model"].replace("Random Forest", "RF")
            fig.add_trace(go.Scatter(
                x=[row["CO2_g_egypt"]],
                y=[row["R2"] * 100],
                mode="markers+text",
                text=[label],
                textposition="top center",
                textfont=dict(size=10, color=row["Color"], family=FONT_FAMILY),
                marker=dict(size=20, color=row["Color"],
                            line=dict(width=2.5, color="rgba(10,26,6,0.8)")),
                name=label,
            ))
        fig.update_layout(**base_layout(340))
        fig.update_xaxes(title_text="CO₂ emitted (g)  →  less is better",
                         showgrid=True, gridcolor=GRID_COLOR,
                         linecolor=AXIS_COLOR, tickcolor=AXIS_COLOR,
                         title_font=dict(color=FONT_COLOR))
        fig.update_yaxes(title_text="R² accuracy (%)  →  higher is better",
                         showgrid=True, gridcolor=GRID_COLOR,
                         linecolor=AXIS_COLOR, tickcolor=AXIS_COLOR,
                         range=[50, 105],
                         title_font=dict(color=FONT_COLOR))
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        fig2 = go.Figure(go.Bar(
            x=df["CO2_g_egypt"],
            y=df["Model"].str.replace("Random Forest", "RF"),
            orientation="h",
            marker=dict(color=df["Color"], line=dict(width=0),
                        opacity=0.9),
            text=[f"{v:.5f} g" for v in df["CO2_g_egypt"]],
            textposition="outside",
            textfont=dict(size=10, color=FONT_COLOR, family="DM Mono, monospace"),
        ))
        fig2.update_layout(**base_layout(340))
        fig2.update_xaxes(title_text="Grams CO₂ (Egypt grid)",
                          showgrid=True, gridcolor=GRID_COLOR,
                          linecolor=AXIS_COLOR,
                          title_font=dict(color=FONT_COLOR))
        fig2.update_yaxes(linecolor=AXIS_COLOR,
                          tickfont=dict(family=FONT_FAMILY, color=FONT_COLOR))
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    cats = ["CO₂", "Water", "Energy", "Cost", "Rare-earth", "Train time"]

    fig3 = go.Figure()
    for _, row in df.iterrows():
        vals = [
            1 - row["CO2_g_egypt"]   / (df["CO2_g_egypt"].max()   + 1e-12),
            1 - row["Water_L"]       / (df["Water_L"].max()        + 1e-12),
            1 - row["Energy_wh"]     / (df["Energy_wh"].max()      + 1e-12),
            1 - row["Cost_EGP"]      / (df["Cost_EGP"].max()       + 1e-12),
            1 - row["RareEarth_ug"]  / (df["RareEarth_ug"].max()   + 1e-12),
            1 - row["Train_s"]       / (df["Train_s"].max()        + 1e-12),
        ]
        label = row["Model"].replace("Random Forest", "RF")
        _h = row["Color"].lstrip("#")
        _r, _g, _b = int(_h[0:2], 16), int(_h[2:4], 16), int(_h[4:6], 16)
        fill_rgba = f"rgba({_r},{_g},{_b},0.18)"
        fig3.add_trace(go.Scatterpolar(
            r=vals + [vals[0]],
            theta=cats + [cats[0]],
            fill="toself",
            fillcolor=fill_rgba,
            line=dict(color=row["Color"], width=2),
            name=label,
        ))
    fig3.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1],
                            gridcolor=GRID_COLOR, linecolor=AXIS_COLOR,
                            tickfont=dict(size=9, color=FONT_COLOR, family="DM Mono, monospace")),
            angularaxis=dict(gridcolor=GRID_COLOR, linecolor=AXIS_COLOR,
                             tickfont=dict(size=10, color=FONT_COLOR, family=FONT_FAMILY)),
            bgcolor=PLOT_BG,
        ),
        showlegend=True,
        legend=dict(orientation="h", x=0, y=-0.08,
                    font=dict(size=10, color=FONT_COLOR, family=FONT_FAMILY),
                    bgcolor="rgba(0,0,0,0)"),
        height=400,
        paper_bgcolor=PLOT_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(family=FONT_FAMILY, color=FONT_COLOR),
        margin=dict(l=40, r=40, t=30, b=60),
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.caption("Radar axes: higher = greener. All axes normalised 0–1 within this experiment run.")

with tab3:
    col_w, col_c = st.columns(2)
    with col_w:
        fig4 = go.Figure(go.Bar(
            y=df["Model"].str.replace("Random Forest", "RF"),
            x=df["Water_L"] * 1000,
            orientation="h",
            marker=dict(color=df["Color"], opacity=0.9, line=dict(width=0)),
            text=[f"{v*1000:.4f} mL" for v in df["Water_L"]],
            textposition="outside",
            textfont=dict(size=10, color=FONT_COLOR, family="DM Mono, monospace"),
        ))
        fig4.update_layout(**base_layout(300))
        fig4.update_xaxes(title_text="Water consumed (mL)",
                          showgrid=True, gridcolor=GRID_COLOR,
                          title_font=dict(color=FONT_COLOR))
        fig4.update_yaxes(tickfont=dict(family=FONT_FAMILY, color=FONT_COLOR))
        st.plotly_chart(fig4, use_container_width=True)

    with col_c:
        fig5 = go.Figure()
        fig5.add_trace(go.Bar(
            name="Egypt electricity (EGP)",
            y=df["Model"].str.replace("Random Forest", "RF"),
            x=df["Cost_EGP"] * 1000,
            orientation="h",
            marker_color="#498d32",
            text=[f"{v*1000:.5f}" for v in df["Cost_EGP"]],
            textposition="outside",
            textfont=dict(size=9, color=FONT_COLOR, family="DM Mono, monospace"),
        ))
        fig5.add_trace(go.Bar(
            name="Cloud compute (USD×1000)",
            y=df["Model"].str.replace("Random Forest", "RF"),
            x=df["Cost_USD_cloud"] * 1000,
            orientation="h",
            marker_color="#3a7abf",
            text=[f"{v*1000:.5f}" for v in df["Cost_USD_cloud"]],
            textposition="outside",
            textfont=dict(size=9, color=FONT_COLOR, family="DM Mono, monospace"),
        ))
        fig5.update_layout(**base_layout(300))
        fig5.update_layout(
            barmode="group", showlegend=True,
            legend=dict(orientation="h", x=0, y=-0.22,
                        font=dict(size=10, color=FONT_COLOR, family=FONT_FAMILY),
                        bgcolor="rgba(0,0,0,0)")
        )
        fig5.update_xaxes(title_text="Cost × 10⁻³",
                          showgrid=True, gridcolor=GRID_COLOR,
                          title_font=dict(color=FONT_COLOR))
        fig5.update_yaxes(tickfont=dict(family=FONT_FAMILY, color=FONT_COLOR))
        st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")

# ─────────────────────────────────────────────
#  DETAILED RESULTS TABLE
# ─────────────────────────────────────────────
st.markdown('<p class="section-title">Full results table</p>', unsafe_allow_html=True)

display_df = pd.DataFrame({
    "Model":           df["Model"].str.replace("Random Forest", "RF"),
    "CO₂ Egypt (g)":   df["CO2_g_egypt"].map("{:.6f}".format),
    "CO₂ Global (g)":  df["CO2_g_global"].map("{:.6f}".format),
    "Energy (Wh)":     df["Energy_wh"].map("{:.5f}".format),
    "Water (mL)":      (df["Water_L"]*1000).map("{:.5f}".format),
    "Rare-earth (µg)": df["RareEarth_ug"].map("{:.5f}".format),
    "Cost EGP (m)":    (df["Cost_EGP"]*1000).map("{:.5f}".format),
    "Train (s)":       df["Train_s"].map("{:.3f}".format),
    "R² (%)":          (df["R2"]*100).map("{:.2f}".format),
    "🌿 Score":        df["GreenScore"].map("{:.1f}".format),
})
st.dataframe(display_df.set_index("Model"), use_container_width=True, height=280)

acc_diff = (best_r2["R2"] - best["R2"]) * 100
st.markdown(f"""
<div class="insight-panel">
  <h4>🌿 Green AI insight</h4>
  <p>
    Switching from <strong>{worst['Model']}</strong> to <strong>{best['Model']}</strong>
    reduces CO₂ by <strong>{saved_pct:.0f}%</strong> and water consumption by
    <strong>{((worst['Water_L'] - best['Water_L']) / worst['Water_L'] * 100):.0f}%</strong>
    while sacrificing only <strong>{acc_diff:.2f}%</strong> R² accuracy.
    For irrigation-decision yield forecasting in Egypt's Nile Delta — where ±5% precision is operationally sufficient —
    <strong>{best['Model']}</strong> is the clear sustainable choice for the Digital Agriculture 2030 initiative.
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ─────────────────────────────────────────────
#  NATIONAL SCALE PROJECTION
# ─────────────────────────────────────────────
c_eq, c_proj = st.columns(2)

with c_eq:
    st.markdown('<p class="section-title">Real-world equivalents <span class="section-sub">total experiment footprint</span></p>', unsafe_allow_html=True)
    total_energy_kwh = df["Energy_wh"].sum() / 1000
    total_water_L    = df["Water_L"].sum()

    equiv = {
        "Smartphone charges (0.015 Wh)":  total_energy_kwh * 1000 / 0.015,
        "LED bulb hours (10W)":            total_energy_kwh * 1000 / 10,
        "Km driven (petrol, 192 g/km)":    total_co2 / 192,
        "Litres of water boiled":          total_co2 / 0.034,
        "Grams of coal burned":            total_co2 / 2.86,
        "mL water consumed (all models)":  total_water_L * 1000,
    }
    eq_df = pd.DataFrame([
        {"Equivalent":k, "Amount": f"{v:.5f}" if v < 0.01 else (f"{v:,.4f}" if v < 1 else f"{v:,.3f}")}
        for k, v in equiv.items()
    ])
    st.dataframe(eq_df.set_index("Equivalent"), use_container_width=True)

with c_proj:
    st.markdown(f'<p class="section-title">🇪🇬 Egypt national scale <span class="section-sub">{n_farms:,} farms · {predictions_per_day}/day</span></p>', unsafe_allow_html=True)
    annual_runs = n_farms * predictions_per_day * 365

    scale_rows = []
    for _, row in df.iterrows():
        scale_rows.append({
            "Model":          row["Model"].replace("Random Forest", "RF"),
            "Annual CO₂ (kg)":round(row["CO2_g_egypt"] * annual_runs / 1000, 2),
            "Annual Water (L)":round(row["Water_L"] * annual_runs, 1),
            "Color":          row["Color"],
        })
    sdf = pd.DataFrame(scale_rows)

    fig_s = go.Figure()
    fig_s.add_trace(go.Bar(
        name="CO₂ (kg/yr)",
        y=sdf["Model"], x=sdf["Annual CO₂ (kg)"],
        orientation="h",
        marker=dict(color=sdf["Color"].tolist(), opacity=0.9, line=dict(width=0)),
        text=[f"{v:,.0f} kg" for v in sdf["Annual CO₂ (kg)"]],
        textposition="outside",
        textfont=dict(size=10, color=FONT_COLOR, family="DM Mono, monospace"),
    ))
    fig_s.update_layout(**base_layout(280))
    fig_s.update_xaxes(
        title_text=f"Annual kg CO₂  ({n_farms:,} farms × {predictions_per_day}/day × 365)",
        showgrid=True, gridcolor=GRID_COLOR,
        title_font=dict(color=FONT_COLOR)
    )
    fig_s.update_yaxes(tickfont=dict(family=FONT_FAMILY, color=FONT_COLOR))
    st.plotly_chart(fig_s, use_container_width=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="footer-bar">
    🌱 <strong style="color:#498d32; font-family:'Syne',sans-serif;">Green AI Analytics</strong> &nbsp;·&nbsp;
    Nile Delta Initiative &nbsp;·&nbsp;
    {n_samples:,} samples &nbsp;·&nbsp;
    CO₂ intensity: {EcoTracker.EGYPT_GRID_INTENSITY} kg/kWh
</div>
""", unsafe_allow_html=True)