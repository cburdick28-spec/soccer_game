# ⚽ Soccer Career Guesser

An advanced Streamlit football (soccer) guessing game inspired by **Beat-Footballer-Career** and **Footballizer**, featuring two game modes, 50+ real players, multiple positions, leagues, eras, and more.

---

## 🎮 Game Modes

### 🏟️ Career Timeline  *(Beat-Footballer-Career style)*
A mystery player's career clubs are revealed **one club at a time**.  
Guess the player as early as possible — the fewer clubs revealed, the more points you earn (up to **1000 pts**).  
Up to 5 wrong guesses are allowed before the round ends.

| Clubs revealed | Points if correct |
|---|---|
| ≤25% | 🏆 1000 |
| ≤50% | ⭐ 700 |
| ≤75% | 🎯 400 |
| All  | ✅ 200 |

### 🟩 Footballer Guesser  *(Footballizer style)*
Guess the mystery player by typing any footballer's name.  
For each guess you see a **colour-coded attribute grid**:

| Colour | Meaning |
|---|---|
| 🟩 Green | Attribute is **correct** |
| 🟨 Yellow | **Close** (age within ±6 years) |
| 🟥 Red | **Wrong** |

Attributes compared: Nationality · Position Group · Main League · Age Group · Current Club · Ballon d'Or Winner

---

## 📊 Features
- **51 legendary players** across all eras (1960s → 2020s)
- **4 position groups**: Goalkeeper, Defender, Midfielder, Forward
- **10 leagues**: Premier League, La Liga, Serie A, Bundesliga, Ligue 1, MLS, Eredivisie, Primeira Liga, Saudi Pro League, and more
- **Era filter**: 1990s / 2000s / 2010s / 2020s
- **Difficulty filter**: Easy / Medium / Hard
- **Score & streak tracking** in session
- **Interactive career timeline** chart (Plotly Gantt)
- **Statistics tab** with cumulative score chart and round history
- **Player database explorer** — search all 51 players

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
├── app.py           # Streamlit UI (Career Timeline + Footballer Guesser + Stats)
├── game_data.py     # Player database (51 players) + game logic
├── requirements.txt # Dependencies
└── README.md
```
