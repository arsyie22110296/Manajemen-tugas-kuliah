import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time

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
        color: black;
    }
    .stDataFrame {
        background-color: white;
        color: black;
    }
    h1, h2, h3, h4, h5, h6, label, p, div {
        color: black !important;
    }
    </style>
""", unsafe_allow_html=True)


data = load_data()

# Fungsi notifikasi sementara
def show_temp_message(msg, type="success", delay=2):
    placeholder = st.empty()
    if type == "success":
        placeholder.success(msg)
    elif type == "warning":
        placeholder.warning(msg)
    elif type == "error":
        placeholder.error(msg)
    time.sleep(delay)
    placeholder.empty()
   
# Inisialisasi kunci form untuk reset
with st.form("form_tugas"):
    # Gunakan kunci dinamis untuk widget
    if "widget_key" not in st.session_state:
        st.session_state.widget_key = 0

    matkul = st.text_input("Nama Mata Kuliah", key=f"matkul_{st.session_state.widget_key}")
    tugas = st.text_input("Nama Tugas", key=f"tugas_{st.session_state.widget_key}")
    deadline = st.date_input("Deadline", datetime.today() + timedelta(days=7), key=f"deadline_{st.session_state.widget_key}")

    col1, col2 = st.columns(2)
    with col1:
        simpan = st.form_submit_button("💾 Simpan")
    with col2:
        reset = st.form_submit_button("🆕 Tugas Baru")

    if simpan and matkul and tugas:
        new_data = pd.DataFrame([[matkul, tugas, deadline]], columns=["Mata Kuliah", "Tugas", "Deadline"])
        data = pd.concat([data, new_data], ignore_index=True)
        save_data(data)
        st.success(f"✅ Tugas '{tugas}' berhasil disimpan!")

        # Bunyi notifikasi
        st.markdown(
            """
            <audio autoplay>
                <source src="https://www.soundjay.com/buttons/sounds/button-09.mp3" type="audio/mpeg">
            </audio>
            """,
            unsafe_allow_html=True
        )

    if reset:
        # Tambah widget_key untuk buat widget baru
        st.session_state.widget_key += 1
        # Hapus kunci widget lama dari session_state
        old_key = f"matkul_{st.session_state.widget_key - 1}"
        if old_key in st.session_state:
            del st.session_state[old_key]
        old_key = f"tugas_{st.session_state.widget_key - 1}"
        if old_key in st.session_state:
            del st.session_state[old_key]
        old_key = f"deadline_{st.session_state.widget_key - 1}"
        if old_key in st.session_state:
            del st.session_state[old_key]
        st.rerun()

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
        show_temp_message(f"Tugas '{selected_task}' berhasil dihapus!")
        st.rerun()
else:
    st.info("Belum ada tugas yang ditambahkan.")

