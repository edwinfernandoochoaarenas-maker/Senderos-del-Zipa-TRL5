import cv2
import pytesseract
import requests
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import threading
import time

# --- CONFIGURACIÓN ---
TOKEN = "7871363448:AAH3ohp0dKU6S7RiThGbbx8oLiy_LLSEEZQ"
CHAT_ID = "8277533417"
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
url_camara = "http://192.168.1.8:8080/shot.jpg"
residentes = ["ABC123", "UNAD26", "AGH430"]

class AppSenderosZipa:
    def __init__(self, root):
        self.root = root
        self.root.title("SENDEROS DEL ZIPA - TRL5")
        self.root.geometry("850x700")
        self.root.configure(bg="#1a1a1a")

        self.monitoreo_activo = False
        self.ultima_placa_confirmada = "" 

        # --- ESTRUCTURA ---
        self.frame_video = tk.Frame(self.root, bg="black", width=850, height=400)
        self.frame_video.pack(side="top", fill="both", expand=True)
        
        self.video_label = tk.Label(self.frame_video, bg="black")
        self.video_label.pack(expand=True)

        self.frame_controles = tk.Frame(self.root, bg="#2d2d2d", height=250, bd=2, relief="raised")
        self.frame_controles.pack(side="bottom", fill="x")

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.frame_controles, text="LECTURA EN TIEMPO REAL:", fg="#00ffcc", bg="#2d2d2d", font=("Arial", 10, "bold")).pack(pady=(10, 0))
        self.lbl_placa = tk.Label(self.frame_controles, text="---", fg="yellow", bg="#2d2d2d", font=("Consolas", 36, "bold"))
        self.lbl_placa.pack()

        self.lbl_estado = tk.Label(self.frame_controles, text="ESPERANDO COINCIDENCIA...", fg="white", bg="#2d2d2d", font=("Arial", 10))
        self.lbl_estado.pack(pady=5)

        self.btn_frame = tk.Frame(self.frame_controles, bg="#2d2d2d")
        self.btn_frame.pack(pady=20)

        self.btn_start = tk.Button(self.btn_frame, text="INICIAR MONITOR", command=self.start_thread, 
                                   bg="#28a745", fg="white", font=("Arial", 10, "bold"), width=20, height=2)
        self.btn_start.pack(side="left", padx=10)

        self.btn_stop = tk.Button(self.btn_frame, text="DETENER", command=self.stop_monitoreo, 
                                  bg="#dc3545", fg="white", font=("Arial", 10, "bold"), width=15, height=2)
        self.btn_stop.pack(side="left", padx=10)

    def start_thread(self):
        if not self.monitoreo_activo:
            self.monitoreo_activo = True
            self.btn_start.config(state="disabled")
            threading.Thread(target=self.proceso, daemon=True).start()

    def stop_monitoreo(self):
        self.monitoreo_activo = False
        self.btn_start.config(state="normal")
        self.lbl_placa.config(text="---", fg="yellow")

    def enviar_telegram(self, msg):
        try:
            requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}", timeout=5)
        except: pass

    def proceso(self):
        while self.monitoreo_activo:
            try:
                resp = requests.get(url_camara, timeout=3)
                img_raw = cv2.imdecode(np.array(bytearray(resp.content), dtype=np.uint8), -1)
                if img_raw is None: continue

                frame = cv2.resize(img_raw, (700, 450))
                h, w = 450, 700
                
                # ZONA DE ESCANEO
                rw, rh = 450, 180
                x1, y1 = (w - rw) // 2, (h - rh) // 2
                roi = frame[y1:y1+rh, x1:x1+rw]
                
                gris = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                umbral = cv2.threshold(cv2.GaussianBlur(gris, (5,5), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                
                config = '-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 7'
                texto = pytesseract.image_to_string(umbral, config=config).strip()
                placa_detectada = "".join(e for e in texto if e.isalnum()).upper()

                # Dibujar el área en el video
                cv2.rectangle(frame, (x1, y1), (x1+rw, y1+rh), (0, 255, 255), 3)

                # --- LÓGICA DE COINCIDENCIA EXACTA ---
                if len(placa_detectada) == 6:
                    self.lbl_placa.config(text=placa_detectada)
                    
                    # Si la placa detectada es una de las que esperamos (Residentes o Alertas conocidas)
                    # O si simplemente quieres que se detenga al detectar CUALQUIER placa de 6 dígitos bien formada
                    if placa_detectada != self.ultima_placa_confirmada:
                        
                        # Mostramos el acierto en la UI
                        if placa_detectada in residentes:
                            self.lbl_placa.config(fg="#00ff00")
                            self.lbl_estado.config(text="COINCIDENCIA: RESIDENTE")
                            threading.Thread(target=self.enviar_telegram, args=(f"✅ ACCESO: {placa_detectada}",)).start()
                        else:
                            self.lbl_placa.config(fg="#ff3333")
                            self.lbl_estado.config(text="COINCIDENCIA: EXTERNO")
                            threading.Thread(target=self.enviar_telegram, args=(f"🚨 ALERTA: {placa_detectada}",)).start()

                        # 1. Actualizamos el video para que se vea la placa con el cuadro amarillo
                        img_tk = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
                        self.video_label.configure(image=img_tk)
                        self.video_label.image = img_tk

                        # 2. PAUSA DE 3 SEGUNDOS (Aquí se detiene el escaneo)
                        time.sleep(3)
                        
                        # 3. Limpiamos para seguir
                        self.lbl_placa.config(text="---", fg="yellow")
                        self.lbl_estado.config(text="BUSCANDO NUEVA COINCIDENCIA...")

                # Actualización normal del video
                img_tk = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
                self.video_label.configure(image=img_tk)
                self.video_label.image = img_tk
                
            except: time.sleep(0.5)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppSenderosZipa(root)
    root.mainloop()
