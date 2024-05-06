from deep_translator import GoogleTranslator

from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from translate import Translator

#Ejecutar el siguiente comando en la terminal para instalar las librerias necesarias
#pip install deep-translator
#pip install translate
#pip install selenium


def traducir_espaniol(texto):
    idioma_destino = "es"
    return GoogleTranslator(source='auto', target=idioma_destino).translate(texto)

    # idioma_destino = "es"
    # translator = Translator(to_lang=idioma_destino)
    # translation = translator.translate(texto)
    # return translation


driver = webdriver.Chrome()
driver.get('https://marxe-qa.forteinnovation.mx/admin918uj8neb1cy1ndjuza/')

# Maximizar la ventana
driver.maximize_window()

# Iniciar sesión
username = driver.find_element(By.ID, 'email')
password = driver.find_element(By.ID, 'passwd')
username.send_keys('ramirezbelloci@gmail.com')
password.send_keys('e9P#&v@mf69=CU%O')
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
select.select_by_value("modules")
time.sleep(1)

driver.find_element(By.XPATH, "//span[@class='select2-selection select2-selection--single']").click()
time.sleep(1)
driver.find_element(By.XPATH, "//input[@class='select2-search__field']").send_keys("constr")
time.sleep(1)
select_marketplace = driver.find_element(By.XPATH, "//ul[@id='select2-form_module-results']/li")
driver.execute_script("arguments[0].scrollIntoView();", select_marketplace)
select_marketplace.click()
time.sleep(1)

select_element = driver.find_element(By.ID, "form_language")
select = Select(select_element)
select.select_by_value("mx")

time.sleep(1)
driver.find_element(By.XPATH, "//span[contains(text(),'Modificar')]/parent::button").click()

#esperar a que carge el contenido
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "translations_form")))
time.sleep(5)

panels = driver.find_elements(By.XPATH, "//form//span/parent::h3/parent::div[@class='panel']")
#imprimir el numero de paneles

contador=0
traducciones_deseadas = 1000000


for panel in panels:
    # Evalúa que el segundo span dentro de h3 sea mayor a 0
    badge_count = panel.find_element(By.XPATH, ".//h3/span[2]").text
    if int(badge_count) > 0 and contador < traducciones_deseadas:
        # Explora todos los tr del panel
        rows = panel.find_elements(By.XPATH, ".//table/tbody/tr")
        print("continuar...")
        input()
        for row in rows:
            try:
                # Obtiene el texto en inglés del primer td
                ingles_texto = row.find_element(By.XPATH, ".//td[1]").text
                # Traduce el texto al español
                traduccion = traducir_espaniol(ingles_texto)
                
                try:
                    # Intenta localizar un input dentro del tercer td
                    input_element = row.find_element(By.XPATH, ".//td[3]/input")
                except Exception as e:
                    # Si no se encuentra un input, intenta localizar un textarea
                    try:
                        input_element = row.find_element(By.XPATH, ".//td[3]/textarea")
                    except Exception as e:
                        # Si tampoco se encuentra un textarea, imprime el error y continúa
                        print(f"Error al localizar el elemento: {e}")
                        continue
                
                # Utiliza JavaScript para desplazarte hasta el elemento
                driver.execute_script("arguments[0].scrollIntoView();", input_element)
                # Verifica si el elemento ya tiene un valor diferente de ""
                if input_element.get_attribute("value") == "":
                    # Asigna el valor de la traducción al elemento
                    input_element.send_keys(traduccion)
                    contador += 1
            except Exception as e:
                # Imprime el error y continúa con la siguiente iteración
                print(f"Error al procesar la fila: {e}")
                print("Presiona Enter para continuar...")
                input()
                continue

print(f"Se tradujeron {contador} textos")
print("Presiona Enter para continuar...")
input()
