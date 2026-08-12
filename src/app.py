import os
import json
import sqlite3
import numpy as np
import pandas as pd
import streamlit as st
from xgboost import XGBRegressor

st.set_page_config(page_title="Soccer Performance Analytics", page_icon="⚽", layout="wide")

# Resolve paths relative to the project root (one level up from this file,
# since app.py lives in src/ while models/ and data/ live at the project
# root), so `streamlit run app.py` works no matter which folder you launch
# it from.
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SRC_DIR)
MODEL_PATH = os.path.join(BASE_DIR, "models", "xgboost_model.json")
FEATURES_PATH = os.path.join(BASE_DIR, "models", "feature_columns.json")
DB_PATH = os.path.join(BASE_DIR, "data", "soccer_research.db")

@st.cache_resource
def load_model_and_features():
    model = XGBRegressor()
    model.load_model(MODEL_PATH)
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


st.title("⚽ Multi-Modal Soccer Performance Analytics Framework")
st.subheader("NASA New York Space Grant Consortium — Research Initiative (2026–2027)")

if not os.path.exists(MODEL_PATH):
    st.error("Model file not found. Please run `python3 src/model_trainer.py` first.")
    st.stop()

init_users_table()

# --- Introduction ------------------------------------------------------
st.markdown(
    """
### What is this?

Most amateur and youth soccer players have no real way to know how their
speed, strength, or technical ability actually compares to a professional
athlete — so ratings players give themselves tend to be guesses, not
measurements.

**This app fixes that.** It's a free tool — no subscription, no paywall —
that lets you:

1. **Learn how to test yourself properly.** Every physical test below
   comes with a short explanation and a link to a real, standardized
   testing protocol (the same kind used in professional combines), so
   you're measuring yourself the right way before you enter anything.
2. **Enter your own results.** Sprint time, agility, strength, and your
   own technical self-ratings.
3. **See exactly where you stand.** Your numbers are compared directly
   against a database of **16,228 real professional players** (EA Sports
   FC 26 ratings data), filtered to your specific position, so a
   defender is compared to pro defenders and a forward to pro forwards —
   not to an unrelated average.

The result is an honest, data-driven snapshot of your current athletic
standing — not an inflated self-rating, and not a generic average, but
a real comparison against the level you're ultimately trying to reach.

*This tool is part of an ongoing NASA New York Space Grant Consortium
research project conducted through Cornell University and Queensborough
Community College (QCC). Your test results and profile information help
support that research.*
"""
)
st.divider()

# --- Signup gate -----------------------------------------------------------
# NOTE FOR RESEARCHER: this form collects name/email/phone from real people.
# Before deploying this publicly, confirm with your research advisor whether
# this requires IRB review / informed consent as part of your Space Grant
# project, since it involves collecting personally identifiable information
# from human participants.
if "signed_up" not in st.session_state:
    st.session_state.signed_up = False
    st.session_state.user_name = ""

if not st.session_state.signed_up:
    st.info("Sign up to get your personalized talent rating and benchmark comparison.")
    with st.form("signup_form"):
        su_name = st.text_input("Full Name")
        su_email = st.text_input("Email")
        su_phone = st.text_input("Phone Number (optional)")
        agree = st.checkbox("I agree to have my submitted test data stored for this research project.")
        submitted = st.form_submit_button("Sign Up")

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
                st.rerun()
    st.stop()

st.success(f"Welcome, {st.session_state.user_name}! Fill out your field test results in the sidebar.")

model, feature_cols = load_model_and_features()
df_baseline = load_baseline_stats()

st.sidebar.header("Player Field Inputs")
player_name = st.sidebar.text_input("Player Name", "Aashish Rawal")
position = st.sidebar.selectbox("Preferred Position", ["Forward", "Midfielder", "Defender"])

st.sidebar.subheader("Player Profile")
age_in = st.sidebar.number_input("Age", min_value=14, max_value=45, value=17, step=1)
height_in = st.sidebar.number_input("Height (cm)", min_value=140, max_value=210, value=175, step=1)
weight_in = st.sidebar.number_input("Weight (kg)", min_value=40, max_value=110, value=68, step=1)
weakfoot_in = st.sidebar.select_slider("Weak Foot Ability (1-5 stars)", options=[1, 2, 3, 4, 5], value=3)
skillmoves_in = st.sidebar.select_slider("Skill Moves (1-5 stars)", options=[1, 2, 3, 4, 5], value=3)

st.sidebar.subheader("Physical Tests")

with st.sidebar.expander("❓ How do I time my 30m sprint?"):
    st.markdown(
        "**Setup:** mark a straight, flat 30m stretch with two cones "
        "(start and finish). Warm up first with light jogging and a few "
        "practice accelerations.\n\n"
        "**How to run it:** start from a stationary position, sprint "
        "maximally through the finish cone (don't slow down before it), "
        "and have a partner time you with a stopwatch from your first "
        "movement to when you cross the line. Run it twice and record "
        "your best time.\n\n"
        "[Full protocol — Topend Sports](https://www.topendsports.com/testing/tests/sprint-30meters.htm)"
    )
