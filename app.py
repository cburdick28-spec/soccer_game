"""
app.py  —  ⚽ Soccer Career Guesser  (Advanced Edition)
Five game modes:
  1. Career Timeline  – reveal clubs one-by-one and guess the footballer
  2. Footballer Guesser – Wordle-style 9-attribute feedback grid
  3. Trophy Cabinet – reveal trophies one-by-one and guess the footballer
  4. Daily Challenge – same mystery player for everyone, seeded by today's date
  5. Statistics & Achievements
"""

import random
import datetime
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from game_data import (
    PLAYERS, LEAGUES, POSITIONS, ERAS, CONTINENTS, LEAGUE_COLOURS, FLAGS,
    ATTRIBUTE_LABELS, filter_players, pick_random_player,
    score_for_guess, all_player_names, compare_players, get_top_league, get_meta,
)

# ──────────────────────────────────────────────────────────────────────────────
# Page config
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Soccer Career Guesser",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────────
# Custom CSS
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0d1b2a 0%, #1b2838 60%, #0d2137 100%); }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a1628 0%, #112240 100%) !important;
        border-right: 2px solid #1db954;
    }
    section[data-testid="stSidebar"] * { color: #e0e0e0 !important; }

    .career-card {
        background: rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 14px 20px;
        margin: 8px 0;
        border-left: 5px solid #1db954;
        transition: transform 0.15s;
    }
    .career-card:hover { transform: translateX(4px); }
    .career-card .club-name { font-size: 1.25rem; font-weight: 700; color: #ffffff; }
    .career-card .club-detail { font-size: 0.9rem; color: #aab8c2; }

    .trophy-card {
        background: rgba(255,215,0,0.08);
        border-radius: 12px;
        padding: 14px 20px;
        margin: 8px 0;
        border-left: 5px solid gold;
        font-size: 1.1rem;
        color: #ffd700;
    }

    .score-box {
        text-align: center;
        background: rgba(29,185,84,0.15);
        border: 2px solid #1db954;
        border-radius: 14px;
        padding: 16px;
        margin: 6px 0;
    }
    .score-box .score-val { font-size: 2rem; font-weight: 800; color: #1db954; }
    .score-box .score-lbl { font-size: 0.8rem; color: #aaa; text-transform: uppercase; letter-spacing: 1px; }

    .daily-box {
        text-align: center;
        background: linear-gradient(135deg, rgba(255,165,0,0.15), rgba(255,100,0,0.1));
        border: 2px solid #ff8c00;
        border-radius: 14px;
        padding: 16px;
        margin: 6px 0;
    }
    .daily-box .score-val { font-size: 2rem; font-weight: 800; color: #ff8c00; }
    .daily-box .score-lbl { font-size: 0.8rem; color: #aaa; text-transform: uppercase; letter-spacing: 1px; }

    .result-correct {
        background: linear-gradient(90deg, #155724, #1db954);
        color: white; border-radius: 12px; padding: 18px; text-align: center;
        font-size: 1.4rem; font-weight: 700; margin: 12px 0;
    }
    .result-wrong {
        background: linear-gradient(90deg, #721c24, #e74c3c);
        color: white; border-radius: 12px; padding: 18px; text-align: center;
        font-size: 1.4rem; font-weight: 700; margin: 12px 0;
    }

    .hint-box {
        background: rgba(255,193,7,0.12);
        border: 1px solid #ffc107;
        border-radius: 10px;
        padding: 10px 16px;
        margin: 6px 0;
        color: #ffc107;
        font-size: 0.95rem;
    }

    .attr-row { display: flex; gap: 6px; margin: 5px 0; align-items: center; }
    .attr-label {
        width: 120px; color: #aab8c2; font-size: 0.78rem; font-weight: 600;
        text-transform: uppercase; letter-spacing: 0.5px; flex-shrink: 0;
    }
    .attr-cell {
        flex: 1; border-radius: 8px; padding: 8px 10px;
        font-size: 0.82rem; font-weight: 600; text-align: center;
        color: white; min-width: 70px;
    }
    .cell-correct  { background: #1a7a40; border: 2px solid #1db954; }
    .cell-close    { background: #856404; border: 2px solid #ffc107; }
    .cell-wrong    { background: #5a2d2d; border: 2px solid #e74c3c; }
    .cell-header   { background: rgba(255,255,255,0.08); border: 2px solid #444; color: #ccc; }

    .trophy-chip {
        display: inline-block;
        background: rgba(255,215,0,0.15);
        border: 1px solid gold;
        border-radius: 20px;
        padding: 4px 12px;
        margin: 3px;
        font-size: 0.78rem;
        color: #ffd700;
    }

    .achievement-card {
        background: rgba(255,215,0,0.08);
        border: 1px solid rgba(255,215,0,0.3);
        border-radius: 12px;
        padding: 12px 16px;
        margin: 6px 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .achievement-locked {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 12px 16px;
        margin: 6px 0;
        opacity: 0.5;
    }

    div[data-testid="stTabs"] button {
        font-weight: 700; font-size: 0.95rem;
        background: transparent !important;
        border-bottom: 3px solid transparent !important;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        border-bottom-color: #1db954 !important;
        color: #1db954 !important;
    }

    h1, h2, h3, h4, h5, h6 { color: #ffffff !important; }
    p, li, label, .stMarkdown { color: #e0e0e0 !important; }

    .stButton > button {
        background: linear-gradient(90deg, #1db954, #17a649);
        color: white; border: none; border-radius: 8px;
        font-weight: 700; padding: 10px 24px; font-size: 1rem;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #17a649, #148f3e);
        transform: translateY(-1px); box-shadow: 0 4px 15px rgba(29,185,84,0.4);
    }

    .stTextInput > div > div > input, .stSelectbox > div > div {
        background: rgba(255,255,255,0.08) !important;
        color: white !important; border-color: #333 !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# Session state helpers
# ──────────────────────────────────────────────────────────────────────────────
DEFAULTS = {
    # Career mode
    "career_player":       None,
    "career_revealed":     0,
    "career_guesses":      [],
    "career_won":          False,
    "career_gave_up":      False,
    "career_input_key":    0,
    "career_hints_used":   [],   # list of hint keys used this round
    "career_hint_penalty": 0,    # points deducted for hints
    # Footballer guesser mode
    "fg_player":           None,
    "fg_guesses":          [],
    "fg_won":              False,
    "fg_gave_up":          False,
    "fg_input_key":        100,
    # Trophy Cabinet mode
    "tc_player":           None,
    "tc_revealed":         0,
    "tc_guesses":          [],
    "tc_won":              False,
    "tc_gave_up":          False,
    "tc_input_key":        200,
    # Daily Challenge
    "daily_date":          None,
    "daily_player":        None,
    "daily_mode":          "Career",
    "daily_revealed":      0,
    "daily_guesses":       [],
    "daily_fg_guesses":    [],
    "daily_won":           False,
    "daily_gave_up":       False,
    "daily_score":         None,
    "daily_input_key":     300,
    "daily_streak":        0,
    "best_daily_streak":   0,
    "last_daily_won_date": None,
    # Global scores
    "total_score":         0,
    "rounds_played":       0,
    "win_streak":          0,
    "best_streak":         0,
    "history":             [],
    # Filters
    "filter_position":     "All Positions",
    "filter_league":       "All Leagues",
    "filter_era":          "All Eras",
    "filter_difficulty":   "All",
    "filter_continent":    "All Continents",
    "filter_world_cup":    "All",
    # AI Career Simulator
    "openai_api_key":      "",
    "ai_player":           None,   # {name, nationality, position_group, style}
    "ai_stage_idx":        -1,     # -1=not started, 0-4=stage, 5=ended
    "ai_awaiting_outcome": False,  # True=user chose, showing outcome; False=showing choices
    "ai_chosen_option":    None,   # 0 or 1
    "ai_narrative":        "",
    "ai_choices":          [],     # [(text, stat_delta), (text, stat_delta)]
    "ai_outcome_text":     "",
    "ai_stats":            {"goals": 0, "assists": 0, "trophies": 0, "caps": 0},
    "ai_history":          [],     # list of {stage, choice, outcome, delta}
}

for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Daily challenge — refresh if date changed ─────────────────────────────
today = datetime.date.today()
if st.session_state.daily_date != str(today):
    rng = random.Random(today.toordinal())
    st.session_state.daily_player      = rng.choice(PLAYERS)
    st.session_state.daily_date        = str(today)
    st.session_state.daily_revealed    = 0
    st.session_state.daily_guesses     = []
    st.session_state.daily_fg_guesses  = []
    st.session_state.daily_won         = False
    st.session_state.daily_gave_up     = False
    st.session_state.daily_score       = None
    st.session_state.daily_input_key  += 1

def reset_career(player):
    st.session_state.career_player       = player
    st.session_state.career_revealed     = 0
    st.session_state.career_guesses      = []
    st.session_state.career_won          = False
    st.session_state.career_gave_up      = False
    st.session_state.career_input_key   += 1
    st.session_state.career_hints_used   = []
    st.session_state.career_hint_penalty = 0

def reset_fg(player):
    st.session_state.fg_player    = player
    st.session_state.fg_guesses   = []
    st.session_state.fg_won       = False
    st.session_state.fg_gave_up   = False
    st.session_state.fg_input_key += 1

def reset_tc(player):
    st.session_state.tc_player    = player
    st.session_state.tc_revealed  = 0
    st.session_state.tc_guesses   = []
    st.session_state.tc_won       = False
    st.session_state.tc_gave_up   = False
    st.session_state.tc_input_key += 1

def get_filtered():
    return filter_players(
        position_group   = st.session_state.filter_position,
        league_filter    = st.session_state.filter_league,
        era_filter       = st.session_state.filter_era,
        difficulty       = st.session_state.filter_difficulty,
        continent_filter = st.session_state.filter_continent,
        world_cup_filter = st.session_state.filter_world_cup,
    )

# ──────────────────────────────────────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚽ Soccer Career Guesser")
    st.markdown("*Advanced Edition*")
    st.markdown("---")

    st.markdown("### 🏅 Score")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="score-box"><div class="score-val">{st.session_state.total_score}</div><div class="score-lbl">Points</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="score-box"><div class="score-val">{st.session_state.rounds_played}</div><div class="score-lbl">Played</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="score-box"><div class="score-val">{st.session_state.win_streak}🔥</div><div class="score-lbl">Streak</div></div>""", unsafe_allow_html=True)

    daily_streak = st.session_state.daily_streak
    st.markdown(f"""<div class="daily-box"><div class="score-val">📅 {daily_streak}</div><div class="score-lbl">Daily Streak</div></div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔍 Filters")

    pos_options = ["All Positions"] + list(POSITIONS.keys())
    st.session_state.filter_position = st.selectbox(
        "Position", pos_options,
        index=pos_options.index(st.session_state.filter_position)
    )
    league_options = LEAGUES
    st.session_state.filter_league = st.selectbox(
        "League", league_options,
        index=league_options.index(st.session_state.filter_league)
    )
    era_options = list(ERAS.keys())
    st.session_state.filter_era = st.selectbox(
        "Era", era_options,
        index=era_options.index(st.session_state.filter_era)
    )
    diff_options = ["All", "Easy", "Medium", "Hard"]
    st.session_state.filter_difficulty = st.selectbox(
        "Difficulty", diff_options,
        index=diff_options.index(st.session_state.filter_difficulty)
    )
    cont_options = CONTINENTS
    st.session_state.filter_continent = st.selectbox(
        "Continent", cont_options,
        index=cont_options.index(st.session_state.filter_continent)
    )
    wc_options = ["All", "Yes", "No"]
    st.session_state.filter_world_cup = st.selectbox(
        "World Cup Winner", wc_options,
        index=wc_options.index(st.session_state.filter_world_cup)
    )

    pool = get_filtered()
    st.caption(f"🎮 {len(pool)} players in pool")

    st.markdown("---")
    st.markdown("### 📜 Recent History")
    if st.session_state.history:
        for h in reversed(st.session_state.history[-5:]):
            icon = "✅" if h["won"] else "❌"
            mode_icon = {"Career": "🏟️", "Guesser": "🟩", "Trophy": "🏆", "Daily": "📅"}.get(h["mode"], "🎮")
            st.markdown(f"**{icon}{mode_icon} {h['name']}** — {h.get('points',0)} pts")
    else:
        st.caption("No rounds played yet")

    st.markdown("---")
    st.markdown("### 📖 How to Play")
    with st.expander("Career Timeline"):
        st.markdown("""
- Clubs revealed one by one  
- Guess sooner = more points (max 1000)
- 5 wrong guesses allowed
- Use 💡 hints (costs points)
""")
    with st.expander("Footballer Guesser"):
        st.markdown("""
- Type a footballer's name  
- 🟩 Correct &nbsp; 🟨 Close &nbsp; 🟥 Wrong  
- 9 attributes compared  
- Unlimited guesses  
""")
    with st.expander("Trophy Cabinet"):
        st.markdown("""
- Trophies revealed one by one  
- Guess from the honours list  
- 5 wrong guesses allowed  
""")
    with st.expander("Daily Challenge"):
        st.markdown("""
- Same mystery player every day  
- Career or Guesser mode  
- Build your daily streak!  
""")

    st.markdown("---")
    st.markdown("### 🤖 AI Career Sim")
    ai_key = st.text_input(
        "OpenAI API Key (optional)",
        type="password",
        key="sidebar_openai_key",
        placeholder="sk-... (enables AI narratives)",
        help="Provide your OpenAI API key to generate personalised AI narratives. Without a key the simulator uses built-in story templates.",
    )
    if ai_key:
        st.session_state.openai_api_key = ai_key
    if st.session_state.openai_api_key:
        st.caption("✅ AI narratives enabled")

# ──────────────────────────────────────────────────────────────────────────────
# Main area — title
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("<h1 style='text-align:center;font-size:2.6rem'>⚽ Soccer Career Guesser</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#aaa;font-size:1rem'>91 legendary footballers · 6 game modes · AI-powered career simulation</p>", unsafe_allow_html=True)
st.markdown("---")

tab_career, tab_fg, tab_tc, tab_daily, tab_stats, tab_ai = st.tabs([
    "🏟️ Career Timeline",
    "🟩 Footballer Guesser",
    "🏆 Trophy Cabinet",
    "📅 Daily Challenge",
    "📊 Stats & Achievements",
    "🤖 AI Career Sim",
])

# ─────────────────── helpers ──────────────────────────────────────────────────
EMOJI_MAP = {"correct": "🟩", "close": "🟨", "wrong": "🟥"}
CSS_MAP    = {"correct": "cell-correct", "close": "cell-close", "wrong": "cell-wrong"}
name_to_player = {p["name"]: p for p in PLAYERS}
attr_keys = list(ATTRIBUTE_LABELS.keys())

def _attr_value(player: dict, key: str) -> str:
    if key == "nationality":    return player["nationality"]
    if key == "continent":      return get_meta(player, "continent", "?")
    if key == "position_group": return player["position_group"]
    if key == "league":         return get_top_league(player)
    if key == "age":
        age = 2026 - player["birth_year"]
        if age < 23:   return "Under 23"
        elif age < 28: return "23-27"
        elif age < 33: return "28-32"
        elif age < 38: return "33-37"
        else:           return "38+"
    if key == "current_club":      return player.get("current_club", "?")
    if key == "ballon_dor_winner": return "Yes" if (player.get("ballon_dor",0) or 0) > 0 else "No"
    if key == "world_cup_winner":  return "Yes" if get_meta(player, "world_cup_winner", False) else "No"
    if key == "peak_club":         return get_meta(player, "peak_club", "?")
    return "?"

def render_fg_header():
    header_cells = "".join(
        f'<div class="attr-cell cell-header">{ATTRIBUTE_LABELS[k]}</div>'
        for k in attr_keys
    )
    st.markdown(
        f'<div class="attr-row"><div class="attr-label">Player</div>{header_cells}</div>',
        unsafe_allow_html=True
    )

def render_fg_row(guess_name: str, cmp: dict):
    gp = name_to_player.get(guess_name)
    if gp is None:
        return
    cells = "".join(
        f'<div class="attr-cell {CSS_MAP[cmp[k]]}">'
        f'{EMOJI_MAP[cmp[k]]} {_attr_value(gp, k)}</div>'
        for k in attr_keys
    )
    st.markdown(
        f'<div class="attr-row"><div class="attr-label" style="color:#fff;font-weight:700">{guess_name}</div>{cells}</div>',
        unsafe_allow_html=True
    )

def render_career_chart(player: dict):
    rows = []
    for e in player["career"]:
        rows.append({"Club": e["club"], "League": e["league"],
                     "Start": e["start"], "End": e["end"] or 2026})
    df = pd.DataFrame(rows)
    if df.empty:
        return
    fig = px.timeline(
        df, x_start="Start", x_end="End",
        y="Club", color="League",
        title=f"{player['name']} — Career Timeline",
        color_discrete_map=LEAGUE_COLOURS,
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="white", height=max(300, len(rows)*40),
        margin=dict(l=10, r=10, t=40, b=10), showlegend=False,
    )
    fig.update_xaxes(type="linear", tickformat="d",
                     showgrid=True, gridcolor="rgba(255,255,255,0.1)")
    fig.update_yaxes(showgrid=False)
    st.plotly_chart(fig, use_container_width=True)

def render_player_profile(player: dict):
    flag = FLAGS.get(player["nationality"], "🌍")
    col_info, col_chart = st.columns([1, 1])
    with col_info:
        st.markdown(f"**Nationality:** {flag} {player['nationality']}")
        st.markdown(f"**Position:** {player['position']} ({player['position_group']})")
        st.markdown(f"**Born:** {player['birth_year']}")
        st.markdown(f"**Continent:** {get_meta(player, 'continent', '?')}")
        st.markdown(f"**World Cup Winner:** {'✅ Yes' if get_meta(player, 'world_cup_winner', False) else '❌ No'}")
        st.markdown(f"**Peak Club:** {get_meta(player, 'peak_club', '?')}")
        st.markdown(f"**Main League:** {get_top_league(player)}")
        bd = player.get("ballon_dor", 0) or 0
        if bd > 0:
            st.markdown(f"**Ballon d'Or:** {'🏆 ' * bd}({bd})")
        st.markdown("**Honours:**")
        for t in player["trophies"]:
            st.markdown(f'<span class="trophy-chip">🏆 {t}</span>', unsafe_allow_html=True)
    with col_chart:
        render_career_chart(player)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — CAREER TIMELINE
# ══════════════════════════════════════════════════════════════════════════════
with tab_career:
    pool = get_filtered()
    cp = st.session_state.career_player

    col_btn, col_hint_btn = st.columns([1, 3])
    with col_btn:
        if st.button("🎲 New Player", key="new_career"):
            if pool:
                reset_career(pick_random_player(pool))
            else:
                st.warning("No players match the current filters.")

    if cp is None:
        st.info("👈 Click **New Player** to start!")
    else:

        career   = cp["career"]
        revealed = st.session_state.career_revealed
        won      = st.session_state.career_won
        gave_up  = st.session_state.career_gave_up
        wrong_guesses = [g for g in st.session_state.career_guesses if g != cp["name"]]

        # ── Metrics bar ──────────────────────────────────────────────────────────
        c1, c2, c3, c4 = st.columns(4)
        base_pts = score_for_guess(revealed, len(career))
        penalty  = st.session_state.career_hint_penalty
        with c1:
            st.metric("Clubs Revealed", f"{revealed} / {len(career)}")
        with c2:
            st.metric("Points if correct now", f"⭐ {max(0, base_pts - penalty)}")
        with c3:
            st.metric("Wrong Guesses", f"{len(wrong_guesses)} / 5")
        with c4:
            st.metric("Position Group", cp["position_group"])

        # ── Hints section ─────────────────────────────────────────────────────────
        if not won and not gave_up:
            hints_used = st.session_state.career_hints_used
            with st.expander("💡 Hints  (each costs points from your score)"):
                h1, h2, h3 = st.columns(3)
                with h1:
                    if "nationality" not in hints_used:
                        if st.button("🌍 Nationality (-100 pts)", key="hint_nat"):
                            st.session_state.career_hints_used.append("nationality")
                            st.session_state.career_hint_penalty += 100
                            st.rerun()
                    else:
                        flag = FLAGS.get(cp["nationality"], "🌍")
                        st.markdown(f'<div class="hint-box">🌍 {flag} {cp["nationality"]}</div>', unsafe_allow_html=True)
                with h2:
                    if "continent" not in hints_used:
                        if st.button("🗺️ Continent (-75 pts)", key="hint_cont"):
                            st.session_state.career_hints_used.append("continent")
                            st.session_state.career_hint_penalty += 75
                            st.rerun()
                    else:
                        st.markdown(f'<div class="hint-box">🗺️ {get_meta(cp, "continent", "?")}</div>', unsafe_allow_html=True)
                with h3:
                    if "birth_decade" not in hints_used:
                        if st.button("🎂 Birth Decade (-50 pts)", key="hint_age"):
                            st.session_state.career_hints_used.append("birth_decade")
                            st.session_state.career_hint_penalty += 50
                            st.rerun()
                    else:
                        decade = (cp["birth_year"] // 10) * 10
                        st.markdown(f'<div class="hint-box">🎂 Born in the {decade}s</div>', unsafe_allow_html=True)

        # ── Career cards ──────────────────────────────────────────────────────────
        st.markdown("### 🏟️ Career Path")
        show_count = revealed if not (won or gave_up) else len(career)
        if show_count == 0 and not (won or gave_up):
            st.info("No clubs revealed yet. Click **Reveal Next Club** to start.")
        else:
            for entry in career[:show_count]:
                lg     = entry["league"]
                colour = LEAGUE_COLOURS.get(lg, LEAGUE_COLOURS.get("Other", "#555555"))
                st.markdown(f"""
    <div class="career-card" style="border-left-color:{colour}">
      <span class="club-name">🏟️ {entry['club']}</span>
      <span class="club-detail"> &nbsp;|&nbsp; {lg} &nbsp;|&nbsp; {entry['years']}</span>
    </div>""", unsafe_allow_html=True)

        # ── Action buttons ────────────────────────────────────────────────────────
        if not won and not gave_up:
            col_reveal, _ = st.columns([1, 3])
            with col_reveal:
                if revealed < len(career):
                    if st.button("🔍 Reveal Next Club", key="reveal_club"):
                        st.session_state.career_revealed += 1
                        st.rerun()
                else:
                    st.warning("All clubs revealed! Take a guess below.")

            st.markdown("### 🤔 Your Guess")
            all_names = all_player_names()
            guess = st.selectbox(
                "Type or select a player name:",
                options=[""] + all_names,
                key=f"career_guess_{st.session_state.career_input_key}",
                label_visibility="collapsed",
            )

            col_guess, col_giveup = st.columns([1, 1])
            with col_guess:
                if st.button("✅ Submit Guess", key="submit_career"):
                    if not guess:
                        st.warning("Please select a player first.")
                    else:
                        st.session_state.career_guesses.append(guess)
                        if guess == cp["name"]:
                            pts = max(0, score_for_guess(revealed, len(career)) - st.session_state.career_hint_penalty)
                            st.session_state.total_score   += pts
                            st.session_state.rounds_played += 1
                            st.session_state.win_streak    += 1
                            st.session_state.best_streak    = max(st.session_state.best_streak, st.session_state.win_streak)
                            st.session_state.career_won     = True
                            st.session_state.history.append({"mode": "Career", "name": cp["name"], "won": True, "points": pts})
                            st.rerun()
                        else:
                            wg = [g for g in st.session_state.career_guesses if g != cp["name"]]
                            if len(wg) >= 5:
                                st.session_state.career_gave_up   = True
                                st.session_state.rounds_played    += 1
                                st.session_state.win_streak        = 0
                                st.session_state.history.append({"mode": "Career", "name": cp["name"], "won": False, "points": 0})
                                st.rerun()
                            else:
                                st.session_state.career_input_key += 1
                                st.rerun()
            with col_giveup:
                if st.button("🏳️ Give Up", key="giveup_career"):
                    st.session_state.career_gave_up   = True
                    st.session_state.rounds_played    += 1
                    st.session_state.win_streak        = 0
                    st.session_state.history.append({"mode": "Career", "name": cp["name"], "won": False, "points": 0})
                    st.rerun()

            if wrong_guesses:
                st.markdown("**❌ Wrong guesses:** " + " • ".join(wrong_guesses))

        # ── Game-over panel ───────────────────────────────────────────────────────
        if won or gave_up:
            flag = FLAGS.get(cp["nationality"], "🌍")
            if won:
                pts = max(0, score_for_guess(
                    next((i for i, g in enumerate(st.session_state.career_guesses) if g == cp["name"]), revealed),
                    len(career)
                ) - st.session_state.career_hint_penalty)
                st.markdown(f'<div class="result-correct">🎉 Correct! That\'s <b>{cp["name"]}</b> {flag} — +{pts} pts!</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="result-wrong">😔 The answer was <b>{cp["name"]}</b> {flag}</div>', unsafe_allow_html=True)

            st.markdown("### 📋 Full Career")
            for entry in career:
                lg     = entry["league"]
                colour = LEAGUE_COLOURS.get(lg, "#555555")
                st.markdown(f"""
    <div class="career-card" style="border-left-color:{colour}">
      <span class="club-name">🏟️ {entry['club']}</span>
      <span class="club-detail"> &nbsp;|&nbsp; {lg} &nbsp;|&nbsp; {entry['years']}</span>
    </div>""", unsafe_allow_html=True)

            st.markdown("### 🌟 Player Profile")
            render_player_profile(cp)

            if st.button("▶️ Play Again", key="play_again_career"):
                pool = get_filtered()
                if pool:
                    reset_career(pick_random_player(pool))
                    st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — FOOTBALLER GUESSER
# ══════════════════════════════════════════════════════════════════════════════
with tab_fg:
    pool  = get_filtered()
    fgp   = st.session_state.fg_player
    guesses = st.session_state.fg_guesses

    col_btn2, _ = st.columns([1, 3])
    with col_btn2:
        if st.button("🎲 New Player", key="new_fg"):
            if pool:
                reset_fg(pick_random_player(pool))
            else:
                st.warning("No players match the current filters.")

    if fgp is None:
        st.info("👈 Click **New Player** to start!")
    else:

        won_fg     = st.session_state.fg_won
        gave_up_fg = st.session_state.fg_gave_up
        flag = FLAGS.get(fgp["nationality"], "🌍")

        if won_fg:
            pts = max(200, 1000 - (len(guesses) - 1) * 100)
            st.markdown(f'<div class="result-correct">🎉 Correct! That\'s <b>{fgp["name"]}</b> {flag} — +{pts} pts!</div>', unsafe_allow_html=True)
        elif gave_up_fg:
            st.markdown(f'<div class="result-wrong">😔 The answer was <b>{fgp["name"]}</b> {flag}</div>', unsafe_allow_html=True)

        # Legend
        st.markdown(
            "🟩 **Correct** &nbsp;&nbsp; 🟨 **Close** (age ±6 yrs) &nbsp;&nbsp; 🟥 **Wrong**",
            unsafe_allow_html=True
        )

        render_fg_header()
        for guess_name, cmp in guesses:
            render_fg_row(guess_name, cmp)

        # ── Guess input ───────────────────────────────────────────────────────────
        if not won_fg and not gave_up_fg:
            st.markdown("### 🤔 Guess a Footballer")
            already_guessed = [g[0] for g in guesses]
            remaining = [n for n in all_player_names() if n not in already_guessed]

            fg_guess = st.selectbox(
                "Type or select a player:",
                options=[""] + remaining,
                key=f"fg_guess_{st.session_state.fg_input_key}",
                label_visibility="collapsed",
            )

            col_g, col_gu = st.columns([1, 1])
            with col_g:
                if st.button("✅ Submit Guess", key="submit_fg"):
                    if not fg_guess:
                        st.warning("Select a player first.")
                    else:
                        gp = name_to_player.get(fg_guess)
                        if gp is None:
                            st.warning("Unknown player.")
                        else:
                            cmp = compare_players(gp, fgp)
                            st.session_state.fg_guesses.append((fg_guess, cmp))
                            if fg_guess == fgp["name"]:
                                pts = max(200, 1000 - (len(st.session_state.fg_guesses) - 1) * 100)
                                st.session_state.total_score   += pts
                                st.session_state.rounds_played += 1
                                st.session_state.win_streak    += 1
                                st.session_state.best_streak    = max(st.session_state.best_streak, st.session_state.win_streak)
                                st.session_state.fg_won         = True
                                st.session_state.history.append({"mode": "Guesser", "name": fgp["name"], "won": True, "points": pts})
                            st.session_state.fg_input_key += 1
                            st.rerun()
            with col_gu:
                if st.button("🏳️ Give Up", key="giveup_fg"):
                    st.session_state.fg_gave_up    = True
                    st.session_state.rounds_played += 1
                    st.session_state.win_streak     = 0
                    st.session_state.history.append({"mode": "Guesser", "name": fgp["name"], "won": False, "points": 0})
                    st.rerun()

            if guesses:
                st.caption(f"💡 Guesses so far: {len(guesses)}")

        if won_fg or gave_up_fg:
            st.markdown("### 🌟 Player Profile")
            render_player_profile(fgp)
            if st.button("▶️ Play Again", key="play_again_fg"):
                pool = get_filtered()
                if pool:
                    reset_fg(pick_random_player(pool))
                    st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — TROPHY CABINET
# ══════════════════════════════════════════════════════════════════════════════
with tab_tc:
    pool  = get_filtered()
    tcp   = st.session_state.tc_player

    col_btn3, _ = st.columns([1, 3])
    with col_btn3:
        if st.button("🎲 New Player", key="new_tc"):
            if pool:
                cand = pick_random_player(pool)
                reset_tc(cand)
            else:
                st.warning("No players match the current filters.")

    if tcp is None:
        st.info("👈 Click **New Player** to start!")
    else:

        trophies    = tcp["trophies"]
        tc_revealed = st.session_state.tc_revealed
        tc_won      = st.session_state.tc_won
        tc_gave_up  = st.session_state.tc_gave_up
        tc_wrong    = [g for g in st.session_state.tc_guesses if g != tcp["name"]]
        flag        = FLAGS.get(tcp["nationality"], "🌍")

        # Metrics
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Trophies Revealed", f"{tc_revealed} / {len(trophies)}")
        with c2:
            tc_pts = score_for_guess(tc_revealed, len(trophies))
            st.metric("Points if correct now", f"⭐ {tc_pts}")
        with c3:
            st.metric("Wrong Guesses", f"{len(tc_wrong)} / 5")

        # Trophy cards
        st.markdown("### 🏆 Trophy Cabinet")
        show_tc = tc_revealed if not (tc_won or tc_gave_up) else len(trophies)
        if show_tc == 0 and not (tc_won or tc_gave_up):
            st.info("No trophies revealed yet. Click **Reveal Next Trophy** to start.")
        else:
            for t in trophies[:show_tc]:
                st.markdown(f'<div class="trophy-card">🏆 {t}</div>', unsafe_allow_html=True)

        if not tc_won and not tc_gave_up:
            col_rev, _ = st.columns([1, 3])
            with col_rev:
                if tc_revealed < len(trophies):
                    if st.button("🔍 Reveal Next Trophy", key="reveal_trophy"):
                        st.session_state.tc_revealed += 1
                        st.rerun()
                else:
                    st.warning("All trophies revealed! Take a guess.")

            st.markdown("### 🤔 Your Guess")
            tc_guess = st.selectbox(
                "Type or select a player:",
                options=[""] + all_player_names(),
                key=f"tc_guess_{st.session_state.tc_input_key}",
                label_visibility="collapsed",
            )
            col_tg, col_tgu = st.columns([1, 1])
            with col_tg:
                if st.button("✅ Submit Guess", key="submit_tc"):
                    if not tc_guess:
                        st.warning("Select a player first.")
                    else:
                        st.session_state.tc_guesses.append(tc_guess)
                        if tc_guess == tcp["name"]:
                            pts = score_for_guess(tc_revealed, len(trophies))
                            st.session_state.total_score   += pts
                            st.session_state.rounds_played += 1
                            st.session_state.win_streak    += 1
                            st.session_state.best_streak    = max(st.session_state.best_streak, st.session_state.win_streak)
                            st.session_state.tc_won         = True
                            st.session_state.history.append({"mode": "Trophy", "name": tcp["name"], "won": True, "points": pts})
                            st.rerun()
                        else:
                            if len(tc_wrong) + 1 >= 5:
                                st.session_state.tc_gave_up    = True
                                st.session_state.rounds_played += 1
                                st.session_state.win_streak     = 0
                                st.session_state.history.append({"mode": "Trophy", "name": tcp["name"], "won": False, "points": 0})
                                st.rerun()
                            else:
                                st.session_state.tc_input_key += 1
                                st.rerun()
            with col_tgu:
                if st.button("🏳️ Give Up", key="giveup_tc"):
                    st.session_state.tc_gave_up    = True
                    st.session_state.rounds_played += 1
                    st.session_state.win_streak     = 0
                    st.session_state.history.append({"mode": "Trophy", "name": tcp["name"], "won": False, "points": 0})
                    st.rerun()

            if tc_wrong:
                st.markdown("**❌ Wrong guesses:** " + " • ".join(tc_wrong))

        if tc_won or tc_gave_up:
            if tc_won:
                pts = score_for_guess(tc_revealed, len(trophies))
                st.markdown(f'<div class="result-correct">🎉 Correct! That\'s <b>{tcp["name"]}</b> {flag} — +{pts} pts!</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="result-wrong">😔 The answer was <b>{tcp["name"]}</b> {flag}</div>', unsafe_allow_html=True)

            st.markdown("### 🌟 Player Profile")
            render_player_profile(tcp)

            if st.button("▶️ Play Again", key="play_again_tc"):
                pool = get_filtered()
                if pool:
                    reset_tc(pick_random_player(pool))
                    st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — DAILY CHALLENGE
# ══════════════════════════════════════════════════════════════════════════════
with tab_daily:
    dp          = st.session_state.daily_player
    d_won       = st.session_state.daily_won
    d_gave_up   = st.session_state.daily_gave_up
    d_mode      = st.session_state.daily_mode

    st.markdown(f"## 📅 Daily Challenge — {today.strftime('%B %d, %Y')}")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="daily-box"><div class="score-val">{st.session_state.daily_streak}</div><div class="score-lbl">Daily Streak</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="daily-box"><div class="score-val">{st.session_state.best_daily_streak}</div><div class="score-lbl">Best Streak</div></div>""", unsafe_allow_html=True)
    with c3:
        ds = st.session_state.daily_score
        pts_str = str(ds) if ds is not None else "—"
        st.markdown(f"""<div class="daily-box"><div class="score-val">{pts_str}</div><div class="score-lbl">Today's Score</div></div>""", unsafe_allow_html=True)

    if not d_won and not d_gave_up:
        mode_choice = st.radio("Game mode:", ["Career Timeline", "Footballer Guesser"], horizontal=True, key="daily_mode_radio")
        st.session_state.daily_mode = "Career" if mode_choice == "Career Timeline" else "Guesser"
        d_mode = st.session_state.daily_mode

    st.markdown("---")
    flag_d = FLAGS.get(dp["nationality"], "🌍")

    # ── Daily: Career mode ─────────────────────────────────────────────────────
    if d_mode == "Career" and not (d_won and st.session_state.daily_mode == "Guesser"):
        career_d   = dp["career"]
        d_revealed = st.session_state.daily_revealed
        d_guesses  = st.session_state.daily_guesses
        d_wrong    = [g for g in d_guesses if g != dp["name"]]

        if not d_won and not d_gave_up:
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Clubs Revealed", f"{d_revealed} / {len(career_d)}")
            with c2:
                d_pts = score_for_guess(d_revealed, len(career_d))
                st.metric("Points if correct now", f"⭐ {d_pts}")
            with c3:
                st.metric("Wrong Guesses", f"{len(d_wrong)} / 5")

        st.markdown("### 🏟️ Career Path")
        show_d = d_revealed if not (d_won or d_gave_up) else len(career_d)
        if show_d == 0 and not (d_won or d_gave_up):
            st.info("Click **Reveal Next Club** to start.")
        else:
            for entry in career_d[:show_d]:
                lg     = entry["league"]
                colour = LEAGUE_COLOURS.get(lg, "#555555")
                st.markdown(f"""<div class="career-card" style="border-left-color:{colour}">
  <span class="club-name">🏟️ {entry['club']}</span>
  <span class="club-detail"> &nbsp;|&nbsp; {lg} &nbsp;|&nbsp; {entry['years']}</span>
</div>""", unsafe_allow_html=True)

        if not d_won and not d_gave_up:
            col_rev2, _ = st.columns([1, 3])
            with col_rev2:
                if d_revealed < len(career_d):
                    if st.button("🔍 Reveal Next Club", key="reveal_daily"):
                        st.session_state.daily_revealed += 1
                        st.rerun()

            st.markdown("### 🤔 Your Guess")
            d_guess = st.selectbox(
                "Type or select:", options=[""] + all_player_names(),
                key=f"daily_guess_{st.session_state.daily_input_key}",
                label_visibility="collapsed",
            )
            col_dg, col_dgu = st.columns([1, 1])
            with col_dg:
                if st.button("✅ Submit", key="submit_daily"):
                    if not d_guess:
                        st.warning("Select a player first.")
                    else:
                        st.session_state.daily_guesses.append(d_guess)
                        if d_guess == dp["name"]:
                            pts = score_for_guess(d_revealed, len(career_d))
                            st.session_state.daily_score      = pts
                            st.session_state.total_score     += pts
                            st.session_state.daily_won        = True
                            st.session_state.last_daily_won_date = str(today)
                            st.session_state.daily_streak    += 1
                            st.session_state.best_daily_streak = max(
                                st.session_state.best_daily_streak, st.session_state.daily_streak
                            )
                            st.session_state.history.append({"mode": "Daily", "name": dp["name"], "won": True, "points": pts})
                            st.rerun()
                        else:
                            dw = [g for g in st.session_state.daily_guesses if g != dp["name"]]
                            if len(dw) >= 5:
                                st.session_state.daily_gave_up = True
                                st.session_state.daily_score   = 0
                                st.session_state.daily_streak  = 0
                                st.session_state.history.append({"mode": "Daily", "name": dp["name"], "won": False, "points": 0})
                                st.rerun()
                            else:
                                st.session_state.daily_input_key += 1
                                st.rerun()
            with col_dgu:
                if st.button("🏳️ Give Up", key="giveup_daily"):
                    st.session_state.daily_gave_up = True
                    st.session_state.daily_score   = 0
                    st.session_state.daily_streak  = 0
                    st.session_state.history.append({"mode": "Daily", "name": dp["name"], "won": False, "points": 0})
                    st.rerun()

            if d_wrong:
                st.markdown("**❌ Wrong guesses:** " + " • ".join(d_wrong))

    # ── Daily: Guesser mode ────────────────────────────────────────────────────
    elif d_mode == "Guesser" and not (d_won and st.session_state.daily_mode == "Career"):
        d_fg_guesses = st.session_state.daily_fg_guesses

        if d_won:
            pts = st.session_state.daily_score or 0
            st.markdown(f'<div class="result-correct">🎉 Correct! That\'s <b>{dp["name"]}</b> {flag_d} — +{pts} pts!</div>', unsafe_allow_html=True)
        elif d_gave_up:
            st.markdown(f'<div class="result-wrong">😔 The answer was <b>{dp["name"]}</b> {flag_d}</div>', unsafe_allow_html=True)

        st.markdown("🟩 **Correct** &nbsp;&nbsp; 🟨 **Close** &nbsp;&nbsp; 🟥 **Wrong**")
        render_fg_header()
        for gn, cmp in d_fg_guesses:
            render_fg_row(gn, cmp)

        if not d_won and not d_gave_up:
            st.markdown("### 🤔 Guess a Footballer")
            already_d = [g[0] for g in d_fg_guesses]
            rem_d = [n for n in all_player_names() if n not in already_d]
            dfg_guess = st.selectbox(
                "Type or select:", options=[""] + rem_d,
                key=f"daily_fg_{st.session_state.daily_input_key}",
                label_visibility="collapsed",
            )
            col_dfg, col_dfgu = st.columns([1, 1])
            with col_dfg:
                if st.button("✅ Submit", key="submit_daily_fg"):
                    if not dfg_guess:
                        st.warning("Select a player first.")
                    else:
                        gpp = name_to_player.get(dfg_guess)
                        if gpp:
                            cmp = compare_players(gpp, dp)
                            st.session_state.daily_fg_guesses.append((dfg_guess, cmp))
                            if dfg_guess == dp["name"]:
                                pts = max(200, 1000 - (len(st.session_state.daily_fg_guesses) - 1) * 100)
                                st.session_state.daily_score      = pts
                                st.session_state.total_score     += pts
                                st.session_state.daily_won        = True
                                st.session_state.daily_streak    += 1
                                st.session_state.best_daily_streak = max(
                                    st.session_state.best_daily_streak, st.session_state.daily_streak
                                )
                                st.session_state.history.append({"mode": "Daily", "name": dp["name"], "won": True, "points": pts})
                            st.session_state.daily_input_key += 1
                            st.rerun()
            with col_dfgu:
                if st.button("🏳️ Give Up", key="giveup_daily_fg"):
                    st.session_state.daily_gave_up = True
                    st.session_state.daily_score   = 0
                    st.session_state.daily_streak  = 0
                    st.session_state.history.append({"mode": "Daily", "name": dp["name"], "won": False, "points": 0})
                    st.rerun()

    # ── Daily reveal ───────────────────────────────────────────────────────────
    if d_won or d_gave_up:
        if d_won:
            pts = st.session_state.daily_score or 0
            st.markdown(f'<div class="result-correct">🎉 Correct! That\'s <b>{dp["name"]}</b> {flag_d} — +{pts} pts!</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="result-wrong">😔 The answer was <b>{dp["name"]}</b> {flag_d}</div>', unsafe_allow_html=True)
        st.markdown("### 🌟 Player Profile")
        render_player_profile(dp)
        tomorrow = today + datetime.timedelta(days=1)
        st.info(f"⏰ Come back tomorrow ({tomorrow.strftime('%B %d')}) for the next Daily Challenge!")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — STATISTICS & ACHIEVEMENTS
# ══════════════════════════════════════════════════════════════════════════════
with tab_stats:
    st.markdown("## 📊 Your Statistics")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="score-box"><div class="score-val">{st.session_state.total_score}</div><div class="score-lbl">Total Score</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="score-box"><div class="score-val">{st.session_state.rounds_played}</div><div class="score-lbl">Rounds Played</div></div>', unsafe_allow_html=True)
    with c3:
        wins = sum(1 for h in st.session_state.history if h["won"])
        wr   = int(wins / max(1, st.session_state.rounds_played) * 100)
        st.markdown(f'<div class="score-box"><div class="score-val">{wr}%</div><div class="score-lbl">Win Rate</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="score-box"><div class="score-val">{st.session_state.best_streak}🔥</div><div class="score-lbl">Best Streak</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    if st.session_state.history:
        df_hist = pd.DataFrame(st.session_state.history)
        df_hist["cumulative"] = df_hist["points"].cumsum()

        # Score chart
        fig_s = px.area(df_hist, y="cumulative", title="📈 Cumulative Score",
                        labels={"index": "Round", "cumulative": "Total Score"})
        fig_s.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="white", margin=dict(l=10, r=10, t=40, b=10),
        )
        fig_s.update_traces(line_color="#1db954", fillcolor="rgba(29,185,84,0.15)")
        fig_s.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.07)")
        fig_s.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.07)")
        st.plotly_chart(fig_s, use_container_width=True)

        # Win rate by mode
        mode_stats = df_hist.groupby("mode").agg(
            Played=("won", "count"),
            Wins=("won", "sum"),
            Points=("points", "sum")
        ).reset_index()
        mode_stats["Win Rate"] = (mode_stats["Wins"] / mode_stats["Played"] * 100).round(1).astype(str) + "%"
        st.markdown("### 📋 Stats by Mode")
        st.dataframe(mode_stats, use_container_width=True, hide_index=True)

        st.markdown("### 📋 Round History")
        df_show = df_hist[["mode", "name", "won", "points"]].copy()
        df_show["won"] = df_show["won"].map({True: "✅", False: "❌"})
        df_show.columns = ["Mode", "Player", "Result", "Points"]
        df_show.index = range(1, len(df_show) + 1)
        st.dataframe(df_show, use_container_width=True)
    else:
        st.info("Play some rounds to see your stats here!")

    # ── Achievements ──────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## 🏅 Achievements")

    total_score  = st.session_state.total_score
    rounds       = st.session_state.rounds_played
    best_streak  = st.session_state.best_streak
    daily_streak = st.session_state.daily_streak
    wins_count   = sum(1 for h in st.session_state.history if h["won"])
    career_wins  = sum(1 for h in st.session_state.history if h["won"] and h["mode"] == "Career")
    guesser_wins = sum(1 for h in st.session_state.history if h["won"] and h["mode"] == "Guesser")
    trophy_wins  = sum(1 for h in st.session_state.history if h["won"] and h["mode"] == "Trophy")

    achievements = [
        {"icon": "🎯", "name": "First Blood",       "desc": "Win your first round",       "unlocked": wins_count >= 1},
        {"icon": "🔟", "name": "Deca-Gamer",         "desc": "Play 10 rounds",             "unlocked": rounds >= 10},
        {"icon": "💯", "name": "Century Club",       "desc": "Play 100 rounds",            "unlocked": rounds >= 100},
        {"icon": "🔥", "name": "On Fire",            "desc": "Reach a 5-win streak",       "unlocked": best_streak >= 5},
        {"icon": "⚡", "name": "Unstoppable",        "desc": "Reach a 10-win streak",      "unlocked": best_streak >= 10},
        {"icon": "⭐", "name": "Point Collector",    "desc": "Score 1,000 total points",   "unlocked": total_score >= 1000},
        {"icon": "🌟", "name": "High Scorer",        "desc": "Score 10,000 total points",  "unlocked": total_score >= 10000},
        {"icon": "🏟️", "name": "Career Expert",      "desc": "Win 5 Career Timeline rounds","unlocked": career_wins >= 5},
        {"icon": "🟩", "name": "Attribute Master",   "desc": "Win 5 Footballer Guesser rounds","unlocked": guesser_wins >= 5},
        {"icon": "🏆", "name": "Trophy Hunter",      "desc": "Win 5 Trophy Cabinet rounds","unlocked": trophy_wins >= 5},
        {"icon": "📅", "name": "Daily Devotee",      "desc": "Get a 3-day daily streak",   "unlocked": daily_streak >= 3},
        {"icon": "📅", "name": "Daily Legend",       "desc": "Get a 7-day daily streak",   "unlocked": daily_streak >= 7},
    ]

    unlocked_count = sum(1 for a in achievements if a["unlocked"])
    st.markdown(f"**{unlocked_count} / {len(achievements)} unlocked**")

    prog = int(unlocked_count / len(achievements) * 100)
    st.progress(prog / 100)

    ach_cols = st.columns(3)
    for i, ach in enumerate(achievements):
        col = ach_cols[i % 3]
        with col:
            if ach["unlocked"]:
                st.markdown(
                    f'<div class="achievement-card">'
                    f'<span style="font-size:1.8rem">{ach["icon"]}</span>'
                    f'<div><strong style="color:#ffd700">{ach["name"]}</strong>'
                    f'<br><span style="font-size:0.8rem;color:#aaa">{ach["desc"]}</span></div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="achievement-locked">'
                    f'<span style="font-size:1.8rem">🔒</span>'
                    f'<div><strong style="color:#666">{ach["name"]}</strong>'
                    f'<br><span style="font-size:0.8rem;color:#555">{ach["desc"]}</span></div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

    # ── Player Database Explorer ───────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🌟 Player Database Explorer")
    col_search, col_filter_pos = st.columns([2, 1])
    with col_search:
        search = st.text_input("🔍 Search by name, nationality, club, or continent:")
    with col_filter_pos:
        db_pos = st.selectbox("Filter position:", ["All"] + list(POSITIONS.keys()), key="db_pos")

    show_all = PLAYERS
    if search:
        q = search.lower()
        show_all = [
            p for p in show_all
            if q in p["name"].lower()
            or q in p["nationality"].lower()
            or any(q in e["club"].lower() for e in p["career"])
            or q in get_meta(p, "continent", "").lower()
        ]
    if db_pos != "All":
        show_all = [p for p in show_all if p["position_group"] == db_pos]

    rows_db = []
    for p in show_all:
        rows_db.append({
            "Name":            p["name"],
            "Nationality":     FLAGS.get(p["nationality"], "🌍") + " " + p["nationality"],
            "Continent":       get_meta(p, "continent", "?"),
            "Position":        p["position"],
            "Group":           p["position_group"],
            "Main League":     get_top_league(p),
            "Peak Club":       get_meta(p, "peak_club", "?"),
            "World Cup":       "✅" if get_meta(p, "world_cup_winner", False) else "❌",
            "Ballon d'Or":     p.get("ballon_dor", 0) or 0,
            "Career Clubs":    len(p["career"]),
            "Difficulty":      p.get("difficulty", "?"),
        })
    if rows_db:
        st.dataframe(pd.DataFrame(rows_db), use_container_width=True, hide_index=True)
    else:
        st.info("No players found.")
    st.caption(f"Total players in database: {len(PLAYERS)}")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — AI CAREER SIMULATOR
# ══════════════════════════════════════════════════════════════════════════════

# ── AI Career Sim: constants ─────────────────────────────────────────────────
_AI_PLAYING_STYLES = [
    "Technical Dribbler", "Powerful Striker", "Playmaking Maestro",
    "Defensive Anchor", "Aerial Threat", "Speed Merchant",
    "Box-to-Box Engine", "Clinical Finisher",
]

_AI_EXTRA_NATIONALITIES = [
    "Mexico", "USA", "Japan", "South Korea", "Australia",
    "Colombia", "Chile", "Nigeria", "Algeria", "Russia",
]

_AI_CAREER_STAGES = [
    {"idx": 0, "id": "youth",   "name": "Youth Academy",       "age": "16–18", "icon": "🌱"},
    {"idx": 1, "id": "debut",   "name": "Professional Debut",  "age": "18–22", "icon": "⚡"},
    {"idx": 2, "id": "rise",    "name": "Rising Star",         "age": "22–26", "icon": "📈"},
    {"idx": 3, "id": "peak",    "name": "Peak Years",          "age": "26–31", "icon": "🏆"},
    {"idx": 4, "id": "veteran", "name": "Veteran Phase",       "age": "31–36", "icon": "🎯"},
]


def _stage_data(position_group: str) -> list:
    """Return list of (narrative, choice_a, choice_b) tuples per stage.
    Each choice is (text: str, stat_delta: dict).
    """
    if position_group == "Forward":
        return [
            (
                "{name} arrived at the academy as a pacy {style}, terrorising defenders in reserve fixtures. "
                "The first-team manager kept a close eye on this emerging talent.",
                ("Push for a first-team debut this season",                  {"goals": 4,  "assists": 2,  "trophies": 0, "caps": 0}),
                ("Accept a loan to a lower-league club for more minutes",    {"goals": 9,  "assists": 3,  "trophies": 0, "caps": 0}),
            ),
            (
                "Turning professional, {name}'s sharp movement and instinctive finishing attracted interest from across Europe. "
                "Two very different paths lay ahead.",
                ("Sign for a top-flight giant and fight for a squad role",   {"goals": 14, "assists": 8,  "trophies": 1, "caps": 5}),
                ("Choose a mid-table club for guaranteed first-team minutes", {"goals": 22, "assists": 10, "trophies": 0, "caps": 8}),
            ),
            (
                "A prolific season has made {name} one of the hottest properties in world football at just 22. "
                "Champions League clubs are circling.",
                ("Join a Champions League contender",                        {"goals": 30, "assists": 15, "trophies": 2, "caps": 15}),
                ("Become the undisputed main man at an ambitious club",      {"goals": 45, "assists": 18, "trophies": 1, "caps": 20}),
            ),
            (
                "At 26, {name} is feared by every defence. A world-record offer arrives — "
                "but so does the chance to cement legendary status at a beloved club.",
                ("Accept the mega-money move to the wealthiest club",        {"goals": 42, "assists": 22, "trophies": 3, "caps": 20}),
                ("Stay loyal and chase the title with a beloved club",       {"goals": 55, "assists": 28, "trophies": 4, "caps": 25}),
            ),
            (
                "31 and still dangerous, {name} has accumulated silverware many players only dream of. "
                "One final chapter remains to be written.",
                ("Embrace a new challenge in MLS or the Saudi Pro League",   {"goals": 30, "assists": 12, "trophies": 1, "caps": 5}),
                ("Stay in the top flight and mentor the next generation",    {"goals": 28, "assists": 18, "trophies": 2, "caps": 10}),
            ),
        ]
    elif position_group == "Midfielder":
        return [
            (
                "{name} quickly stood out in the academy with a {style} game that made the coaches compare the youngster "
                "to midfield legends of the past.",
                ("Train extra hours on shooting and scoring",                {"goals": 5,  "assists": 6,  "trophies": 0, "caps": 0}),
                ("Focus on passing range, vision, and game management",      {"goals": 2,  "assists": 12, "trophies": 0, "caps": 0}),
            ),
            (
                "Two clubs made compelling offers. {name}'s ability to control the tempo of matches was already evident — "
                "but where to develop that talent best?",
                ("Sign for a glamour club as a squad midfielder",            {"goals": 8,  "assists": 14, "trophies": 1, "caps": 4}),
                ("Choose a team where {name} will be the heartbeat",         {"goals": 12, "assists": 20, "trophies": 0, "caps": 9}),
            ),
            (
                "22 and flourishing, {name}'s range of passing and box-to-box energy are drawing national headlines. "
                "A pivotal transfer window opens.",
                ("Move to a top-four side fighting for the title",           {"goals": 18, "assists": 35, "trophies": 2, "caps": 18}),
                ("Lead the midfield at an ambitious club building for glory",{"goals": 25, "assists": 40, "trophies": 1, "caps": 22}),
            ),
            (
                "At 26, {name} is arguably the best midfielder in the league. A historic club wants their new midfield general "
                "and they're willing to pay.",
                ("Join the historic giant and chase the Champions League",   {"goals": 22, "assists": 42, "trophies": 3, "caps": 22}),
                ("Stay and break the all-time appearances record",           {"goals": 28, "assists": 50, "trophies": 3, "caps": 28}),
            ),
            (
                "31 and still covering every blade of grass, {name}'s experience compensates for whatever edge of pace "
                "time has taken. The question now is legacy.",
                ("Move abroad to a new league for one last challenge",       {"goals": 12, "assists": 25, "trophies": 1, "caps": 8}),
                ("Stay in domestic football until the very last whistle",    {"goals": 15, "assists": 30, "trophies": 2, "caps": 12}),
            ),
        ]
    elif position_group == "Defender":
        return [
            (
                "{name} was a commanding {style} from day one of the academy, throwing themselves into every training "
                "session with fearless determination.",
                ("Develop as a ball-playing sweeper with attacking instincts",{"goals": 3, "assists": 5,  "trophies": 0, "caps": 0}),
                ("Master the fundamentals — positioning, heading, tackling", {"goals": 1, "assists": 3,  "trophies": 1, "caps": 0}),
            ),
            (
                "Defenders mature late, but {name} was ahead of schedule. Two clubs wanted to sign the young stopper — "
                "one a title contender, one desperate for defensive solidarity.",
                ("Join the title contender as a squad defender",             {"goals": 2, "assists": 8,  "trophies": 2, "caps": 4}),
                ("Anchor the defence at a mid-table club as undisputed no. 1",{"goals": 3, "assists": 10, "trophies": 0, "caps": 9}),
            ),
            (
                "22 and reliable as a rock, {name} is now one of the most sought-after defenders on the continent. "
                "A powerhouse club wants to build their entire backline around this talent.",
                ("Sign for the powerhouse — elite level, intense competition",{"goals": 5, "assists": 15, "trophies": 3, "caps": 16}),
                ("Become the captain of a title-chasing side",               {"goals": 8, "assists": 20, "trophies": 2, "caps": 22}),
            ),
            (
                "At 26, {name} is at the peak of defensive powers. Clean sheets are a regular occurrence and "
                "a huge club arrives with a lavish offer.",
                ("Join the mega-club and play in the biggest matches",       {"goals": 5, "assists": 18, "trophies": 3, "caps": 22}),
                ("Become a club legend — captain them to an unlikely title", {"goals": 8, "assists": 22, "trophies": 4, "caps": 28}),
            ),
            (
                "31 and still a rock. Experience makes {name} even more dangerous — anticipation and positioning "
                "compensate for any reduction in pace.",
                ("Accept a final challenge in a top foreign league",         {"goals": 3, "assists": 10, "trophies": 1, "caps": 6}),
                ("See out the career in the domestic top flight",            {"goals": 4, "assists": 12, "trophies": 2, "caps": 10}),
            ),
        ]
    else:  # Goalkeeper
        return [
            (
                "At 16, {name} had the reflexes of a cat and the presence of a {style}. "
                "The goalkeeping coach predicted an international career from the very first training session.",
                ("Work obsessively on shot-stopping, reflexes and positioning",{"goals": 0, "assists": 0, "trophies": 1, "caps": 0}),
                ("Develop sweeper-keeper skills and precise distribution",    {"goals": 0, "assists": 2, "trophies": 0, "caps": 0}),
            ),
            (
                "{name} is 18 and ready for the professional stage. Goalkeepers need experience — "
                "but two very different paths are available.",
                ("Fight for a spot at a top-flight club's first team",        {"goals": 0, "assists": 2, "trophies": 1, "caps": 3}),
                ("Take a loan to a lower-league club for 200 games in two seasons",{"goals": 0, "assists": 4, "trophies": 0, "caps": 6}),
            ),
            (
                "A string of brilliant performances has made {name} one of the most coveted keepers in Europe. "
                "Two clubs are desperate to sign them.",
                ("Join a Champions League regular at a premium price",        {"goals": 0, "assists": 5, "trophies": 3, "caps": 16}),
                ("Become the undisputed no. 1 at a passionate mid-table club",{"goals": 0, "assists": 8, "trophies": 2, "caps": 22}),
            ),
            (
                "26 and at the absolute peak of their powers, {name} is being talked about as the best goalkeeper "
                "in the world. A historic contract offer arrives.",
                ("Sign for the wealthiest club and target every trophy",      {"goals": 0, "assists": 6, "trophies": 4, "caps": 20}),
                ("Remain loyal and carry the beloved club to an unlikely title",{"goals": 0, "assists": 8, "trophies": 3, "caps": 26}),
            ),
            (
                "31 is young for a goalkeeper. {name} can realistically play at the top level for five more years — "
                "but where?",
                ("Move to a glamour league abroad for a new adventure",       {"goals": 0, "assists": 5, "trophies": 1, "caps": 5}),
                ("Stay as the evergreen no. 1 in the domestic top flight",    {"goals": 0, "assists": 6, "trophies": 2, "caps": 10}),
            ),
        ]


def _ai_generate_stage(player: dict, stage: dict, stats: dict, api_key: str) -> dict:
    """Return {narrative, choices: [str, str], stat_deltas: [dict, dict]}.
    Falls back to templates when api_key is empty or on any error.
    """
    templates = _stage_data(player["position_group"])
    tmpl_narr, tmpl_a, tmpl_b = templates[stage["idx"]]
    fallback = {
        "narrative":   tmpl_narr.format(name=player["name"], style=player["style"]),
        "choices":     [tmpl_a[0], tmpl_b[0]],
        "stat_deltas": [tmpl_a[1], tmpl_b[1]],
    }
    if not api_key:
        return fallback
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        stat_line = (
            f"Career stats so far: {stats['goals']} goals, {stats['assists']} assists, "
            f"{stats['trophies']} trophies, {stats['caps']} international caps."
        ) if stats["goals"] + stats["assists"] + stats["trophies"] + stats["caps"] > 0 else ""
        prompt = (
            f"Create a career stage for this footballer:\n"
            f"Name: {player['name']} | Nationality: {player['nationality']} | "
            f"Position: {player['position_group']} | Style: {player['style']}\n"
            f"Stage: {stage['name']} (Age {stage['age']})\n"
            f"{stat_line}\n\n"
            f"Respond in EXACTLY this format (keep each section to 1–2 sentences):\n"
            f"NARRATIVE: [dramatic career narrative for this stage]\n"
            f"CHOICE_A: [{tmpl_a[0]}]\n"
            f"CHOICE_B: [{tmpl_b[0]}]"
        )
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": (
                    "You are a football career narrator creating an engaging text-adventure game. "
                    "Be concise, dramatic, and use authentic football details. "
                    "Keep the two choices close to the template options provided."
                )},
                {"role": "user", "content": prompt},
            ],
            max_tokens=220,
            temperature=0.85,
        )
        lines = {}
        for line in resp.choices[0].message.content.strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                lines[k.strip()] = v.strip()
        # Fall back to template values for any missing keys
        return {
            "narrative":   lines.get("NARRATIVE") or fallback["narrative"],
            "choices":     [lines.get("CHOICE_A") or tmpl_a[0], lines.get("CHOICE_B") or tmpl_b[0]],
            "stat_deltas": [tmpl_a[1], tmpl_b[1]],
        }
    except Exception as exc:
        import openai as _oai
        if not isinstance(exc, _oai.OpenAIError):
            raise
        return fallback


def _ai_generate_outcome(player: dict, stage: dict, choice_text: str, delta: dict, api_key: str) -> str:
    """Return outcome narrative string."""
    parts = []
    if delta.get("goals"):    parts.append(f"{delta['goals']} goals")
    if delta.get("assists"):  parts.append(f"{delta['assists']} assists")
    if delta.get("trophies"): parts.append(f"{delta['trophies']} trophies")
    if delta.get("caps"):     parts.append(f"{delta['caps']} international caps")
    stat_str = ", ".join(parts) if parts else "valuable experience"
    fallback = (
        f"A tremendous spell for {player['name']}! "
        f"The decision paid off with {stat_str} earned across this stage of the career."
    )
    if not api_key:
        return fallback
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": (
                    "You are a football career narrator. Write punchy, vivid outcome paragraphs."
                )},
                {"role": "user", "content": (
                    f"{player['name']} ({player['nationality']} {player['position_group']}) chose: \"{choice_text}\"\n"
                    f"Stage: {stage['name']}\n"
                    f"Results: {stat_str}\n\n"
                    f"Write ONE paragraph (2–3 sentences) describing what happened. "
                    f"Be specific and dramatic. Do NOT start with the player's name."
                )},
            ],
            max_tokens=130,
            temperature=0.85,
        )
        return resp.choices[0].message.content.strip()
    except Exception as exc:
        import openai as _oai
        if not isinstance(exc, _oai.OpenAIError):
            raise
        return fallback


def _career_rating(stats: dict) -> tuple[int, str]:
    """Return (0-100 rating, badge label) based on accumulated stats."""
    score = (
        stats["goals"] * 1.0
        + stats["assists"] * 0.8
        + stats["trophies"] * 15
        + stats["caps"] * 0.5
    )
    if score >= 350: return 97, "🐐 All-Time Legend"
    if score >= 280: return 93, "⭐ World-Class"
    if score >= 210: return 88, "🌟 Elite"
    if score >= 140: return 82, "📈 Very Good"
    if score >= 80:  return 75, "✅ Solid Pro"
    return 65, "🎓 Journeyman"


# ── AI Career Sim: tab rendering ─────────────────────────────────────────────
with tab_ai:
    st.markdown("## 🤖 AI Career Simulator")
    st.markdown(
        "Create your own footballer and guide them from the youth academy to retirement. "
        "Every decision shapes your legacy — goals, trophies, caps, and all."
    )
    if not st.session_state.openai_api_key:
        st.info(
            "💡 **Tip:** Enter your OpenAI API key in the sidebar to unlock AI-generated "
            "personalised narratives. The simulator works great with built-in story templates too!"
        )

    ai_stage_idx = st.session_state.ai_stage_idx
    ai_player    = st.session_state.ai_player

    # ── Career creation form (not yet started) ────────────────────────────────
    if ai_stage_idx == -1:
        st.markdown("### ⚽ Create Your Footballer")
        col_form1, col_form2 = st.columns(2)
        with col_form1:
            ai_name = st.text_input("Player Name", placeholder="e.g. Marco Reyes", key="ai_name_input")
            nat_options = sorted(list(FLAGS.keys()) + _AI_EXTRA_NATIONALITIES)
            ai_nat = st.selectbox("Nationality", nat_options, key="ai_nat_input")
        with col_form2:
            ai_pos = st.selectbox("Position Group", list(POSITIONS.keys()), key="ai_pos_input")
            ai_style = st.selectbox("Playing Style", _AI_PLAYING_STYLES, key="ai_style_input")

        if st.button("🚀 Start Career", key="ai_start"):
            if not ai_name.strip():
                st.warning("Please enter a player name.")
            else:
                st.session_state.ai_player = {
                    "name": ai_name.strip(),
                    "nationality": ai_nat,
                    "position_group": ai_pos,
                    "style": ai_style,
                }
                st.session_state.ai_stage_idx       = 0
                st.session_state.ai_awaiting_outcome = False
                st.session_state.ai_chosen_option    = None
                st.session_state.ai_narrative        = ""
                st.session_state.ai_choices          = []
                st.session_state.ai_outcome_text     = ""
                st.session_state.ai_stats            = {"goals": 0, "assists": 0, "trophies": 0, "caps": 0}
                st.session_state.ai_history          = []
                st.rerun()

    # ── Active stage ──────────────────────────────────────────────────────────
    elif ai_stage_idx < len(_AI_CAREER_STAGES):
        stage   = _AI_CAREER_STAGES[ai_stage_idx]
        player  = st.session_state.ai_player
        stats   = st.session_state.ai_stats
        api_key = st.session_state.openai_api_key

        # Stage progress bar
        st.markdown(f"### {stage['icon']} Stage {ai_stage_idx + 1} / {len(_AI_CAREER_STAGES)}: {stage['name']}  *(Age {stage['age']})*")
        st.progress((ai_stage_idx) / len(_AI_CAREER_STAGES))

        # Live stats bar
        sc1, sc2, sc3, sc4 = st.columns(4)
        with sc1:
            st.metric("⚽ Goals",     stats["goals"])
        with sc2:
            st.metric("🎯 Assists",   stats["assists"])
        with sc3:
            st.metric("🏆 Trophies",  stats["trophies"])
        with sc4:
            st.metric("🌍 Int'l Caps", stats["caps"])

        st.markdown("---")

        # Generate narrative if not yet loaded for this stage
        if not st.session_state.ai_narrative:
            with st.spinner("✍️ Writing your career story…"):
                data = _ai_generate_stage(player, stage, stats, api_key)
            st.session_state.ai_narrative  = data["narrative"]
            st.session_state.ai_choices    = list(zip(data["choices"], data["stat_deltas"]))
            st.rerun()

        # Show narrative
        st.markdown(
            f'<div style="background:rgba(255,255,255,0.06);border-left:4px solid #1db954;'
            f'border-radius:10px;padding:16px 20px;margin-bottom:16px;font-size:1.05rem;color:#e0e0e0;">'
            f'{st.session_state.ai_narrative}</div>',
            unsafe_allow_html=True,
        )

        # ── Showing outcome (after choice made) ───────────────────────────────
        if st.session_state.ai_awaiting_outcome:
            chosen_idx = st.session_state.ai_chosen_option
            choice_text, delta = st.session_state.ai_choices[chosen_idx]

            if not st.session_state.ai_outcome_text:
                with st.spinner("⚡ Simulating the outcome…"):
                    outcome = _ai_generate_outcome(player, stage, choice_text, delta, api_key)
                st.session_state.ai_outcome_text = outcome
                st.rerun()

            st.markdown(f"**You chose:** *{choice_text}*")
            st.markdown(
                f'<div style="background:rgba(29,185,84,0.1);border-left:4px solid #ffc107;'
                f'border-radius:10px;padding:14px 20px;margin:10px 0;color:#e0e0e0;">'
                f'{st.session_state.ai_outcome_text}</div>',
                unsafe_allow_html=True,
            )

            # Stat gains
            gain_parts = []
            if delta.get("goals"):    gain_parts.append(f"⚽ +{delta['goals']} goals")
            if delta.get("assists"):  gain_parts.append(f"🎯 +{delta['assists']} assists")
            if delta.get("trophies"): gain_parts.append(f"🏆 +{delta['trophies']} trophies")
            if delta.get("caps"):     gain_parts.append(f"🌍 +{delta['caps']} caps")
            if gain_parts:
                st.markdown("**Stats earned:** " + "  ·  ".join(gain_parts))

            next_label = "▶️ Next Stage" if ai_stage_idx < len(_AI_CAREER_STAGES) - 1 else "🏁 Retire & See Legacy"
            if st.button(next_label, key="ai_next_stage"):
                # Apply stats
                for k, v in delta.items():
                    st.session_state.ai_stats[k] += v
                # Save history
                st.session_state.ai_history.append({
                    "stage":   stage["name"],
                    "choice":  choice_text,
                    "outcome": st.session_state.ai_outcome_text,
                    "delta":   delta,
                })
                # Advance
                st.session_state.ai_stage_idx       += 1
                st.session_state.ai_awaiting_outcome  = False
                st.session_state.ai_chosen_option     = None
                st.session_state.ai_narrative         = ""
                st.session_state.ai_choices           = []
                st.session_state.ai_outcome_text      = ""
                st.rerun()

        # ── Showing choices (awaiting decision) ───────────────────────────────
        else:
            st.markdown("### 🤔 What do you do?")
            choices = st.session_state.ai_choices
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button(f"**A:** {choices[0][0]}", key="ai_choice_a", use_container_width=True):
                    st.session_state.ai_chosen_option    = 0
                    st.session_state.ai_awaiting_outcome = True
                    st.rerun()
            with col_b:
                if st.button(f"**B:** {choices[1][0]}", key="ai_choice_b", use_container_width=True):
                    st.session_state.ai_chosen_option    = 1
                    st.session_state.ai_awaiting_outcome = True
                    st.rerun()

    # ── Career ended — legacy screen ──────────────────────────────────────────
    elif ai_stage_idx >= len(_AI_CAREER_STAGES):
        player = st.session_state.ai_player
        stats  = st.session_state.ai_stats
        rating, badge = _career_rating(stats)
        flag   = FLAGS.get(player["nationality"], "🌍")

        st.markdown(f"## 🏁 {player['name']} — Career Over")
        st.markdown(
            f'<div class="result-correct" style="font-size:1.6rem">'
            f'{badge} &nbsp; Career Rating: {rating} / 100'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.markdown(f"**{flag} {player['nationality']} · {player['position_group']} · {player['style']}**")

        # Final stats
        s1, s2, s3, s4 = st.columns(4)
        with s1: st.metric("⚽ Career Goals",    stats["goals"])
        with s2: st.metric("🎯 Career Assists",   stats["assists"])
        with s3: st.metric("🏆 Trophies Won",     stats["trophies"])
        with s4: st.metric("🌍 International Caps", stats["caps"])

        st.markdown("---")
        st.markdown("### 📖 Career Chronicle")
        for entry in st.session_state.ai_history:
            st.markdown(
                f'<div style="background:rgba(255,255,255,0.05);border-left:4px solid #1db954;'
                f'border-radius:8px;padding:12px 16px;margin:8px 0;">'
                f'<strong style="color:#1db954">{entry["stage"]}</strong><br>'
                f'<em style="color:#ffc107">Chose: {entry["choice"]}</em><br>'
                f'<span style="color:#ccc">{entry["outcome"]}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

        if st.button("🔄 Start a New Career", key="ai_restart"):
            st.session_state.ai_player           = None
            st.session_state.ai_stage_idx        = -1
            st.session_state.ai_awaiting_outcome = False
            st.session_state.ai_chosen_option    = None
            st.session_state.ai_narrative        = ""
            st.session_state.ai_choices          = []
            st.session_state.ai_outcome_text     = ""
            st.session_state.ai_stats            = {"goals": 0, "assists": 0, "trophies": 0, "caps": 0}
            st.session_state.ai_history          = []
            st.rerun()

