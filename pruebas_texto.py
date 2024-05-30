import re
from deep_translator import GoogleTranslator

def traducir(texto):
    idioma_destino = "es"
    return GoogleTranslator(source='auto', target=idioma_destino).translate(texto)

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

#Ejecutar test

texto_original = """
Hi <strong>{seller_name}</strong>,
<strong>{reporter}</strong> just reported your shop <strong>{shop_name}</strong> created by <strong>{shop_seller}</strong> as abused.
<p><strong>{reporter}</strong> just reported product <strong><a href="{link_report}">{product_name}</a></strong> as abused.</p>
<a href="{link_report}" class="button_link" style="text-align: center; border-radius: 5px; color: #fff; display: inline-block; font-size: 17px; font-weight: normal; padding: 8px 30px; text-decoration: none; margin-top: 10px;" target="_blank" rel="noopener" data-mce-href="{link_report}" data-mce-style="text-align: center; border-radius: 5px; color: #fff; display: inline-block; font-size: 17px; font-weight: normal; padding: 8px 30px; text-decoration: none; margin-top: 10px;">{shop_name}</a>
"""

texto_final = traducir_correo(texto_original)
print(texto_final)

versiontxt = version_txt(texto_final)
print(versiontxt)

renglones = texto_final.split("\n")
print(renglones)