sprint_time = st.sidebar.slider("30m Sprint Time (seconds)", 3.5, 6.0, 4.2, 0.1)

with st.sidebar.expander("❓ How do I run the 5-10-5 shuttle?"):
    st.markdown(
        "**Setup:** place 3 cones in a straight line, 5 yards apart "
        "(so 10 yards total between the outer two).\n\n"
        "**How to run it:** start straddling the middle cone in a "
        "3-point stance. Sprint 5 yards to one side and touch the line, "
        "change direction and sprint 10 yards to the far cone and touch "
        "it, then sprint back 5 yards through the middle cone to finish. "
        "Time starts on your first movement and stops when you cross "
        "the middle cone at the end.\n\n"
        "[Full protocol — Science for Sport](https://www.scienceforsport.com/pro-agility-5-10-5-test/) · "
        "[Video walkthrough](https://www.youtube.com/watch?v=tYhCJd7LaBU)"
    )
shuttle_time = st.sidebar.slider("5-10-5 Shuttle Time (seconds)", 4.0, 7.0, 4.8, 0.1)

with st.sidebar.expander("❓ How do I test max bench press reps?"):
    st.markdown(
        "**Setup:** standard barbell + 135 lbs loaded, bench with a "
        "spotter present. **Always use a spotter for this test.**\n\n"
        "**How to run it:** lie flat, grip the bar shoulder-width apart, "
        "lower it to your chest with control, then press to full elbow "
        "extension. That's 1 rep. Repeat with proper form until you "
        "can't complete another full rep — that count is your score.\n\n"
        "[Full protocol — Topend Sports](https://www.topendsports.com/testing/tests/max-bench-press.htm)"
    )
bench_reps = st.sidebar.slider("Max Bench Press Reps (135 lbs)", 0, 30, 12)

st.sidebar.subheader(f"{position}-Specific Technical Ratings")
st.sidebar.caption(
    "These change based on your selected position, since a striker's "
    "shot power and a center-back's tackling aren't measuring the same "
    "thing. More attributes will be added per position over time."
)

# Reset all technical inputs each run; only the branch matching the
# selected position actually gets set, everything else stays None and
# falls back to the position-average baseline further down.
finishing_in = shotpower_in = None
passing_in = ballcontrol_in = vision_in = None
standingtackle_in = slidingtackle_in = interceptions_in = physical_in = None
dribbling_in = longshots_in = positioning_in = headingaccuracy_in = None
curve_in = penalties_in = crossing_in = freekickaccuracy_in = None
composure_in = stamina_in = jumping_in = defensiveawareness_in = None

