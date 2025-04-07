import os
import json
import re

def buscar_en_json(texto_buscado_1, texto_buscado_2, texto_buscado_3, texto_buscado_4):
    archivos_json = [archivo for archivo in os.listdir() if archivo.endswith('.json')]
    textos_encontrados = []

    if texto_buscado_1.strip():
        texto_a_buscar = texto_buscado_1
    elif texto_buscado_2.strip():
        texto_a_buscar = texto_buscado_2
    elif texto_buscado_3.strip():
        texto_a_buscar = texto_buscado_3
    elif texto_buscado_4.strip():
        texto_a_buscar = texto_buscado_4
    else:
        print("No se proporcionó ningún texto válido para la búsqueda.")
        return

    for archivo in archivos_json:
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Convertir a string para la búsqueda
            data_str = json.dumps(data, ensure_ascii=False)

            if texto_a_buscar.lower() in data_str.lower():
                pattern = r'\{.*?\}'
                llaves_encontradas = re.findall(pattern, data_str, re.DOTALL)
                

                for bloque in llaves_encontradas:
                    if (texto_a_buscar.lower() in bloque.lower() and
                        (not texto_buscado_2.strip() or texto_buscado_2.lower() in bloque.lower()) and
                        (not texto_buscado_3.strip() or texto_buscado_3.lower() in bloque.lower()) and
                        (not texto_buscado_4.strip() or texto_buscado_4.lower() in bloque.lower())):

                        textos_encontrados.append(json.loads(bloque))  # Guardar la estructura JSON

                        # Eliminar el bloque del JSON original
                        if isinstance(data, list):  # Si el JSON es una lista
                            data = [item for item in data if json.dumps(item, ensure_ascii=False) != bloque]
                        elif isinstance(data, dict):  # Si el JSON es un diccionario
                            data = {k: v for k, v in data.items() if json.dumps(v, ensure_ascii=False) != bloque}
                        break  # No seguir buscando en este archivo

            # Si data es una lista, la convertimos en un diccionario con "datos"
            if isinstance(data, list):
                data = {"datos": data, "TODO BUSCADO": True}
            elif isinstance(data, dict):
                data["TODO BUSCADO"] = True

            # Guardar resultados en aresultado.json
            if textos_encontrados:
                with open('aresultado.json', 'w', encoding='utf-8') as f_resultado:
                    json.dump(textos_encontrados, f_resultado, ensure_ascii=False, indent=4)

                # Sobreescribir el archivo JSON sin los bloques eliminados
                with open(archivo, 'w', encoding='utf-8') as f_actualizado:
                    data["FINALIZADO"] = True
                    json.dump(data, f_actualizado, ensure_ascii=False, indent=4)


        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"Error al leer el archivo {archivo}: {e}")

    if textos_encontrados:
        print("Textos encontrados y guardados en 'aresultado.json':")
        for texto in textos_encontrados:
            print(texto)
    else:
        print("No se encontraron coincidencias.")

def obtener_contenido_archivo(archivo):
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"El archivo {archivo} no se encontró.")
        return ""

texto_buscado_1 = obtener_contenido_archivo('aapellido.txt')
texto_buscado_2 = obtener_contenido_archivo('anombre.txt')
texto_buscado_3 = obtener_contenido_archivo('aci.txt')
texto_buscado_4 = obtener_contenido_archivo('afecha.txt')
buscar_en_json(texto_buscado_1, texto_buscado_2, texto_buscado_3, texto_buscado_4)
