import os
import html
import json
import sqlite3
import urllib.request
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from mlp_inference import NumpyMLP
 
from test_guides import PHYSICAL_TESTS, TECHNICAL_TESTS
 
st.set_page_config(
    page_title="Soccer Performance Analytics",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed",
)
 
# Resolve paths relative to the project root (one level up from this file,
# since app.py lives in src/ while models/ and data/ live at the project
# root), so the app works no matter which folder you launch it from.
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SRC_DIR)
MODEL_PATH = os.path.join(BASE_DIR, "models", "mlp_model.npz")
FEATURES_PATH = os.path.join(BASE_DIR, "models", "feature_columns.json")
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "soccer_research.db")
CSV_PATH = os.path.join(DATA_DIR, "ea_fc26_players.csv")
DATA_URL = "https://huggingface.co/datasets/Kishohar/footballIQ/resolve/main/ea_fc26_players.csv"
 
POSITIONS = ["Forward", "Midfielder", "Defender"]
POSITION_CODE = {"Forward": "ST", "Midfielder": "CM", "Defender": "CB"}
 
 
# ---------------------------------------------------------------------------
# Data and model loading (same logic as before)
# ---------------------------------------------------------------------------
@st.cache_resource
def ensure_database_ready():
    """Build data/soccer_research.db from the public source dataset if it
    doesn't already exist. This is what lets the app run on a fresh
    checkout (e.g. Streamlit Community Cloud) where data/ is intentionally
    excluded from git, instead of requiring the .db file to be shipped in
    the repo."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(DB_PATH):
        return True
 
    with st.spinner("First-time setup: downloading and preparing the player database. This can take a minute..."):
        if not os.path.exists(CSV_PATH):
            urllib.request.urlretrieve(DATA_URL, CSV_PATH)
 
        df = pd.read_csv(CSV_PATH)
        df.columns = df.columns.str.strip().str.lower()
 
        name_col = next((c for c in ["name", "short_name", "long_name", "player_name"] if c in df.columns), None)
        age_col = next((c for c in ["age"] if c in df.columns), None)
        pace_col = next((c for c in ["pace", "pace_total", "sprint_speed"] if c in df.columns), None)
        dribbling_col = next((c for c in ["dribbling", "dribbling_total"] if c in df.columns), None)
 
        check_cols = [c for c in [name_col, age_col, pace_col, dribbling_col] if c is not None]
        if check_cols:
            df.dropna(subset=check_cols, inplace=True)
 
        numeric_cols = [c for c in ["pace", "acceleration", "sprint_speed", "strength", "stamina", "agility", "dribbling"] if c in df.columns]
        for col in numeric_cols:
            df = df[df[col] > 0]
 
        conn = sqlite3.connect(DB_PATH)
        df.to_sql("players", conn, if_exists="replace", index=False)
        conn.close()
 
    return True
 
 
@st.cache_resource
def load_model_and_features():
    model = NumpyMLP.load(MODEL_PATH)  # PyTorch-trained weights, run with NumPy
    with open(FEATURES_PATH, "r") as f:
        feature_cols = json.load(f)
    return model, feature_cols
 
 
@st.cache_data
def load_baseline_stats():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM players;", conn)
    conn.close()
    return df
 
 
def init_users_table():
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    conn.commit()
    conn.close()
 
 
def save_user(name, email, phone):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO users (name, email, phone) VALUES (?, ?, ?);",
        (name, email, phone),
    )
    conn.commit()
    conn.close()
 
 
# ---------------------------------------------------------------------------
# Turning the form answers into the model's input row (same logic as before)
# ---------------------------------------------------------------------------
def clamp(value, lo=30.0, hi=99.0):
    return max(lo, min(hi, value))
 
 
def rating_from_time(seconds, best_time, worst_time):
    """Faster (lower) time -> higher rating. Linearly interpolates between
    a recreational-level time (worst_time -> 30) and an elite time
    (best_time -> 99)."""
    span = worst_time - best_time
    scaled = 99.0 - (seconds - best_time) * (69.0 / span)
    return clamp(scaled)
 
 
def rating_from_reps(reps, min_reps, max_reps):
    span = max_reps - min_reps
    scaled = 30.0 + (reps - min_reps) * (69.0 / span)
    return clamp(scaled)
 
 
# technical answer -> the model column(s) it fills in
TECHNICAL_TO_COLUMNS = {
    "finishing": ["finishing"],
    "shotpower": ["shotpower", "volleys"],
    "passing": ["shortpassing", "longpassing"],
    "ballcontrol": ["ballcontrol"],
    "vision": ["vision"],
    "standingtackle": ["standingtackle"],
    "slidingtackle": ["slidingtackle"],
    "interceptions": ["interceptions"],
    "physical": ["strength", "aggression"],
    "dribbling": ["dribbling"],
    "longshots": ["longshots"],
    "positioning": ["positioning"],
    "headingaccuracy": ["headingaccuracy"],
    "curve": ["curve"],
    "penalties": ["penalties"],
    "crossing": ["crossing"],
    "freekickaccuracy": ["freekickaccuracy"],
    "composure": ["composure"],
    "stamina": ["stamina"],
    "jumping": ["jumping"],
    "defensiveawareness": ["defensiveawareness"],
}
 
COMPOSITE_SOURCES = {
    "pac": ["acceleration", "sprintspeed"],
    "dri": ["dribbling", "ballcontrol", "agility", "balance"],
    "pas": ["shortpassing", "longpassing", "vision"],
    "sho": ["finishing", "shotpower", "volleys", "longshots", "penalties"],
    "def": ["standingtackle", "slidingtackle", "interceptions", "defensiveawareness"],
    "phy": ["strength", "stamina", "aggression", "jumping"],
}
 
CATEGORY_LABELS = {
    "pac": "Pace",
    "dri": "Dribbling",
    "pas": "Passing",
    "sho": "Shooting",
    "def": "Defending",
    "phy": "Physical",
}
 
 
def build_input_row(answers, position, df_position, feature_cols):
    """Start every feature at the position-specific baseline mean, then
    overwrite the ones the user actually answered. Returns the filled-in
    dict and the set of model columns the user's answers touched."""
    input_dict = {col: float(df_position[col].mean()) for col in feature_cols}
    touched = set()
 
    def put(col, value):
        if col in input_dict:
            input_dict[col] = float(value)
            touched.add(col)
 
    # Profile (note: "age" is not a model feature, so it is display-only)
    put("height", answers["height"])
    put("weight", answers["weight"])
    put("weakfootability", answers["weakfoot"])
    put("skillmoves", answers["skillmoves"])
 
    # Physical tests
    sprint_rating = rating_from_time(answers["sprint_time"], best_time=3.5, worst_time=6.0)
    shuttle_rating = rating_from_time(answers["shuttle_time"], best_time=4.0, worst_time=7.0)
    strength_rating = rating_from_reps(answers["bench_reps"], min_reps=0, max_reps=30)
    for col in ("acceleration", "sprintspeed"):
        put(col, sprint_rating)
    for col in ("agility", "balance", "reactions"):
        put(col, shuttle_rating)
    put("strength", strength_rating)
 
    # Technical ratings (only the ones asked for this position are in answers)
    for key, columns in TECHNICAL_TO_COLUMNS.items():
        if key in answers:
            for col in columns:
                put(col, answers[key])
 
    # Keep the six category columns consistent with the detail columns
    for composite_col, source_cols in COMPOSITE_SOURCES.items():
        present = [c for c in source_cols if c in input_dict]
        if composite_col in input_dict and present:
            input_dict[composite_col] = float(np.mean([input_dict[c] for c in present]))
 
    return input_dict, touched
 
 