if position == "Forward":
    with st.sidebar.expander("❓ How do I rate my Finishing (Shot Accuracy)?"):
        st.markdown(
            "**Objective anchor:** take 10 shots at a goal (or a target "
            "on a wall) from 12-18 yards, varying angle and pace of "
            "service. Count how many go exactly where you intended, "
            "not just 'on target.'\n\n"
            "- **2-3/10 on target, poor placement control** → rate **30-45**\n"
            "- **4-6/10, decent placement but inconsistent under pressure** → rate **45-65**\n"
            "- **7-8/10, reliable placement, both feet usable** → rate **65-80**\n"
            "- **9-10/10 consistently, clinical under pressure/1st touch finishes** → rate **80+**"
        )
    finishing_in = st.sidebar.slider("Finishing (Shot Accuracy)", 30, 99, 68)

    with st.sidebar.expander("❓ How do I rate my Shot Power?"):
        st.markdown(
            "**Objective anchor — ball speed.** If you have access to a "
            "radar/speed gun app, real-world shot speeds break down "
            "roughly like this:\n\n"
            "- **Youth/U12: ~30-40 mph** → rate **30-45**\n"
            "- **Amateur/recreational adult: ~40-55 mph** → rate **45-60**\n"
            "- **Competitive club/high school: ~55-65 mph** → rate **60-70**\n"
            "- **Strong amateur/college level: ~65-70 mph** → rate **70-80**\n"
            "- **Professional average: ~70-80 mph** → rate **80-90**\n"
            "- **Elite pro / top strikers: 80mph+** → rate **90+**\n\n"
            "**No radar gun?** Rate how hard you're able to strike it "
            "while still keeping the shot on target — raw power that "
            "sends the ball wildly off target isn't useful power.\n\n"
            "[Shot speed research](https://www.frontiersin.org/journals/sports-and-active-living/articles/10.3389/fspor.2026.1766063/full) · "
            "[Pro vs. amateur benchmarks](https://stmichaelssoccer.com/rules-rocketing-shots-how-fast-are-soccer-shots/)"
        )
    shotpower_in = st.sidebar.slider("Shot Power", 30, 99, 68)

    with st.sidebar.expander("❓ How do I rate my Dribbling?"):
        st.markdown(
            "**Objective anchor — cone weave drill.** Set up 5-6 cones "
            "5 yards apart, weave through with both feet, staying tight.\n\n"
            "- **12-15+ sec, frequent loss of control** → rate **30-45**\n"
            "- **8-10 sec, occasional wide touches** → rate **45-60**\n"
            "- **Under 8 sec, tight touches, comfortable both feet** → rate **60-75**\n"
            "- **Fast, tight, beats real defenders 1v1 in games** → rate **75-90**\n\n"
            "[Cone drill benchmarks](https://goalnyx.com/soccer-cone-drills-for-ball-control/)"
        )
    dribbling_in = st.sidebar.slider("Dribbling", 30, 99, 68)

    with st.sidebar.expander("❓ How do I rate my Long Shots?"):
        st.markdown(
            "**Objective anchor:** take 10 shots from 25+ yards at a "
            "goal or wall target. Count how many stay on target (not "
            "just how many would be goals).\n\n"
            "- **0-2/10 on target** → rate **30-45**\n"
            "- **3-5/10 on target** → rate **45-65**\n"
            "- **6-8/10 on target, decent placement from distance** → rate **65-80**\n"
            "- **9-10/10, genuine threat from distance** → rate **80+**"
        )
    longshots_in = st.sidebar.slider("Long Shots", 30, 99, 60)

    with st.sidebar.expander("❓ How do I rate my Positioning?"):
        st.markdown(
            "Positioning is about *where you are before the ball "
            "arrives*, so it's hard to time-test — use this checklist "
            "from your last few games instead:\n\n"
            "- I regularly get goal-scoring chances without needing to dribble past multiple defenders first\n"
            "- I time my runs to beat the offside line rather than getting caught level or behind\n"
            "- Coaches/teammates say I find space well in the box\n"
            "- I get more shots per game than most attacking teammates\n"
            "- I react quickly to loose balls/rebounds in the box\n\n"
            "**0-1 true** → rate **30-50** · **2-3 true** → rate **50-70** · "
            "**4-5 true, consistently** → rate **70-90**"
        )
    positioning_in = st.sidebar.slider("Positioning", 30, 99, 65)

    with st.sidebar.expander("❓ How do I rate my Heading Accuracy?"):
        st.markdown(
            "**Objective anchor — aerial duel win rate.** Over a few "
            "games or crossing/heading drills, track contested headers "
            "won vs. attempted.\n\n"
            "- **Under 40% win rate** → rate **30-50**\n"
            "- **40-55% win rate** → rate **50-65**\n"
            "- **55-70% win rate** → rate **65-80**\n"
            "- **70%+ win rate (above pro top-flight average of ~66%)** → rate **80+**\n\n"
            "[Aerial duel benchmarks](https://www.athletepath.com/soccer-aerial-duel-calculator/)"
        )
    headingaccuracy_in = st.sidebar.slider("Heading Accuracy", 30, 99, 60)

    with st.sidebar.expander("❓ How do I rate my Curve?"):
        st.markdown(
            "**Objective anchor:** from the corner of the 18-yard box, "
            "try to bend 10 shots around an obstacle (a cone or bag "
            "placed between you and the goal) and on target.\n\n"
            "- **0-2/10 successfully bent on target** → rate **30-50**\n"
            "- **3-5/10** → rate **50-65**\n"
            "- **6-8/10, reliable curl on both power and placed shots** → rate **65-80**\n"
            "- **9-10/10, can consistently shape shots around a wall/defender** → rate **80+**"
        )
    curve_in = st.sidebar.slider("Curve", 30, 99, 55)

    with st.sidebar.expander("❓ How do I rate my Penalties?"):
        st.markdown(
            "**Objective anchor — conversion rate.** Track your last 10 "
            "penalty attempts (practice counts, but game penalties are "
            "more representative since nerves are part of the skill).\n\n"
            "- **Under 50% scored** → rate **30-50**\n"
            "- **50-65% scored** → rate **50-65**\n"
            "- **65-80% scored (near pro average of ~76-85% in regular play)** → rate **65-85**\n"
            "- **85%+ scored, consistently composed** → rate **85+**\n\n"
            "[Pro penalty conversion data](https://www.athletepath.com/soccer-penalty-conversion-calculator/)"
        )
    penalties_in = st.sidebar.slider("Penalties", 30, 99, 60)

    with st.sidebar.expander("❓ How do I rate my Crossing?"):
        st.markdown(
            "Mainly relevant if you play wide. **Objective anchor:** "
            "deliver 10 crosses from the flank into the box aimed at a "
            "target (cone, teammate, or marked zone).\n\n"
            "- **0-2/10 reach the target zone** → rate **30-50**\n"
            "- **3-5/10** → rate **50-65**\n"
            "- **6-8/10, consistent delivery, good pace on the ball** → rate **65-80**\n"
            "- **9-10/10, reliably picks out a specific target** → rate **80+**"
        )
    crossing_in = st.sidebar.slider("Crossing", 30, 99, 55)

