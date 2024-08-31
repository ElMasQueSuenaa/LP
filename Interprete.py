import re

# EBNF para las diferentes expresiones
corchete = r"\}"
igual = r"=="
mayor = r">"
menor = r"<"
define = r"\s*DEFINE\s+\$_[A-Z][A-Za-z]*\s*$"
asignacion = r"\s*DP\s+\$_[A-Z][A-Za-z]*\s+ASIG\s+(True|False|\d+|#[^#]*#|\$_[A-Z][A-Za-z]*)\s*$"
suma = r"\s*DP\s+\$_[A-Z][A-Za-z]*\s+\+\s+(\$_[A-Z][A-Za-z]*|\d+|#[^#]*#)\s+(\$_[A-Z][A-Za-z]*|\d+|#[^#]*#)$"
multiplicacion = r"\s*^DP\s+\$_[A-Z][A-Za-z]*\s+\*\s+(\$_[A-Z][A-Za-z]*|\d+)\s+(\$_[A-Z][A-Za-z]*|\d+)$"
leer_if = r"\s*^if\s+\(\s*\$_[A-Z][A-Za-z]*\s*\)\s+\{\s*$"
leer_else = r"\s*^\s*\}\s*else\s*\{\s*$"
mostrar = r"\s*^MOSTRAR\s*\(\s*\$_[A-Z][A-Za-z]*\s*\)\s*$"
cond = r"\s*^DP\s+\$_[A-Z][A-Za-z]*\s+(>|<|==)\s+\$_[A-Z][A-Za-z]*\s+\$_[A-Z][A-Za-z]*\s*$"


archivo_output = open("output.txt", "w")

variables = {}

def definir_variable(linea, numero_linea):
    """
    Parámetros:
    - linea: str. La línea de código en PySimplex.
    - numero_linea: int. El número de línea en el archivo de código.

    Retorna:
    - 0 si la operación se realizó con éxito.
    - 1 si ocurrió un error.

    Descripción:
    Esta función procesa la instrucción DEFINE en PySimplex. 
    Busca el nombre de la variable entre paréntesis, verifica si la variable ya está definida, 
    y luego agrega la variable al diccionario de variables con un valor inicial de None.
    """
    linea = linea.strip()
    matches = re.findall(r"\$_[A-Z][A-Za-z]*", linea)
    if matches:
        nombre_var = matches[0]
        if nombre_var in variables:
            print("Error: Variable ya definida", nombre_var, "Linea:", numero_linea)
            return 1
        variables[nombre_var] = None
        return 0
    else:
        print("Error: No se encontró un nombre de variable válido en la línea.", numero_linea)
        return 1

def asignar_variable(linea, numero_linea):
    """
    Parámetros:
    - linea: str. La línea de código en PySimplex.
    - numero_linea: int. El número de línea en el archivo de código.

    Retorna:
    - 0 si la operación se realizó con éxito.
    - 1 si ocurrió un error.

    Descripción:
    Esta función procesa la instrucción ASIG en PySimplex. 
    Busca el nombre de la variable, verifica si la variable ya está definida,
    y luego asigna un valor a la variable en el diccionario de variables.
    """
    linea = linea.strip()
    temp = linea.split()
    var_nombre = temp[1]
    if var_nombre not in variables:
        print("Error en la linea", numero_linea, ": Variable no definida")
        return 1
    valor = " ".join(temp[3:])
    if valor.isdigit():
        variables[var_nombre] = int(valor)
        return 0
    elif valor in ["True", "False"]:
        variables[var_nombre] = valor
        return 0
    elif valor.startswith("#") and valor.endswith("#"):
        valor = re.search(r"#(.*?)#", linea)
        variables[var_nombre] = valor.group(1)
        return 0
    elif valor in variables:
        variables[var_nombre] = variables[valor]
        return 0
    else:
        print("Error en la linea", numero_linea, ": Valor inválido")
        return 1

