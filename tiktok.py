from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
import requests
import os

service = Service("C:/Tools/chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Función principal
def descargar_fotos_facebook(email, password, url_fotos, carpeta_destino="fotos_facebook"):
    try:
        driver.get("https://www.facebook.com")
        time.sleep(6)

        driver.find_element(By.ID, "email").send_keys(email)
        driver.find_element(By.ID, "pass").send_keys(password)
        driver.find_element(By.ID, "pass").send_keys(Keys.RETURN)
        time.sleep(10)

        driver.get(url_fotos)
        time.sleep(10)

        # Crear la carpeta
        os.makedirs(carpeta_destino, exist_ok=True)

        # Scroll infinito para cargar todas las fotos
        scrolls = 3  # Ajusta la cantidad de scrolls según lo necesario
        for _ in range(scrolls):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(6)

        imagenes = driver.find_elements(By.TAG_NAME, "img")
        print(f"Se encontraron {len(imagenes)} imágenes.")

        for i, img in enumerate(imagenes):
            src = img.get_attribute("src")
            if src: 
                try:
                    response = requests.get(src)
                    with open(f"{carpeta_destino}/imagen_{i}.jpg", "wb") as file:
                        file.write(response.content)
                    print(f"Imagen {i} descargada.")
                except Exception as e:
                    print(f"No se pudo descargar la imagen {i}: {e}")

    except Exception as e:
        print(f"Hubo un error: {e}")
    finally:
        driver.quit()
        print("Proceso completado y navegador cerrado.")

# Datos de entrada
email = "Ejemplo@gmailcom"  
password = "Ejemplo de contraseña"
url_fotos = "https://www.facebook.com/profile.php?id=100013256821295&sk=photos" 

descargar_fotos_facebook(email, password, url_fotos)
