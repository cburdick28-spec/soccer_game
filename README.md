# ⚽ Soccer Career Guesser — Advanced Edition

An advanced Streamlit football (soccer) guessing game inspired by **Beat-Footballer-Career** and **Footballizer**, featuring five game modes, 91 real players, multiple positions, leagues, eras, continents, and more.

---

## 🎮 Game Modes

### 🏟️ Career Timeline  *(Beat-Footballer-Career style)*
A mystery player's career clubs are revealed **one club at a time**.  
Guess the player as early as possible — the fewer clubs revealed, the more points you earn (up to **1000 pts**).  
Up to 5 wrong guesses are allowed before the round ends.  
Use optional **💡 Hints** (nationality, continent, birth decade) — each costs points.

| Clubs revealed | Points if correct |
|---|---|
| ≤25% | 🏆 1000 |
| ≤50% | ⭐ 700 |
| ≤75% | 🎯 400 |
| All  | ✅ 200 |

### 🟩 Footballer Guesser  *(Footballizer style)*
Guess the mystery player by typing any footballer's name.  
For each guess you see a **colour-coded 9-attribute grid**:

| Colour | Meaning |
|---|---|
| 🟩 Green | Attribute is **correct** |
| 🟨 Yellow | **Close** (age within ±6 years) |
| 🟥 Red | **Wrong** |

Attributes compared: Nationality · Continent · Position Group · Main League · Age Group · Current Club · Ballon d'Or · World Cup Winner · Peak Club

### 🏆 Trophy Cabinet
A mystery player's trophies are revealed **one at a time**.  
Guess the player from their honours list — up to 5 wrong guesses allowed.

### 📅 Daily Challenge
Same mystery player for **everyone, every day** (seeded by date).  
Choose Career Timeline or Footballer Guesser mode.  
Build your **daily streak** by coming back each day!

### 📊 Stats & Achievements
Track your total score, win rate, streaks, and unlock **12 achievements**.

---

## 📊 Features
- **91 legendary players** across all eras (1960s → 2020s)
- **4 position groups**: Goalkeeper, Defender, Midfielder, Forward
- **10+ leagues**: Premier League, La Liga, Serie A, Bundesliga, Ligue 1, MLS, Eredivisie, Primeira Liga, Saudi Pro League, and more
- **6 continents**: Europe, South America, Africa, Asia, North America
- **Era filter**: 1990s / 2000s / 2010s / 2020s
- **Difficulty filter**: Easy / Medium / Hard
- **World Cup Winner filter**: filter pool to WC winners or non-winners
- **Score & streak tracking** (including daily streaks)
- **Interactive career timeline** chart (Plotly Gantt)
- **Player database explorer** — search all 91 players with full attribute table

---

## 🚀 Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open **http://localhost:8501** in your browser.

---

## 📁 File Structure

```
soccer_game/
├── app.py           # Streamlit UI (5 game modes + sidebar + stats)
├── game_data.py     # Player database (91 players) + game logic
├── requirements.txt # Dependencies
└── README.md
```
