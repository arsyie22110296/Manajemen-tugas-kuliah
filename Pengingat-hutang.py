import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time

# File untuk simpan data
FILE_NAME = "hutang.csv"

# Load data
def load_data():
    try:
        return pd.read_csv(FILE_NAME)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Nama Peminjam", "Jumlah Hutang", "Tenggat", "Keterangan"])

# Save data
def save_data(df):
    df.to_csv(FILE_NAME, index=False)

# UI Streamlit
st.set_page_config(page_title="Pengingat Hutang", page_icon="💰", layout="centered")

# Center judul
st.markdown("""
    <style>
    .centered-title {
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="centered-title">💰 Pengingat Hutang</h1>', unsafe_allow_html=True)

# CSS untuk tampilan (mirip app tugas kuliah)
st.markdown("""
    <style>
    /* Background utama dengan gradien */
    .stApp {
        background: linear-gradient(to bottom right, #B3E5FC, #2A4066) !important;
        color: black !important;
        min-height: 100vh; /* Pastikan background full */
    }
    /* Pastikan elemen input tetap putih */
    .stTextInput > div > div > input {
        background-color: white !important;
        color: black !important;
        border: 1px solid #ccc !important;
    }
    .stNumberInput > div > div > input {
        background-color: white !important;
        color: black !important;
        border: 1px solid #ccc !important;
    }
    .stDateInput > div > div > input {
        background-color: white !important;
        color: black !important;
        border: 1px solid #ccc !important;
    }
    .stSelectbox > div > div > select {
        background-color: white !important;
        color: black !important;
        border: 1px solid #ccc !important;
    }
    /* Tombol hijau */
    .stButton > button {
        background-color: #4CAF50 !important;
        color: white !important;
        border: none !important;
        padding: 8px 16px !important;
        border-radius: 4px !important;
        transition: all 0.3s ease; /* Animasi halus */
    }
    .stButton > button:hover {
        background-color: #45a049 !important;
    }
    /* Tabel putih */
    .stDataFrame {
        background-color: white !important;
        color: black !important;
    }
    /* Teks hitam untuk semua elemen */
    h1, h2, h3, h4, h5, h6, label, p, div {
        color: black !important;
    }
    </style>
""", unsafe_allow_html=True)

# Load data
data = load_data()

# Fungsi notifikasi sementara
def show_temp_message(msg, type="success", delay=2):
    placeholder = st.empty()
    if type == "success":
        placeholder.success(msg)
    elif type == "error":
        placeholder.error(msg)
    time.sleep(delay)
    placeholder.empty()

# Form input hutang
with st.form("form_hutang"):
    if "widget_key" not in st.session_state:
        st.session_state.widget_key = 0

    nama = st.text_input("Nama Peminjam", key=f"nama_{st.session_state.widget_key}")
    jumlah = st.number_input("Jumlah Hutang (Rp)", min_value=0, step=100000, key=f"jumlah_{st.session_state.widget_key}")
    tenggat = st.date_input("Tenggat Bayar", datetime.today() + timedelta(days=7), key=f"tenggat_{st.session_state.widget_key}")
    keterangan = st.text_input("Keterangan (opsional)", key=f"keterangan_{st.session_state.widget_key}")

    col1, col2 = st.columns(2)
    with col1:
        simpan = st.form_submit_button("💾 Simpan")
    with col2:
        reset = st.form_submit_button("🆕 Input Baru")

    if simpan and nama and jumlah:
        new_data = pd.DataFrame([[nama, jumlah, tenggat, keterangan]], columns=["Nama Peminjam", "Jumlah Hutang", "Tenggat", "Keterangan"])
        data = pd.concat([data, new_data], ignore_index=True)
        save_data(data)
        show_temp_message(f"✅ Data hutang '{nama}' berhasil disimpan!")
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
        st.session_state.widget_key += 1
        # Hapus kunci widget lama
        for key in [f"nama_{st.session_state.widget_key-1}", f"jumlah_{st.session_state.widget_key-1}", 
                    f"tenggat_{st.session_state.widget_key-1}", f"keterangan_{st.session_state.widget_key-1}"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

# Tampilkan daftar hutang
st.subheader("📋 Daftar Hutang")
if not data.empty:
    # Highlight tenggat yang mendekati atau lewat
    def highlight_tenggat(row):
        tenggat_date = datetime.strptime(str(row["Tenggat"]), "%Y-%m-%d")
        days_left = (tenggat_date - datetime.today()).days
        if days_left < 0:
            return ['background-color: #ff4d4d']*4  # Merah (lewat)
        elif days_left <= 3:
            return ['background-color: #ffcc00']*4  # Kuning (dekat)
        return ['']*4

    st.dataframe(data.style.apply(highlight_tenggat, axis=1))

    # Hapus hutang
    selected_hutang = st.selectbox("Pilih hutang yang mau dihapus:", data["Nama Peminjam"])
    if st.button("❌ Hapus Hutang"):
        data = data[data["Nama Peminjam"] != selected_hutang]
        save_data(data)
        show_temp_message(f"Data Hutang '{selected_hutang}' berhasil dihapus!")
        st.rerun()
else:
    st.info("Belum ada data hutang yang ditambahkan.")