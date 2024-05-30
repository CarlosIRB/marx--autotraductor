#Carlos Ismael Ramirez Bello
from deep_translator import GoogleTranslator

from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re
from translate import Translator

#Ejecutar el siguiente comando en la terminal para instalar las librerias necesarias
#pip install deep-translator
#pip install translate
#pip install selenium

#funciones de manejo de texto
def traducir(texto):
    idioma_destino = "es"
    return GoogleTranslator(source='auto', target=idioma_destino).translate(texto)

    # idioma_destino = "es"
    # translator = Translator(to_lang=idioma_destino)
    # translation = translator.translate(texto)
    # return translation


def extraer_llaves(texto):
    texto_dentro_llaves = re.findall(r'{.*?}', texto)
    return texto_dentro_llaves
def extraer_tags(texto):
    # Extraer texto dentro de etiquetas <>
    texto_dentro_tags = re.findall(r'<[^>]+>', texto)
    return texto_dentro_tags

def traducir_correo(correo):
    correo_tratado = re.sub(r'<a\s+href="[^"]*"\s+class="button_link".*?>', '<ahl>', correo)
    correo_tratado = re.sub(r'<a\s+href="[^"]*".*?>', '<ah>', correo_tratado)
    texto_traducido = traducir(correo_tratado)
    
    texto_dentro_tags = extraer_tags(correo)
    texto_dentro_llaves = extraer_llaves(correo_tratado)
    # Diccionario para almacenar los valores originales de las llaves
    tags_cambiados = extraer_tags(texto_traducido)
    llaves_cambiadas = extraer_llaves(texto_traducido)
    
    # Crear un diccionario donde las claves son las llaves encontradas y los valores son los textos dentro de las llaves
    diccionario_reemplazo = {}
    for llave in llaves_cambiadas:
        # Asumiendo que cada llave tiene un valor único en texto_dentro_llaves, obtenemos ese valor
        valor_llave = texto_dentro_llaves[llaves_cambiadas.index(llave)]
        # Agregamos al diccionario
        diccionario_reemplazo[llave] = valor_llave
    
    texto_final = texto_traducido
    for llave, valor in diccionario_reemplazo.items():
        texto_final = texto_final.replace(llave , valor)
    
    #lo mismo pero con tags
    diccionario_reemplazo_tags = {}
    for tag in tags_cambiados:
        valor_tag = texto_dentro_tags[tags_cambiados.index(tag)]
        diccionario_reemplazo_tags[tag] = valor_tag
    # Reemplazar las llaves en texto_traducido con sus valores correspondientes
    for tag, valor in diccionario_reemplazo_tags.items():
        texto_final = texto_final.replace(tag , valor)
    
    
    return texto_final

def version_txt(texto):
    correo_tratado = re.sub(r'<a\s+href="[^"]*"\s+class="button_link".*?>', '<ahl>', texto)
    correo_tratado = re.sub(r'<a\s+href="[^"]*".*?>', '<ah>', correo_tratado)
    texto_tratado = re.sub(r'(<ahl>.*?</a>)', r'\1 : {link_report}', correo_tratado)
    # Expresión regular que captura todo entre <>
    patron = r'<[^>]+>'
    # Reemplaza todo lo que coincida con el patrón por ''
    texto_sin_etiquetas = re.sub(patron, '', texto_tratado)
    return texto_sin_etiquetas

driver = webdriver.Chrome()
driver.get('https://marxe-qa..../')

# Maximizar la ventana
driver.maximize_window()

# Iniciar sesión
username = driver.find_element(By.ID, 'email')
password = driver.find_element(By.ID, 'passwd')
username.send_keys('...')
password.send_keys('...')
driver.find_element(By.ID, 'submit_login').click()


WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//li[@id='subtab-AdminInternational']/a")))
# Localiza el elemento al que quieres desplazarte
element = driver.find_element(By.XPATH, "//li[@id='subtab-AdminInternational']/a")
# Utiliza JavaScript para desplazarte hasta el elemento
driver.execute_script("arguments[0].scrollIntoView();", element)
# Ahora intenta hacer clic en el elemento
element.click()
time.sleep(1)