def multiplicacion_variables(linea, numero_linea):
    """
    Parámetros:
    - linea: str. La línea de código en PySimplex.
    - numero_linea: int. El número de línea en el archivo de código.

    Retorna:
    - 0 si la operación se realizó con éxito.
    - 1 si ocurrió un error.

    Descripción:
    Esta función procesa la operación * en PySimplex. 
    Busca el nombre de la variable donde se quiere guardar el resultado,
    verifica si las variables a multiplicar están definidas y tienen un valor asignado,
    y luego realiza la multiplicación y guarda el resultado en la variable.
    """
    temp = linea.split()
    var_nombre = temp[1]
    operando1 = temp[3]
    operando2 = temp[4]
    if var_nombre not in variables:
        print("Error en la línea", numero_linea, ": Variable no definida")
        return 1

    operando1_val = variables.get(operando1, None) if operando1 in variables else int(operando1)
    operando2_val = variables.get(operando2, None) if operando2 in variables else int(operando2)

    if operando1_val is None or operando2_val is None:
        print("Error en la línea", numero_linea, ": Uno de los operandos no está definido")
        return 1

    variables[var_nombre] = operando1_val * operando2_val
    return 0

def suma_variables(linea, numero_linea):
    """
    Parámetros:
    - linea: str. La línea de código en PySimplex.
    - numero_linea: int. El número de línea en el archivo de código.

    Retorna:
    - 0 si la operación se realizó con éxito.
    - 1 si ocurrió un error.

    Descripción:
    Esta función procesa la operación + en PySimplex. 
    Busca el nombre de la variable donde se quiere guardar el resultado,
    verifica si las variables a sumar están definidas y tienen un valor asignado,
    y luego realiza la suma o concatenación, dependiendo del tipo de dato que sean los operandos
    y guarda el resultado en la variable.
    """
    temp = linea.split()
    var_nombre = temp[1]
    operando1 = temp[3]
    operando2 = temp[4]
    if var_nombre not in variables:
        print("Error en la línea", numero_linea, ": Variable no definida")
        return 1
    if operando1 not in variables:
        print("Error en la línea", numero_linea, ": Operando 1 no definido")
        return 1
    else:
        operando1_val = variables[operando1]
    if operando2 not in variables:
        print("Error en la línea", numero_linea, ": Operando 2 no definido")
        return 1
    else:
        operando2_val = variables[operando2]
    if operando1_val is None or operando2_val is None:
        print("Error en la línea", numero_linea, ": Uno de los operandos no está definido")
        return 1
    if isinstance(operando1_val, int) and isinstance(operando2_val, int):
        variables[var_nombre] = operando1_val + operando2_val
    else:
        variables[var_nombre] = str(operando1_val) + " " + str(operando2_val)
    return 0

def ejecutar_mostrar(linea, numero_linea):
    """
    Parámetros:
    - linea: str. La línea de código en PySimplex.
    - numero_linea: int. El número de línea en el archivo de código.

    Retorna:
    - 0 si la operación se realizó con éxito.
    - 1 si ocurrió un error.

    Descripción:
    Esta función procesa la instrucción MOSTRAR en PySimplex. 
    Busca el nombre de la variable entre paréntesis, verifica si la variable existe 
    y tiene un valor asignado, y luego escribe ese valor en el archivo de salida "output.txt".
    """
    resultado = re.search(r"\((.*?)\)", linea)
    if resultado:
        variable_nombre = resultado.group(1)
    else:
        print(f"Error en la línea {numero_linea}: Sintaxis incorrecta en la instrucción MOSTRAR")
        return 1
    if variable_nombre not in variables:
        print(f"Error en la línea {numero_linea}: Variable '{variable_nombre}' no definida")
        return 1
    valor = variables[variable_nombre]
    if valor is None:
        print(f"Error en la línea {numero_linea}: Variable '{variable_nombre}' no tiene un valor asignado")
        return 1
    archivo_output.write(str(valor) + "\n")
    return 0

