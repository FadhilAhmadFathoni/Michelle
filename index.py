import speech_recognition as srec
from gtts import gTTS
import os
import webbrowser

NAMA_ASISTEN = "michelle"  # Nama asisten suara

print(f"Pustaka berhasil diimpor! Panggil \"{NAMA_ASISTEN}\" untuk mulai.")

def ngomong(teks):
    if teks:  
        bahasa = 'id'
        namafile = 'Ngomong.mp3'
        suara = gTTS(text=teks, lang=bahasa, slow=False)
        suara.save(namafile)
        
        if os.name == 'nt':  
            os.system(f'start {namafile}')
        else:  
            os.system(f'xdg-open {namafile}')

def perintah():
    mendengar = srec.Recognizer()
    with srec.Microphone() as source:
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

def buka_terjemahan(teks):
    if teks:
        ngomong(f"Menerjemahkan: {teks}")
        teks_url = teks.replace(" ", "%20")  # Format URL
        url = f"https://translate.google.co.id/?hl=id&sl=en&tl=id&text={teks_url}&op=translate"
        webbrowser.open(url)

def buka_chatgpt():
    ngomong("Membuka ChatGPT...")
    webbrowser.open("https://chatgpt.com/")

def buka_notepad():
    ngomong("Membuka Notepad.")
    os.system("start notepad")  # Membuka Notepad di Windows

def tutup_notepad():
    ngomong("Menutup Notepad.")
    os.system("taskkill /IM notepad.exe /F")  # Memaksa menutup Notepad di Windows

def jalankan_perintah(perintah):
    if "buka google" in perintah:
        ngomong("Membuka Google...")
        webbrowser.open("https://www.google.com")
    elif "buka chat gpt" in perintah:
        buka_chatgpt()
    elif "buka notepad" in perintah:
        buka_notepad()
    elif "tutup notepad" in perintah:
        tutup_notepad()
    elif "halo" in perintah:
        ngomong("Halo! Apa kabar?")
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

if __name__ == "__main__":
    # Perkenalan saat program dijalankan
    ngomong(f"Halo, nama saya {NAMA_ASISTEN}. Saya adalah asisten virtual Anda. Silakan panggil saya jika butuh bantuan.")
    
    run_michelle()  # Mulai asisten suara
