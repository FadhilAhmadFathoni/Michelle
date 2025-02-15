import pygame
import threading
import speech_recognition as srec
from gtts import gTTS
import os
import webbrowser
import time
from datetime import datetime

NAMA_ASISTEN = "michelle"  # Nama asisten suara

# Inisialisasi pygame untuk pemutaran suara
pygame.mixer.init()

sedang_berbicara = False  # Flag untuk mengontrol pendengaran


print(f"Pustaka berhasil diimpor! Panggil \"{NAMA_ASISTEN}\" untuk mulai.")

pengingat_list = []  # List untuk menyimpan pengingat

def ngomong(teks):
    """Memainkan suara dengan gTTS dan menunggu hingga selesai"""
    global sedang_berbicara
    if teks:
        sedang_berbicara = True  

        bahasa = 'id'
        namafile = 'Ngomong.mp3'

        # Jika file masih ada, pastikan pygame tidak menggunakannya sebelum menghapus
        if os.path.exists(namafile):
            try:
                pygame.mixer.quit()  # Matikan pygame untuk melepaskan file
                time.sleep(0.5)  # Tunggu sejenak agar pygame benar-benar tertutup
                os.remove(namafile)  # Hapus file
            except PermissionError:
                print("File masih digunakan, tidak bisa dihapus.")
                return  # Keluar dari fungsi untuk mencegah error lebih lanjut

        # Simpan suara baru
        suara = gTTS(text=teks, lang=bahasa, slow=False)
        suara.save(namafile)

        # Re-inisialisasi pygame setelah quit
        pygame.mixer.init()
        pygame.mixer.music.load(namafile)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.quit()  # Pastikan pygame dilepas setelah pemutaran
        sedang_berbicara = False  

def perintah():
    """Mendengarkan perintah suara, tetapi menunggu jika sedang berbicara"""
    global sedang_berbicara
    mendengar = srec.Recognizer()
    
    with srec.Microphone() as source:
        while sedang_berbicara:  # Tunggu jika sedang berbicara
            time.sleep(0.1)

        mendengar.adjust_for_ambient_noise(source)  # Sesuaikan dengan noise sekitar
        print('Mendengarkan...')
        try:
            suara = mendengar.listen(source, phrase_time_limit=5)
            print('Diterima...')
            dengar = mendengar.recognize_google(suara, language='id-ID').lower()
            print(f'Anda berkata: {dengar}')
            return dengar
        except srec.UnknownValueError:
            print("Maaf, saya tidak mengerti.")
            return None
        except srec.RequestError:
            print("Terjadi kesalahan pada layanan pengenalan suara.")
            return None

def cek_waktu():
    sekarang = datetime.now()
    hari = sekarang.strftime("%A").lower()
    tanggal = sekarang.strftime("%d %B %Y")
    jam = sekarang.strftime("%H")
    waktu_hari = "pagi" if 5 <= int(jam) < 12 else "siang" if 12 <= int(jam) < 18 else "malam"
    ngomong(f"Hari ini hari {hari}, pukul {sekarang.strftime('%H:%M')} {waktu_hari}, tanggal {tanggal}.")

def atur_pengingat(waktu, pesan):
    global pengingat_list
    waktu = waktu.zfill(5)  # Pastikan format selalu HH:MM
    pengingat_list.append((waktu, pesan))
    print(f"Pengingat disimpan: {pengingat_list}")  # Debugging
    ngomong(f"Pengingat telah diset untuk pukul {waktu}.")

def cek_pengingat():
    while True:
        sekarang = datetime.now().strftime("%H:%M")
        for waktu, pesan in pengingat_list:
            if waktu == sekarang:
                for _ in range(2):
                    ngomong(f"Sekarang pukul {waktu}. Jangan lupa {pesan} ya!")
                    time.sleep(5)  # Beri jeda 5 detik antara pengulangan
                pengingat_list.remove((waktu, pesan))  # Hapus pengingat setelah eksekusi
        time.sleep(30)  # Cek setiap 30 detik


def buka_terjemahan(teks):
    if teks:
        ngomong(f"Menerjemahkan: {teks}")
        teks_url = teks.replace(" ", "%20")  # Format URL
        url = f"https://translate.google.co.id/?hl=id&sl=en&tl=id&text={teks_url}&op=translate"
        webbrowser.open(url)

