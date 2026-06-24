import os 
import unicodedata #libreria para normalizar texto
# --------------------------------------------------
#                   MENU PRINCIPAL
# --------------------------------------------------
def menu():
    print('''\n
        ------------------------------------------
                    GESTION DE PAISES                       
        ------------------------------------------
        
        1 - Agregar país
        2 - Actualizar datos del país
        3 - Buscar país
        4 - Filtrar país
        5 - Ordenar paises
        6 - Mostrar estadisticas
        7 - Ver todos los paises
        8 - Salir
        
        ------------------------------------------
        ''')  

def menu_buscar_paises():
    print('''\n
        ------------------------------------------
                    ORDENAR PAISES                       
        ------------------------------------------
        
        1 - Por Nombre
        2 - Por Poblacion
        3 - Por Superficie
        4 - Salir al menu
        
        ------------------------------------------
        ''')
    
def salvarlinea(lineadepais):#salva de errores al programa si se manipula el archivo csv en ejecución (agregando lineas vacias)
    if lineadepais == "\n":
        return False
    return True

def cargardatos(archivo):
    paises=[]
    dirpaises={}
    try:
        carpeta = os.path.dirname(archivo)
        if carpeta and not os.path.exists(carpeta): #crea la carpeta contenedora (ej. 'datos') si no existe
            os.makedirs(carpeta)
            print(f"[OK] Carpeta creada: {carpeta}")

        if not os.path.exists(archivo): #se usa libreria os, para ver si existe el archivo
            print("Error: No existe lista, se creará una nueva")
            with open(archivo, "w", encoding="utf-8") as f: #se crea un nuevo archivo si no existe
                f.write("nombre,poblacion,superficie,continente\n") #escribe el encabezado para evitar error en la proxima lectura
            return paises
        else:
            with open(archivo,"r",encoding="utf-8") as archivopaises: #se abre el archivo y se leen sus datos
                encabezado=next(archivopaises).strip().split(",")
                for fila in archivopaises:
                    salva_linea=salvarlinea(fila)
                    if not salva_linea:
                        continue
                    partes=fila.strip().split(",")
                    dirpaises = dict(zip(encabezado, partes))
                    paises.append(dirpaises)
    except PermissionError:
        print("Error: El archivo está siendo utilizado por otro programa.")
    except FileNotFoundError:
        print("Error: El archivo no fue encontrado")
    except Exception as e:
        print(f"Error de tipo {e}")
    else:
        print("Datos cargados correctamente!")
    return paises

# funcion para guardar los datos del país en la lista de diccionarios
def guardar_datos(paises):
    nombre = pedir_texto("Ingrese el nombre del país para agregar [Use 'salir' para volver al menu principal]: ").capitalize()
    if nombre == "Salir":
        return
    for p in paises:
        if p["nombre"].lower() == nombre.lower():
            print("El país ya existe en el sistema, no puede continuar.")
            return

    poblacion = pedir_entero("Ingrese la población del país: ") 
    superficie = pedir_entero("Ingrese la superficie del país: ")
    menucontinentes()   
    seleccion_continente=0
    #se agrega while para que cicle en la selección de continente
    while not seleccion_continente in [1,2,3,4,5]: 
        seleccion_continente=pedir_entero(("Seleccione continente: "))
        match seleccion_continente:
            case 1:
                continente="America"
            case 2:
                continente="Europa"
            case 3:
                continente="Oceania"
            case 4:
                continente="Africa"
            case 5:
                continente="Asia"
            case _:
                print("Error: Continente no seleccionado correctame")

    pais = {
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente
    }

    paises.append(pais)
    return pais

# funcion para agregar datos al archivo csv
def añadir_datos_archivo(pais, archivo):
    try:
        with open(archivo, "a", encoding="utf-8") as f:
            linea = f"{pais['nombre']},{pais['poblacion']},{pais['superficie']},{pais['continente']}\n"
            f.write(linea)
        print("País agregado y guardado correctamente!")

    except PermissionError:
        print("Error: El archivo está siendo utilizado por otro programa. No se pudieron guardar los datos.")
    except FileNotFoundError:
        print("Error: El archivo no existe. No se pudieron guardar los datos.")
    except Exception as e:
        print(f"Error inesperado: {e}")

