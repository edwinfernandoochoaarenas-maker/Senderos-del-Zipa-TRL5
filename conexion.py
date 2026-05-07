import cv2
import requests
import numpy as np

# Dirección confirmada por tu PING exitoso
url = "http://192.168.1.8:8080/shot.jpg"

print(">>> Probando acceso a la imagen del celular...")

try:
    # Hacemos una petición directa
    respuesta = requests.get(url, timeout=10)
    
    if respuesta.status_code == 200:
        print("✅ ¡Servidor encontrado! Procesando imagen...")
        img_arr = np.array(bytearray(respuesta.content), dtype=np.uint8)
        frame = cv2.imdecode(img_arr, -1)
        
        if frame is not None:
            cv2.imshow("PRUEBA FINAL CONEXION - UNAD", frame)
            cv2.waitKey(0) # Se quedará abierta hasta que presiones una tecla
            cv2.destroyAllWindows()
        else:
            print("❌ La respuesta no es una imagen válida.")
    else:
        print(f"❌ El servidor respondió con error: {respuesta.status_code}")

except Exception as e:
    print(f"❌ Error crítico: {e}")
