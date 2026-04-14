"""
app.py  —  ⚽ Soccer Career Guesser  (Advanced Edition)
Eight game modes:
  1. Career Timeline  – reveal clubs one-by-one and guess the footballer
  2. Footballer Guesser – Wordle-style 9-attribute feedback grid
  3. Trophy Cabinet – reveal trophies one-by-one and guess the footballer
  4. Daily Challenge – same mystery player for everyone, seeded by today's date
  5. Statistics & Achievements
  6. AI Career Simulator – guide your own footballer from academy to retirement
  7. Beat the Footballer – face a star in a 5-question career trivia duel
  8. Coach Career Sim – build a managerial career from grassroots to glory
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
    "ai_stage_idx":        -1,     # -1=not started, 0-7=stage, 8=ended
    "ai_awaiting_outcome": False,  # True=user chose, showing outcome; False=showing choices
    "ai_chosen_option":    None,   # 0 or 1
    "ai_narrative":        "",
    "ai_choices":          [],     # [(text, stat_delta), (text, stat_delta)]
    "ai_outcome_text":     "",
    "ai_stats":            {"goals": 0, "assists": 0, "trophies": 0, "caps": 0},
    "ai_history":          [],     # list of {stage, choice, outcome, delta}
    # Beat the Footballer
    "btf_player":          None,
    "btf_questions":       [],
    "btf_q_idx":           0,      # index of current question (0-4), 5 = done
    "btf_selected":        None,   # answer the user selected; None = awaiting
    "btf_answers":         [],     # list of bool
    "btf_won":             False,
    "btf_gave_up":         False,
    "btf_input_key":       400,
    # Coach Career Sim
    "coach_manager":       None,   # {name, nationality, philosophy}
    "coach_stage_idx":     -1,     # -1=not started, 0-7=stage, 8=ended
    "coach_awaiting_outcome": False,
    "coach_chosen_option": None,
    "coach_narrative":     "",
    "coach_choices":       [],
    "coach_outcome_text":  "",
    "coach_stats":         {"wins": 0, "trophies": 0, "players_developed": 0, "reputation": 0},
    "coach_history":       [],
    "coach_prefill":       None,   # {name, nationality} pre-filled from player sim transition
    # NFL Player Sim
    "nfl_player":           None,   # {name, position_group, style}
    "nfl_stage_idx":        -1,     # -1=not started, 0-7=stage, 8=ended
    "nfl_awaiting_outcome": False,
    "nfl_chosen_option":    None,
    "nfl_narrative":        "",
    "nfl_choices":          [],
    "nfl_outcome_text":     "",
    "nfl_stats":            {"touchdowns": 0, "yards": 0, "pro_bowls": 0, "super_bowls": 0},
    "nfl_history":          [],
    # NFL Coach Sim
    "nfl_coach_manager":       None,   # {name, philosophy}
    "nfl_coach_stage_idx":     -1,
    "nfl_coach_awaiting_outcome": False,
    "nfl_coach_chosen_option": None,
    "nfl_coach_narrative":     "",
    "nfl_coach_choices":       [],
    "nfl_coach_outcome_text":  "",
    "nfl_coach_stats":         {"wins": 0, "super_bowls": 0, "players_developed": 0, "reputation": 0},
    "nfl_coach_history":       [],
    "nfl_coach_prefill":       None,   # {name} pre-filled from NFL player sim transition
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

def generate_btf_questions(target: dict, all_players: list) -> list:
    """Generate 5 multiple-choice trivia questions about *target* player."""
    rng = random.Random()
    others = [p for p in all_players if p["name"] != target["name"]]
    name   = target["name"]
    career = target["career"]
    pool   = []

    # Nationality (easy)
    wrong_nats = list({p["nationality"] for p in others if p["nationality"] != target["nationality"]})
    rng.shuffle(wrong_nats)
    choices = wrong_nats[:3] + [target["nationality"]]
    rng.shuffle(choices)
    pool.append({"q": f"🌍 What is {name}'s nationality?",
                 "choices": choices, "correct": target["nationality"],
                 "category": "Nationality"})

    # Position group (easy)
    pos_groups = ["Forward", "Midfielder", "Defender", "Goalkeeper"]
    wrong_pos  = [p for p in pos_groups if p != target["position_group"]]
    choices    = wrong_pos[:3] + [target["position_group"]]
    rng.shuffle(choices)
    pool.append({"q": f"⚽ What position group does {name} play in?",
                 "choices": choices, "correct": target["position_group"],
                 "category": "Position"})

    # Club in a specific period (medium)
    if career:
        entry      = rng.choice(career)
        wrong_clubs = list({e["club"] for p in others for e in p["career"]
                            if e["club"] != entry["club"]})
        rng.shuffle(wrong_clubs)
        choices = wrong_clubs[:3] + [entry["club"]]
        rng.shuffle(choices)
        pool.append({"q": f"🏟️ Which club did {name} play for from {entry['years']}?",
                     "choices": choices, "correct": entry["club"],
                     "category": "Career Club"})

    # Number of career clubs (medium)
    n_clubs    = len(career)
    wrong_ns   = list({n for n in range(max(1, n_clubs - 3), n_clubs + 4) if n != n_clubs})
    rng.shuffle(wrong_ns)
    choices = [str(n) for n in wrong_ns[:3]] + [str(n_clubs)]
    rng.shuffle(choices)
    pool.append({"q": f"🔢 How many clubs has {name} played for in their career?",
                 "choices": choices, "correct": str(n_clubs),
                 "category": "Career Length"})

    # Main league (medium)
    main_lg     = get_top_league(target)
    known_lgs   = ["Premier League", "La Liga", "Serie A", "Bundesliga", "Ligue 1",
                   "MLS", "Saudi Pro League", "Eredivisie", "Primeira Liga"]
    wrong_lgs   = [l for l in known_lgs if l != main_lg]
    rng.shuffle(wrong_lgs)
    choices = wrong_lgs[:3] + [main_lg]
    rng.shuffle(choices)
    pool.append({"q": f"🏆 In which league did {name} spend the most time in their career?",
                 "choices": choices, "correct": main_lg,
                 "category": "Main League"})

    # World Cup (medium)
    wc      = get_meta(target, "world_cup_winner", False)
    correct_wc = "Yes" if wc else "No"
    pool.append({"q": f"🌍 Did {name} win the FIFA World Cup?",
                 "choices": ["Yes", "No"], "correct": correct_wc,
                 "category": "World Cup"})

    # Ballon d'Or count (hard — only if won at least one)
    ballon = target.get("ballon_dor", 0) or 0
    if ballon > 0:
        wrong_bs = list({b for b in [1, 2, 3, 4, 5, 6, 7, 8] if b != ballon})
        rng.shuffle(wrong_bs)
        choices = [str(b) for b in wrong_bs[:3]] + [str(ballon)]
        rng.shuffle(choices)
        pool.append({"q": f"🥇 How many Ballon d'Or awards has {name} won?",
                     "choices": choices, "correct": str(ballon),
                     "category": "Ballon d'Or"})

    # Birth decade (medium)
    decade      = (target["birth_year"] // 10) * 10
    wrong_dec   = [d for d in [1960, 1965, 1970, 1975, 1980, 1985, 1990, 1995, 2000]
                   if d != decade]
    rng.shuffle(wrong_dec)
    choices = [str(d) + "s" for d in wrong_dec[:3]] + [str(decade) + "s"]
    rng.shuffle(choices)
    pool.append({"q": f"🎂 Which decade was {name} born in?",
                 "choices": choices, "correct": str(decade) + "s",
                 "category": "Birth Decade"})

    # Current / last club (medium)
    curr = target.get("current_club", "")
    if curr:
        wrong_cc = list({p.get("current_club", "") for p in others
                         if p.get("current_club") and p.get("current_club") != curr})
        rng.shuffle(wrong_cc)
        choices = wrong_cc[:3] + [curr]
        rng.shuffle(choices)
        pool.append({"q": f"🔵 What is {name}'s current or most recent club?",
                     "choices": choices, "correct": curr,
                     "category": "Current Club"})

    # Pick 5: always lead with nationality (easy warm-up), then 4 random others
    rng.shuffle(pool)
    nat_q     = next((q for q in pool if q["category"] == "Nationality"), None)
    remainder = [q for q in pool if q["category"] != "Nationality"]
    selected  = ([nat_q] + remainder) if nat_q else pool
    return selected[:5]

def reset_btf(player: dict):
    pool = get_filtered() or PLAYERS
    st.session_state.btf_player    = player
    st.session_state.btf_questions = generate_btf_questions(player, pool)
    st.session_state.btf_q_idx     = 0
    st.session_state.btf_selected  = None
    st.session_state.btf_answers   = []
    st.session_state.btf_won       = False
    st.session_state.btf_gave_up   = False
    st.session_state.btf_input_key += 1

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
            mode_icon = {"Career": "🏟️", "Guesser": "🟩", "Trophy": "🏆", "Daily": "📅", "Beat": "⚔️"}.get(h["mode"], "🎮")
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
    with st.expander("Beat the Footballer"):
        st.markdown("""
- A star footballer challenges you  
- Answer 5 multiple-choice questions about their career  
- Get 3 or more right to **beat** them!  
- Max 1 000 pts for a perfect 5/5  
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
st.markdown("<p style='text-align:center;color:#aaa;font-size:1rem'>91 legendary footballers · 8 game modes · AI-powered career simulation</p>", unsafe_allow_html=True)
st.markdown("---")