def guardar_archivo(paises, archivo):
    try:
        with open(archivo, "w", encoding="utf-8") as f:
                encabezado="nombre,poblacion,superficie,continente\n"
                f.write(encabezado)
                for fila in paises:
                    salva_linea=salvarlinea(fila)
                    if not salva_linea:
                        continue
                    linea = f"{fila['nombre']},{fila['poblacion']},{fila['superficie']},{fila['continente']}\n"
                    f.write(linea)

        print("Archivo guardado correctamente!")

    except PermissionError:
        print("Error: El archivo está siendo utilizado por otro programa. No se pudieron guardar los datos.")
    except FileNotFoundError:
        print("Error: El archivo no existe. No se pudieron guardar los datos.")
    except Exception as e:
        print(f"Error inesperado: {e}")

# --------------------------------------------------
#              ACTUALIZAR DATOS DE PAIS
# --------------------------------------------------
def actualizardatospais(paises):
    print("""
        ------------------------------------------
                    ACTUALIZAR PAIS                      
        ------------------------------------------
        """)
    while True:
        nombrepais = pedir_texto("Ingrese nombre de pais a actualizar [Use 'salir' para volver al menu principal]:  ").lower()
        if nombrepais == "salir":
            break
        for pais in paises:
            if normalizar(pais["nombre"]) == normalizar(nombrepais): #se usa normalizar para evitar problemas de tildes
                try:
                    print(f"Datos actuales de -- {pais['nombre']} --\n")
                    print(f"Población: {pais['poblacion']} | Superficie: {pais['superficie']}")
                    nuevapoblacion = input("Ingrese la nueva población [Enter para mantener la actual]\n").strip()
                    nuevasuperficie = input("Ingrese la nueva superficie [Enter para mantener la actual]\n").strip()
                    if nuevapoblacion:
                        pais["poblacion"] = validar_numero_correcto(nuevapoblacion) #si ingresa poblacion nueva, la valida
                    if nuevasuperficie:
                        pais["superficie"] = validar_numero_correcto(nuevasuperficie) #si ingresa superficie nueva, la valida
                    if not nuevapoblacion and not nuevasuperficie: #no ingreso nada
                        print("No se actualizó ningún registro")
                        break
                    else:
                        print(f"Los datos de {pais['nombre']} fueron actualizados correctamente")
                        break
                except ValueError:
                    print("Error: Valor ingresado es incorrecto [Ingrese valor entero positivo o ENTER si no requiere actualización]")
                    return
        else:
            print(f"Error: Pais '{nombrepais}' no encontrado [puede cargar un país en la opción 1]")
        return

#VALIDA NUMERO CORRECTO Y NO TIENE EN CUENTA SI EL USUARIO DEJA EL ESPACIO VACIO (NO ACTUALIZA EL REGISTRO)
def validar_numero_correcto(vnc_nuevavalidacion):
    numero_a_verificar = int(vnc_nuevavalidacion)
    try:
        if numero_a_verificar <= 0:
            raise ValueError
        return numero_a_verificar
    except ValueError:
        raise ValueError("Error: El valor ingresado debe ser un valor entero positivo")

# funcion para pedir un numero entero
def pedir_entero(mensaje):
    while True:
        entrada = input(mensaje).strip()
        try:
            numero = int(entrada)
            if numero >= 0:
                return numero
            else:
                print("Error: El numero no puede ser negativo")
        except ValueError:
            print("Error: Debe ingresar un número entero válido.")