elif position == "Midfielder":
    with st.sidebar.expander("❓ How do I rate my Passing Accuracy?"):
        st.markdown(
            "**Objective anchor — wall pass test.** Stand 5-8 yards from "
            "a flat wall, pass with the inside of your foot, control the "
            "rebound with one touch, pass again. Do 100 total attempts "
            "(50 per foot), count clean/accurate returns.\n\n"
            "- **Under 50/100 clean** → rate **30-45**\n"
            "- **50-70/100 clean** → rate **45-60**\n"
            "- **70-85/100 clean** → rate **60-75**\n"
            "- **85-95/100 clean, solid weak foot too** → rate **75-88**\n"
            "- **95+/100 clean, minimal foot difference** → rate **88+**\n\n"
            "**Context:** professional teams complete roughly **77-82%** "
            "of all passes in matches (with defensive pressure), and "
            "**90-95%** on simple ground passes. Since a wall drill has "
            "no defender, aim well above match-pressure rates to justify "
            "a top-tier score.\n\n"
            "[Wall pass benchmarks](https://www.ritfitsports.com/blogs/article/how-to-improve-soccer-passing) · "
            "[Pro passing accuracy data](https://www.sportmonks.com/glossary/passing-accuracy/)"
        )
    passing_in = st.sidebar.slider("Short Passing Accuracy", 30, 99, 72)

    with st.sidebar.expander("❓ How do I rate my Ball Control?"):
        st.markdown(
            "**Objective anchor — cone weave / juggling.** Weave a ball "
            "through 5-6 cones 5 yards apart using both feet, staying "
            "tight, OR count how many consecutive juggles you can do "
            "without the ball hitting the ground.\n\n"
            "- **10+ seconds through cones / under 10 juggles** → rate **30-45**\n"
            "- **8-10 sec / 10-20 juggles** → rate **45-60**\n"
            "- **Under 8 sec, tight touches / 20-50 juggles** → rate **60-75**\n"
            "- **Fast + tight, comfortable both feet / 50+ juggles** → rate **75-90**\n\n"
            "[Cone drill benchmarks](https://goalnyx.com/soccer-cone-drills-for-ball-control/)"
        )
    ballcontrol_in = st.sidebar.slider("Ball Control", 30, 99, 70)

    with st.sidebar.expander("❓ How do I rate my Vision?"):
        st.markdown(
            "Vision is harder to self-time, so use this self-assessment "
            "checklist instead — count how many describe you honestly:\n\n"
            "- I scan over my shoulder *before* receiving the ball, not after\n"
            "- I regularly spot a teammate in space that others miss\n"
            "- I can complete a first-time pass into a teammate's stride without looking twice\n"
            "- Coaches/teammates have specifically praised my passing choices, not just my technique\n"
            "- I rarely give the ball away because I passed into a bad situation\n\n"
            "**0-1 true** → rate **30-50** · **2-3 true** → rate **50-70** · "
            "**4 true** → rate **70-85** · **5 true, consistently** → rate **85+**\n\n"
            "[Scanning & passing vision research](https://www.mdpi.com/2673-7078/5/3/61)"
        )
    vision_in = st.sidebar.slider("Vision", 30, 99, 70)

    with st.sidebar.expander("❓ How do I rate my Dribbling?"):
        st.markdown(
            "**Objective anchor — cone weave drill.** Set up 5-6 cones "
            "5 yards apart, weave through with both feet, staying tight "
            "under simulated pressure.\n\n"
            "- **12-15+ sec, frequent loss of control** → rate **30-45**\n"
            "- **8-10 sec, occasional wide touches** → rate **45-60**\n"
            "- **Under 8 sec, tight touches, comfortable both feet** → rate **60-75**\n"
            "- **Fast, tight, retains possession under real pressure in games** → rate **75-90**\n\n"
            "[Cone drill benchmarks](https://goalnyx.com/soccer-cone-drills-for-ball-control/)"
        )
    dribbling_in = st.sidebar.slider("Dribbling", 30, 99, 65)

    with st.sidebar.expander("❓ How do I rate my Crossing?"):
        st.markdown(
            "**Objective anchor:** deliver 10 crosses/switches of play "
            "into the box or to a target zone from a wide or deep "
            "position.\n\n"
            "- **0-2/10 reach the target zone** → rate **30-50**\n"
            "- **3-5/10** → rate **50-65**\n"
            "- **6-8/10, consistent delivery** → rate **65-80**\n"
            "- **9-10/10, reliably picks out a specific target** → rate **80+**"
        )
    crossing_in = st.sidebar.slider("Crossing", 30, 99, 55)

    with st.sidebar.expander("❓ How do I rate my Curve?"):
        st.markdown(
            "**Objective anchor:** try to bend 10 long passes or shots "
            "around an obstacle placed between you and the target, "
            "landing on target.\n\n"
            "- **0-2/10 successfully bent on target** → rate **30-50**\n"
            "- **3-5/10** → rate **50-65**\n"
            "- **6-8/10, reliable curl on passes/shots** → rate **65-80**\n"
            "- **9-10/10, can consistently shape the ball around obstacles** → rate **80+**"
        )
    curve_in = st.sidebar.slider("Curve", 30, 99, 55)

    with st.sidebar.expander("❓ How do I rate my Free Kick Accuracy?"):
        st.markdown(
            "**Objective anchor:** take 10 direct free kicks from "
            "18-25 yards at a goal (use a wall of cones/bags to "
            "simulate a defensive wall if possible).\n\n"
            "- **0-2/10 on target** → rate **30-50**\n"
            "- **3-5/10** → rate **50-65**\n"
            "- **6-8/10, consistent placement over/around a wall** → rate **65-80**\n"
            "- **9-10/10, genuine set-piece threat** → rate **80+**"
        )
    freekickaccuracy_in = st.sidebar.slider("Free Kick Accuracy", 30, 99, 55)

    with st.sidebar.expander("❓ How do I rate my Composure?"):
        st.markdown(
            "Composure is decision-making quality under pressure — use "
            "this checklist honestly based on recent real games:\n\n"
            "- I take my first touch calmly even when closed down immediately\n"
            "- I rarely panic-clear or panic-pass under pressure\n"
            "- I can slow the game down when needed instead of always rushing\n"
            "- My decision quality doesn't drop late in games when tired\n"
            "- I stay level-headed after a mistake instead of it affecting my next few plays\n\n"
            "**0-1 true** → rate **30-50** · **2-3 true** → rate **50-70** · "
            "**4-5 true, consistently** → rate **70-90**"
        )
    composure_in = st.sidebar.slider("Composure", 30, 99, 65)

    with st.sidebar.expander("❓ How do I rate my Stamina?"):
        st.markdown(
            "**Objective anchor — beep test (multi-stage fitness "
            "test).** Run the standard 20m shuttle beep test and note "
            "the level you reach before you can no longer keep pace.\n\n"
            "- **Level 6-8** → rate **30-50**\n"
            "- **Level 9-10 (solid recreational/amateur fitness)** → rate **50-65**\n"
            "- **Level 11-13 (strong amateur/college level)** → rate **65-80**\n"
            "- **Level 14+ (elite outfield range; pro midfielders often "
            "score highest of any position)** → rate **80+**\n\n"
            "[Beep test standards by level](https://peakvo2trainer.com/blog/beep-test-soccer/) · "
            "[Age/position benchmarks](https://www.thebeeptest.com/sports/football)"
        )
    stamina_in = st.sidebar.slider("Stamina", 30, 99, 65)

    with st.sidebar.expander("❓ How do I rate my Long Shots?"):
        st.markdown(
            "**Objective anchor:** take 10 shots from 25+ yards at a "
            "goal or wall target, counting how many stay on target.\n\n"
            "- **0-2/10 on target** → rate **30-45**\n"
            "- **3-5/10 on target** → rate **45-65**\n"
            "- **6-8/10 on target** → rate **65-80**\n"
            "- **9-10/10, genuine threat from distance** → rate **80+**"
        )
    longshots_in = st.sidebar.slider("Long Shots", 30, 99, 55)

