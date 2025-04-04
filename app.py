import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# File to store data
data_file = "fitness_data.csv"

# Estimated calories burned per minute for different workouts
calories_per_min = {
    "Running": 10,
    "Cycling": 8,
    "Yoga": 4,
    "Strength Training": 7,
    "Other": 5
}

# Check if file exists, otherwise create one
if not os.path.exists(data_file):
    df = pd.DataFrame(columns=["Date", "Workout Type", "Duration (min)", "Calories Burned"])
    df.to_csv(data_file, index=False)

# Load the data
def load_data():
    return pd.read_csv(data_file)

def save_data(data):
    data.to_csv(data_file, index=False)

st.title("🏋️ Fitness Tracker")

# Sidebar - Input section
st.sidebar.header("Log Your Workout")
date = st.sidebar.date_input("Date")
workout_type = st.sidebar.selectbox("Workout Type", list(calories_per_min.keys()))
duration = st.sidebar.number_input("Duration (minutes)", min_value=1, max_value=300, step=1)

# Automatically calculate calories burned
calories = duration * calories_per_min[workout_type]

if st.sidebar.button("Add Entry"):
    new_entry = pd.DataFrame({"Date": [date], "Workout Type": [workout_type], "Duration (min)": [duration], "Calories Burned": [calories]})
    df = load_data()
    df = pd.concat([df, new_entry], ignore_index=True)
    save_data(df)
    st.sidebar.success(f"Workout added successfully! Estimated Calories Burned: {calories}")

# Display the data
df = load_data()
st.subheader("Workout History")
st.dataframe(df)

# Modern Visualization
st.subheader("📊 Progress Overview")
if not df.empty:
    df["Date"] = pd.to_datetime(df["Date"])
    df_sorted = df.sort_values("Date")
    
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=df_sorted, x="Date", y="Calories Burned", marker="o", linewidth=2, color="royalblue")
    ax.fill_between(df_sorted["Date"], df_sorted["Calories Burned"], alpha=0.3, color="royalblue")
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Calories Burned", fontsize=12)
    ax.set_title("Calories Burned Over Time", fontsize=14, fontweight='bold')
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.info("No data available. Please log your workouts.")