# funcion para pedir texto
def pedir_texto(mensaje):
    while True:
        entrada = input(mensaje).strip()
        if entrada == "":
            print("Error: El campo no puede quedar vacío.")
        elif entrada.isdigit() or entrada < "0":
            print("Error: Debe ingresar texto, no un número.")
        elif not entrada.replace(" ", "").isalpha():
            print("Error: Debe ingresar texto válido (sin números ni caracteres especiales).")
        else:
            return entrada

# --------------------------------------------------
#              BUSCAR PAIS
# --------------------------------------------------

def buscar_pais_por_nombre(paises):
    pais_usuario = normalizar(pedir_texto("Ingrese el pais a buscar: "))
    coincidencias = []
    try:
        for p in paises:
            if pais_usuario in normalizar(str(p["nombre"]).lower()):
                coincidencias.append(p)
        outputmostrardatos(coincidencias, "País no encontrado")
    except KeyError as e:
        print(f"Error al buscar el país: {e}")
    except Exception as e:
        print(f"Error inesperado al buscar el país: {e}")

# --------------------------------------------------
#              ORDENAR PAISES
# --------------------------------------------------
def seleccion_ordenar_paises(paises):
    opcion_orden = 0
    while opcion_orden != 4:
        menu_buscar_paises()
        opcion_orden = pedir_entero("\nOpción (1-4): ")
        if opcion_orden != 4:
            if opcion_orden in [1, 2, 3]:
                print(f"¿Ordenar de forma ascendente o descendente?")
                while True:
                    opcion_forma = pedir_entero("1 - Asc | 2 - Des: ")
                    if opcion_forma in [1, 2]:
                        break
                    print("Opción no válida. Por favor, seleccione 1 para ascendente o 2")
            match opcion_orden:
                case 1: ordenar_paises(paises, "nombre", opcion_forma)
                case 2: ordenar_paises(paises, "poblacion", opcion_forma)
                case 3: ordenar_paises(paises, "superficie", opcion_forma)
                case _: print("No se encuentra entre las opciones")
    print("Saliendo al menú principal...")
    
def ordenar_paises(paises, criterio, orden):
    lista_copia = paises.copy()
    cantidad_paises = len(paises)
    try:
        for indice_pasada in range(cantidad_paises - 1):
            for indice_actual in range(cantidad_paises - 1 - indice_pasada):
                lista_copia = mover_elementos(lista_copia, orden, criterio, indice_actual)
        outputmostrardatos(lista_copia)
    except KeyError:
        print(f"Error: Falta la clave en los datos de los países.")
    except ValueError:
        print(f"Error: No se pudo procesar numéricamente el criterio '{criterio}'.")
    except Exception as e:
        print(f"Error inesperado al ordenar los países: {e}")

def mover_elementos(lista_copia, orden, criterio, indice_actual):
    if criterio == "nombre":
        ele_actual = lista_copia[indice_actual][criterio].lower()
        ele_siguiente = lista_copia[indice_actual + 1][criterio].lower()
    else: 
        ele_actual = int(lista_copia[indice_actual][criterio])
        ele_siguiente = int(lista_copia[indice_actual + 1][criterio])

    debe_mover = False

    match orden:
        case 1:  
            if ele_actual > ele_siguiente:
                debe_mover = True
        case 2:  
            if ele_actual < ele_siguiente:
                debe_mover = True

    if debe_mover:
        lista_copia[indice_actual], lista_copia[indice_actual + 1] = (
            lista_copia[indice_actual + 1], 
            lista_copia[indice_actual]
        )
    return lista_copia