# ---------------------------------------------------------------------------
# Look and feel
# ---------------------------------------------------------------------------
CSS = """
<style>
.block-container { padding-top: 6.5rem; max-width: 760px; }
.eyebrow { color:#4ade80; font-size:0.78rem; letter-spacing:0.12em; text-transform:uppercase; font-weight:600; }
.hero-title { font-size:2.5rem; font-weight:800; line-height:1.1; margin:0.2rem 0 0.6rem 0; }
.hero-sub { color:#b6d4c1; font-size:1.05rem; margin-bottom:1.2rem; }
.how-card { background:#12301f; border:1px solid #1f5136; border-radius:14px; padding:0.9rem 1rem; height:100%; margin-bottom:0.9rem; }
.how-card b { color:#4ade80; }
.rating-card { background:linear-gradient(135deg,#14452a 0%,#0d2a1a 100%); border:1px solid #2a6b44;
  border-radius:18px; padding:1.6rem 1rem; text-align:center; margin:0.6rem 0 0.8rem 0; }
.rating-big { font-size:4.2rem; font-weight:800; color:#4ade80; line-height:1; }
.rating-big span { font-size:1.4rem; color:#86c9a0; font-weight:600; }
.rating-label { color:#b6d4c1; text-transform:uppercase; letter-spacing:0.1em; font-size:0.78rem; margin-bottom:0.4rem; }
.rating-note { color:#e8f5ec; margin-top:0.7rem; font-size:1.02rem; }
.chip { display:inline-block; background:#12301f; border:1px solid #1f5136; color:#b6d4c1;
  border-radius:999px; padding:0.15rem 0.7rem; font-size:0.85rem; margin-right:0.4rem; }
.mini-card { border-radius:14px; padding:0.8rem 1rem; margin-bottom:0.5rem; border:1px solid #1f5136; background:#12301f; }
.mini-card.gap { border-color:#6b4a1f; background:#2a2012; }
.mini-card .t { font-weight:700; }
.mini-card .s { color:#b6d4c1; font-size:0.92rem; }
 .tile-grid { display:grid; grid-template-columns:repeat(auto-fit, minmax(105px, 1fr)); gap:0.55rem; margin:0.3rem 0 0.8rem 0; }
.tile { border-radius:12px; padding:0.6rem 0.5rem; text-align:center; border:1px solid #1f5136; background:#12301f; }
.tile.down { border-color:#6b4a1f; background:#2a2012; }
.tile .tl { color:#b6d4c1; font-size:0.72rem; letter-spacing:0.08em; text-transform:uppercase; }
.tile .tv { font-size:1.9rem; font-weight:800; line-height:1.15; color:#4ade80; }
.tile.down .tv { color:#f0b35a; }
.tile .tp { color:#8fb3a0; font-size:0.78rem; }
.fine { color:#8fb3a0; font-size:0.85rem; }
div[data-testid="stFormSubmitButton"], div[data-testid="stButton"] { width:100%; }
div[data-testid="stFormSubmitButton"] button, div[data-testid="stButton"] button,
[data-testid^="stBaseButton-"] { width:100%; }
div[data-testid="stForm"] { border:1px solid #1f5136; border-radius:16px; padding:1.2rem; }
</style>
"""
 
 
# ---------------------------------------------------------------------------
# Session state helpers
# ---------------------------------------------------------------------------
def init_state():
    defaults = {
        "page": "welcome",     # welcome -> form -> results
        "answers": {},
        "user_name": "",
        "signed_up": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
 
 
def goto(page):
    st.session_state.page = page
    st.rerun()
 
 
def start_over():
    st.session_state.answers = {}
    goto("form")
 
 
# ---------------------------------------------------------------------------
# Page 1: welcome + sign-up
# ---------------------------------------------------------------------------
def render_welcome():
    st.markdown(
        """
        <div class="eyebrow">Multi-Modal Soccer Performance Analytics Framework</div>
        <div class="hero-title">Where do you really stand?</div>
        <div class="hero-sub">Test yourself the right way, enter your results, and see how you compare
        with 16,228 professional players at your position. Free, no paywall.</div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3)
    c1.markdown('<div class="how-card"><b>1. Learn the tests</b><br>Short, standard protocols for each skill, so you measure instead of guess.</div>', unsafe_allow_html=True)
    c2.markdown('<div class="how-card"><b>2. Fill in one form</b><br>Pick your position and rate yourself on the tests shown for it.</div>', unsafe_allow_html=True)
    c3.markdown('<div class="how-card"><b>3. See your results</b><br>Your rating, a chart against pros, and your strengths and gaps.</div>', unsafe_allow_html=True)
 
    with st.expander("About this research project"):
        st.markdown(
            "This tool is part of an ongoing NASA New York Space Grant Consortium "
            "research project conducted through Cornell University and Queensborough "
            "Community College (QCC). Your test results and profile information help "
            "support that research.\n\n"
            "Most amateur and youth players have no real way to know how their speed, "
            "strength, or technical ability compares to a professional, so the ratings "
            "players give themselves tend to be guesses. Here, your numbers are compared "
            "with EA Sports FC 26 ratings for professionals, filtered to your position, so "
            "a defender is compared with pro defenders and a forward with pro forwards."
        )
 
    st.write("")
    # NOTE FOR RESEARCHER: this form collects name/email/phone from real people.
    # Before deploying this publicly, confirm with your research advisor whether
    # this requires IRB review / informed consent as part of your Space Grant
    # project, since it involves collecting personally identifiable information
    # from human participants.
    st.markdown("#### Sign up to get started")
    with st.form("signup_form"):
        su_name = st.text_input("Full Name")
        su_email = st.text_input("Email")
        su_phone = st.text_input("Phone Number (optional)")
        agree = st.checkbox("I agree to have my submitted test data stored for this research project.")
        submitted = st.form_submit_button("Sign Up and Start", type="primary")
 
        if submitted:
            if not su_name.strip() or not su_email.strip():
                st.error("Name and email are required.")
            elif "@" not in su_email or "." not in su_email:
                st.error("Please enter a valid email address.")
            elif not agree:
                st.error("You must agree to data storage to continue.")
            else:
                save_user(su_name.strip(), su_email.strip(), su_phone.strip())
                st.session_state.signed_up = True
                st.session_state.user_name = su_name.strip()
                st.session_state.answers = {"name": su_name.strip()}
                goto("form")
 
 
# ---------------------------------------------------------------------------
# Page 2: the input form (one page; the position choice reveals its attributes)
# ---------------------------------------------------------------------------
def guide_box(item):
    if item.get("guide_md"):
        with st.expander(item["guide_title"]):
            st.markdown(item["guide_md"])
 
 
def number_or_slider(item, answers, key_prefix):
    default = answers.get(item["key"], item["default"])
    kwargs = {}
    if item.get("step") is not None:
        kwargs["step"] = item["step"]
    return st.slider(
        item["label"], item["min"], item["max"], default,
        key=f"{key_prefix}_{item['key']}", **kwargs,
    )
 
 
def render_form():
    answers = st.session_state.answers
 
    st.markdown('<div class="eyebrow">Your details</div>', unsafe_allow_html=True)
    st.markdown("### Tell us about you")
 
    # Name and position sit OUTSIDE the form on purpose: that way, choosing a
    # position instantly shows that position's attributes below.
    name = st.text_input("Player Name", answers.get("name", st.session_state.user_name), key="f_name")
    pos_default = POSITIONS.index(answers["position"]) if answers.get("position") in POSITIONS else 0
    position = st.selectbox("Preferred Position", POSITIONS, index=pos_default, key="f_position")
    # Earlier answers only count for the same position, so another position's
    # attributes can never leak into this one's rating.
    prev = answers if answers.get("position") == position else {}
 
    with st.form("player_form"):
        st.markdown("#### Profile")
        c1, c2, c3 = st.columns(3)
        age = c1.number_input("Age", min_value=14, max_value=45, value=int(prev.get("age", 17)), step=1, key="f_age")
        height = c2.number_input("Height (cm)", min_value=140, max_value=210, value=int(prev.get("height", 175)), step=1, key="f_height")
        weight = c3.number_input("Weight (kg)", min_value=40, max_value=110, value=int(prev.get("weight", 68)), step=1, key="f_weight")
        c4, c5 = st.columns(2)
        weakfoot = c4.select_slider("Weak Foot Ability (1-5 stars)", options=[1, 2, 3, 4, 5], value=prev.get("weakfoot", 3), key="f_weakfoot")
        skillmoves = c5.select_slider("Skill Moves (1-5 stars)", options=[1, 2, 3, 4, 5], value=prev.get("skillmoves", 3), key="f_skillmoves")
 
        st.markdown("#### Physical tests")
        st.caption("Open the box above each slider to see exactly how to run the test. Use your real result.")
        physical_values = {}
        for item in PHYSICAL_TESTS:
            guide_box(item)
            physical_values[item["key"]] = number_or_slider(item, prev, "f")
 
        st.markdown(f"#### {position} technical ratings")
        st.caption(
            "These change with your position, since a striker's shot power and a "
            "center-back's tackling aren't measuring the same thing. Open the box above "
            "each slider for a test you can use to rate yourself."
        )
        technical_values = {}
        tech_items = TECHNICAL_TESTS[position]
        for i in range(0, len(tech_items), 2):
            row = st.columns(2)           # two attributes side by side (stacks on phones)
            for col, item in zip(row, tech_items[i:i + 2]):
                with col:
                    guide_box(item)
                    technical_values[item["key"]] = number_or_slider(item, prev, f"f_{position}")
 
        submitted = st.form_submit_button("Get my rating →", type="primary")
 
    if submitted:
        # Start a fresh answer set so only this position's answers are kept.
        st.session_state.answers = {
            "name": name.strip() or st.session_state.user_name,
            "position": position, "age": age, "height": height, "weight": weight,
            "weakfoot": weakfoot, "skillmoves": skillmoves,
            **physical_values, **technical_values,
        }
        goto("results")
 
 
# ---------------------------------------------------------------------------
# Page 3: results
# ---------------------------------------------------------------------------
def radar_chart(user_vals, pro_vals, labels):
    theta = labels + labels[:1]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=pro_vals + pro_vals[:1], theta=theta, name="Pro average",
        line=dict(color="#8fb3a0", width=2, dash="dot"), fill="toself",
        fillcolor="rgba(143,179,160,0.12)",
    ))
    fig.add_trace(go.Scatterpolar(
        r=user_vals + user_vals[:1], theta=theta, name="You",
        line=dict(color="#4ade80", width=3), fill="toself",
        fillcolor="rgba(74,222,128,0.30)",
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(range=[20, 100], showticklabels=True, tickfont=dict(color="#8fb3a0", size=10),
                            gridcolor="#1f5136", linecolor="#1f5136"),
            angularaxis=dict(tickfont=dict(color="#e8f5ec", size=13), gridcolor="#1f5136", linecolor="#1f5136"),
        ),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e8f5ec"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
        margin=dict(l=75, r=75, t=20, b=40), height=380,
    )
    return fig
 
 
def render_results():
    answers = st.session_state.answers
    position = answers["position"]
    name = answers.get("name") or st.session_state.user_name or "Player"
 
    model, feature_cols = load_model_and_features()
    df_baseline = load_baseline_stats()
    df_position = df_baseline[df_baseline.get("position", pd.Series(dtype=str)) == POSITION_CODE[position]]
    if df_position.empty:
        df_position = df_baseline  # fallback if position labels don't match the DB
 
    input_dict, touched = build_input_row(answers, position, df_position, feature_cols)
    input_df = pd.DataFrame([input_dict])[feature_cols]
    predicted_rating = float(np.clip(model.predict(input_df)[0], 1, 99))
 
    pos_ratings = df_position["overallrating"]
    pro_avg = float(pos_ratings.mean())
    percentile = float((pos_ratings < predicted_rating).mean() * 100)
 
    safe_name = html.escape(name)
    st.markdown(
        f'<div class="eyebrow">Your results</div>'
        f'<div class="hero-title" style="font-size:2rem">{safe_name}</div>'
        f'<span class="chip">{position}</span><span class="chip">Age {int(answers["age"])}</span>',
        unsafe_allow_html=True,
    )
 
    if percentile >= 1:
        note = f"Higher than <b>{percentile:.0f}%</b> of pro {position.lower()}s in the database."
    else:
        note = (f"Every pro {position.lower()} in the database is rated higher. "
                "Most players start well below pro level, and that gap is what you can train.")
    st.markdown(
        f'<div class="rating-card"><div class="rating-label">Predicted talent rating</div>'
        f'<div class="rating-big">{predicted_rating:.1f}<span> / 99</span></div>'
        f'<div class="rating-note">{note}</div>'
        f'<div class="fine" style="margin-top:0.4rem">Pro {position.lower()} average: {pro_avg:.1f}</div></div>',
        unsafe_allow_html=True,
    )
 
    # --- category comparison -------------------------------------------------
    cats = list(CATEGORY_LABELS)
    labels = [CATEGORY_LABELS[c] for c in cats]
    user_vals = [float(input_dict[c]) for c in cats if c in input_dict]
    pro_vals = [float(df_position[c].mean()) for c in cats if c in df_position.columns]
    if len(user_vals) == len(cats) and len(pro_vals) == len(cats):
        st.markdown("#### Your numbers vs. the pro average")
        tiles = ""
        for c, label, you, pro in zip(cats, labels, user_vals, pro_vals):
            state = "up" if you >= pro else "down"
            tiles += (f'<div class="tile {state}"><div class="tl">{label}</div>'
                      f'<div class="tv">{you:.0f}</div><div class="tp">pro avg {pro:.0f}</div></div>')
        st.markdown(f'<div class="tile-grid">{tiles}</div>', unsafe_allow_html=True)
        st.plotly_chart(radar_chart(user_vals, pro_vals, labels),
                        config={"displayModeBar": False})
        st.caption("Categories you didn't enter anything for sit at the pro average for your position.")
 
        # strengths and gaps (only categories the user's answers actually touched)
        rows = []
        for c in cats:
            sources = COMPOSITE_SOURCES[c]
            if not any(s in touched for s in sources):
                continue
            std = float(df_position[c].std())
            z = (float(input_dict[c]) - float(df_position[c].mean())) / std if std > 0 else 0.0
            rows.append((CATEGORY_LABELS[c], z, float(input_dict[c]), float(df_position[c].mean())))
        rows.sort(key=lambda r: r[1], reverse=True)
 
        if len(rows) >= 2:
            st.markdown("#### Your strengths and biggest gaps")
            left, right = st.columns(2)
            with left:
                st.markdown("**Closest to pro level**")
                for label, z, you, pro in rows[:2]:
                    st.markdown(f'<div class="mini-card"><div class="t">{label}</div>'
                                f'<div class="s">You {you:.0f} · pro average {pro:.0f}</div></div>',
                                unsafe_allow_html=True)
            with right:
                st.markdown("**Furthest from pro level**")
                for label, z, you, pro in rows[::-1][:2]:
                    st.markdown(f'<div class="mini-card gap"><div class="t">{label}</div>'
                                f'<div class="s">You {you:.0f} · pro average {pro:.0f}</div></div>',
                                unsafe_allow_html=True)
 
    st.markdown(
        '<div class="fine" style="margin:0.8rem 0 0.8rem 0">This is an estimate that compares your self-reported results with EA Sports FC 26 '
        'ratings of professional players. It is not a measure of your real ability.</div>',
        unsafe_allow_html=True,
    )
 
    # --- the detailed numbers, tucked away ----------------------------------
    with st.expander("See the numbers"):
        zscore_features = {
            "Overall (Predicted)": ("overallrating", predicted_rating),
            "Pace": ("pac", input_dict.get("pac")),
            "Dribbling": ("dri", input_dict.get("dri")),
            "Passing": ("pas", input_dict.get("pas")),
            "Shooting": ("sho", input_dict.get("sho")),
            "Defending": ("def", input_dict.get("def")),
            "Physical": ("phy", input_dict.get("phy")),
            "Height (cm)": ("height", input_dict.get("height")),
            "Weight (kg)": ("weight", input_dict.get("weight")),
        }
        zrows = []
        for label, (col, user_value) in zscore_features.items():
            if col not in df_position.columns or user_value is None:
                continue
            pos_mean = df_position[col].mean()
            pos_std = df_position[col].std()
            z = (user_value - pos_mean) / pos_std if pos_std > 0 else 0.0
            zrows.append({"Attribute": label, "Your Value": round(user_value, 1),
                          "Position Avg": round(pos_mean, 1), "Z-Score": round(z, 2)})
        zscore_df = pd.DataFrame(zrows).set_index("Attribute")
        st.caption(
            "A Z-score shows how many standard deviations above or below the position average "
            "you fall. 0 = exactly average, +1 = one above, -1 = one below."
        )
        st.dataframe(zscore_df)
        st.write(f"**{position} baselines (n={len(df_position)})**")
        st.dataframe(df_position[["overallrating", "height", "weight"]].describe().T[["mean", "std", "min", "max"]])
        st.write("**Overall rating distribution of all 16,228 pros**")
        st.bar_chart(df_baseline["overallrating"].value_counts().sort_index())
 
    st.write("")
    b1, b2 = st.columns(2)
    if b1.button("← Edit my answers"):
        goto("form")
    if b2.button("Start over"):
        start_over()
 
 
# ---------------------------------------------------------------------------
# App entry point
# ---------------------------------------------------------------------------
st.markdown(CSS, unsafe_allow_html=True)
 
if not os.path.exists(MODEL_PATH):
    st.error("Model file not found. Please run `python3 src/model_trainer.py` first.")
    st.stop()
 
ensure_database_ready()
init_users_table()
init_state()
 
# Someone who already signed up in this session never sees the sign-up page again.
if st.session_state.page == "welcome" and st.session_state.signed_up:
    st.session_state.page = "form"
 
if st.session_state.page == "welcome":
    render_welcome()
elif st.session_state.page == "form":
    render_form()
else:
    if not st.session_state.answers.get("position"):
        goto("form")
    render_results()
 