def reconocer_condicion(linea, numero_linea):
    """
    Parámetros:
    - linea: str. La línea de código en PySimplex.
    - numero_linea: int. El número de línea en el archivo de código.

    Retorna:
    - 0 si la operación se realizó con éxito.
    - 1 si ocurrió un error.

    Descripción:
    Esta función procesa la instrucción DP con los caracteres ">" o "==" en PySimplex. 
    Busca el nombre de la variable y verifica si está definida, luego busca los operandos
    y verifica si están definidos, y finalmente compara los operandos y guarda el resultado
    en la variable de la condición.
    """
    temp = linea.split()
    nombre_condicion = temp[1]
    operacion = temp[2]
    operando1 = temp[3]
    operando2 = temp[4]
    variables[nombre_condicion] = None
    if operando1 not in variables:
        print("Error en la línea", numero_linea, ": Operando 1 no definido")
        return 1
    if operando2 not in variables:
        print("Error en la línea", numero_linea, ": Operando 2 no definido")
        return 1
    if re.match(igual, operacion):
        if variables[operando1] == variables[operando2]:
            variables[nombre_condicion] = "True"
        else:
            variables[nombre_condicion] = "False"
        return 0
    elif re.match(mayor, operacion):
        if variables[operando1] > variables[operando2]:
            variables[nombre_condicion] = "True"
        else:
            variables[nombre_condicion] = "False"
        return 0
    elif re.match(menor, operacion):
        if variables[operando1] < variables[operando2]:
            variables[nombre_condicion] = "True"
        else:
            variables[nombre_condicion] = "False"
        return 0
    else:
        return 1
    
def procesar_if(linea, numero_linea, lista):
    """
    Procesa la instrucción 'if' en PySimplex.
    
    Parámetros:
    - linea: str. La línea de código que contiene la instrucción 'if'.
    - numero_linea: int. El número de línea actual en el archivo de código.
    - lista: list. Lista con todas las líneas de código del archivo.
    
    Retorna:
    - Un nuevo valor para `numero_linea` para continuar con la ejecución del código.
    - Retorna -1 si hay un error.
    """
    temp = linea.split()
    nombre = temp[1]  
    resultado = re.search(r"\((.*?)\)", nombre)
    nombre_var = resultado.group(1)
    if nombre_var not in variables:
        print(f"Error en la línea {numero_linea + 1}: Variable '{nombre_var}' no definida")
        return -1
    valor = variables[nombre_var]
    if valor is None:
        print(f"Error en la línea {numero_linea + 1}: Variable '{nombre_var}' no tiene un valor asignado")
        return -1
    if valor == "True":
        temp = numero_linea
        while temp < len(lista):
            if  re.match(leer_else, lista[temp]):
                return temp
            temp += 1
        return numero_linea
    else:
        numero_linea += 1
        while numero_linea < len(lista):
            if re.match(leer_else, lista[numero_linea]):
                return numero_linea
            numero_linea += 1
        return numero_linea

#def procesar_else(linea, numero_linea, lista):
    """
    Procesa la instrucción 'else' en PySimplex.
    
    Parámetros:
    - linea: str. La línea de código que contiene la instrucción 'else'.
    - numero_linea: int. El número de línea actual en el archivo de código.
    - lista: list. Lista con todas las líneas de código del archivo.
    
    Retorna:
    - El nuevo valor de `numero_linea` para continuar con la ejecución del código.
    - Retorna -1 si hay un error.
    """
    temp = numero_linea
    
    
    print(f"Error: Bloque else no tiene un final válido en la línea {numero_linea}")
    return -1

nombre_archivo = "codigo.txt"
with open(nombre_archivo) as file_object:
    archivo = file_object.readlines()

i = 0
hayerror = 0
while i < len(archivo):
    codigo = archivo[i].strip()
    #print(codigo)
    if re.match(define, codigo):
        hayerror = definir_variable(codigo, i)
    elif re.match(asignacion, codigo):
        hayerror = asignar_variable(codigo, i)
    elif re.match(multiplicacion, codigo):
        hayerror = multiplicacion_variables(codigo, i)
    elif re.match(suma, codigo):
        hayerror = suma_variables(codigo, i)
    elif re.match(mostrar, codigo):
        hayerror = ejecutar_mostrar(codigo, i)
    elif re.match(cond, codigo):
        hayerror = reconocer_condicion(codigo, i)
    elif re.match(leer_if, codigo):
        temp = i
        i = procesar_if(codigo, i, archivo)
        if i == -1:
            print("Hay un error de sintaxis en la linea", temp)
            hayerror = 1
    else:
        print("Hay un error de sintaxis en la linea", i)
        hayerror = 1    
    if hayerror == 1:
        archivo_output.close()
        file_object.close()
        break
    i += 1

