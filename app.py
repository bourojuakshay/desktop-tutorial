import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Shooting Game - Au", page_icon="🎮", layout="centered")

st.title("🎯 Shooting Game - Au")
st.markdown("""
Welcome to **Shooting Game - Au** made with Pygame.

- Use **Arrow Keys** to move.
- Press **SPACE** to shoot.
- Press **P** to Pause.
- Avoid enemies hitting the bottom!
""")

if st.button("▶️ Start Game"):
    if os.name == 'nt':  # For Windows
        subprocess.Popen(["python", "game.py"], shell=True)
    else:  # macOS/Linux
        subprocess.Popen(["python3", "game.py"])

st.markdown("---")
st.subheader("📈 High Score")

# Show the current high score
try:
    with open("highscore.txt", "r") as f:
        high_score = int(f.read())
    st.success(f"Current High Score: **{high_score}**")
except:
    st.info("No high score found yet.")