elif position == "Defender":
    with st.sidebar.expander("❓ How do I rate my Standing Tackle?"):
        st.markdown(
            "**Objective anchor — tackle success rate.** Over your next "
            "few practice games or 1v1 defending drills, track: "
            "attempted standing tackles vs. tackles won cleanly (no foul, "
            "ball recovered).\n\n"
            "- **Under 40% win rate** → rate **30-50**\n"
            "- **40-55% win rate** → rate **50-65**\n"
            "- **55-70% win rate** → rate **65-80**\n"
            "- **70%+ win rate (matches pro top-flight average)** → rate **80+**\n\n"
            "Pros in top leagues average roughly **60-65% tackle success**, "
            "with **70%+ considered excellent** — use that as your ceiling "
            "reference, not your floor.\n\n"
            "[Tackle success benchmarks](https://www.athletepath.com/soccer-tackle-success-rate-calculator/)"
        )
    standingtackle_in = st.sidebar.slider("Standing Tackle", 30, 99, 70)

    with st.sidebar.expander("❓ How do I rate my Sliding Tackle?"):
        st.markdown(
            "Same logic as standing tackle, but specifically for slide "
            "challenges: track attempted slide tackles vs. clean wins "
            "(ball won, no foul, you recover quickly afterward).\n\n"
            "- **Frequently mistimed/fouls** → rate **30-50**\n"
            "- **Sometimes clean, sometimes late** → rate **50-65**\n"
            "- **Mostly clean and well-timed** → rate **65-80**\n"
            "- **Consistently clean, good recovery afterward** → rate **80+**\n\n"
            "Note: many modern top defenders intentionally slide-tackle "
            "*less* than older generations (higher foul/injury risk), so "
            "don't assume a low attempt count means a low rating — "
            "judge purely on success rate when you do commit."
        )
    slidingtackle_in = st.sidebar.slider("Sliding Tackle", 30, 99, 65)

    with st.sidebar.expander("❓ How do I rate my Interceptions?"):
        st.markdown(
            "Track how often you read a pass and step in front of it "
            "*before* it reaches its target, across a few games.\n\n"
            "- **Rarely anticipate passes** → rate **30-50**\n"
            "- **Occasionally read the play, 1-2 real interceptions per game** → rate **50-70**\n"
            "- **Regularly reading passing lanes, 2-3+ per game** → rate **70-85**\n"
            "- **Elite anticipation, routinely cuts out attacks before they develop** → rate **85+**\n\n"
            "Professional defenders average roughly **1-3 interceptions "
            "per match** as a baseline reference.\n\n"
            "[Defender metric benchmarks](https://thepfsa.co.uk/10-essential-football-metrics-you-should-know/)"
        )
    interceptions_in = st.sidebar.slider("Interceptions", 30, 99, 68)

    with st.sidebar.expander("❓ How do I rate my Physicality?"):
        st.markdown(
            "This combines your strength (reuse your bench press result "
            "above) with aggression/duel-winning — how you fare in "
            "physical, shoulder-to-shoulder and aerial contests.\n\n"
            "- **Consistently loses physical duels/out-muscled** → rate **30-50**\n"
            "- **Competitive but inconsistent in duels** → rate **50-70**\n"
            "- **Wins most 50/50s and aerial duels** → rate **70-85**\n"
            "- **Dominant physically, rarely beaten in a duel** → rate **85+**"
        )
    physical_in = st.sidebar.slider("Physical / Duel Strength", 30, 99, 68)

    with st.sidebar.expander("❓ How do I rate my Defensive Awareness?"):
        st.markdown(
            "This is about positioning and reading the game rather than "
            "any single physical action — use this checklist from "
            "recent real games:\n\n"
            "- I rarely get caught out of position or beaten for pace on the last line\n"
            "- I recognize danger and adjust my position before the ball arrives, not after\n"
            "- I communicate and organize teammates around me\n"
            "- I rarely commit to a challenge I don't need to make\n"
            "- Coaches trust me in high-pressure defensive moments\n\n"
            "**0-1 true** → rate **30-50** · **2-3 true** → rate **50-70** · "
            "**4-5 true, consistently** → rate **70-90**"
        )
    defensiveawareness_in = st.sidebar.slider("Defensive Awareness", 30, 99, 68)

    with st.sidebar.expander("❓ How do I rate my Heading Accuracy?"):
        st.markdown(
            "**Objective anchor — aerial duel win rate.** Over a few "
            "games or set-piece defending drills, track contested "
            "headers won vs. attempted (both defending crosses and "
            "clearing set pieces).\n\n"
            "- **Under 40% win rate** → rate **30-50**\n"
            "- **40-55% win rate** → rate **50-65**\n"
            "- **55-70% win rate** → rate **65-80**\n"
            "- **70%+ win rate (above pro top-flight average of ~66%)** → rate **80+**\n\n"
            "[Aerial duel benchmarks](https://www.athletepath.com/soccer-aerial-duel-calculator/)"
        )
    headingaccuracy_in = st.sidebar.slider("Heading Accuracy", 30, 99, 65)

    with st.sidebar.expander("❓ How do I rate my Jumping?"):
        st.markdown(
            "**Objective anchor — standing vertical jump.** Stand flat "
            "next to a wall, mark your standing reach, jump straight up "
            "and mark your peak reach. The difference is your vertical "
            "jump.\n\n"
            "- **Under 14 inches** → rate **30-50**\n"
            "- **14-18 inches (average adult male range)** → rate **50-65**\n"
            "- **18-24 inches (good athletic level)** → rate **65-80**\n"
            "- **24+ inches (strong athletic level for a field-sport athlete)** → rate **80+**\n\n"
            "[Vertical jump norms](https://www.topendsports.com/testing/norms/vertical-jump.htm)"
        )
    jumping_in = st.sidebar.slider("Jumping", 30, 99, 60)

    with st.sidebar.expander("❓ How do I rate my Composure?"):
        st.markdown(
            "For a defender, composure mostly shows up in how you "
            "handle pressure near your own goal — use this checklist:\n\n"
            "- I can take a calm first touch under pressure in my own box\n"
            "- I don't panic-clear the ball when I have time to play out\n"
            "- A mistake doesn't rattle my next few defensive actions\n"
            "- I stay calm and communicate even when the team is under sustained pressure\n"
            "- I make good decisions in the last few minutes of close games\n\n"
            "**0-1 true** → rate **30-50** · **2-3 true** → rate **50-70** · "
            "**4-5 true, consistently** → rate **70-90**"
        )
    composure_in = st.sidebar.slider("Composure", 30, 99, 65)

    with st.sidebar.expander("❓ How do I rate my Build-Up Passing?"):
        st.markdown(
            "Modern defenders are expected to play out from the back, "
            "not just clear the ball. **Objective anchor — wall pass "
            "test:** 100 total attempts (50 per foot) against a wall, "
            "count clean returns, same as a midfielder's passing test.\n\n"
            "- **Under 50/100 clean** → rate **30-45**\n"
            "- **50-70/100 clean** → rate **45-60**\n"
            "- **70-85/100 clean** → rate **60-75**\n"
            "- **85+/100 clean, comfortable playing out under pressure** → rate **75+**\n\n"
            "[Wall pass benchmarks](https://www.ritfitsports.com/blogs/article/how-to-improve-soccer-passing)"
        )
    passing_in = st.sidebar.slider("Build-Up Passing", 30, 99, 60)

