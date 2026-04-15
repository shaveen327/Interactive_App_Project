import streamlit as st
import pandas as pd

#  Page config 
st.set_page_config(page_title="Calendar | Hoos Hungry?", layout="centered", initial_sidebar_state="collapsed")

# Session state defaults 
if "saved_meals" not in st.session_state:
    st.session_state.saved_meals = []

# CSS 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;900&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"] {
    background: #b8ccb5 !important;
    font-family: 'Nunito', sans-serif !important;
}
[data-testid="stAppViewContainer"] > .main { background: #b8ccb5 !important; padding-bottom: 60px !important; }
#MainMenu, footer { visibility: hidden; }
[data-testid="stToolbar"] { background: #7a9e7e !important; }
header[data-testid="stHeader"] { background: #7a9e7e !important; }
[data-testid="stDecoration"] { display: none; }
[data-testid="stSidebarNav"] { display: block !important; }
[data-testid="stSidebarCollapsedControl"] { display: block !important; }
[data-testid="stCaptionContainer"] p { color: black !important; }

/* Calendar card */
.cal-card { background: #fff; border-radius: 20px; padding: 18px 14px 14px; }
.cal-month-row { display: flex; align-items: center; margin-bottom: 16px; }
.cal-month-label {
    background: #8fa98c; color: #1a1a1a; font-size: 1.7rem; font-weight: 900;
    border-radius: 14px; padding: 10px 32px; flex: 1; text-align: center;
}
.cal-star { font-size: 2rem; margin-left: 12px; }
.cal-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 6px; }
.cal-day-header { text-align: center; font-size: 0.75rem; font-weight: 700; color: #555; padding-bottom: 6px; }
.cal-day {
    background: #8fa98c; border-radius: 50%; aspect-ratio: 1;
    display: flex; flex-direction: column; align-items: center;
    justify-content: center; padding: 4px 2px; cursor: pointer;
}
.cal-day.has-meal { background: #4a7a50; }
.cal-day-num { font-size: 0.55rem; font-weight: 700; color: #fff; align-self: flex-start; padding-left: 5px; }
.cal-lines { display: flex; flex-direction: column; gap: 2px; width: 70%; }
.cal-line { height: 2px; border-radius: 2px; background: #3d6b42; }
.cal-line.light { background: #a8c5a0; }
.cal-empty { aspect-ratio: 1; }

div[data-testid="stButton"] > button {
    background: #6b6b6b !important; color: white !important;
    border: none !important; border-radius: 8px !important;
    font-family: 'Nunito', sans-serif !important; font-weight: 700 !important;
}
div[data-testid="stButton"] > button:hover { background: #4a7a50 !important; }
</style>
""", unsafe_allow_html=True)

# Cached data 
@st.cache_data
def load_calendar_data():
    """Load and cache the pre-populated meal plan for March."""
    return {
        1: ["Oatmeal"], 3: ["Butter Chickpeas"], 5: ["Caesar Wrap"],
        7: ["Samosas", "Greek Salad"], 10: ["Burrito Bowl"],
        12: ["Fettucine Alfredo"], 15: ["Avocado Toast", "Lentil Soup"],
        18: ["Mushroom Spinach Pasta"], 20: ["Veggie Stir Fry"],
        22: ["Caesar Wrap"], 25: ["Butter Chickpeas", "Samosas"],
        28: ["Mozzarella Pesto Sandwich"], 30: ["Lentil Soup"],
    }

meal_data = load_calendar_data()

#  Page title 
st.title("📅 Calendar")

# Layout primitive 1: st.tabs for Month / Week / Day views 
tab_month, tab_week, tab_day = st.tabs(["📅 Month", "📆 Week", "🗓️ Day"])

# Month View 
with tab_month:
    cal_html = '''<div class="cal-card">
      <div class="cal-month-row">
        <div class="cal-month-label">March</div>
        <div class="cal-star">⭐</div>
      </div>
      <div class="cal-grid">'''

    for d in ["Sun.", "Mon.", "Tues.", "Wed.", "Thurs.", "Fri.", "Sat."]:
        cal_html += f'<div class="cal-day-header">{d}</div>'

    for _ in range(6):  # March 1 = Saturday → 6 leading blank cells
        cal_html += '<div class="cal-empty"></div>'

    for day in range(1, 32):
        css = "cal-day has-meal" if day in meal_data else "cal-day"
        lines = "".join([f'<div class="cal-line{"" if i%2==0 else " light"}"></div>' for i in range(4)])
        cal_html += f'<div class="{css}"><div class="cal-day-num">{day}</div><div class="cal-lines">{lines}</div></div>'

    cal_html += '</div></div>'
    st.markdown(cal_html, unsafe_allow_html=True)
    st.caption("Dark circles = days with planned meals")

# Week View 
with tab_week:
    st.subheader("Week of March 24–30")
    week_days = {
        24: meal_data.get(24, []), 25: meal_data.get(25, []),
        26: meal_data.get(26, []), 27: meal_data.get(27, []),
        28: meal_data.get(28, []), 29: meal_data.get(29, []),
        30: meal_data.get(30, [])
    }
    # Layout primitive 2: st.columns for side-by-side day view
    cols = st.columns(7)
    for col, (day_num, meals), name in zip(cols, week_days.items(), ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]):
        with col:
            st.markdown(f"**{name}**\n\n*{day_num}*")
            for m in meals:
                st.markdown(f"🍽 {m}")
            if not meals:
                st.markdown("—")

# Day View 
with tab_day:
    st.subheader("March 26")
    today_meals = meal_data.get(26, [])
    if today_meals:
        for m in today_meals:
            st.info(f"🍽️ {m}")
    else:
        st.warning("No meals planned for today.")

# Add Meal form 
st.write("")
st.subheader("➕ Add a Meal")

# Layout primitive: st.columns for form fields side by side
col_a, col_b = st.columns(2)
with col_a:
    # Widget 1: date input
    # key="add_meal_date" — stable identity prevents date from resetting when other
    # widgets on the page change, avoiding confusing UX for Bob mid-entry
    meal_date = st.date_input("Date", key="add_meal_date")
with col_b:
    # Widget 2: selectbox for meal type
    meal_type = st.selectbox("Meal type", ["Breakfast", "Lunch", "Dinner", "Snack"], key="meal_type_sel")

# Widget 3: text input for meal name
# key="add_meal_name" — required so the field can be individually addressed;
# if we were to add a reset/clear button, the key lets us clear just this field
meal_name = st.text_input("Meal name", placeholder="e.g. Butter Chickpeas", key="add_meal_name")

if st.button("Add Meal ✅", key="add_meal_btn"):
    if meal_name.strip():
        st.session_state.saved_meals.append({
            "date": str(meal_date), "type": meal_type, "name": meal_name
        })
        st.success(f"✅ Added **{meal_name}** ({meal_type}) on {meal_date}!")
    else:
        st.warning("⚠️ Please enter a meal name before saving.")

# Display saved meals as a dataframe if any exist
if st.session_state.saved_meals:
    st.write("**Your planned meals:**")
    st.dataframe(pd.DataFrame(st.session_state.saved_meals), use_container_width=True)
