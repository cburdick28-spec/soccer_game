"""
app.py  —  ⚽ Soccer Career Guesser
Two game modes:
  1. Career Timeline  – reveal clubs one-by-one and guess the footballer (Beat-Footballer-Career style)
  2. Footballer Guesser – Wordle-style attribute feedback grid (Footballizer-style)
"""

import random
import streamlit as st
import plotly.express as px
import pandas as pd

from game_data import (
    PLAYERS, LEAGUES, POSITIONS, ERAS, LEAGUE_COLOURS, FLAGS,
    ATTRIBUTE_LABELS, filter_players, pick_random_player,
    score_for_guess, all_player_names, compare_players, get_top_league,
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
    /* Main background */
    .stApp { background: linear-gradient(135deg, #0d1b2a 0%, #1b2838 60%, #0d2137 100%); }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a1628 0%, #112240 100%) !important;
        border-right: 2px solid #1db954;
    }
    section[data-testid="stSidebar"] * { color: #e0e0e0 !important; }

    /* Cards */
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

    /* Score board */
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

    /* Result banner */
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

    /* Attribute grid (Footballizer mode) */
    .attr-row {
        display: flex; gap: 8px; margin: 6px 0; align-items: center;
    }
    .attr-label {
        width: 150px; color: #aab8c2; font-size: 0.85rem; font-weight: 600;
        text-transform: uppercase; letter-spacing: 0.5px; flex-shrink: 0;
    }
    .attr-cell {
        flex: 1; border-radius: 8px; padding: 10px 14px;
        font-size: 0.95rem; font-weight: 600; text-align: center;
        color: white; min-width: 90px;
    }
    .cell-correct  { background: #1a7a40; border: 2px solid #1db954; }
    .cell-close    { background: #856404; border: 2px solid #ffc107; }
    .cell-wrong    { background: #5a2d2d; border: 2px solid #e74c3c; }
    .cell-header   { background: rgba(255,255,255,0.08); border: 2px solid #444; color: #ccc; }

    /* Trophy row */
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

    /* Mode tab */
    div[data-testid="stTabs"] button {
        font-weight: 700; font-size: 1rem;
        background: transparent !important;
        border-bottom: 3px solid transparent !important;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        border-bottom-color: #1db954 !important;
        color: #1db954 !important;
    }

    /* General text */
    h1, h2, h3, h4, h5, h6 { color: #ffffff !important; }
    p, li, label, .stMarkdown { color: #e0e0e0 !important; }

    /* Button */
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

    /* Input */
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
    # Footballer guesser mode
    "fg_player":           None,
    "fg_guesses":          [],  # list of (name, compare_result dict)
    "fg_won":              False,
    "fg_gave_up":          False,
    "fg_input_key":        100,
    # Global scores
    "total_score":         0,
    "rounds_played":       0,
    "win_streak":          0,
    "best_streak":         0,
    "history":             [],  # list of dicts per round
    # Filters
    "filter_position":     "All Positions",
    "filter_league":       "All Leagues",
    "filter_era":          "All Eras",
    "filter_difficulty":   "All",
}

for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

def reset_career(player):
    st.session_state.career_player   = player
    st.session_state.career_revealed = 0
    st.session_state.career_guesses  = []
    st.session_state.career_won      = False
    st.session_state.career_gave_up  = False
    st.session_state.career_input_key += 1

def reset_fg(player):
    st.session_state.fg_player    = player
    st.session_state.fg_guesses   = []
    st.session_state.fg_won       = False
    st.session_state.fg_gave_up   = False
    st.session_state.fg_input_key += 1

def get_filtered():
    return filter_players(
        position_group = st.session_state.filter_position,
        league_filter  = st.session_state.filter_league,
        era_filter     = st.session_state.filter_era,
        difficulty     = st.session_state.filter_difficulty,
    )

# ──────────────────────────────────────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚽ Soccer Career Guesser")
    st.markdown("---")

    st.markdown("### �� Score")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="score-box"><div class="score-val">{st.session_state.total_score}</div><div class="score-lbl">Points</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="score-box"><div class="score-val">{st.session_state.rounds_played}</div><div class="score-lbl">Played</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="score-box"><div class="score-val">{st.session_state.win_streak}🔥</div><div class="score-lbl">Streak</div></div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔍 Filters")

    pos_options = ["All Positions"] + list(POSITIONS.keys())
    st.session_state.filter_position = st.selectbox(
        "Position Group", pos_options,
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

    pool = get_filtered()
    st.caption(f"🎮 {len(pool)} players in pool")

    st.markdown("---")
    st.markdown("### 📜 Recent History")
    if st.session_state.history:
        for h in reversed(st.session_state.history[-5:]):
            icon = "✅" if h["won"] else "❌"
            st.markdown(f"**{icon} {h['name']}** — {h.get('points',0)} pts", unsafe_allow_html=True)
    else:
        st.caption("No rounds played yet")

    st.markdown("---")
    st.markdown("### 📖 How to Play")
    st.markdown("""
**Career Timeline**
- Clubs are revealed one by one  
- Guess sooner = more points (up to 1000)
- Up to 5 wrong guesses allowed

**Footballer Guesser**
- Type any footballer's name  
- 🟩 Green = correct attribute  
- 🟨 Yellow = close (age ±6 yrs)  
- 🟥 Red = wrong  
- Unlimited guesses  
""")

# ──────────────────────────────────────────────────────────────────────────────
# Main area — title
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("<h1 style='text-align:center;font-size:2.8rem'>⚽ Soccer Career Guesser</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#aaa;font-size:1.1rem'>Two game modes — guess legendary footballers by their career or by their attributes</p>", unsafe_allow_html=True)
st.markdown("---")

tab_career, tab_fg, tab_stats = st.tabs(["🏟️ Career Timeline", "🟩 Footballer Guesser", "📊 Statistics"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — CAREER TIMELINE
# ══════════════════════════════════════════════════════════════════════════════
with tab_career:
    pool = get_filtered()
    cp = st.session_state.career_player

    # ── New game button ──────────────────────────────────────────────────────
    col_btn, col_hint = st.columns([1, 3])
    with col_btn:
        if st.button("🎲 New Player", key="new_career"):
            if pool:
                reset_career(pick_random_player(pool))
            else:
                st.warning("No players match the current filters. Try adjusting the sidebar filters.")

    if cp is None:
        st.info("👈 Click **New Player** to start!")
        st.stop()

    career = cp["career"]
    revealed = st.session_state.career_revealed
    won      = st.session_state.career_won
    gave_up  = st.session_state.career_gave_up

    # ── Top info bar ─────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Clubs Revealed", f"{revealed} / {len(career)}")
    with c2:
        pts = score_for_guess(revealed, len(career))
        st.metric("Points if correct now", f"⭐ {pts}")
    with c3:
        wrong_guesses = [g for g in st.session_state.career_guesses if g != cp["name"]]
        st.metric("Wrong Guesses", f"{len(wrong_guesses)} / 5")
    with c4:
        st.metric("Position", cp["position_group"])

    # ── Career cards ─────────────────────────────────────────────────────────
    st.markdown("### 🏆 Career Path")
    show_count = revealed if not (won or gave_up) else len(career)

    if show_count == 0 and not (won or gave_up):
        st.info("No clubs revealed yet. Click **Reveal Next Club** to start.")
    else:
        for i, entry in enumerate(career[:show_count]):
            lg   = entry["league"]
            colour = LEAGUE_COLOURS.get(lg, LEAGUE_COLOURS["Other"])
            st.markdown(f"""
<div class="career-card" style="border-left-color:{colour}">
  <span class="club-name">🏟️ {entry['club']}</span>
  <span class="club-detail"> &nbsp;|&nbsp; {lg} &nbsp;|&nbsp; {entry['years']}</span>
</div>""", unsafe_allow_html=True)

    # ── Action buttons (only when not finished) ──────────────────────────────
    if not won and not gave_up:
        col_reveal, col_spacer = st.columns([1, 3])
        with col_reveal:
            if revealed < len(career):
                if st.button("🔍 Reveal Next Club", key="reveal_club"):
                    st.session_state.career_revealed += 1
                    st.rerun()
            else:
                st.warning("All clubs revealed! Take a guess below.")

        # ── Guess input ──────────────────────────────────────────────────────
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
                        pts = score_for_guess(revealed, len(career))
                        st.session_state.total_score  += pts
                        st.session_state.rounds_played += 1
                        st.session_state.win_streak   += 1
                        st.session_state.best_streak   = max(
                            st.session_state.best_streak, st.session_state.win_streak
                        )
                        st.session_state.career_won = True
                        st.session_state.history.append({
                            "mode": "Career", "name": cp["name"],
                            "won": True, "points": pts
                        })
                        st.rerun()
                    else:
                        wrong = [g for g in st.session_state.career_guesses if g != cp["name"]]
                        if len(wrong) >= 5:
                            st.session_state.career_gave_up  = True
                            st.session_state.rounds_played   += 1
                            st.session_state.win_streak       = 0
                            st.session_state.history.append({
                                "mode": "Career", "name": cp["name"],
                                "won": False, "points": 0
                            })
                            st.rerun()
                        else:
                            st.session_state.career_input_key += 1
                            st.rerun()
        with col_giveup:
            if st.button("🏳️ Give Up", key="giveup_career"):
                st.session_state.career_gave_up  = True
                st.session_state.rounds_played   += 1
                st.session_state.win_streak       = 0
                st.session_state.history.append({
                    "mode": "Career", "name": cp["name"],
                    "won": False, "points": 0
                })
                st.rerun()

        # Show wrong guesses
        if wrong_guesses:
            st.markdown("**❌ Wrong guesses:** " + " • ".join(wrong_guesses))

    # ── Game-over panel ──────────────────────────────────────────────────────
    if won or gave_up:
        flag = FLAGS.get(cp["nationality"], "")
        if won:
            pts = score_for_guess(
                next((i for i,g in enumerate(st.session_state.career_guesses) if g == cp["name"]), revealed),
                len(career)
            )
            st.markdown(f'<div class="result-correct">🎉 Correct! That\'s <b>{cp["name"]}</b> {flag} — +{pts} pts!</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="result-wrong">😔 The answer was <b>{cp["name"]}</b> {flag}</div>', unsafe_allow_html=True)

        # Full career reveal
        st.markdown("### 📋 Full Career")
        for entry in career:
            lg     = entry["league"]
            colour = LEAGUE_COLOURS.get(lg, LEAGUE_COLOURS["Other"])
            st.markdown(f"""
<div class="career-card" style="border-left-color:{colour}">
  <span class="club-name">🏟️ {entry['club']}</span>
  <span class="club-detail"> &nbsp;|&nbsp; {lg} &nbsp;|&nbsp; {entry['years']}</span>
</div>""", unsafe_allow_html=True)

        # Player info
        col_info, col_chart = st.columns([1, 1])
        with col_info:
            st.markdown(f"**Nationality:** {flag} {cp['nationality']}")
            st.markdown(f"**Position:** {cp['position']}")
            st.markdown(f"**Born:** {cp['birth_year']}")
            bd = cp.get("ballon_dor", 0) or 0
            if bd > 0:
                st.markdown(f"**Ballon d'Or:** {'🏆 ' * bd}({bd})")
            st.markdown("**Honours:**")
            for t in cp["trophies"]:
                st.markdown(f'<span class="trophy-chip">🏆 {t}</span>', unsafe_allow_html=True)

        with col_chart:
            # Timeline chart
            rows = []
            for e in career:
                rows.append({
                    "Club":   e["club"],
                    "League": e["league"],
                    "Start":  e["start"],
                    "End":    e["end"] or 2025,
                })
            df = pd.DataFrame(rows)
            if not df.empty:
                fig = px.timeline(
                    df,
                    x_start="Start", x_end="End",
                    y="Club", color="League",
                    title=f"{cp['name']} — Career Timeline",
                    color_discrete_map=LEAGUE_COLOURS,
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="white",
                    height=300,
                    margin=dict(l=10, r=10, t=40, b=10),
                    showlegend=False,
                )
                fig.update_xaxes(
                    type="linear",
                    tickformat="d",
                    showgrid=True, gridcolor="rgba(255,255,255,0.1)"
                )
                fig.update_yaxes(showgrid=False)
                st.plotly_chart(fig, use_container_width=True)

        if st.button("▶️ Play Again", key="play_again_career"):
            pool = get_filtered()
            if pool:
                reset_career(pick_random_player(pool))
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — FOOTBALLER GUESSER  (Footballizer-style)
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
        st.info("�� Click **New Player** to start!")
        st.stop()

    won_fg     = st.session_state.fg_won
    gave_up_fg = st.session_state.fg_gave_up

    flag = FLAGS.get(fgp["nationality"], "🌍")

    if won_fg:
        pts = max(200, 1000 - (len(guesses) - 1) * 100)
        st.markdown(f'<div class="result-correct">🎉 Correct! That\'s <b>{fgp["name"]}</b> {flag} — +{pts} pts!</div>', unsafe_allow_html=True)
    elif gave_up_fg:
        st.markdown(f'<div class="result-wrong">😔 The answer was <b>{fgp["name"]}</b> {flag}</div>', unsafe_allow_html=True)

    # ── Attribute header row ─────────────────────────────────────────────────
    attr_keys = list(ATTRIBUTE_LABELS.keys())
    header_cells = "".join(
        f'<div class="attr-cell cell-header">{ATTRIBUTE_LABELS[k]}</div>'
        for k in attr_keys
    )
    st.markdown(
        f'<div class="attr-row"><div class="attr-label">Player</div>{header_cells}</div>',
        unsafe_allow_html=True
    )

    # ── Past guess rows ──────────────────────────────────────────────────────
    def _attr_value(player: dict, key: str) -> str:
        if key == "nationality":    return player["nationality"]
        if key == "position_group": return player["position_group"]
        if key == "league":         return get_top_league(player)
        if key == "age":
            age = 2025 - player["birth_year"]
            if age < 23:   bucket = "Under 23"
            elif age < 28: bucket = "23-27"
            elif age < 33: bucket = "28-32"
            elif age < 38: bucket = "33-37"
            else:           bucket = "38+"
            return bucket
        if key == "current_club":      return player.get("current_club", "?")
        if key == "ballon_dor_winner": return "Yes" if (player.get("ballon_dor",0) or 0) > 0 else "No"
        return "?"

    EMOJI_MAP = {"correct": "🟩", "close": "🟨", "wrong": "🟥"}
    CSS_MAP    = {"correct": "cell-correct", "close": "cell-close", "wrong": "cell-wrong"}

    # Name lookup
    name_to_player = {p["name"]: p for p in PLAYERS}

    for guess_name, cmp in guesses:
        gp    = name_to_player.get(guess_name)
        if gp is None:
            continue
        cells = "".join(
            f'<div class="attr-cell {CSS_MAP[cmp[k]]}">'
            f'{EMOJI_MAP[cmp[k]]} {_attr_value(gp, k)}</div>'
            for k in attr_keys
        )
        st.markdown(
            f'<div class="attr-row"><div class="attr-label" style="color:#fff;font-weight:700">{guess_name}</div>{cells}</div>',
            unsafe_allow_html=True
        )

    # ── Guess input ──────────────────────────────────────────────────────────
    if not won_fg and not gave_up_fg:
        st.markdown("### 🤔 Guess a Footballer")
        all_names = all_player_names()
        already_guessed = [g[0] for g in guesses]
        remaining = [n for n in all_names if n not in already_guessed]

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
                            st.session_state.best_streak    = max(
                                st.session_state.best_streak, st.session_state.win_streak
                            )
                            st.session_state.fg_won = True
                            st.session_state.history.append({
                                "mode": "Guesser", "name": fgp["name"],
                                "won": True, "points": pts
                            })
                        st.session_state.fg_input_key += 1
                        st.rerun()

        with col_gu:
            if st.button("🏳️ Give Up", key="giveup_fg"):
                st.session_state.fg_gave_up   = True
                st.session_state.rounds_played += 1
                st.session_state.win_streak    = 0
                st.session_state.history.append({
                    "mode": "Guesser", "name": fgp["name"],
                    "won": False, "points": 0
                })
                st.rerun()

        if guesses:
            st.caption(f"💡 Guesses so far: {len(guesses)}")

    # ── Post-game info ────────────────────────────────────────────────────────
    if won_fg or gave_up_fg:
        st.markdown("### 📋 Player Profile")
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown(f"**Name:** {fgp['name']}")
            st.markdown(f"**Nationality:** {FLAGS.get(fgp['nationality'],'🌍')} {fgp['nationality']}")
            st.markdown(f"**Position:** {fgp['position']} ({fgp['position_group']})")
            st.markdown(f"**Born:** {fgp['birth_year']}")
            st.markdown(f"**Current / Last Club:** {fgp.get('current_club','?')}")
            st.markdown(f"**Main League:** {get_top_league(fgp)}")
            bd = fgp.get("ballon_dor", 0) or 0
            if bd > 0:
                st.markdown(f"**Ballon d'Or:** {'🏆 ' * bd}({bd})")
            st.markdown("**Honours:**")
            for t in fgp["trophies"]:
                st.markdown(f'<span class="trophy-chip">🏆 {t}</span>', unsafe_allow_html=True)
        with c2:
            rows2 = []
            for e in fgp["career"]:
                rows2.append({"Club": e["club"], "League": e["league"],
                               "Start": e["start"], "End": e["end"] or 2025})
            df2 = pd.DataFrame(rows2)
            if not df2.empty:
                fig2 = px.timeline(
                    df2, x_start="Start", x_end="End",
                    y="Club", color="League",
                    title=f"{fgp['name']} — Career Timeline",
                    color_discrete_map=LEAGUE_COLOURS,
                )
                fig2.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font_color="white", height=350,
                    margin=dict(l=10, r=10, t=40, b=10), showlegend=False,
                )
                fig2.update_xaxes(type="linear", tickformat="d",
                                  showgrid=True, gridcolor="rgba(255,255,255,0.1)")
                fig2.update_yaxes(showgrid=False)
                st.plotly_chart(fig2, use_container_width=True)

        if st.button("▶️ Play Again", key="play_again_fg"):
            pool = get_filtered()
            if pool:
                reset_fg(pick_random_player(pool))
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — STATISTICS
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
        # Cumulative score chart
        df_hist["cumulative"] = df_hist["points"].cumsum()
        fig_s = px.area(df_hist, y="cumulative", title="Cumulative Score",
                        labels={"index":"Round","cumulative":"Total Score"})
        fig_s.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="white", margin=dict(l=10, r=10, t=40, b=10),
        )
        fig_s.update_traces(line_color="#1db954", fillcolor="rgba(29,185,84,0.15)")
        fig_s.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.07)")
        fig_s.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.07)")
        st.plotly_chart(fig_s, use_container_width=True)

        st.markdown("### 📋 Round History")
        df_show = df_hist[["mode","name","won","points"]].copy()
        df_show["won"] = df_show["won"].map({True: "✅", False: "❌"})
        df_show.columns = ["Mode", "Player", "Result", "Points"]
        df_show.index = range(1, len(df_show) + 1)
        st.dataframe(df_show, use_container_width=True)
    else:
        st.info("Play some rounds to see your stats here!")

    st.markdown("---")
    st.markdown("### 🌟 Player Database Explorer")
    search = st.text_input("Search players by name, nationality, or club:")
    show_all = PLAYERS
    if search:
        q = search.lower()
        show_all = [
            p for p in PLAYERS
            if q in p["name"].lower()
            or q in p["nationality"].lower()
            or any(q in e["club"].lower() for e in p["career"])
        ]
    rows_db = []
    for p in show_all:
        rows_db.append({
            "Name":        p["name"],
            "Nationality": FLAGS.get(p["nationality"],"🌍") + " " + p["nationality"],
            "Position":    p["position"],
            "Group":       p["position_group"],
            "Main League": get_top_league(p),
            "Career Clubs":len(p["career"]),
            "Difficulty":  p.get("difficulty","?"),
        })
    if rows_db:
        st.dataframe(pd.DataFrame(rows_db), use_container_width=True, hide_index=True)
    else:
        st.info("No players found.")
