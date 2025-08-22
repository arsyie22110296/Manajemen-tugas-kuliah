import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# File untuk simpan data
FILE_NAME = "tugas.csv"

# Load data
def load_data():
    try:
        return pd.read_csv(FILE_NAME)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Mata Kuliah", "Tugas", "Deadline"])

# Save data
def save_data(df):
    df.to_csv(FILE_NAME, index=False)

# UI Streamlit
st.set_page_config(page_title="Manajemen Tugas Kuliah ", page_icon="📚", layout="centered")
# Center judul
st.markdown("""
    <style>
    .centered-title {
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="centered-title">📚 Manajemen Tugas Kuliah Semester 7</h1>', unsafe_allow_html=True)

# CSS untuk dark mode
# CSS untuk dark mode (full background)
st.markdown("""
    <style>
    .stApp {
        background-color: lightcyan;
        color: white;
    }
    .stDataFrame {
        background-color: #1e1e1e;
        color: lightgrey;
    }
    h1, h2, h3, h4, h5, h6, label, p, div {
        color: black !important;
    }
    </style>
""", unsafe_allow_html=True)


data = load_data()

# Form input tugas
with st.form("form_tugas"):
    matkul = st.text_input("Nama Mata Kuliah")
    tugas = st.text_input("Nama Tugas")
    deadline = st.date_input("Deadline", datetime.today() + timedelta(days=7))
    submit = st.form_submit_button("Tambah Tugas")

    if submit and matkul and tugas:
        new_data = pd.DataFrame([[matkul, tugas, deadline]], columns=data.columns)
        data = pd.concat([data, new_data], ignore_index=True)
        save_data(data)
        st.success("✅ Tugas berhasil ditambahkan!")

         # Bunyi notifikasi
        st.markdown(
            """
            <audio autoplay>
                <source src="https://www.soundjay.com/buttons/sounds/button-09.mp3" type="audio/mpeg">
            </audio>
            """,
            unsafe_allow_html=True
        )

# Tampilkan daftar tugas
st.subheader("📋 Daftar Tugas")
if not data.empty:
    # Highlight tugas yang mendekati deadline
    def highlight_deadline(row):
        deadline_date = datetime.strptime(str(row["Deadline"]), "%Y-%m-%d")
        days_left = (deadline_date - datetime.today()).days
        if days_left < 0:
            return ['background-color: #ff4d4d']*3  # Merah (sudah lewat)
        elif days_left <= 3:
            return ['background-color: #ffcc00']*3  # Kuning (mendekati deadline)
        return ['']*3

    st.dataframe(data.style.apply(highlight_deadline, axis=1))
     # Pilih tugas yang mau dihapus
    selected_task = st.selectbox("Pilih tugas yang mau dihapus:", data["Tugas"])
    if st.button("❌ Hapus Tugas"):
        data = data[data["Tugas"] != selected_task]  # filter, hapus yang dipilih
        save_data(data)
        st.success(f"Tugas '{selected_task}' berhasil dihapus!")
        st.experimental_rerun()
else:
    st.info("Belum ada tugas yang ditambahkan.")