else:
    st.sidebar.info("Select a position above to see position-specific technical ratings.")

# Start every feature at the position-specific baseline mean (not the whole
# population), so attributes we don't directly test still reflect a realistic
# player at that position rather than a generic average.
position_map = {"Forward": "ST", "Midfielder": "CM", "Defender": "CB"}
df_position = df_baseline[df_baseline.get("position", pd.Series(dtype=str)) == position_map.get(position, "")]
if df_position.empty:
    df_position = df_baseline  # fallback if position labels don't match the DB

input_dict = {col: float(df_position[col].mean()) for col in feature_cols}


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


# --- Profile inputs -> feature columns ------------------------------------
# Note: "age" isn't in feature_columns.json, so the trained model has no
# slot for it. We still collect it for display/context, but it can't
# influence the prediction unless the model gets retrained with age added
# to its feature set.
if 'height' in input_dict:
    input_dict['height'] = float(height_in)
if 'weight' in input_dict:
    input_dict['weight'] = float(weight_in)
if 'weakfootability' in input_dict:
    input_dict['weakfootability'] = float(weakfoot_in)
if 'skillmoves' in input_dict:
    input_dict['skillmoves'] = float(skillmoves_in)

# --- Physical test inputs -> feature columns -----------------------------
# 30m sprint: elite ~3.5s, recreational ~6.0s
sprint_rating = rating_from_time(sprint_time, best_time=3.5, worst_time=6.0)
# 5-10-5 shuttle: elite ~4.0s, recreational ~7.0s (agility/change of direction)
shuttle_rating = rating_from_time(shuttle_time, best_time=4.0, worst_time=7.0)
# Bench press reps at 135lbs: 0-30 reps mapped to strength
strength_rating = rating_from_reps(bench_reps, min_reps=0, max_reps=30)