# --------------------------------------------------
#              MOSTRAR ESTADISTICAS
# --------------------------------------------------
def mostrarestadisticas(paises):
    print(f"""
        ------------------------------------------
                MOSTRAR ESTADISTICAS                            
        ------------------------------------------
        """)
    print(f"\nTotal de paises: {len(paises)}\n")
    mayor_poblacion = max(paises, key=lambda p: int(p["poblacion"]))
    menor_poblacion = min(paises, key=lambda p: int(p["poblacion"]))
    print("-"*40)
    print("Población")
    print("-"*40)
    print(f"Mayor: {mayor_poblacion['nombre']} ({int(mayor_poblacion['poblacion']):,} hab.)")
    print(f"Menor: {menor_poblacion['nombre']} ({int(menor_poblacion['poblacion']):,} hab.)")
    total=0
    for pais in paises:
        total+=int(pais["poblacion"])
    promediopoblacion = total / len(paises)
    print(f"Promedio de población: {promediopoblacion:,.2f}hab.")
    total=0
    for pais in paises:
        total+=int(pais["superficie"])

    promediosuperficie = total / len(paises)
    print("-"*40)
    print("Superficie")
    print("-"*40)    
    print(f"Promedio de superficie: {promediosuperficie:,.2f}km.")
    america=0
    africa=0
    europa=0
    asia=0
    oceania=0
    for pais in paises:
        continente = normalizar(pais["continente"]).lower()
        if continente == "america":
            america+=1
        elif continente == "africa":
             africa+=1
        elif continente == "europa":
             europa+=1
        elif continente == "asia":
             asia+=1
        else: oceania+=1
    print("-"*40)
    print("Paises por continentes")
    print("-"*40)   
    print(f"{'America:':<8}: {america} paises.")
    print(f"{'Africa:':<8}: {africa} paises.")
    print(f"{'Europa:':<8}: {europa} paises.")
    print(f"{'Asia:':<8}: {asia} paises.")
    print(f"{'Oceania:':<8}: {oceania} paises.")

# --------------------------------------------------
#              MODELO DE MOSTRAR DATOS
# --------------------------------------------------
def outputmostrardatos(paises, mensaje_vacio="[La lista esta vacía."):
    if not paises:
        print(mensaje_vacio)
        return
    print(f"\n{'Nombre':<20} {'Población':>15} {'Superficie':>15}  {'Continente':<12}")
    print("-" * 65)
    for p in paises:
        print(f"{p['nombre']:<20} {int(p['poblacion']):>15,} {int(p['superficie']):>15,}  {p['continente']:<12}")

# --------------------------------------------------
#              NORMALIZADOR DE TILDES
# --------------------------------------------------
def normalizar(texto):
    return unicodedata.normalize("NFD", texto).encode("ascii", "ignore").decode("utf-8").lower()

# --------------------------------------------------
#               FILTRADO DE PAISES 
# --------------------------------------------------
def menu_filtrar(paises):
    while True:
        print("""
        ------------------------------------------
                    FILTRAR PAISES                      
        ------------------------------------------
        
        1 - Por continente
        2 - Por rango de población
        3 - Por rango de superficie
        4 - Volver al menú principal
        
        """)
        opcion = pedir_entero("Seleccione una opción: ")
        if opcion == 1:
            filtrar_por_continente(paises)
        elif opcion == 2:
            filtrar_por_rango_poblacion(paises)
        elif opcion == 3:
            filtrar_por_rango_superficie(paises)
        elif opcion == 4:
            break
        else:
            print("Error: Opción inválida.")

def filtrar_por_rango_superficie(paises):
    print("""
        ------------------------------------------
                  FILTRAR POR SUPERFICIE                      
        ------------------------------------------
        """)
    try:
        minimo = input("Superficie mínima (Enter para sin límite): ")
        maximo = input("Superficie máxima (Enter para sin límite): ")
        min_val = int(minimo)if minimo else 0 #para usar el enter
        max_val = int(maximo) if maximo else float("inf") #el uso del enter
        if min_val < 0 or max_val < 0:
            raise ValueError("Los valores no pueden ser negativos.")
        if min_val > max_val:
            print("La superficie minima no puede ser mayor que la superficie máxima")
            return
        resultados = []
        for p in paises:
            if min_val <= int(p["superficie"]) <= max_val:
                resultados.append(p)
        if not resultados:
            print("No hay países en ese rango de superficie.")
            return
        print(f"\nPaises con superficie desde {min_val}km hasta {max_val}km = {len(resultados)} paises encontrados")
        outputmostrardatos(resultados)
    except ValueError:
        print(f"Error: Debe ingresar numeros enteros positivos")

