import re

# EBNF para las diferentes expresiones
define = r"^DEFINE\s+\$_[A-Z][A-Za-z]*\s*$"
asignacion = r"^DP\s+\$_[A-Z][A-Za-z]*\s+ASIG\s+(True|False|\d+|#[^#]*#|\$_[A-Z][A-Za-z]*)\s*$"
suma = r"^DP\s+\$_[A-Z][A-Za-z]*\s+\+\s+(\$_[A-Z][A-Za-z]*|\d+|#[^#]*#)\s+(\$_[A-Z][A-Za-z]*|\d+|#[^#]*#)$"
multiplicacion = r"^DP\s+\$_[A-Z][A-Za-z]*\s+\*\s+(\$_[A-Z][A-Za-z]*|\d+)\s*$"
leer_if = r"^if\s*\(\s*\$_[A-Z][A-Za-z]*\s*\)\s*\{\s*$"
leer_else = r"^\}\s*else\s*\{\s*$"
mostrar = r"^MOSTRAR\s*\(\s*\$_[A-Z][A-Za-z]*\s*\)\s*$"

archivo_output = open("output.txt", "w")

variables = {}

def definir_variable(linea, numero_linea):
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
    # Extraer el nombre de la variable dentro de los paréntesis
    resultado = re.search(r"\((.*?)\)", linea)
    if resultado:
        variable_nombre = resultado.group(1)
    else:
        print(f"Error en la línea {numero_linea}: Sintaxis incorrecta en la instrucción MOSTRAR")
        return 1
    
    # Verificar si la variable existe
    if variable_nombre not in variables:
        print(f"Error en la línea {numero_linea}: Variable '{variable_nombre}' no definida")
        return 1
    
    # Obtener el valor de la variable
    valor = variables[variable_nombre]
    
    # Verificar si la variable tiene un valor asignado
    if valor is None:
        print(f"Error en la línea {numero_linea}: Variable '{variable_nombre}' no tiene un valor asignado")
        return 1
    
    # Escribir el valor en el archivo de salida
    archivo_output.write(str(valor) + "\n")
    return 0


nombre_archivo = "codigo.txt"
with open(nombre_archivo) as file_object:
    lista = file_object.readlines()

i = 1
hayerror = 0
for codigo in lista:
    codigo = codigo.strip()
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
    else:
        print("Hay un error de sintaxis en la linea", i)
        hayerror = 1    
    if hayerror == 1:
        archivo_output.close()
        file_object.close()
        break
    i += 1

