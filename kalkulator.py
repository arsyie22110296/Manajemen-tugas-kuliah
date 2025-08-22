print("=== Kalkulator Sederhana ===")

angka1 = float(input("Masukkan angka pertama: "))
angka2 = float(input("Masukkan angka kedua: "))

print("Pilih operasi (+, -, *, /)")
operasi = input("Masukkan operasi: ")

if operasi == "+":
    hasil = angka1 + angka2
elif operasi == "-":
    hasil = angka1 - angka2
elif operasi == "*":
    hasil = angka1 * angka2
elif operasi == "/":
    if angka2 != 0:
        hasil = angka1 / angka2
    else:
        hasil = "Error: pembagian dengan nol!"
else:
    hasil = "Operasi tidak dikenal."

print("Hasil:", hasil)