for col in ("acceleration", "sprintspeed"):
    if col in input_dict:
        input_dict[col] = sprint_rating
for col in ("agility", "balance", "reactions"):
    if col in input_dict:
        input_dict[col] = shuttle_rating
for col in ("strength",):
    if col in input_dict:
        input_dict[col] = strength_rating

# --- Technical rating inputs -> feature columns ---------------------------
# Only override attributes actually shown for the selected position; every
# other attribute stays at the position-average baseline set above.
if finishing_in is not None and 'finishing' in input_dict:
    input_dict['finishing'] = float(finishing_in)
if shotpower_in is not None:
    for col in ('shotpower', 'volleys'):
        if col in input_dict:
            input_dict[col] = float(shotpower_in)

if passing_in is not None:
    for col in ('shortpassing', 'longpassing'):
        if col in input_dict:
            input_dict[col] = float(passing_in)
if ballcontrol_in is not None and 'ballcontrol' in input_dict:
    input_dict['ballcontrol'] = float(ballcontrol_in)
if vision_in is not None and 'vision' in input_dict:
    input_dict['vision'] = float(vision_in)

if standingtackle_in is not None and 'standingtackle' in input_dict:
    input_dict['standingtackle'] = float(standingtackle_in)
if slidingtackle_in is not None and 'slidingtackle' in input_dict:
    input_dict['slidingtackle'] = float(slidingtackle_in)
