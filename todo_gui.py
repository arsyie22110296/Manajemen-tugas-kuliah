import tkinter as tk
from tkinter import ttk, messagebox
import datetime

# Simpan data tugas dalam list of dict
tugas_list = []

def tambah_tugas():
    matkul = entry_matkul.get()
    nama_tugas = entry_tugas.get()
    deadline = entry_deadline.get()

    if matkul and nama_tugas and deadline:
        try:
            # cek apakah format tanggal valid (YYYY-MM-DD)
            deadline_date = datetime.datetime.strptime(deadline, "%Y-%m-%d").date()
            
            tugas = {
                "matkul": matkul,
                "tugas": nama_tugas,
                "deadline": deadline_date
            }
            tugas_list.append(tugas)

            # masukkan ke tabel
            tree.insert("", tk.END, values=(matkul, nama_tugas, deadline))
            
            # clear input
            entry_matkul.delete(0, tk.END)
            entry_tugas.delete(0, tk.END)
            entry_deadline.delete(0, tk.END)

        except ValueError:
            messagebox.showwarning("Format Salah", "Gunakan format tanggal: YYYY-MM-DD")
    else:
        messagebox.showwarning("Peringatan", "Semua field harus diisi!")

def hapus_tugas():
    selected = tree.selection()
    if selected:
        for item in selected:
            tree.delete(item)
        messagebox.showinfo("Info", "Tugas dihapus!")
    else:
        messagebox.showwarning("Peringatan", "Pilih tugas yang ingin dihapus!")

def cek_deadline():
    today = datetime.date.today()
    warning_list = []
    for tugas in tugas_list:
        sisa = (tugas["deadline"] - today).days
        if sisa < 0:
            warning_list.append(f"{tugas['tugas']} (TELAT)")
        elif sisa <= 2:
            warning_list.append(f"{tugas['tugas']} (Deadline {sisa} hari lagi!)")

    if warning_list:
        messagebox.showwarning("Deadline Alert", "\n".join(warning_list))
    else:
        messagebox.showinfo("Deadline Alert", "Belum ada deadline dekat 😊")

# === Setup GUI ===
root = tk.Tk()
root.title("📚 Manajemen Tugas Kuliah")
root.geometry("600x400")

# Styling pakai ttk
style = ttk.Style()
style.configure("TButton", font=("Arial", 10), padding=5)
style.configure("Treeview.Heading", font=("Arial", 11, "bold"))

frame_input = tk.Frame(root, pady=10)
frame_input.pack()

tk.Label(frame_input, text="Mata Kuliah:").grid(row=0, column=0, padx=5, pady=5)
entry_matkul = tk.Entry(frame_input)
entry_matkul.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Nama Tugas:").grid(row=1, column=0, padx=5, pady=5)
entry_tugas = tk.Entry(frame_input)
entry_tugas.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Deadline (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5)
entry_deadline = tk.Entry(frame_input)
entry_deadline.grid(row=2, column=1, padx=5, pady=5)

btn_frame = tk.Frame(root, pady=10)
btn_frame.pack()

ttk.Button(btn_frame, text="Tambah Tugas", command=tambah_tugas).grid(row=0, column=0, padx=10)
ttk.Button(btn_frame, text="Hapus Tugas", command=hapus_tugas).grid(row=0, column=1, padx=10)
ttk.Button(btn_frame, text="Cek Deadline", command=cek_deadline).grid(row=0, column=2, padx=10)

# Tabel daftar tugas
columns = ("matkul", "tugas", "deadline")
tree = ttk.Treeview(root, columns=columns, show="headings", height=8)
tree.heading("matkul", text="Mata Kuliah")
tree.heading("tugas", text="Tugas")
tree.heading("deadline", text="Deadline")
tree.pack(fill="both", expand=True, pady=10)

root.mainloop()