def buka_chatgpt():
    ngomong("Membuka ChatGPT...")
    webbrowser.open("https://chatgpt.com/")

def buka_youtube():
    ngomong("Membuka Youtube...")
    webbrowser.open("https://www.youtube.com/")

def buka_notepad():
    ngomong("Membuka Notepad.")
    os.system("start notepad")  # Membuka Notepad di Windows

def tutup_notepad():
    ngomong("Menutup Notepad.")
    os.system("taskkill /IM notepad.exe /F")  # Memaksa menutup Notepad di Windows

def buka_file_explorer():
    ngomong("Membuka File Explorer.")
    os.system("explorer")

def tutup_file_explorer():
    ngomong("Menutup File Explorer.")
    os.system("taskkill /IM explorer.exe /F")
    os.system("start explorer")

def bantuan():
    daftar_perintah = """
    Saya Michelle bisa melakukan hal-hal berikut:
    - "Buka Google" untuk membuka Google
    - "Buka ChatGPT" untuk membuka ChatGPT
    - "Buka Youtube" untuk membuka Youtube
    - "Buka Notepad" atau "Tutup Notepad"
    - "Buka Folder" atau "Tutup Folder"
    - "Hari apa sekarang" untuk cek waktu
    - "Pengingat. Contoh ingatkan saya pukul 08:00 untuk makan"
    - "Terjemahkan [teks]" untuk menerjemahkan ke Indonesia
    - "Keluar" untuk menutup program
    """
    ngomong(daftar_perintah)
    print(daftar_perintah)

def jalankan_perintah(perintah):
    if "buka google" in perintah:
        ngomong("Membuka Google...")
        webbrowser.open("https://www.google.com")
    elif "buka chat gpt" in perintah:
        buka_chatgpt()
    elif "buka youtube" in perintah:
        buka_youtube()
    elif "buka notepad" in perintah:
        buka_notepad()
    elif "tutup notepad" in perintah:
        tutup_notepad()
    elif "buka folder" in perintah:
        buka_file_explorer()
    elif "tutup folder" in perintah:
        tutup_file_explorer()
    elif "hari apa sekarang" in perintah:
        cek_waktu()
    elif "ingatkan saya" in perintah:
        try:
            parts = perintah.replace("ingatkan saya", "").strip().split("untuk")
            waktu = parts[0].strip().replace("pukul ", "").replace(".", ":")  # Ganti titik ke titik dua
            pesan = parts[1].strip() if len(parts) > 1 else "Jangan lupa melakukan tugas Anda."
            waktu = waktu.zfill(5)  # Pastikan formatnya selalu HH:MM
            atur_pengingat(waktu, pesan)
        except:
            ngomong("Format pengingat tidak dikenali. Coba katakan 'Michelle, ingatkan saya pukul 08:00 untuk makan'.")
    elif "halo" in perintah:
        ngomong("Halo! Apa kabar?")
    elif "bantuan" in perintah or "apa yang bisa kamu lakukan" in perintah:
        bantuan()
    elif "terjemahkan" in perintah:
        teks = perintah.replace("terjemahkan", "").strip()
        if teks:
            buka_terjemahan(teks)
        else:
            ngomong("Apa yang ingin Anda terjemahkan?")
    elif "keluar" in perintah:
        ngomong("Sampai jumpa!")
        exit()
    else:
        ngomong("Maaf, saya tidak mengerti perintah itu.")

def run_michelle():
    threading.Thread(target=cek_pengingat, daemon=True).start()
    while True:
        layanan = perintah()
        if layanan:
            if "keluar" in layanan:
                ngomong("Sampai jumpa!")
                break
            elif NAMA_ASISTEN in layanan:  # Cek apakah nama asisten disebut
                layanan = layanan.replace(NAMA_ASISTEN, "").strip()  # Hapus nama asisten dari teks
                if layanan:  # Jika masih ada perintah setelah menyebut nama
                    jalankan_perintah(layanan)
                else:
                    ngomong(f"Ya, ada yang bisa saya bantu?")
            else:
                print("Menunggu panggilan...")
        time.sleep(0.5)  # Tambahkan jeda 0.5 detik sebelum mendengar lagi

if __name__ == "__main__":
    ngomong(f"Halo, nama saya {NAMA_ASISTEN}. Saya adalah asisten virtual Anda. Silakan panggil saya jika butuh bantuan.")
    run_michelle()  # Mulai asisten suara