def filtrar_por_rango_poblacion(paises):
    print("""
        ------------------------------------------
                  FILTRAR POR POBLACION                      
        ------------------------------------------
        """)
    try:
        minimo = input("Población mínima (Enter para sin límite): ")
        maximo = input("Población máxima (Enter para sin límite): ")
        #validacion del enter para minimo
        if minimo:
            min_val= int(minimo)
        else: min_val=0
        #validacion del enter para maximo
        if maximo:
            max_val = int(maximo)
        else: max_val = float("inf") 
        if min_val < 0 or max_val < 0:
            raise ValueError("Los valores no pueden ser negativos.")
        if min_val > max_val:
            print("La población minima no puede ser mayor que la población máxima")
            return
        resultados = []
        for p in paises:
            if min_val <= int(p["poblacion"]) <= max_val:
                resultados.append(p)
        if not resultados:
            print("No hay países en ese rango de población.")
            return
        outputmostrardatos(resultados)
    except ValueError:
        print(f"Error: Debe ingresar numeros enteros positivos")

def filtrar_por_continente(paises):
    print("""
        ------------------------------------------
                  FILTRAR POR CONTINENTES                      
        ------------------------------------------
        """)
    menucontinentes()
    seleccioncontinente=pedir_entero("Seleccione un continente [1-5]: ")
    match seleccioncontinente:
        case 1: filtrar_y_mostrar_continentes(paises, "America")
        case 2: filtrar_y_mostrar_continentes(paises, "Europa")  
        case 3: filtrar_y_mostrar_continentes(paises, "Oceania")
        case 4: filtrar_y_mostrar_continentes(paises, "Africa")
        case 5: filtrar_y_mostrar_continentes(paises, "Asia") 
        case _: print("Selección invalida [reintente con números del 1 al 5]")   

def filtrar_y_mostrar_continentes(paises, continente):
    resultados=[]
    for p in paises:
        if normalizar(p["continente"]) == normalizar(continente):
            resultados.append(p)
    if not resultados:
        print(f"No hay paises en agregados en {continente}")
        return
    outputmostrardatos(resultados)

def menucontinentes():
    print("""Seleccione continente
          1 - America
          2 - Europa
          3 - Oceania
          4 - Africa
          5 - Asia
          """)
    
# --------------------------------------------------
#           SELECCIONAR OPCION DEL MENU 
# --------------------------------------------------
def seleccionmenu():
    opcion = 0
    while opcion != 8:
        menu()
        opcion = pedir_entero("\nSeleccione una opción (1-8): ")
        try:
            match opcion:
                case 1:
                    diccionarioCreado = guardar_datos(paises)
                    if diccionarioCreado:
                        añadir_datos_archivo(diccionarioCreado, archivopaises)
                case 2:
                    actualizardatospais(paises)
                case 3:
                    buscar_pais_por_nombre(paises)
                case 4:
                    menu_filtrar(paises)
                case 5:
                    seleccion_ordenar_paises(paises)
                case 6:
                    mostrarestadisticas(paises)
                case 7:
                    outputmostrardatos(paises)    
                case 8:
                    guardar_archivo(paises, archivopaises)
                    print("Saliendo del sistema...")
                case _:
                    print("Opción no válida. Por favor, seleccione una opción del 1 al 8. \n")
        except ValueError:
            print("Error: Valor ingresado es incorrecto")
        

# --------------------------------------------------
#                  MAIN DEL SISTEMA
# --------------------------------------------------
print("\nCargando datos...")
ruta_actual = os.path.dirname(__path__ if '__path__' in locals() else __file__) #solucion a la ruta del archivo
archivopaises = os.path.join(ruta_actual, "datos/paises.csv")
paises = cargardatos(archivopaises)
seleccionmenu()