if interceptions_in is not None and 'interceptions' in input_dict:
    input_dict['interceptions'] = float(interceptions_in)
if physical_in is not None:
    for col in ('strength', 'aggression'):
        if col in input_dict:
            input_dict[col] = float(physical_in)

if dribbling_in is not None and 'dribbling' in input_dict:
    input_dict['dribbling'] = float(dribbling_in)
if longshots_in is not None and 'longshots' in input_dict:
    input_dict['longshots'] = float(longshots_in)
if positioning_in is not None and 'positioning' in input_dict:
    input_dict['positioning'] = float(positioning_in)
if headingaccuracy_in is not None and 'headingaccuracy' in input_dict:
    input_dict['headingaccuracy'] = float(headingaccuracy_in)
if curve_in is not None and 'curve' in input_dict:
    input_dict['curve'] = float(curve_in)
if penalties_in is not None and 'penalties' in input_dict:
    input_dict['penalties'] = float(penalties_in)
if crossing_in is not None and 'crossing' in input_dict:
    input_dict['crossing'] = float(crossing_in)
if freekickaccuracy_in is not None and 'freekickaccuracy' in input_dict:
    input_dict['freekickaccuracy'] = float(freekickaccuracy_in)
if composure_in is not None and 'composure' in input_dict:
    input_dict['composure'] = float(composure_in)
if stamina_in is not None and 'stamina' in input_dict:
    input_dict['stamina'] = float(stamina_in)
if jumping_in is not None and 'jumping' in input_dict:
    input_dict['jumping'] = float(jumping_in)
if defensiveawareness_in is not None and 'defensiveawareness' in input_dict:
    input_dict['defensiveawareness'] = float(defensiveawareness_in)

# --- Recompute the aggregate category columns so they stay consistent with
#     the detail columns we just changed above (these composites exist in
#     the EA-style schema and should never contradict their sub-attributes).
composite_sources = {
    "pac": ["acceleration", "sprintspeed"],
    "dri": ["dribbling", "ballcontrol", "agility", "balance"],
    "pas": ["shortpassing", "longpassing", "vision"],
    "sho": ["finishing", "shotpower", "volleys", "longshots", "penalties"],
    "def": ["standingtackle", "slidingtackle", "interceptions", "defensiveawareness"],
    "phy": ["strength", "stamina", "aggression", "jumping"],
}
for composite_col, source_cols in composite_sources.items():
    present_sources = [c for c in source_cols if c in input_dict]
    if composite_col in input_dict and present_sources:
        input_dict[composite_col] = float(np.mean([input_dict[c] for c in present_sources]))

input_df = pd.DataFrame([input_dict])[feature_cols]

# Model Prediction
predicted_rating = float(model.predict(input_df)[0])

# Dashboard View
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Player Name", player_name)
    st.metric("Position", position)
    st.metric("Age", age_in)

with col2:
    st.metric("Predicted Talent Rating", f"{predicted_rating:.1f} / 99")

with col3:
    st.metric("Calculated Pace Rating", f"{input_dict.get('pac', sprint_rating):.1f}")

st.divider()
st.write(f"### Your Standing vs. Pro {position}s (Z-Score Comparison)")
st.caption(
    "A Z-score shows how many standard deviations above or below the "
    "position average you fall. 0 = exactly average for the position, "
    "+1 = one std. dev. above average, -1 = one std. dev. below."
)

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

zscore_rows = []
for label, (col, user_value) in zscore_features.items():
    if col not in df_position.columns or user_value is None:
        continue
    pos_mean = df_position[col].mean()
    pos_std = df_position[col].std()
    z = (user_value - pos_mean) / pos_std if pos_std > 0 else 0.0
    zscore_rows.append({"Attribute": label, "Your Value": round(user_value, 1), "Position Avg": round(pos_mean, 1), "Z-Score": round(z, 2)})

zscore_df = pd.DataFrame(zscore_rows).set_index("Attribute")
col_z1, col_z2 = st.columns([2, 1])
with col_z1:
    st.bar_chart(zscore_df["Z-Score"])
with col_z2:
    st.dataframe(zscore_df)

st.divider()
st.write("### Benchmark Comparison Against 16,228 Professional Records")

col_a, col_b = st.columns(2)
with col_a:
    st.write("**Database Overall Rating Distribution**")
    st.bar_chart(df_baseline['overallrating'].value_counts().sort_index())

with col_b:
    st.write(f"**{position} Position Baselines (n={len(df_position)})**")
    st.dataframe(df_position[['overallrating', 'height', 'weight']].describe().T[['mean', 'std', 'min', 'max']])