tab_career, tab_fg, tab_tc, tab_daily, tab_stats, tab_ai, tab_btf, tab_coach, tab_nfl_player, tab_nfl_coach = st.tabs([
    "🏟️ Career Timeline",
    "🟩 Footballer Guesser",
    "🏆 Trophy Cabinet",
    "📅 Daily Challenge",
    "📊 Stats & Achievements",
    "🤖 AI Career Sim",
    "⚔️ Beat the Footballer",
    "🧑‍💼 Coach Career Sim",
    "🏈 NFL Player Sim",
    "🏈 NFL Head Coach",
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
    beat_wins    = sum(1 for h in st.session_state.history if h["won"] and h["mode"] == "Beat")

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
        {"icon": "⚔️", "name": "Giant Slayer",       "desc": "Beat a footballer 3 times",  "unlocked": beat_wins >= 3},
        {"icon": "🥊", "name": "Unbeatable",         "desc": "Beat 10 footballers",         "unlocked": beat_wins >= 10},
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
    {"idx": 0, "id": "youth",    "name": "Youth Academy",       "age": "16–18", "icon": "🌱"},
    {"idx": 1, "id": "debut",    "name": "Professional Debut",  "age": "18–21", "icon": "⚡"},
    {"idx": 2, "id": "rise",     "name": "Rising Star",         "age": "21–24", "icon": "📈"},
    {"idx": 3, "id": "breakout", "name": "Breakout Season",     "age": "24–26", "icon": "💥"},
    {"idx": 4, "id": "peak",     "name": "Peak Years",          "age": "26–29", "icon": "🏆"},
    {"idx": 5, "id": "prime",    "name": "Prime Dominance",     "age": "29–32", "icon": "👑"},
    {"idx": 6, "id": "veteran",  "name": "Veteran Phase",       "age": "32–36", "icon": "🎯"},
    {"idx": 7, "id": "final",    "name": "Final Chapter",       "age": "36–40", "icon": "🏁"},
]


def _stage_data(position_group: str) -> list:
    """Return list of (narrative, choice_a, choice_b) tuples per stage (8 total).
    Each choice is (text: str, stat_delta: dict).
    """
    if position_group == "Forward":
        return [
            # 0 – Youth Academy (16-18)
            (
                "{name} arrived at the academy as a pacy {style}, terrorising defenders in reserve fixtures. "
                "The first-team manager kept a close eye on this emerging talent.",
                ("Push for a first-team debut this season",                  {"goals": 4,  "assists": 2,  "trophies": 0, "caps": 0}),
                ("Accept a loan to a lower-league club for more minutes",    {"goals": 9,  "assists": 3,  "trophies": 0, "caps": 0}),
            ),
            # 1 – Professional Debut (18-21)
            (
                "Turning professional, {name}'s sharp movement and instinctive finishing attracted interest from across Europe. "
                "Two very different paths lay ahead.",
                ("Sign for a top-flight giant and fight for a squad role",   {"goals": 14, "assists": 8,  "trophies": 1, "caps": 5}),
                ("Choose a mid-table club for guaranteed first-team minutes", {"goals": 22, "assists": 10, "trophies": 0, "caps": 8}),
            ),
            # 2 – Rising Star (21-24)
            (
                "A prolific season has made {name} one of the hottest properties in world football. "
                "Champions League clubs are circling and the phone hasn't stopped ringing.",
                ("Join a Champions League contender",                        {"goals": 30, "assists": 15, "trophies": 2, "caps": 15}),
                ("Become the undisputed main man at an ambitious club",      {"goals": 45, "assists": 18, "trophies": 1, "caps": 20}),
            ),
            # 3 – Breakout Season (24-26)  ← NEW
            (
                "The footballing world is watching {name}. A spectacular individual campaign has produced record-breaking numbers "
                "and sparked a transfer frenzy. Two life-changing paths have emerged.",
                ("Stay and break the club scoring record before moving on",  {"goals": 38, "assists": 14, "trophies": 1, "caps": 12}),
                ("Accept a marquee transfer and prove brilliance in a new top flight", {"goals": 30, "assists": 16, "trophies": 2, "caps": 10}),
            ),
            # 4 – Peak Years (26-29)
            (
                "At 26, {name} is feared by every defence. A world-record offer arrives — "
                "but so does the chance to cement legendary status at a beloved club.",
                ("Accept the mega-money move to the wealthiest club",        {"goals": 42, "assists": 22, "trophies": 3, "caps": 20}),
                ("Stay loyal and chase the title with a beloved club",       {"goals": 55, "assists": 28, "trophies": 4, "caps": 25}),
            ),
            # 5 – Prime Dominance (29-32)  ← NEW
            (
                "At 29, {name} stands at the very pinnacle of the sport. Every metric confirms what fans already know — "
                "a generational talent defying gravity. Two epic challenges remain.",
                ("Lead the national team on an international mission — a World Cup or continental title", {"goals": 22, "assists": 18, "trophies": 2, "caps": 28}),
                ("Cement club immortality with back-to-back domestic and European crowns", {"goals": 38, "assists": 24, "trophies": 4, "caps": 14}),
            ),
            # 6 – Veteran Phase (32-36)
            (
                "32 and still dangerous, {name} has accumulated silverware many players only dream of. "
                "One final chapter in the top flight remains to be written.",
                ("Embrace a new challenge in MLS or the Saudi Pro League",   {"goals": 30, "assists": 12, "trophies": 1, "caps": 5}),
                ("Stay in the top flight and mentor the next generation",    {"goals": 28, "assists": 18, "trophies": 2, "caps": 10}),
            ),
            # 7 – Final Chapter (36-40)  ← NEW
            (
                "The curtain is drawing close on an extraordinary career. {name}'s name is already written in football's golden book. "
                "One final decision will shape the farewell.",
                ("Return to the boyhood club for an emotional homecoming season", {"goals": 10, "assists": 8,  "trophies": 1, "caps": 0}),
                ("Push on for one last trophy as a talismanic figure at a new club", {"goals": 14, "assists": 10, "trophies": 2, "caps": 0}),
            ),
        ]
    elif position_group == "Midfielder":
        return [
            # 0 – Youth Academy (16-18)
            (
                "{name} quickly stood out in the academy with a {style} game that made the coaches compare the youngster "
                "to midfield legends of the past.",
                ("Train extra hours on shooting and scoring",                {"goals": 5,  "assists": 6,  "trophies": 0, "caps": 0}),
                ("Focus on passing range, vision, and game management",      {"goals": 2,  "assists": 12, "trophies": 0, "caps": 0}),
            ),
            # 1 – Professional Debut (18-21)
            (
                "Two clubs made compelling offers. {name}'s ability to control the tempo of matches was already evident — "
                "but where to develop that talent best?",
                ("Sign for a glamour club as a squad midfielder",            {"goals": 8,  "assists": 14, "trophies": 1, "caps": 4}),
                ("Choose a team where {name} will be the heartbeat",         {"goals": 12, "assists": 20, "trophies": 0, "caps": 9}),
            ),
            # 2 – Rising Star (21-24)
            (
                "21 and flourishing, {name}'s range of passing and box-to-box energy are drawing national headlines. "
                "A pivotal transfer window opens.",
                ("Move to a top-four side fighting for the title",           {"goals": 18, "assists": 35, "trophies": 2, "caps": 18}),
                ("Lead the midfield at an ambitious club building for glory",{"goals": 25, "assists": 40, "trophies": 1, "caps": 22}),
            ),
            # 3 – Breakout Season (24-26)  ← NEW
            (
                "{name}'s vision and technique have made the back pages every week. A defining breakout campaign has earned rave reviews, "
                "and two compelling opportunities have arrived simultaneously.",
                ("Win Player of the Season and sign a bumper new deal",      {"goals": 18, "assists": 28, "trophies": 1, "caps": 14}),
                ("Accept a high-profile move to a title contender",          {"goals": 14, "assists": 32, "trophies": 2, "caps": 10}),
            ),
            # 4 – Peak Years (26-29)
            (
                "At 26, {name} is arguably the best midfielder in the league. A historic club wants their new midfield general "
                "and they're willing to pay.",
                ("Join the historic giant and chase the Champions League",   {"goals": 22, "assists": 42, "trophies": 3, "caps": 22}),
                ("Stay and break the all-time appearances record",           {"goals": 28, "assists": 50, "trophies": 3, "caps": 28}),
            ),
            # 5 – Prime Dominance (29-32)  ← NEW
            (
                "At 29, {name} is the fulcrum around which everything revolves. Captaincy beckons and legacy is being built game by game.",
                ("Captain your club to a historic league and cup double",    {"goals": 20, "assists": 44, "trophies": 3, "caps": 20}),
                ("Become the driving force behind your nation's deepest tournament run in decades", {"goals": 14, "assists": 38, "trophies": 2, "caps": 32}),
            ),
            # 6 – Veteran Phase (32-36)
            (
                "32 and still covering every blade of grass, {name}'s experience compensates for whatever edge of pace "
                "time has taken. The question now is legacy.",
                ("Move abroad to a new league for one last challenge",       {"goals": 12, "assists": 25, "trophies": 1, "caps": 8}),
                ("Stay in domestic football until the very last whistle",    {"goals": 15, "assists": 30, "trophies": 2, "caps": 12}),
            ),
            # 7 – Final Chapter (36-40)  ← NEW
            (
                "A storied midfield career is entering its final act. {name} reads the game as well as ever, even if the legs have slowed. "
                "Where does the last chapter unfold?",
                ("Return to the club where it all began for one last emotional season", {"goals": 8,  "assists": 20, "trophies": 1, "caps": 0}),
                ("Accept a player-coach role to pass on a lifetime of football wisdom", {"goals": 5,  "assists": 16, "trophies": 2, "caps": 0}),
            ),
        ]
    elif position_group == "Defender":
        return [
            # 0 – Youth Academy (16-18)
            (
                "{name} was a commanding {style} from day one of the academy, throwing themselves into every training "
                "session with fearless determination.",
                ("Develop as a ball-playing sweeper with attacking instincts",{"goals": 3, "assists": 5,  "trophies": 0, "caps": 0}),
                ("Master the fundamentals — positioning, heading, tackling", {"goals": 1, "assists": 3,  "trophies": 1, "caps": 0}),
            ),
            # 1 – Professional Debut (18-21)
            (
                "Defenders mature late, but {name} was ahead of schedule. Two clubs wanted to sign the young stopper — "
                "one a title contender, one desperate for defensive solidarity.",
                ("Join the title contender as a squad defender",             {"goals": 2, "assists": 8,  "trophies": 2, "caps": 4}),
                ("Anchor the defence at a mid-table club as undisputed no. 1",{"goals": 3, "assists": 10, "trophies": 0, "caps": 9}),
            ),
            # 2 – Rising Star (21-24)
            (
                "21 and reliable as a rock, {name} is now one of the most sought-after defenders on the continent. "
                "A powerhouse club wants to build their entire backline around this talent.",
                ("Sign for the powerhouse — elite level, intense competition",{"goals": 5, "assists": 15, "trophies": 3, "caps": 16}),
                ("Become the captain of a title-chasing side",               {"goals": 8, "assists": 20, "trophies": 2, "caps": 22}),
            ),
            # 3 – Breakout Season (24-26)  ← NEW
            (
                "{name} has become the most talked-about defender on the continent after a near-impenetrable season. "
                "Europe's elite are queuing up with proposals.",
                ("Lead a charge deep into the Champions League as the defensive cornerstone", {"goals": 6, "assists": 16, "trophies": 2, "caps": 14}),
                ("Sign for a rebuilding powerhouse who promise to build around {name}", {"goals": 8, "assists": 20, "trophies": 1, "caps": 10}),
            ),
            # 4 – Peak Years (26-29)
            (
                "At 26, {name} is at the peak of defensive powers. Clean sheets are a regular occurrence and "
                "a huge club arrives with a lavish offer.",
                ("Join the mega-club and play in the biggest matches",       {"goals": 5, "assists": 18, "trophies": 3, "caps": 22}),
                ("Become a club legend — captain them to an unlikely title", {"goals": 8, "assists": 22, "trophies": 4, "caps": 28}),
            ),
            # 5 – Prime Dominance (29-32)  ← NEW
            (
                "29 and utterly dominant. {name} is captaining teams to silverware, marshalling defences with telepathic leadership. "
                "Two landmark opportunities have emerged.",
                ("Skipper the national team to World Cup glory",             {"goals": 4, "assists": 14, "trophies": 3, "caps": 30}),
                ("Lead your club to an unprecedented clean-sheet record and title glory", {"goals": 7, "assists": 20, "trophies": 4, "caps": 16}),
            ),
            # 6 – Veteran Phase (32-36)
            (
                "32 and still a rock. Experience makes {name} even more dangerous — anticipation and positioning "
                "compensate for any reduction in pace.",
                ("Accept a final challenge in a top foreign league",         {"goals": 3, "assists": 10, "trophies": 1, "caps": 6}),
                ("See out the career in the domestic top flight",            {"goals": 4, "assists": 12, "trophies": 2, "caps": 10}),
            ),
            # 7 – Final Chapter (36-40)  ← NEW
            (
                "36 and still imposing. {name} has one final gift to give the game before hanging up the boots. "
                "How does the legend's story end?",
                ("Return to the community club roots for a poignant farewell season", {"goals": 2, "assists": 6,  "trophies": 1, "caps": 0}),
                ("Carry an emerging young club into a trophy final as the experienced guardian", {"goals": 3, "assists": 8, "trophies": 2, "caps": 0}),
            ),
        ]
    else:  # Goalkeeper
        return [
            # 0 – Youth Academy (16-18)
            (
                "At 16, {name} had the reflexes of a cat and the presence of a {style}. "
                "The goalkeeping coach predicted an international career from the very first training session.",
                ("Work obsessively on shot-stopping, reflexes and positioning",{"goals": 0, "assists": 0, "trophies": 1, "caps": 0}),
                ("Develop sweeper-keeper skills and precise distribution",    {"goals": 0, "assists": 2, "trophies": 0, "caps": 0}),
            ),
            # 1 – Professional Debut (18-21)
            (
                "{name} is 18 and ready for the professional stage. Goalkeepers need experience — "
                "but two very different paths are available.",
                ("Fight for a spot at a top-flight club's first team",        {"goals": 0, "assists": 2, "trophies": 1, "caps": 3}),
                ("Take a loan to a lower-league club for 200 games in two seasons",{"goals": 0, "assists": 4, "trophies": 0, "caps": 6}),
            ),
            # 2 – Rising Star (21-24)
            (
                "A string of brilliant performances has made {name} one of the most coveted keepers in Europe. "
                "Two clubs are desperate to sign them.",
                ("Join a Champions League regular at a premium price",        {"goals": 0, "assists": 5, "trophies": 3, "caps": 16}),
                ("Become the undisputed no. 1 at a passionate mid-table club",{"goals": 0, "assists": 8, "trophies": 2, "caps": 22}),
            ),
            # 3 – Breakout Season (24-26)  ← NEW
            (
                "{name}'s shot-stopping brilliance has drawn comparisons to the all-time greats. After a season of jaw-dropping saves, "
                "two landmark offers have materialised.",
                ("Win the Golden Glove and sign a bumper new deal at your current club", {"goals": 0, "assists": 4, "trophies": 2, "caps": 14}),
                ("Accept a transfer to a club where the Champions League is a guaranteed stage", {"goals": 0, "assists": 3, "trophies": 1, "caps": 10}),
            ),
            # 4 – Peak Years (26-29)
            (
                "26 and at the absolute peak of their powers, {name} is being talked about as the best goalkeeper "
                "in the world. A historic contract offer arrives.",
                ("Sign for the wealthiest club and target every trophy",      {"goals": 0, "assists": 6, "trophies": 4, "caps": 20}),
                ("Remain loyal and carry the beloved club to an unlikely title",{"goals": 0, "assists": 8, "trophies": 3, "caps": 26}),
            ),
            # 5 – Prime Dominance (29-32)  ← NEW
            (
                "29 and unquestionably the best goalkeeper in the world. {name} is as commanding in the dressing room as in the goal. "
                "Two monumental challenges beckon.",
                ("Lead the national team to the World Cup final as the last line of defence", {"goals": 0, "assists": 4, "trophies": 2, "caps": 30}),
                ("Mastermind a historic treble — league, cup, and Champions League in one season", {"goals": 0, "assists": 5, "trophies": 3, "caps": 14}),
            ),
            # 6 – Veteran Phase (32-36)
            (
                "32 is still young for a goalkeeper. {name} can realistically play at the top level for several more years — "
                "but where?",
                ("Move to a glamour league abroad for a new adventure",       {"goals": 0, "assists": 5, "trophies": 1, "caps": 5}),
                ("Stay as the evergreen no. 1 in the domestic top flight",    {"goals": 0, "assists": 6, "trophies": 2, "caps": 10}),
            ),
            # 7 – Final Chapter (36-40)  ← NEW
            (
                "Goalkeepers age like fine wine, and at 36 {name} is still proving the point. "
                "But the day of retirement is on the horizon. How does the final chapter read?",
                ("Return to the club where the story began — the prodigal no. 1 comes home", {"goals": 0, "assists": 3, "trophies": 1, "caps": 0}),
                ("Stay at the top as a shot-stopper-mentor hybrid, inspiring the next generation", {"goals": 0, "assists": 4, "trophies": 2, "caps": 0}),
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
    """Return (0-100 rating, badge label) based on accumulated stats (8-stage career)."""
    score = (
        stats["goals"] * 1.0
        + stats["assists"] * 0.8
        + stats["trophies"] * 15
        + stats["caps"] * 0.5
    )
    if score >= 560: return 97, "🐐 All-Time Legend"
    if score >= 440: return 93, "⭐ World-Class"
    if score >= 330: return 88, "🌟 Elite"
    if score >= 220: return 82, "📈 Very Good"
    if score >= 130: return 75, "✅ Solid Pro"
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

        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
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
        with btn_col2:
            if st.button("🧑‍💼 Continue as Coach", key="ai_to_coach"):
                st.session_state.coach_prefill          = {
                    "name":        player["name"],
                    "nationality": player["nationality"],
                }
                st.session_state.coach_manager          = None
                st.session_state.coach_stage_idx        = -1
                st.session_state.coach_awaiting_outcome = False
                st.session_state.coach_chosen_option    = None
                st.session_state.coach_narrative        = ""
                st.session_state.coach_choices          = []
                st.session_state.coach_outcome_text     = ""
                st.session_state.coach_stats            = {"wins": 0, "trophies": 0, "players_developed": 0, "reputation": 0}
                st.session_state.coach_history          = []
                st.rerun()

        if st.session_state.coach_prefill:
            st.info("🧑‍💼 Your coaching career is ready! Head to the **Coach Career Sim** tab to begin your managerial journey.")

# ══════════════════════════════════════════════════════════════════════════════
# COACH CAREER SIM — constants, helpers, tab rendering
# ══════════════════════════════════════════════════════════════════════════════

_COACH_PHILOSOPHIES = [
    "High-Press Gegenpressing",
    "Tiki-Taka Possession",
    "Counter-Attack Specialist",
    "Wing-Play Maestro",
    "Total Football",
    "Defensive Pragmatist",
    "High-Tempo Direct Play",
    "False-9 Innovator",
]

_COACH_STAGES = [
    {"idx": 0, "id": "grassroots",   "name": "Grassroots & Youth Coaching", "age": "30–35", "icon": "🌱"},
    {"idx": 1, "id": "assistant",    "name": "Assistant Coach Role",         "age": "35–38", "icon": "📋"},
    {"idx": 2, "id": "first_role",   "name": "First Head Coach Role",        "age": "38–42", "icon": "⚡"},
    {"idx": 3, "id": "mid_table",    "name": "Mid-Table Manager",            "age": "42–46", "icon": "📈"},
    {"idx": 4, "id": "title_chase",  "name": "Title Contender",              "age": "46–50", "icon": "💥"},
    {"idx": 5, "id": "elite",        "name": "Elite Club Manager",           "age": "50–55", "icon": "🏆"},
    {"idx": 6, "id": "international","name": "International Manager",        "age": "55–60", "icon": "👑"},
    {"idx": 7, "id": "legacy",       "name": "Legendary Final Chapter",      "age": "60+",   "icon": "🏁"},
]


def _coach_stage_data(philosophy: str) -> list:
    """Return list of (narrative, choice_a, choice_b) tuples for 8 coaching stages.
    Each choice is (text: str, stat_delta: dict) where stats are:
      wins, trophies, players_developed, reputation.
    """
    return [
        # 0 – Grassroots & Youth Coaching (30-35)
        (
            "After hanging up the boots, {name} took their first coaching badge and joined a local club's youth set-up. "
            "The {philosophy} philosophy was already taking shape on the training ground.",
            ("Focus on developing young talent — run an elite academy programme",
             {"wins": 10, "trophies": 0, "players_developed": 8, "reputation": 6}),
            ("Take charge of the reserve team and target a cup run to raise the profile",
             {"wins": 18, "trophies": 1, "players_developed": 3, "reputation": 10}),
        ),
        # 1 – Assistant Coach (35-38)
        (
            "An impressive stint in the youth ranks caught the attention of a professional club. "
            "{name} was offered an assistant role, learning the art of management from the dugout.",
            ("Learn from a world-renowned head coach at a top-flight club",
             {"wins": 22, "trophies": 2, "players_developed": 4, "reputation": 16}),
            ("Take the assistant role at an ambitious lower-league club with full tactical freedom",
             {"wins": 30, "trophies": 1, "players_developed": 6, "reputation": 18}),
        ),
        # 2 – First Head Coach Role (38-42)
        (
            "The moment had arrived. {name} was handed the keys to a club for the first time. "
            "The {philosophy} system was installed from day one — but the squad needed time to adapt.",
            ("Implement the system boldly and demand results from the start",
             {"wins": 38, "trophies": 2, "players_developed": 5, "reputation": 22}),
            ("Earn trust by building team spirit first, then gradually introduce the philosophy",
             {"wins": 32, "trophies": 1, "players_developed": 9, "reputation": 25}),
        ),
        # 3 – Mid-Table Manager (42-46)
        (
            "A strong first stint earned {name} a move to a more established club. "
            "The challenge now was punching above the club's weight — and turning heads across the continent.",
            ("Go all-in on an exciting young transfer policy to build for the future",
             {"wins": 44, "trophies": 2, "players_developed": 12, "reputation": 28}),
            ("Prioritise results and pragmatic tactics to secure European football for the first time",
             {"wins": 55, "trophies": 3, "players_developed": 5, "reputation": 32}),
        ),
        # 4 – Title Contender (46-50)
        (
            "A European finish attracted serious attention. {name} was now managing a genuine title contender, "
            "with real ambitions of silverware and continental glory on the agenda.",
            ("Challenge for the title and domestic cup double in one historic season",
             {"wins": 62, "trophies": 4, "players_developed": 8, "reputation": 38}),
            ("Target a deep Champions League run to put your name on the European map",
             {"wins": 50, "trophies": 3, "players_developed": 6, "reputation": 42}),
        ),
        # 5 – Elite Club Manager (50-55)
        (
            "Europe's elite came calling. {name} was appointed at one of the world's most scrutinised clubs, "
            "where only trophies and attractive {philosophy} football would satisfy the fanbase.",
            ("Win back-to-back league titles and reinforce your domestic dominance",
             {"wins": 80, "trophies": 5, "players_developed": 7, "reputation": 48}),
            ("Lead the club to an unprecedented Champions League triumph and become a continental legend",
             {"wins": 65, "trophies": 4, "players_developed": 6, "reputation": 55}),
        ),
        # 6 – International Manager (55-60)
        (
            "After trophy-laden club years, {name} accepted the call to manage the national team — "
            "the ultimate honour in football management.",
            ("Build a golden generation of young talent for a long-term World Cup project",
             {"wins": 40, "trophies": 2, "players_developed": 15, "reputation": 55}),
            ("Inspire an experienced squad to an immediate major tournament triumph",
             {"wins": 35, "trophies": 3, "players_developed": 8, "reputation": 60}),
        ),
        # 7 – Legendary Final Chapter (60+)
        (
            "At 60, {name}'s legacy was already assured. But one final chapter remained — "
            "a chance to cement a place among the all-time managerial greats.",
            ("Return to a former club for an emotional reunion and one last title push",
             {"wins": 30, "trophies": 2, "players_developed": 10, "reputation": 40}),
            ("Write football history by managing a club from the lower leagues to a trophy in record time",
             {"wins": 45, "trophies": 3, "players_developed": 18, "reputation": 50}),
        ),
    ]


def _coach_generate_stage(manager: dict, stage: dict, stats: dict, api_key: str) -> dict:
    """Return {narrative, choices: [str, str], stat_deltas: [dict, dict]}.
    Falls back to built-in templates when no API key or on error.
    """
    templates = _coach_stage_data(manager["philosophy"])
    tmpl_narr, tmpl_a, tmpl_b = templates[stage["idx"]]
    fallback = {
        "narrative":   tmpl_narr.format(name=manager["name"], philosophy=manager["philosophy"]),
        "choices":     [tmpl_a[0], tmpl_b[0]],
        "stat_deltas": [tmpl_a[1], tmpl_b[1]],
    }
    if not api_key:
        return fallback
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        stat_line = (
            f"Career stats so far: {stats['wins']} wins, {stats['trophies']} trophies, "
            f"{stats['players_developed']} players developed, {stats['reputation']} reputation points."
        ) if any(stats.values()) else ""
        prompt = (
            f"Create a coaching career stage for this manager:\n"
            f"Name: {manager['name']} | Nationality: {manager['nationality']} | "
            f"Philosophy: {manager['philosophy']}\n"
            f"Stage: {stage['name']} (Age {stage['age']})\n"
            f"{stat_line}\n\n"
            f"Respond in EXACTLY this format (keep each section to 1–2 sentences):\n"
            f"NARRATIVE: [dramatic coaching career narrative for this stage]\n"
            f"CHOICE_A: [{tmpl_a[0]}]\n"
            f"CHOICE_B: [{tmpl_b[0]}]"
        )
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": (
                    "You are a football management career narrator creating an engaging text-adventure game. "
                    "Be concise, dramatic, and use authentic football management details. "
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


def _coach_generate_outcome(manager: dict, stage: dict, choice_text: str, delta: dict, api_key: str) -> str:
    """Return outcome narrative string for a coaching stage choice."""
    parts = []
    if delta.get("wins"):              parts.append(f"{delta['wins']} wins")
    if delta.get("trophies"):          parts.append(f"{delta['trophies']} trophies")
    if delta.get("players_developed"): parts.append(f"{delta['players_developed']} players developed")
    if delta.get("reputation"):        parts.append(f"{delta['reputation']} reputation points")
    stat_str = ", ".join(parts) if parts else "invaluable experience"
    fallback = (
        f"A superb spell of management for {manager['name']}! "
        f"The decision paid off with {stat_str} earned across this stage of the coaching career."
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
                    "You are a football management career narrator. Write punchy, vivid outcome paragraphs."
                )},
                {"role": "user", "content": (
                    f"{manager['name']} ({manager['nationality']} manager, {manager['philosophy']}) "
                    f"chose: \"{choice_text}\"\n"
                    f"Stage: {stage['name']}\n"
                    f"Results: {stat_str}\n\n"
                    f"Write ONE paragraph (2–3 sentences) describing what happened. "
                    f"Be specific and dramatic. Do NOT start with the manager's name."
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


def _coach_career_rating(stats: dict) -> tuple[int, str]:
    """Return (0-100 rating, badge label) based on accumulated coaching stats."""
    score = (
        stats["wins"] * 0.6
        + stats["trophies"] * 18
        + stats["players_developed"] * 2.5
        + stats["reputation"] * 1.2
    )
    if score >= 850: return 99, "🐐 Greatest Manager of All Time"
    if score >= 650: return 95, "⭐ Legendary Manager"
    if score >= 480: return 90, "🌟 Elite Tactician"
    if score >= 330: return 83, "📈 Accomplished Manager"
    if score >= 200: return 74, "✅ Respected Coach"
    return 62, "🎓 Journeyman Manager"

# ══════════════════════════════════════════════════════════════════════════════
# TAB 8 — COACH CAREER SIM
# ══════════════════════════════════════════════════════════════════════════════
with tab_coach:
    st.markdown("## 🧑‍💼 Coach Career Simulator")
    st.markdown(
        "Build your managerial career from grassroots football all the way to international glory. "
        "Every decision shapes your tactical legacy — wins, trophies, players developed, and reputation."
    )
    if not st.session_state.openai_api_key:
        st.info(
            "💡 **Tip:** Enter your OpenAI API key in the sidebar to unlock AI-generated "
            "personalised narratives. The simulator works great with built-in story templates too!"
        )

    coach_stage_idx = st.session_state.coach_stage_idx
    coach_manager   = st.session_state.coach_manager
    coach_prefill   = st.session_state.coach_prefill

    # ── Manager creation form ─────────────────────────────────────────────────
    if coach_stage_idx == -1:
        if coach_prefill:
            st.success(
                f"🎉 Welcome to management, **{coach_prefill['name']}**! "
                f"Your playing days are over — now it's time to shape the beautiful game from the dugout. "
                f"Choose your coaching philosophy to begin."
            )

        st.markdown("### 📋 Create Your Manager")
        col_cf1, col_cf2 = st.columns(2)
        with col_cf1:
            _default_name = coach_prefill["name"] if coach_prefill else ""
            coach_name = st.text_input("Manager Name", value=_default_name, placeholder="e.g. Ana Ferreira", key="coach_name_input")
            coach_nat_options = sorted(list(FLAGS.keys()) + _AI_EXTRA_NATIONALITIES)
            _default_nat_idx = coach_nat_options.index(coach_prefill["nationality"]) if coach_prefill and coach_prefill["nationality"] in coach_nat_options else 0
            coach_nat = st.selectbox("Nationality", coach_nat_options, index=_default_nat_idx, key="coach_nat_input")
        with col_cf2:
            coach_philosophy = st.selectbox("Coaching Philosophy", _COACH_PHILOSOPHIES, key="coach_phil_input")

        if st.button("🚀 Start Coaching Career", key="coach_start"):
            if not coach_name.strip():
                st.warning("Please enter a manager name.")
            else:
                st.session_state.coach_manager = {
                    "name": coach_name.strip(),
                    "nationality": coach_nat,
                    "philosophy": coach_philosophy,
                }
                st.session_state.coach_prefill          = None
                st.session_state.coach_stage_idx        = 0
                st.session_state.coach_awaiting_outcome = False
                st.session_state.coach_chosen_option    = None
                st.session_state.coach_narrative        = ""
                st.session_state.coach_choices          = []
                st.session_state.coach_outcome_text     = ""
                st.session_state.coach_stats            = {"wins": 0, "trophies": 0, "players_developed": 0, "reputation": 0}
                st.session_state.coach_history          = []
                st.rerun()

    # ── Active coaching stage ─────────────────────────────────────────────────
    elif coach_stage_idx < len(_COACH_STAGES):
        stage   = _COACH_STAGES[coach_stage_idx]
        manager = st.session_state.coach_manager
        stats   = st.session_state.coach_stats
        api_key = st.session_state.openai_api_key

        st.markdown(f"### {stage['icon']} Stage {coach_stage_idx + 1} / {len(_COACH_STAGES)}: {stage['name']}  *(Age {stage['age']})*")
        st.progress(coach_stage_idx / len(_COACH_STAGES))

        # Live stats bar
        cs1, cs2, cs3, cs4 = st.columns(4)
        with cs1:
            st.metric("🏅 Wins",              stats["wins"])
        with cs2:
            st.metric("🏆 Trophies",          stats["trophies"])
        with cs3:
            st.metric("🌱 Players Developed", stats["players_developed"])
        with cs4:
            st.metric("⭐ Reputation",         stats["reputation"])

        st.markdown("---")

        # Generate narrative if not yet loaded for this stage
        if not st.session_state.coach_narrative:
            with st.spinner("✍️ Writing your coaching story…"):
                data = _coach_generate_stage(manager, stage, stats, api_key)
            st.session_state.coach_narrative = data["narrative"]
            st.session_state.coach_choices   = list(zip(data["choices"], data["stat_deltas"]))
            st.rerun()

        # Show narrative
        st.markdown(
            f'<div style="background:rgba(255,255,255,0.06);border-left:4px solid #ff8c00;'
            f'border-radius:10px;padding:16px 20px;margin-bottom:16px;font-size:1.05rem;color:#e0e0e0;">'
            f'{st.session_state.coach_narrative}</div>',
            unsafe_allow_html=True,
        )

        # ── Showing outcome ────────────────────────────────────────────────────
        if st.session_state.coach_awaiting_outcome:
            chosen_idx = st.session_state.coach_chosen_option
            choice_text, delta = st.session_state.coach_choices[chosen_idx]

            if not st.session_state.coach_outcome_text:
                with st.spinner("⚡ Simulating the outcome…"):
                    outcome = _coach_generate_outcome(manager, stage, choice_text, delta, api_key)
                st.session_state.coach_outcome_text = outcome
                st.rerun()

            st.markdown(f"**You chose:** *{choice_text}*")
            st.markdown(
                f'<div style="background:rgba(255,140,0,0.1);border-left:4px solid #ffc107;'
                f'border-radius:10px;padding:14px 20px;margin:10px 0;color:#e0e0e0;">'
                f'{st.session_state.coach_outcome_text}</div>',
                unsafe_allow_html=True,
            )

            gain_parts = []
            if delta.get("wins"):              gain_parts.append(f"🏅 +{delta['wins']} wins")
            if delta.get("trophies"):          gain_parts.append(f"🏆 +{delta['trophies']} trophies")
            if delta.get("players_developed"): gain_parts.append(f"🌱 +{delta['players_developed']} players")
            if delta.get("reputation"):        gain_parts.append(f"⭐ +{delta['reputation']} reputation")
            if gain_parts:
                st.markdown("**Stats earned:** " + "  ·  ".join(gain_parts))

            next_label = "▶️ Next Stage" if coach_stage_idx < len(_COACH_STAGES) - 1 else "🏁 Retire & See Legacy"
            if st.button(next_label, key="coach_next_stage"):
                for k, v in delta.items():
                    st.session_state.coach_stats[k] += v
                st.session_state.coach_history.append({
                    "stage":   stage["name"],
                    "choice":  choice_text,
                    "outcome": st.session_state.coach_outcome_text,
                    "delta":   delta,
                })
                st.session_state.coach_stage_idx        += 1
                st.session_state.coach_awaiting_outcome  = False
                st.session_state.coach_chosen_option     = None
                st.session_state.coach_narrative         = ""
                st.session_state.coach_choices           = []
                st.session_state.coach_outcome_text      = ""
                st.rerun()

        # ── Awaiting decision ──────────────────────────────────────────────────
        else:
            st.markdown("### 🤔 What do you do?")
            choices = st.session_state.coach_choices
            col_ca, col_cb = st.columns(2)
            with col_ca:
                if st.button(f"**A:** {choices[0][0]}", key="coach_choice_a", use_container_width=True):
                    st.session_state.coach_chosen_option    = 0
                    st.session_state.coach_awaiting_outcome = True
                    st.rerun()
            with col_cb:
                if st.button(f"**B:** {choices[1][0]}", key="coach_choice_b", use_container_width=True):
                    st.session_state.coach_chosen_option    = 1
                    st.session_state.coach_awaiting_outcome = True
                    st.rerun()

    # ── Career ended — legacy screen ──────────────────────────────────────────
    elif coach_stage_idx >= len(_COACH_STAGES):
        manager = st.session_state.coach_manager
        stats   = st.session_state.coach_stats
        rating, badge = _coach_career_rating(stats)
        flag = FLAGS.get(manager["nationality"], "🌍")

        st.markdown(f"## 🏁 {manager['name']} — Coaching Career Over")
        st.markdown(
            f'<div class="result-correct" style="font-size:1.6rem;background:linear-gradient(90deg,#7b3f00,#ff8c00);">'
            f'{badge} &nbsp; Career Rating: {rating} / 100'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.markdown(f"**{flag} {manager['nationality']} · {manager['philosophy']}**")

        # Final stats
        r1, r2, r3, r4 = st.columns(4)
        with r1: st.metric("🏅 Career Wins",        stats["wins"])
        with r2: st.metric("🏆 Trophies Won",        stats["trophies"])
        with r3: st.metric("🌱 Players Developed",   stats["players_developed"])
        with r4: st.metric("⭐ Total Reputation",     stats["reputation"])

        st.markdown("---")
        st.markdown("### 📖 Managerial Chronicle")
        for entry in st.session_state.coach_history:
            st.markdown(
                f'<div style="background:rgba(255,255,255,0.05);border-left:4px solid #ff8c00;'
                f'border-radius:8px;padding:12px 16px;margin:8px 0;">'
                f'<strong style="color:#ff8c00">{entry["stage"]}</strong><br>'
                f'<em style="color:#ffc107">Chose: {entry["choice"]}</em><br>'
                f'<span style="color:#ccc">{entry["outcome"]}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

        if st.button("🔄 Start a New Coaching Career", key="coach_restart"):
            st.session_state.coach_manager          = None
            st.session_state.coach_stage_idx        = -1
            st.session_state.coach_awaiting_outcome = False
            st.session_state.coach_chosen_option    = None
            st.session_state.coach_narrative        = ""
            st.session_state.coach_choices          = []
            st.session_state.coach_outcome_text     = ""
            st.session_state.coach_stats            = {"wins": 0, "trophies": 0, "players_developed": 0, "reputation": 0}
            st.session_state.coach_history          = []
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# TAB 7 — BEAT THE FOOTBALLER
# ══════════════════════════════════════════════════════════════════════════════
with tab_btf:
    st.markdown("## ⚔️ Beat the Footballer")
    st.markdown(
        "A legendary footballer challenges you to a career trivia showdown! "
        "Answer **5 questions** about their career — get **3 or more correct** to beat them!"
    )

    pool = get_filtered()

    col_btn_btf, _ = st.columns([1, 3])
    with col_btn_btf:
        if st.button("🎲 New Opponent", key="new_btf"):
            if pool:
                reset_btf(pick_random_player(pool))
            else:
                st.warning("No players match the current filters.")

    bp = st.session_state.btf_player

    if bp is None:
        st.info("👈 Click **New Opponent** to start a challenge!")
    else:
        questions  = st.session_state.btf_questions
        q_idx      = st.session_state.btf_q_idx
        answers    = st.session_state.btf_answers
        btf_gave_up = st.session_state.btf_gave_up
        flag_btf   = FLAGS.get(bp["nationality"], "🌍")

        correct          = sum(answers)
        answered         = len(answers)
        footballer_score = answered - correct

        # ── Opponent card ─────────────────────────────────────────────────────
        st.markdown(
            f'<div style="background:rgba(255,100,0,0.12);border:2px solid #ff6b00;'
            f'border-radius:14px;padding:16px 20px;margin:12px 0;">'
            f'<div style="font-size:1.4rem;font-weight:800;color:#ff8c00;">⚔️ Your Opponent</div>'
            f'<div style="font-size:1.2rem;color:white;margin-top:4px;">'
            f'{flag_btf} <strong>{bp["name"]}</strong></div>'
            f'<div style="color:#aaa;font-size:0.9rem;">'
            f'{bp["position_group"]} · {bp["nationality"]} · {bp.get("difficulty","?")} difficulty'
            f'</div></div>',
            unsafe_allow_html=True,
        )

        # ── Live score bar ────────────────────────────────────────────────────
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            st.markdown(
                f'<div class="score-box"><div class="score-val">{correct} ⚽</div>'
                f'<div class="score-lbl">You</div></div>',
                unsafe_allow_html=True,
            )
        with sc2:
            st.markdown(
                f'<div class="score-box"><div class="score-val">{answered} / 5</div>'
                f'<div class="score-lbl">Questions</div></div>',
                unsafe_allow_html=True,
            )
        with sc3:
            first_name = bp["name"].split()[0]
            st.markdown(
                f'<div class="daily-box"><div class="score-val">{footballer_score} ⚽</div>'
                f'<div class="score-lbl">{first_name}</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")

        # ── Game over (all 5 answered, or gave up) ────────────────────────────
        if q_idx >= len(questions) or btf_gave_up:
            if btf_gave_up:
                st.markdown(
                    f'<div class="result-wrong">🏳️ You gave up! {correct}/{answered} correct before quitting.</div>',
                    unsafe_allow_html=True,
                )
            elif correct >= 3:
                pts_map = {5: 1000, 4: 750, 3: 500}
                pts     = pts_map.get(correct, 500)
                st.markdown(
                    f'<div class="result-correct">🏆 You beat {bp["name"]}! {correct}/5 correct — +{pts} pts!</div>',
                    unsafe_allow_html=True,
                )
            else:
                pts_map = {2: 250, 1: 100, 0: 0}
                pts     = pts_map.get(correct, 0)
                msg     = f" — +{pts} pts for trying!" if pts > 0 else ""
                st.markdown(
                    f'<div class="result-wrong">😔 {bp["name"]} beat you! ({correct}/5 correct){msg}</div>',
                    unsafe_allow_html=True,
                )

            # Question review
            st.markdown("### 📋 Question Review")
            for i, (q_item, was_correct) in enumerate(zip(questions[:len(answers)], answers)):
                icon = "✅" if was_correct else "❌"
                st.markdown(f"**{icon} Q{i+1}: {q_item['q']}**")
                st.markdown(f"&nbsp;&nbsp;&nbsp;➜ Correct answer: **{q_item['correct']}**")

            if st.button("▶️ New Challenge", key="btf_play_again"):
                pool = get_filtered()
                if pool:
                    reset_btf(pick_random_player(pool))
                    st.rerun()

        # ── Showing feedback for current question ─────────────────────────────
        elif st.session_state.btf_selected is not None:
            q        = questions[q_idx]
            selected = st.session_state.btf_selected
            is_correct = (selected == q["correct"])

            st.markdown(f"### Q{q_idx + 1} / 5 — {q['category']}")
            st.markdown(f"#### {q['q']}")

            if is_correct:
                st.markdown(
                    f'<div class="result-correct">✅ Correct! The answer is <b>{q["correct"]}</b></div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="result-wrong">❌ Wrong! You said <b>{selected}</b> — '
                    f'the answer is <b>{q["correct"]}</b></div>',
                    unsafe_allow_html=True,
                )

            next_label = "▶️ Next Question" if q_idx < len(questions) - 1 else "🏁 See Results"
            if st.button(next_label, key="btf_next"):
                st.session_state.btf_answers.append(is_correct)
                st.session_state.btf_q_idx   += 1
                st.session_state.btf_selected  = None

                # Record stats when last question is answered
                new_q_idx  = st.session_state.btf_q_idx
                if new_q_idx >= len(questions):
                    new_correct = sum(st.session_state.btf_answers)
                    won         = new_correct >= 3
                    st.session_state.btf_won = won
                    if won:
                        pts = {5: 1000, 4: 750, 3: 500}.get(new_correct, 500)
                        st.session_state.total_score   += pts
                        st.session_state.rounds_played += 1
                        st.session_state.win_streak    += 1
                        st.session_state.best_streak    = max(
                            st.session_state.best_streak, st.session_state.win_streak
                        )
                        st.session_state.history.append(
                            {"mode": "Beat", "name": bp["name"], "won": True, "points": pts}
                        )
                    else:
                        pts = {2: 250, 1: 100, 0: 0}.get(new_correct, 0)
                        st.session_state.total_score   += pts
                        st.session_state.rounds_played += 1
                        st.session_state.win_streak     = 0
                        st.session_state.history.append(
                            {"mode": "Beat", "name": bp["name"], "won": False, "points": pts}
                        )
                st.rerun()

        # ── Awaiting answer for current question ──────────────────────────────
        else:
            q = questions[q_idx]
            st.markdown(f"### Q{q_idx + 1} / 5 — {q['category']}")
            st.markdown(f"#### {q['q']}")

            btn_cols = st.columns(2)
            for i, choice in enumerate(q["choices"]):
                with btn_cols[i % 2]:
                    if st.button(
                        choice,
                        key=f"btf_choice_{st.session_state.btf_input_key}_{q_idx}_{i}",
                        use_container_width=True,
                    ):
                        st.session_state.btf_selected = choice
                        st.rerun()

            st.markdown("---")
            col_quit, _ = st.columns([1, 3])
            with col_quit:
                if st.button("🏳️ Give Up", key="btf_giveup"):
                    st.session_state.btf_gave_up   = True
                    st.session_state.rounds_played += 1
                    st.session_state.win_streak     = 0
                    st.session_state.history.append(
                        {"mode": "Beat", "name": bp["name"], "won": False, "points": 0}
                    )
                    st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# NFL PLAYER SIM — constants, helpers, tab rendering
# ══════════════════════════════════════════════════════════════════════════════

_NFL_PLAYING_STYLES = [
    "Scrambling Dual-Threat",
    "Elite Pocket Passer",
    "Explosive Speed Back",
    "Power Runner",
    "Route Runner",
    "Deep Threat",
    "Pass Rusher",
    "Coverage Specialist",
    "Run Stopper",
    "Red Zone Target",
]

_NFL_POSITION_GROUPS = ["Quarterback", "Running Back", "Wide Receiver", "Defender"]

_NFL_CAREER_STAGES = [
    {"idx": 0, "id": "high_school", "name": "High School Star",       "age": "16–18", "icon": "🌱"},
    {"idx": 1, "id": "college",     "name": "College Career",          "age": "18–22", "icon": "🎓"},
    {"idx": 2, "id": "nfl_draft",   "name": "NFL Draft & Rookie Year", "age": "22–23", "icon": "⚡"},
    {"idx": 3, "id": "rising",      "name": "Rising Star",             "age": "23–25", "icon": "📈"},
    {"idx": 4, "id": "breakout",    "name": "Breakout Season",         "age": "25–27", "icon": "💥"},
    {"idx": 5, "id": "peak",        "name": "Peak Years",              "age": "27–30", "icon": "🏆"},
    {"idx": 6, "id": "veteran",     "name": "Veteran Phase",           "age": "30–34", "icon": "👑"},
    {"idx": 7, "id": "final",       "name": "Final Chapter",           "age": "34–38", "icon": "🏁"},
]


def _nfl_stage_data(position_group: str) -> list:
    """Return list of (narrative, choice_a, choice_b) tuples for 8 NFL career stages."""
    if position_group == "Quarterback":
        return [
            # 0 – High School Star (16-18)
            (
                "{name} lit up the Friday night lights as a {style}, breaking every state passing record in sight. "
                "College recruiters were lining up before junior year was over.",
                ("Commit early to a powerhouse program to compete for a national title",
                 {"touchdowns": 30, "yards": 4, "pro_bowls": 0, "super_bowls": 0}),
                ("Choose a program where you'll be the undisputed starter from day one",
                 {"touchdowns": 48, "yards": 6, "pro_bowls": 0, "super_bowls": 0}),
            ),
            # 1 – College Career (18-22)
            (
                "College scouts quickly confirmed what high school rivals already knew — {name} was special. "
                "A {style} who could read defences like a chess grandmaster, the Heisman conversation started in sophomore year.",
                ("Chase the national championship and build a trophy-laden college resume",
                 {"touchdowns": 64, "yards": 9, "pro_bowls": 0, "super_bowls": 0}),
                ("Declare early for the Draft after a record-breaking junior season",
                 {"touchdowns": 48, "yards": 7, "pro_bowls": 0, "super_bowls": 0}),
            ),
            # 2 – NFL Draft & Rookie Year (22-23)
            (
                "Draft night arrived and {name}'s name echoed through the arena. Every training camp rep confirmed "
                "this was a future franchise cornerstone, but the NFL learning curve is steep.",
                ("Start immediately — embrace the sink-or-swim challenge as the Week 1 starter",
                 {"touchdowns": 28, "yards": 4, "pro_bowls": 0, "super_bowls": 0}),
                ("Learn from a veteran QB for a season before taking the starting job",
                 {"touchdowns": 18, "yards": 3, "pro_bowls": 0, "super_bowls": 0}),
            ),
            # 3 – Rising Star (23-25)
            (
                "The league was on notice. {name}'s ability to extend plays and dissect zone coverages made every "
                "defensive coordinator lose sleep on Saturday nights.",
                ("Sign a prove-it contract extension and silence the doubters in a playoff push",
                 {"touchdowns": 62, "yards": 9, "pro_bowls": 1, "super_bowls": 0}),
                ("Request a trade to a contender with a stronger supporting cast",
                 {"touchdowns": 55, "yards": 8, "pro_bowls": 1, "super_bowls": 0}),
            ),
            # 4 – Breakout Season (25-27)
            (
                "The breakout campaign was historic. {name} led the league in passer rating, threw for 40-plus touchdowns, "
                "and finally silenced every remaining sceptic. Two massive paths lay ahead.",
                ("Lead the franchise deep into the playoffs — a Super Bowl run begins now",
                 {"touchdowns": 70, "yards": 10, "pro_bowls": 2, "super_bowls": 0}),
                ("Sign a record-breaking contract extension and become the face of the league",
                 {"touchdowns": 65, "yards": 10, "pro_bowls": 2, "super_bowls": 0}),
            ),
            # 5 – Peak Years (27-30)
            (
                "At 27, {name} was operating at the very pinnacle of the position. MVPs were discussed annually, "
                "and every deep playoff run seemed destined to end with a Lombardi Trophy.",
                ("Win back-to-back Super Bowls and cement an all-time legacy",
                 {"touchdowns": 90, "yards": 13, "pro_bowls": 3, "super_bowls": 2}),
                ("Sacrifice individual stats to run a system that maximises team wins",
                 {"touchdowns": 72, "yards": 11, "pro_bowls": 2, "super_bowls": 1}),
            ),
            # 6 – Veteran Phase (30-34)
            (
                "30 and still commanding, {name} led every film session and owned every two-minute drill. "
                "Experience now compensated for the half-step of athleticism time had taken.",
                ("Chase one final ring with a legitimate Super Bowl contender",
                 {"touchdowns": 68, "yards": 9, "pro_bowls": 2, "super_bowls": 1}),
                ("Stay with the beloved franchise and mentor the next generation of signal-callers",
                 {"touchdowns": 58, "yards": 8, "pro_bowls": 1, "super_bowls": 0}),
            ),
            # 7 – Final Chapter (34-38)
            (
                "Father Time waits for no quarterback, but {name} had rewritten what was possible. "
                "One final act remained to be written before the cleats came off.",
                ("Return to the franchise where it all started for an emotional farewell season",
                 {"touchdowns": 35, "yards": 5, "pro_bowls": 1, "super_bowls": 0}),
                ("Join a contender as a savvy veteran and push for a storybook championship exit",
                 {"touchdowns": 42, "yards": 6, "pro_bowls": 1, "super_bowls": 1}),
            ),
        ]
    elif position_group == "Running Back":
        return [
            # 0 – High School Star (16-18)
            (
                "Friday nights belonged to {name}. A {style} who made varsity defenders look like they were "
                "standing still, the offers flooded in before sophomore year ended.",
                ("Commit to the top recruiting class and chase a national title",
                 {"touchdowns": 40, "yards": 5, "pro_bowls": 0, "super_bowls": 0}),
                ("Choose the program that promises immediate carries and full feature-back usage",
                 {"touchdowns": 55, "yards": 7, "pro_bowls": 0, "super_bowls": 0}),
            ),
            # 1 – College Career (18-22)
            (
                "The Heisman was handed over in a landslide. {name}'s combination of vision, burst, and physicality "
                "made college defenders look like helpless cones on a practice field.",
                ("Stay all four years, become a program legend, and perfect the craft",
                 {"touchdowns": 72, "yards": 10, "pro_bowls": 0, "super_bowls": 0}),
                ("Declare after three seasons while at the absolute peak of college form",
                 {"touchdowns": 56, "yards": 8, "pro_bowls": 0, "super_bowls": 0}),
            ),
            # 2 – NFL Draft & Rookie Year (22-23)
            (
                "Selected in the first round, {name} arrived to an expectant fanbase ready to transform "
                "the ground game. The NFL grind was real, but the talent was undeniable.",
                ("Take the starting role from Week 1 and earn Offensive Rookie of the Year",
                 {"touchdowns": 18, "yards": 4, "pro_bowls": 0, "super_bowls": 0}),
                ("Ease into a committee backfield and absorb the pro game for a season",
                 {"touchdowns": 10, "yards": 3, "pro_bowls": 0, "super_bowls": 0}),
            ),
            # 3 – Rising Star (23-25)
            (
                "{name} was racking up 1,500-yard seasons and making the Pro Bowl feel like a formality. "
                "The league was witnessing a generational back in full flight.",
                ("Demand a feature-back workload and chase a 2,000-yard season",
                 {"touchdowns": 44, "yards": 9, "pro_bowls": 2, "super_bowls": 0}),
                ("Stay versatile — pass-catching duties added a new lethal dimension",
                 {"touchdowns": 36, "yards": 8, "pro_bowls": 1, "super_bowls": 0}),
            ),
            # 4 – Breakout Season (25-27)
            (
                "The breakout campaign had stat lines that felt fictional. {name} rushed for over 2,000 yards, "
                "scored 20-plus touchdowns, and was the undisputed best player on the planet.",
                ("Capitalise on the monster year with a record-setting running back contract",
                 {"touchdowns": 50, "yards": 10, "pro_bowls": 2, "super_bowls": 0}),
                ("Join a powerhouse offence as the final piece to push for a Super Bowl",
                 {"touchdowns": 42, "yards": 8, "pro_bowls": 2, "super_bowls": 1}),
            ),
            # 5 – Peak Years (27-30)
            (
                "At 27, {name} was at the intersection of peak athleticism and veteran savvy. "
                "Every carry was a masterclass in patience, power, and instinct.",
                ("Lead the franchise to a Super Bowl and etch the name in Canton stone",
                 {"touchdowns": 52, "yards": 9, "pro_bowls": 3, "super_bowls": 1}),
                ("Chase a second massive contract while running backs' windows remain open",
                 {"touchdowns": 48, "yards": 8, "pro_bowls": 2, "super_bowls": 0}),
            ),
            # 6 – Veteran Phase (30-34)
            (
                "30 is ancient for running backs, but {name} defied every rule. A reduced but explosive workload "
                "kept the defence honest and the highlights coming.",
                ("Pivot to a committee role that prolongs the career and chases rings",
                 {"touchdowns": 28, "yards": 5, "pro_bowls": 1, "super_bowls": 1}),
                ("Sign a one-year prove-it deal and chase a final Pro Bowl appearance",
                 {"touchdowns": 24, "yards": 4, "pro_bowls": 1, "super_bowls": 0}),
            ),
            # 7 – Final Chapter (34-38)
            (
                "Few running backs reached 34 still contributing at an elite level. {name} was the exception "
                "that proved every rule — and the story deserved a worthy final chapter.",
                ("Return to the team that drafted you for a sentimental farewell season",
                 {"touchdowns": 14, "yards": 2, "pro_bowls": 0, "super_bowls": 0}),
                ("Sign with a Super Bowl favourite as a veteran change-of-pace back for one last ring",
                 {"touchdowns": 16, "yards": 3, "pro_bowls": 0, "super_bowls": 1}),
            ),
        ]
    elif position_group == "Wide Receiver":
        return [
            # 0 – High School Star (16-18)
            (
                "The combination of {name}'s {style} route-running and sideline-threatening speed made "
                "college coaches drive hundreds of miles just to watch a practice.",
                ("Commit to a pass-heavy Air Raid programme to maximise receiving stats",
                 {"touchdowns": 38, "yards": 6, "pro_bowls": 0, "super_bowls": 0}),
                ("Choose a storied program with NFL pipeline pedigree to sharpen every skill",
                 {"touchdowns": 28, "yards": 5, "pro_bowls": 0, "super_bowls": 0}),
            ),
            # 1 – College Career (18-22)
            (
                "{name}'s route tree read like a doctoral thesis on deception. By junior year the name was "
                "synonymous with uncoverable, and mock drafts were debating top-five or top-ten.",
                ("Stack the Biletnikoff Award on the resume with a record-breaking senior season",
                 {"touchdowns": 66, "yards": 10, "pro_bowls": 0, "super_bowls": 0}),
                ("Declare early and begin turning elite college tape into an NFL contract",
                 {"touchdowns": 50, "yards": 8, "pro_bowls": 0, "super_bowls": 0}),
            ),
            # 2 – NFL Draft & Rookie Year (22-23)
            (
                "Selected in the first round and handed a number jersey already selling merchandise, "
                "{name} arrived to immediate expectations. The NFL cornerbacks were the sternest test yet.",
                ("Attack the starting role aggressively — WR1 from the jump",
                 {"touchdowns": 12, "yards": 4, "pro_bowls": 0, "super_bowls": 0}),
                ("Build chemistry with the QB over a full season to develop a telepathic connection",
                 {"touchdowns": 8, "yards": 3, "pro_bowls": 0, "super_bowls": 0}),
            ),
            # 3 – Rising Star (23-25)
            (
                "1,200-yard seasons and double-digit touchdowns had become the baseline expectation. "
                "{name} was making Pro Bowl appearances look like a formality.",
                ("Demand WR1 usage and a top-of-market extension at the position",
                 {"touchdowns": 30, "yards": 9, "pro_bowls": 1, "super_bowls": 0}),
                ("Accept a secondary role on a loaded contender to chase a Super Bowl early",
                 {"touchdowns": 22, "yards": 6, "pro_bowls": 0, "super_bowls": 1}),
            ),
            # 4 – Breakout Season (25-27)
            (
                "The breakout year cemented the case for best receiver in football. {name} posted "
                "a 100-catch, 1,600-yard, 14-touchdown campaign that left cornerbacks humbled.",
                ("Sign a record-breaking wide receiver contract and raise the position's market",
                 {"touchdowns": 36, "yards": 11, "pro_bowls": 2, "super_bowls": 0}),
                ("Join an elite quarterback to build an all-time passing duo",
                 {"touchdowns": 40, "yards": 10, "pro_bowls": 2, "super_bowls": 1}),
            ),
            # 5 – Peak Years (27-30)
            (
                "At 27, {name} owned every cornerback matchup on the planet. Route-running had become "
                "an art form and the touchdowns were arriving in highlight packages every Sunday.",
                ("Chase back-to-back Super Bowl rings as the top offensive weapon",
                 {"touchdowns": 48, "yards": 12, "pro_bowls": 3, "super_bowls": 2}),
                ("Win an offensive MVP and become the face of the highest-scoring offence in history",
                 {"touchdowns": 54, "yards": 14, "pro_bowls": 3, "super_bowls": 0}),
            ),
            # 6 – Veteran Phase (30-34)
            (
                "30 and still separating at will, {name} had evolved from a speed merchant into "
                "the most intelligent route runner in the game. Younger defenders were in a classroom.",
                ("Mentor a rising receiver alongside regular starting duties",
                 {"touchdowns": 30, "yards": 8, "pro_bowls": 1, "super_bowls": 0}),
                ("Chase one final big contract while the production still justifies it",
                 {"touchdowns": 26, "yards": 7, "pro_bowls": 1, "super_bowls": 0}),
            ),
            # 7 – Final Chapter (34-38)
            (
                "The journey that started under Friday night lights was nearing its final act. "
                "{name}'s hands and savvy remained elite even as the recovery days got longer.",
                ("Return to the franchise where the legacy was built for one last season",
                 {"touchdowns": 14, "yards": 3, "pro_bowls": 0, "super_bowls": 0}),
                ("Join a Super Bowl contender as a veteran leader for one storybook ring",
                 {"touchdowns": 16, "yards": 4, "pro_bowls": 0, "super_bowls": 1}),
            ),
        ]
    else:  # Defender
        return [
            # 0 – High School Star (16-18)
            (
                "{name} was a {style} nightmare for every opposing offence from the very first kick-off. "
                "College recruiters called it the most dominant high-school defensive performance in a decade.",
                ("Join a powerhouse programme known for producing NFL defensive talent",
                 {"touchdowns": 5, "yards": 1, "pro_bowls": 0, "super_bowls": 0}),
                ("Choose a programme where you'll be the defensive centrepiece from day one",
                 {"touchdowns": 8, "yards": 2, "pro_bowls": 0, "super_bowls": 0}),
            ),
            # 1 – College Career (18-22)
            (
                "The Butkus and Bednarik Award committees were watching every snap. {name} was turning "
                "college offences into a personal highlight reel — sacks, picks, and forced fumbles galore.",
                ("Stay all four years to win the Butkus Award and complete a degree",
                 {"touchdowns": 10, "yards": 2, "pro_bowls": 0, "super_bowls": 0}),
                ("Declare early with the highest defensive prospect grade in the class",
                 {"touchdowns": 6, "yards": 1, "pro_bowls": 0, "super_bowls": 0}),
            ),
            # 2 – NFL Draft & Rookie Year (22-23)
            (
                "Drafted in the top ten, {name} arrived to a defence hungry for a difference-maker. "
                "The learning curve was real — but the impact was immediate.",
                ("Start immediately and earn Defensive Rookie of the Year",
                 {"touchdowns": 4, "yards": 1, "pro_bowls": 0, "super_bowls": 0}),
                ("Come off the bench and absorb the complexity of the professional game for a season",
                 {"touchdowns": 2, "yards": 0, "pro_bowls": 0, "super_bowls": 0}),
            ),
            # 3 – Rising Star (23-25)
            (
                "Quarterbacks were checking down before {name} could even get out of their stance. "
                "The annual Pro Bowl invitations were becoming a formality.",
                ("Anchor the defence as the defensive captain and chase a Defensive Player of the Year award",
                 {"touchdowns": 10, "yards": 2, "pro_bowls": 2, "super_bowls": 0}),
                ("Request a move to a defensive powerhouse scheme that maximises every strength",
                 {"touchdowns": 8, "yards": 2, "pro_bowls": 1, "super_bowls": 0}),
            ),
            # 4 – Breakout Season (25-27)
            (
                "Defensive Player of the Year. The award was unanimous and deserved. "
                "{name}'s season-long dominance had completely altered how the opposition game-planned.",
                ("Win a Super Bowl as the anchor of the league's most feared defence",
                 {"touchdowns": 12, "yards": 2, "pro_bowls": 2, "super_bowls": 1}),
                ("Sign a record-breaking defensive contract and become the highest-paid player at the position",
                 {"touchdowns": 10, "yards": 2, "pro_bowls": 2, "super_bowls": 0}),
            ),
            # 5 – Peak Years (27-30)
            (
                "At 27, {name} was the last piece any Super Bowl contender wanted to face. "
                "Every play call began with a plan to account for the defensive nightmare on the field.",
                ("Lead a dynasty defence to back-to-back championships",
                 {"touchdowns": 14, "yards": 3, "pro_bowls": 3, "super_bowls": 2}),
                ("Become the defensive cornerstone of a franchise rebuild and lift a long-suffering fanbase",
                 {"touchdowns": 12, "yards": 2, "pro_bowls": 2, "super_bowls": 1}),
            ),
            # 6 – Veteran Phase (30-34)
            (
                "30 and still causing chaos on every play. {name}'s football IQ and film study had become "
                "almost supernatural — anticipating plays before the snap.",
                ("Pivot to a mentoring role while still starting and chasing one more ring",
                 {"touchdowns": 8, "yards": 1, "pro_bowls": 1, "super_bowls": 1}),
                ("Chase a final Defensive Player of the Year award to bookend an elite career",
                 {"touchdowns": 10, "yards": 2, "pro_bowls": 2, "super_bowls": 0}),
            ),
            # 7 – Final Chapter (34-38)
            (
                "The career that had terrorised quarterbacks and running backs across two decades was "
                "drawing to a close. {name}'s farewell would be written on the biggest stage possible.",
                ("Return to the city where the legend was born for a final home-crowd goodbye",
                 {"touchdowns": 4, "yards": 1, "pro_bowls": 0, "super_bowls": 0}),
                ("Sign with a Super Bowl contender and chase one last ring before hanging up the pads",
                 {"touchdowns": 6, "yards": 1, "pro_bowls": 0, "super_bowls": 1}),
            ),
        ]


def _nfl_generate_stage(player: dict, stage: dict, stats: dict, api_key: str) -> dict:
    """Return {narrative, choices: [str, str], stat_deltas: [dict, dict]}."""
    templates = _nfl_stage_data(player["position_group"])
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
            f"Career stats so far: {stats['touchdowns']} touchdowns, {stats['yards']}k yards, "
            f"{stats['pro_bowls']} Pro Bowls, {stats['super_bowls']} Super Bowls."
        ) if stats["touchdowns"] + stats["yards"] + stats["pro_bowls"] + stats["super_bowls"] > 0 else ""
        prompt = (
            f"Create a career stage for this NFL player:\\n"
            f"Name: {player['name']} | Position: {player['position_group']} | Style: {player['style']}\\n"
            f"Stage: {stage['name']} (Age {stage['age']})\\n"
            f"{stat_line}\\n\\n"
            f"Respond in EXACTLY this format (keep each section to 1-2 sentences):\\n"
            f"NARRATIVE: [dramatic NFL career narrative for this stage]\\n"
            f"CHOICE_A: [{tmpl_a[0]}]\\n"
            f"CHOICE_B: [{tmpl_b[0]}]"
        )
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": (
                    "You are an NFL career narrator creating an engaging text-adventure game. "
                    "Be concise, dramatic, and use authentic NFL details. "
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


def _nfl_generate_outcome(player: dict, stage: dict, choice_text: str, delta: dict, api_key: str) -> str:
    """Return outcome narrative string for an NFL career stage choice."""
    parts = []
    if delta.get("touchdowns"): parts.append(f"{delta['touchdowns']} touchdowns")
    if delta.get("yards"):      parts.append(f"{delta['yards']}k yards")
    if delta.get("pro_bowls"):  parts.append(f"{delta['pro_bowls']} Pro Bowl selections")
    if delta.get("super_bowls"):parts.append(f"{delta['super_bowls']} Super Bowl rings")
    stat_str = ", ".join(parts) if parts else "valuable experience"
    fallback = (
        f"A tremendous stretch for {player['name']}! "
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
                    "You are an NFL career narrator. Write punchy, vivid outcome paragraphs."
                )},
                {"role": "user", "content": (
                    f"{player['name']} (NFL {player['position_group']}) chose: \"{choice_text}\"\\n"
                    f"Stage: {stage['name']}\\n"
                    f"Results: {stat_str}\\n\\n"
                    f"Write ONE paragraph (2-3 sentences) describing what happened. "
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


def _nfl_career_rating(stats: dict) -> tuple[int, str]:
    """Return (0-100 rating, badge label) based on accumulated NFL career stats."""
    score = (
        stats["touchdowns"] * 1.5
        + stats["yards"] * 2.0
        + stats["pro_bowls"] * 30
        + stats["super_bowls"] * 50
    )
    if score >= 700: return 99, "\U0001f410 All-Time NFL Legend"
    if score >= 530: return 95, "\u2b50 Hall of Fame Lock"
    if score >= 380: return 90, "\U0001f31f Elite Pro"
    if score >= 260: return 83, "\U0001f4c8 Multiple Pro Bowler"
    if score >= 160: return 75, "\u2705 Solid NFL Starter"
    return 65, "\U0001f393 NFL Journeyman"


# ── NFL Player Sim: tab rendering ─────────────────────────────────────────────
with tab_nfl_player:
    st.markdown("## \U0001f3c8 NFL Player Career Simulator")
    st.markdown(
        "Create your own NFL player and guide them from high school all the way to retirement. "
        "Every decision shapes your legacy — touchdowns, yards, Pro Bowls, and Super Bowl rings."
    )
    if not st.session_state.openai_api_key:
        st.info(
            "\U0001f4a1 **Tip:** Enter your OpenAI API key in the sidebar to unlock AI-generated "
            "personalised narratives. The simulator works great with built-in story templates too!"
        )

    nfl_stage_idx = st.session_state.nfl_stage_idx
    nfl_player    = st.session_state.nfl_player

    if nfl_stage_idx == -1:
        st.markdown("### \U0001f3c8 Create Your NFL Player")
        col_nf1, col_nf2 = st.columns(2)
        with col_nf1:
            nfl_name  = st.text_input("Player Name", placeholder="e.g. Marcus Rivers", key="nfl_name_input")
            nfl_pos   = st.selectbox("Position Group", _NFL_POSITION_GROUPS, key="nfl_pos_input")
        with col_nf2:
            nfl_style = st.selectbox("Playing Style", _NFL_PLAYING_STYLES, key="nfl_style_input")

        if st.button("\U0001f680 Start NFL Career", key="nfl_start"):
            if not nfl_name.strip():
                st.warning("Please enter a player name.")
            else:
                st.session_state.nfl_player = {
                    "name":           nfl_name.strip(),
                    "position_group": nfl_pos,
                    "style":          nfl_style,
                }
                st.session_state.nfl_stage_idx        = 0
                st.session_state.nfl_awaiting_outcome = False
                st.session_state.nfl_chosen_option    = None
                st.session_state.nfl_narrative        = ""
                st.session_state.nfl_choices          = []
                st.session_state.nfl_outcome_text     = ""
                st.session_state.nfl_stats            = {"touchdowns": 0, "yards": 0, "pro_bowls": 0, "super_bowls": 0}
                st.session_state.nfl_history          = []
                st.rerun()

    elif nfl_stage_idx < len(_NFL_CAREER_STAGES):
        stage   = _NFL_CAREER_STAGES[nfl_stage_idx]
        player  = st.session_state.nfl_player
        stats   = st.session_state.nfl_stats
        api_key = st.session_state.openai_api_key

        st.markdown(f"### {stage['icon']} Stage {nfl_stage_idx + 1} / {len(_NFL_CAREER_STAGES)}: {stage['name']}  *(Age {stage['age']})*")
        st.progress(nfl_stage_idx / len(_NFL_CAREER_STAGES))

        ns1, ns2, ns3, ns4 = st.columns(4)
        with ns1: st.metric("\U0001f3c8 Touchdowns",   stats["touchdowns"])
        with ns2: st.metric("\U0001f4cf Yards (000s)", stats["yards"])
        with ns3: st.metric("\u2b50 Pro Bowls",        stats["pro_bowls"])
        with ns4: st.metric("\U0001f48d Super Bowls",  stats["super_bowls"])

        st.markdown("---")

        if not st.session_state.nfl_narrative:
            with st.spinner("\u270d\ufe0f Writing your NFL story\u2026"):
                data = _nfl_generate_stage(player, stage, stats, api_key)
            st.session_state.nfl_narrative = data["narrative"]
            st.session_state.nfl_choices   = list(zip(data["choices"], data["stat_deltas"]))
            st.rerun()

        st.markdown(
            f'<div style="background:rgba(255,255,255,0.06);border-left:4px solid #005a8e;'
            f'border-radius:10px;padding:16px 20px;margin-bottom:16px;font-size:1.05rem;color:#e0e0e0;">'
            f'{st.session_state.nfl_narrative}</div>',
            unsafe_allow_html=True,
        )

        if st.session_state.nfl_awaiting_outcome:
            chosen_idx = st.session_state.nfl_chosen_option
            choice_text, delta = st.session_state.nfl_choices[chosen_idx]

            if not st.session_state.nfl_outcome_text:
                with st.spinner("\u26a1 Simulating the outcome\u2026"):
                    outcome = _nfl_generate_outcome(player, stage, choice_text, delta, api_key)
                st.session_state.nfl_outcome_text = outcome
                st.rerun()

            st.markdown(f"**You chose:** *{choice_text}*")
            st.markdown(
                f'<div style="background:rgba(0,90,142,0.1);border-left:4px solid #ffc107;'
                f'border-radius:10px;padding:14px 20px;margin:10px 0;color:#e0e0e0;">'
                f'{st.session_state.nfl_outcome_text}</div>',
                unsafe_allow_html=True,
            )

            gain_parts = []
            if delta.get("touchdowns"): gain_parts.append(f"\U0001f3c8 +{delta['touchdowns']} TDs")
            if delta.get("yards"):      gain_parts.append(f"\U0001f4cf +{delta['yards']}k yards")
            if delta.get("pro_bowls"):  gain_parts.append(f"\u2b50 +{delta['pro_bowls']} Pro Bowls")
            if delta.get("super_bowls"):gain_parts.append(f"\U0001f48d +{delta['super_bowls']} Super Bowls")
            if gain_parts:
                st.markdown("**Stats earned:** " + "  \u00b7  ".join(gain_parts))

            next_label = "\u25b6\ufe0f Next Stage" if nfl_stage_idx < len(_NFL_CAREER_STAGES) - 1 else "\U0001f3c1 Retire & See Legacy"
            if st.button(next_label, key="nfl_next_stage"):
                for k, v in delta.items():
                    st.session_state.nfl_stats[k] += v
                st.session_state.nfl_history.append({
                    "stage":   stage["name"],
                    "choice":  choice_text,
                    "outcome": st.session_state.nfl_outcome_text,
                    "delta":   delta,
                })
                st.session_state.nfl_stage_idx        += 1
                st.session_state.nfl_awaiting_outcome  = False
                st.session_state.nfl_chosen_option     = None
                st.session_state.nfl_narrative         = ""
                st.session_state.nfl_choices           = []
                st.session_state.nfl_outcome_text      = ""
                st.rerun()

        else:
            st.markdown("### \U0001f914 What do you do?")
            choices = st.session_state.nfl_choices
            col_na, col_nb = st.columns(2)
            with col_na:
                if st.button(f"**A:** {choices[0][0]}", key="nfl_choice_a", use_container_width=True):
                    st.session_state.nfl_chosen_option    = 0
                    st.session_state.nfl_awaiting_outcome = True
                    st.rerun()
            with col_nb:
                if st.button(f"**B:** {choices[1][0]}", key="nfl_choice_b", use_container_width=True):
                    st.session_state.nfl_chosen_option    = 1
                    st.session_state.nfl_awaiting_outcome = True
                    st.rerun()

    elif nfl_stage_idx >= len(_NFL_CAREER_STAGES):
        player = st.session_state.nfl_player
        stats  = st.session_state.nfl_stats
        rating, badge = _nfl_career_rating(stats)

        st.markdown(f"## \U0001f3c1 {player['name']} \u2014 NFL Career Over")
        st.markdown(
            f'<div class="result-correct" style="font-size:1.6rem;background:linear-gradient(90deg,#003366,#005a8e);">'
            f'{badge} &nbsp; Career Rating: {rating} / 100'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.markdown(f"**{player['position_group']} \u00b7 {player['style']}**")

        n1, n2, n3, n4 = st.columns(4)
        with n1: st.metric("\U0001f3c8 Career TDs",       stats["touchdowns"])
        with n2: st.metric("\U0001f4cf Career Yards (k)", stats["yards"])
        with n3: st.metric("\u2b50 Pro Bowls",             stats["pro_bowls"])
        with n4: st.metric("\U0001f48d Super Bowls",       stats["super_bowls"])

        st.markdown("---")
        st.markdown("### \U0001f4d6 NFL Career Chronicle")
        for entry in st.session_state.nfl_history:
            st.markdown(
                f'<div style="background:rgba(255,255,255,0.05);border-left:4px solid #005a8e;'
                f'border-radius:8px;padding:12px 16px;margin:8px 0;">'
                f'<strong style="color:#4da6d9">{entry["stage"]}</strong><br>'
                f'<em style="color:#ffc107">Chose: {entry["choice"]}</em><br>'
                f'<span style="color:#ccc">{entry["outcome"]}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("\U0001f504 Start a New NFL Career", key="nfl_restart"):
                st.session_state.nfl_player           = None
                st.session_state.nfl_stage_idx        = -1
                st.session_state.nfl_awaiting_outcome = False
                st.session_state.nfl_chosen_option    = None
                st.session_state.nfl_narrative        = ""
                st.session_state.nfl_choices          = []
                st.session_state.nfl_outcome_text     = ""
                st.session_state.nfl_stats            = {"touchdowns": 0, "yards": 0, "pro_bowls": 0, "super_bowls": 0}
                st.session_state.nfl_history          = []
                st.rerun()
        with btn_col2:
            if st.button("\U0001f9d1\u200d\U0001f4bc Continue as NFL Head Coach", key="nfl_to_coach"):
                st.session_state.nfl_coach_prefill          = {"name": player["name"]}
                st.session_state.nfl_coach_manager          = None
                st.session_state.nfl_coach_stage_idx        = -1
                st.session_state.nfl_coach_awaiting_outcome = False
                st.session_state.nfl_coach_chosen_option    = None
                st.session_state.nfl_coach_narrative        = ""
                st.session_state.nfl_coach_choices          = []
                st.session_state.nfl_coach_outcome_text     = ""
                st.session_state.nfl_coach_stats            = {"wins": 0, "super_bowls": 0, "players_developed": 0, "reputation": 0}
                st.session_state.nfl_coach_history          = []
                st.rerun()

        if st.session_state.nfl_coach_prefill:
            st.info("\U0001f9d1\u200d\U0001f4bc Your coaching career is ready! Head to the **NFL Head Coach** tab to begin your journey.")


# ══════════════════════════════════════════════════════════════════════════════
# NFL COACH SIM — constants, helpers, tab rendering
# ══════════════════════════════════════════════════════════════════════════════

_NFL_COACH_PHILOSOPHIES = [
    "West Coast Offense",
    "Air Raid Spread",
    "Smash-Mouth Run Game",
    "4-3 Pass Rush Defence",
    "3-4 Zone Blitz",
    "Two-Minute Drill Specialist",
    "Defensive Ball Control",
    "Dynamic Spread Option",
]

_NFL_COACH_STAGES = [
    {"idx": 0, "id": "position_coach", "name": "Position Coach",            "age": "28-33", "icon": "\U0001f331"},
    {"idx": 1, "id": "coordinator",    "name": "Offensive/Defensive Coord.", "age": "33-38", "icon": "\U0001f4cb"},
    {"idx": 2, "id": "first_hc",       "name": "First Head Coach Role",      "age": "38-42", "icon": "\u26a1"},
    {"idx": 3, "id": "rebuilding",     "name": "Rebuilding a Franchise",     "age": "42-46", "icon": "\U0001f4c8"},
    {"idx": 4, "id": "playoffs",       "name": "Playoff Contender",          "age": "46-50", "icon": "\U0001f4a5"},
    {"idx": 5, "id": "super_bowl_run", "name": "Super Bowl Run",             "age": "50-54", "icon": "\U0001f3c6"},
    {"idx": 6, "id": "dynasty",        "name": "Dynasty Builder",            "age": "54-58", "icon": "\U0001f451"},
    {"idx": 7, "id": "legacy",         "name": "Legacy Chapter",             "age": "58+",   "icon": "\U0001f3c1"},
]


def _nfl_coach_stage_data(philosophy: str) -> list:
    """Return list of (narrative, choice_a, choice_b) tuples for 8 NFL coaching stages."""
    return [
        # 0 – Position Coach (28-33)
        (
            "After retiring, {name} took a quality-control position and quickly impressed the staff with "
            "a deep understanding of the game. The {philosophy} philosophy began taking shape on the whiteboard.",
            ("Coach the skill positions and build a reputation developing young talent",
             {"wins": 0, "super_bowls": 0, "players_developed": 8, "reputation": 8}),
            ("Focus on special teams coordination to get a full-unit coaching role immediately",
             {"wins": 0, "super_bowls": 0, "players_developed": 3, "reputation": 12}),
        ),
        # 1 – Coordinator (33-38)
        (
            "The head coach noticed the brilliance on the practice field and in the film room. "
            "{name} was promoted to coordinator — the real proving ground for future head coaches.",
            ("Accept an offensive coordinator role at a high-profile franchise with a star quarterback",
             {"wins": 35, "super_bowls": 0, "players_developed": 6, "reputation": 20}),
            ("Take a defensive coordinator role with full scheme authority at an ambitious team",
             {"wins": 28, "super_bowls": 0, "players_developed": 8, "reputation": 22}),
        ),
        # 2 – First Head Coach Role (38-42)
        (
            "The call came on a Tuesday morning in January. {name} was a head coach in the National Football League. "
            "The {philosophy} system was installed from the first OTA — but building a winning culture takes time.",
            ("Install the system boldly and demand immediate buy-in from veterans",
             {"wins": 30, "super_bowls": 0, "players_developed": 5, "reputation": 24}),
            ("Build trust through the locker room first, then gradually impose the full philosophy",
             {"wins": 26, "super_bowls": 0, "players_developed": 10, "reputation": 28}),
        ),
        # 3 – Rebuilding a Franchise (42-46)
        (
            "A struggling franchise came calling with a mandate to rebuild from the ground up. "
            "{name} took the challenge — turning a losing culture around is the ultimate test of any head coach.",
            ("Go all-in on the NFL Draft and develop homegrown stars over a three-year plan",
             {"wins": 32, "super_bowls": 0, "players_developed": 14, "reputation": 30}),
            ("Use free agency aggressively to fast-track the rebuild and reach the playoffs",
             {"wins": 42, "super_bowls": 0, "players_developed": 5, "reputation": 34}),
        ),
        # 4 – Playoff Contender (46-50)
        (
            "The rebuild was complete. {name}'s roster was now playoff-calibre, and the fanbase "
            "was buzzing with Super Bowl energy for the first time in years.",
            ("Make a deep playoff run — win the division and host a postseason game",
             {"wins": 50, "super_bowls": 0, "players_developed": 8, "reputation": 38}),
            ("Target the AFC/NFC championship with an aggressive in-season trade",
             {"wins": 44, "super_bowls": 0, "players_developed": 5, "reputation": 44}),
        ),
        # 5 – Super Bowl Run (50-54)
        (
            "A Super Bowl contender at last. {name}'s {philosophy} system was operating at full efficiency, "
            "and the squad had the firepower to go all the way.",
            ("Win the Super Bowl and cement a place among the coaching greats",
             {"wins": 52, "super_bowls": 1, "players_developed": 6, "reputation": 52}),
            ("Build the infrastructure for sustained excellence — roster depth over one-season glory",
             {"wins": 44, "super_bowls": 0, "players_developed": 10, "reputation": 48}),
        ),
        # 6 – Dynasty Builder (54-58)
        (
            "Back-to-back Super Bowl windows opened as {name} had assembled a dynasty-level roster. "
            "Only the greatest coaches in NFL history had achieved what was now within reach.",
            ("Win consecutive Super Bowls and become the face of the modern NFL",
             {"wins": 60, "super_bowls": 2, "players_developed": 8, "reputation": 60}),
            ("Prioritise developing the next generation of stars alongside continuing to win",
             {"wins": 48, "super_bowls": 1, "players_developed": 18, "reputation": 55}),
        ),
        # 7 – Legacy Chapter (58+)
        (
            "At 58, {name}'s legacy was already etched into NFL history. "
            "But one final chapter remained — a chance to be remembered as the greatest coach of all time.",
            ("Return to a beloved former team for an emotional reunion and a final championship push",
             {"wins": 30, "super_bowls": 1, "players_developed": 10, "reputation": 45}),
            ("Take over a first-time Super Bowl contender and deliver the ultimate storybook ending",
             {"wins": 40, "super_bowls": 2, "players_developed": 12, "reputation": 55}),
        ),
    ]


def _nfl_coach_generate_stage(manager: dict, stage: dict, stats: dict, api_key: str) -> dict:
    """Return {narrative, choices: [str, str], stat_deltas: [dict, dict]}."""
    templates = _nfl_coach_stage_data(manager["philosophy"])
    tmpl_narr, tmpl_a, tmpl_b = templates[stage["idx"]]
    fallback = {
        "narrative":   tmpl_narr.format(name=manager["name"], philosophy=manager["philosophy"]),
        "choices":     [tmpl_a[0], tmpl_b[0]],
        "stat_deltas": [tmpl_a[1], tmpl_b[1]],
    }
    if not api_key:
        return fallback
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        stat_line = (
            f"Career stats so far: {stats['wins']} wins, {stats['super_bowls']} Super Bowls, "
            f"{stats['players_developed']} players developed, {stats['reputation']} reputation points."
        ) if any(stats.values()) else ""
        prompt = (
            f"Create an NFL coaching career stage for this head coach:\\n"
            f"Name: {manager['name']} | Philosophy: {manager['philosophy']}\\n"
            f"Stage: {stage['name']} (Age {stage['age']})\\n"
            f"{stat_line}\\n\\n"
            f"Respond in EXACTLY this format (keep each section to 1-2 sentences):\\n"
            f"NARRATIVE: [dramatic NFL coaching career narrative for this stage]\\n"
            f"CHOICE_A: [{tmpl_a[0]}]\\n"
            f"CHOICE_B: [{tmpl_b[0]}]"
        )
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": (
                    "You are an NFL coaching career narrator creating an engaging text-adventure game. "
                    "Be concise, dramatic, and use authentic NFL coaching details. "
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


def _nfl_coach_generate_outcome(manager: dict, stage: dict, choice_text: str, delta: dict, api_key: str) -> str:
    """Return outcome narrative string for an NFL coaching stage choice."""
    parts = []
    if delta.get("wins"):              parts.append(f"{delta['wins']} wins")
    if delta.get("super_bowls"):       parts.append(f"{delta['super_bowls']} Super Bowl(s)")
    if delta.get("players_developed"): parts.append(f"{delta['players_developed']} players developed")
    if delta.get("reputation"):        parts.append(f"{delta['reputation']} reputation points")
    stat_str = ", ".join(parts) if parts else "invaluable experience"
    fallback = (
        f"A superb spell of coaching for {manager['name']}! "
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
                    "You are an NFL coaching career narrator. Write punchy, vivid outcome paragraphs."
                )},
                {"role": "user", "content": (
                    f"{manager['name']} (NFL head coach, {manager['philosophy']}) "
                    f"chose: \"{choice_text}\"\\n"
                    f"Stage: {stage['name']}\\n"
                    f"Results: {stat_str}\\n\\n"
                    f"Write ONE paragraph (2-3 sentences) describing what happened. "
                    f"Be specific and dramatic. Do NOT start with the coach's name."
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


def _nfl_coach_career_rating(stats: dict) -> tuple[int, str]:
    """Return (0-100 rating, badge label) based on accumulated NFL coaching stats."""
    score = (
        stats["wins"] * 0.7
        + stats["super_bowls"] * 80
        + stats["players_developed"] * 3
        + stats["reputation"] * 1.5
    )
    if score >= 900: return 99, "\U0001f410 Greatest NFL Coach of All Time"
    if score >= 700: return 95, "\u2b50 Hall of Fame Coach"
    if score >= 500: return 90, "\U0001f31f Dynasty Architect"
    if score >= 350: return 83, "\U0001f4c8 Accomplished Head Coach"
    if score >= 220: return 74, "\u2705 Respected NFL Coach"
    return 62, "\U0001f393 Journeyman Head Coach"


# ── NFL Coach Sim: tab rendering ──────────────────────────────────────────────
with tab_nfl_coach:
    st.markdown("## \U0001f3c8 NFL Head Coach Career Simulator")
    st.markdown(
        "Build your NFL coaching career from a quality-control assistant all the way to Super Bowl glory. "
        "Every decision shapes your legacy — wins, Super Bowls, players developed, and reputation."
    )
    if not st.session_state.openai_api_key:
        st.info(
            "\U0001f4a1 **Tip:** Enter your OpenAI API key in the sidebar to unlock AI-generated "
            "personalised narratives. The simulator works great with built-in story templates too!"
        )

    nfl_coach_stage_idx = st.session_state.nfl_coach_stage_idx
    nfl_coach_manager   = st.session_state.nfl_coach_manager
    nfl_coach_prefill   = st.session_state.nfl_coach_prefill

    if nfl_coach_stage_idx == -1:
        if nfl_coach_prefill:
            st.success(
                f"\U0001f389 Welcome to the NFL sideline, **{nfl_coach_prefill['name']}**! "
                f"Your playing days are over — now it's time to shape the game from the coach's box. "
                f"Choose your philosophy to begin."
            )

        st.markdown("### \U0001f4cb Create Your NFL Head Coach")
        col_nc1, col_nc2 = st.columns(2)
        with col_nc1:
            _default_nfl_name = nfl_coach_prefill["name"] if nfl_coach_prefill else ""
            nfl_coach_name = st.text_input(
                "Coach Name", value=_default_nfl_name,
                placeholder="e.g. Alex Donovan", key="nfl_coach_name_input"
            )
        with col_nc2:
            nfl_coach_philosophy = st.selectbox(
                "Coaching Philosophy", _NFL_COACH_PHILOSOPHIES, key="nfl_coach_phil_input"
            )

        if st.button("\U0001f680 Start NFL Coaching Career", key="nfl_coach_start"):
            if not nfl_coach_name.strip():
                st.warning("Please enter a coach name.")
            else:
                st.session_state.nfl_coach_manager = {
                    "name":       nfl_coach_name.strip(),
                    "philosophy": nfl_coach_philosophy,
                }
                st.session_state.nfl_coach_prefill          = None
                st.session_state.nfl_coach_stage_idx        = 0
                st.session_state.nfl_coach_awaiting_outcome = False
                st.session_state.nfl_coach_chosen_option    = None
                st.session_state.nfl_coach_narrative        = ""
                st.session_state.nfl_coach_choices          = []
                st.session_state.nfl_coach_outcome_text     = ""
                st.session_state.nfl_coach_stats            = {"wins": 0, "super_bowls": 0, "players_developed": 0, "reputation": 0}
                st.session_state.nfl_coach_history          = []
                st.rerun()

    elif nfl_coach_stage_idx < len(_NFL_COACH_STAGES):
        stage   = _NFL_COACH_STAGES[nfl_coach_stage_idx]
        manager = st.session_state.nfl_coach_manager
        stats   = st.session_state.nfl_coach_stats
        api_key = st.session_state.openai_api_key

        st.markdown(f"### {stage['icon']} Stage {nfl_coach_stage_idx + 1} / {len(_NFL_COACH_STAGES)}: {stage['name']}  *(Age {stage['age']})*")
        st.progress(nfl_coach_stage_idx / len(_NFL_COACH_STAGES))

        ncs1, ncs2, ncs3, ncs4 = st.columns(4)
        with ncs1: st.metric("\U0001f3c5 Wins",             stats["wins"])
        with ncs2: st.metric("\U0001f48d Super Bowls",      stats["super_bowls"])
        with ncs3: st.metric("\U0001f331 Players Developed", stats["players_developed"])
        with ncs4: st.metric("\u2b50 Reputation",            stats["reputation"])

        st.markdown("---")

        if not st.session_state.nfl_coach_narrative:
            with st.spinner("\u270d\ufe0f Writing your NFL coaching story\u2026"):
                data = _nfl_coach_generate_stage(manager, stage, stats, api_key)
            st.session_state.nfl_coach_narrative = data["narrative"]
            st.session_state.nfl_coach_choices   = list(zip(data["choices"], data["stat_deltas"]))
            st.rerun()

        st.markdown(
            f'<div style="background:rgba(255,255,255,0.06);border-left:4px solid #c8102e;'
            f'border-radius:10px;padding:16px 20px;margin-bottom:16px;font-size:1.05rem;color:#e0e0e0;">'
            f'{st.session_state.nfl_coach_narrative}</div>',
            unsafe_allow_html=True,
        )

        if st.session_state.nfl_coach_awaiting_outcome:
            chosen_idx = st.session_state.nfl_coach_chosen_option
            choice_text, delta = st.session_state.nfl_coach_choices[chosen_idx]

            if not st.session_state.nfl_coach_outcome_text:
                with st.spinner("\u26a1 Simulating the outcome\u2026"):
                    outcome = _nfl_coach_generate_outcome(manager, stage, choice_text, delta, api_key)
                st.session_state.nfl_coach_outcome_text = outcome
                st.rerun()

            st.markdown(f"**You chose:** *{choice_text}*")
            st.markdown(
                f'<div style="background:rgba(200,16,46,0.1);border-left:4px solid #ffc107;'
                f'border-radius:10px;padding:14px 20px;margin:10px 0;color:#e0e0e0;">'
                f'{st.session_state.nfl_coach_outcome_text}</div>',
                unsafe_allow_html=True,
            )

            gain_parts = []
            if delta.get("wins"):              gain_parts.append(f"\U0001f3c5 +{delta['wins']} wins")
            if delta.get("super_bowls"):       gain_parts.append(f"\U0001f48d +{delta['super_bowls']} Super Bowls")
            if delta.get("players_developed"): gain_parts.append(f"\U0001f331 +{delta['players_developed']} players")
            if delta.get("reputation"):        gain_parts.append(f"\u2b50 +{delta['reputation']} reputation")
            if gain_parts:
                st.markdown("**Stats earned:** " + "  \u00b7  ".join(gain_parts))

            next_label = "\u25b6\ufe0f Next Stage" if nfl_coach_stage_idx < len(_NFL_COACH_STAGES) - 1 else "\U0001f3c1 Retire & See Legacy"
            if st.button(next_label, key="nfl_coach_next_stage"):
                for k, v in delta.items():
                    st.session_state.nfl_coach_stats[k] += v
                st.session_state.nfl_coach_history.append({
                    "stage":   stage["name"],
                    "choice":  choice_text,
                    "outcome": st.session_state.nfl_coach_outcome_text,
                    "delta":   delta,
                })
                st.session_state.nfl_coach_stage_idx        += 1
                st.session_state.nfl_coach_awaiting_outcome  = False
                st.session_state.nfl_coach_chosen_option     = None
                st.session_state.nfl_coach_narrative         = ""
                st.session_state.nfl_coach_choices           = []
                st.session_state.nfl_coach_outcome_text      = ""
                st.rerun()

        else:
            st.markdown("### \U0001f914 What do you do?")
            choices = st.session_state.nfl_coach_choices
            col_nca, col_ncb = st.columns(2)
            with col_nca:
                if st.button(f"**A:** {choices[0][0]}", key="nfl_coach_choice_a", use_container_width=True):
                    st.session_state.nfl_coach_chosen_option    = 0
                    st.session_state.nfl_coach_awaiting_outcome = True
                    st.rerun()
            with col_ncb:
                if st.button(f"**B:** {choices[1][0]}", key="nfl_coach_choice_b", use_container_width=True):
                    st.session_state.nfl_coach_chosen_option    = 1
                    st.session_state.nfl_coach_awaiting_outcome = True
                    st.rerun()

    elif nfl_coach_stage_idx >= len(_NFL_COACH_STAGES):
        manager = st.session_state.nfl_coach_manager
        stats   = st.session_state.nfl_coach_stats
        rating, badge = _nfl_coach_career_rating(stats)

        st.markdown(f"## \U0001f3c1 {manager['name']} \u2014 NFL Coaching Career Over")
        st.markdown(
            f'<div class="result-correct" style="font-size:1.6rem;background:linear-gradient(90deg,#5a0010,#c8102e);">'
            f'{badge} &nbsp; Career Rating: {rating} / 100'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.markdown(f"**{manager['philosophy']}**")

        nr1, nr2, nr3, nr4 = st.columns(4)
        with nr1: st.metric("\U0001f3c5 Career Wins",      stats["wins"])
        with nr2: st.metric("\U0001f48d Super Bowls Won",  stats["super_bowls"])
        with nr3: st.metric("\U0001f331 Players Developed", stats["players_developed"])
        with nr4: st.metric("\u2b50 Total Reputation",      stats["reputation"])

        st.markdown("---")
        st.markdown("### \U0001f4d6 NFL Coaching Chronicle")
        for entry in st.session_state.nfl_coach_history:
            st.markdown(
                f'<div style="background:rgba(255,255,255,0.05);border-left:4px solid #c8102e;'
                f'border-radius:8px;padding:12px 16px;margin:8px 0;">'
                f'<strong style="color:#e05070">{entry["stage"]}</strong><br>'
                f'<em style="color:#ffc107">Chose: {entry["choice"]}</em><br>'
                f'<span style="color:#ccc">{entry["outcome"]}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

        if st.button("\U0001f504 Start a New NFL Coaching Career", key="nfl_coach_restart"):
            st.session_state.nfl_coach_manager          = None
            st.session_state.nfl_coach_stage_idx        = -1
            st.session_state.nfl_coach_awaiting_outcome = False
            st.session_state.nfl_coach_chosen_option    = None
            st.session_state.nfl_coach_narrative        = ""
            st.session_state.nfl_coach_choices          = []
            st.session_state.nfl_coach_outcome_text     = ""
            st.session_state.nfl_coach_stats            = {"wins": 0, "super_bowls": 0, "players_developed": 0, "reputation": 0}
            st.session_state.nfl_coach_history          = []
            st.rerun()