driver.find_element(By.XPATH, "//li[@id='subtab-AdminTranslations']/a").click()
time.sleep(1)

WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "form_translation_type")))
select_element = driver.find_element(By.ID, "form_translation_type")
select = Select(select_element)
select.select_by_value("mails")
time.sleep(1)

select_element = driver.find_element(By.ID, "form_email_content_type")
select = Select(select_element)
select.select_by_value("body")
time.sleep(1)

WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.ID, "form_theme")))
select_element = driver.find_element(By.ID, "form_theme")
select = Select(select_element)
select.select_by_value("0")
time.sleep(1)


select_element = driver.find_element(By.ID, "form_language")
select = Select(select_element)
select.select_by_value("mx")

time.sleep(1)
driver.find_element(By.XPATH, "//span[contains(text(),'Modificar')]/parent::button").click()

#esperar a que carge el contenido
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "translations_form")))
time.sleep(2)
enlace_seccion =driver.find_element(By.XPATH,"//a[contains(text(),'ets_marketplace')]")

driver.execute_script("arguments[0].scrollIntoView();",enlace_seccion)
time.sleep(1)
enlace_seccion.click()

panels = driver.find_elements(By.XPATH, "//div[@class='mails_field']/div[@id='ets_marketplace']/div")

contador=0
traducciones_deseadas = 1000


for index,panel in enumerate(panels):
    try:
        print("Nueva traduccion")
        driver.execute_script("arguments[0].scrollIntoView(true);", panel)
        time.sleep(1)
        
        # Encontrar y hacer clic en "abrir correo" usando JavaScript
        abrir_correo = panel.find_element(By.XPATH, "./a")
        driver.execute_script("arguments[0].click();", abrir_correo)
        time.sleep(1)
        
        # Encontrar y hacer clic en "Editar versión HTML" usando JavaScript
        editor = panel.find_element(By.XPATH, "./div/ul//li/a[contains(text(),'Editar versión HTML')]")
        driver.execute_script("arguments[0].scrollIntoView(true);", editor)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", editor)
        
        if contador < traducciones_deseadas:
            # Explora todos los tr del panel
                time.sleep(1)
                
                iframe_contenido = panel.find_elements(By.XPATH,".//iframe")[1]
                
                driver.switch_to.frame(iframe_contenido)
                print("...")
                # esperar a que carge el siguiente elemento para poder hacer click
                time.sleep(1)
                
                
                parrafo = driver.find_elements(By.XPATH,"//table[@class='table table-mail mce-item-table']//table//td[@class='box']//tr[2]/td[2]/div//p")
                
                correo_completo =""
                for i,renglon in enumerate(parrafo):
                    correo_completo += renglon.get_attribute('innerHTML') +"\n"
                    
                correo_completo = correo_completo.replace('Yours sincerely.', 'Atentamente.')
                print("caja 1")
                
                correo_traducido = traducir_correo(correo_completo)
                
                
                renglones_correo = correo_traducido.split("\n")
                correo_version_txt = version_txt(correo_traducido)
                
                
                
                for i,renglon in enumerate(parrafo):
                    driver.execute_script("arguments[0].innerHTML = arguments[1];", renglon, renglones_correo[i])
                    
                input()
                print("caja 2")
                driver.switch_to.default_content()
                time.sleep(1)
                if correo_version_txt != "":
                    enlace_txt = panel.find_element(By.XPATH,".//a[contains(text(),'TXT')]")
                    driver.execute_script("arguments[0].scrollIntoView(true);", enlace_txt)
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", enlace_txt)
                    
                    parrafo_txt = panel.find_element(By.XPATH,".//textarea[@class='rte noEditor']")
                    driver.execute_script("arguments[0].innerHTML = arguments[1];", parrafo_txt, correo_version_txt)
                    input()
                contador+=1
                
                print(f"Fin {contador}")
                if contador == 5:
                    input()
        else:
            break
    except Exception as e:
        driver.switch_to.default_content()
        print(e)

print(f"Se tradujeron {contador} textos")
print("Presiona Enter para continuar...")
input()
