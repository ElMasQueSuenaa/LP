import re

# EBNF para las diferentes expresiones
define = r"^\s*DEFINE\s*\$_[A-Z][A-Za-z]*\s*$"
asignacion = r"^\s*DP\s+(\$_[A-Z][A-Za-z]*)\s+ASIG\s+(True|False|\d+|#[^#]*#|\$_[A-Z][A-Za-z]*)\s*$"
suma = r"^\s*DP\s+\$_[A-Z][A-Za-z]*\s+\+\s+(\$_[A-Z][A-Za-z]*|\d+|#[^#]*#)\s+(\$_[A-Z][A-Za-z]*|\d+|#[^#]*#)\s*$"
multiplicacion = r"^\s*DP\s+\$_[A-Z][A-Za-z]*\s+\*\s+(\$_[A-Z][A-Za-z]*|\d+)\s+(\$_[A-Z][A-Za-z]*|\d+)\s*$"
leer_if = r"^\s*if\s*\(\s*\$_[A-Z][A-Za-z]*\s*\)\s*\{\s*$"
leer_else = r"^\s*\}\s*else\s*\{\s*$"
mostrar = r"^\s*MOSTRAR\(\s*\$_[A-Z][A-Za-z]*\s*\)\s*$"
concatenacion_texto = r"^\s*DP\s+\$_[A-Z][A-Za-z]*\s+\+\s+(\$_[A-Z][A-Za-z]*|#[^#]*#)\s+(\$_[A-Z][A-Za-z]*|#[^#]*#)\s*$"

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
    temp = linea.split()
    var_nombre = temp[1]
    valor = temp[3]
    if var_nombre not in variables:
        print("Error en la linea", numero_linea, "Variable no definida")
        return 1
    if valor.startswith("#") and valor.endswith("#"):
        variables[var_nombre] = re.search(r"#(.*?)#", valor).group(1)
    elif valor.isdigit():
        variables[var_nombre] = int(valor)
    elif valor in ["True", "False"]:
        variables[var_nombre] = valor == "True"
    elif valor in variables:
        variables[var_nombre] = variables[valor]
    else:
        print("Error: Valor inválido en la línea", numero_linea)
        return 1
    return 0

def multiplicacion_variables(linea, numero_linea):
    temp = linea.split()
    var_nombre = temp[1]
    operando1 = temp[3]
    operando2 = temp[4]
    if var_nombre not in variables:
        print("Error en la línea", numero_linea, ": Variable no definida")
        return 1
    if operando1.isdigit():
        operando1_val = int(operando1)
    elif operando1 in variables:
        operando1_val = variables[operando1]
    else:
        print("Error en la línea", numero_linea, ": Operando 1 no es válido")
        return 1
    if operando2.isdigit():
        operando2_val = int(operando2)
    elif operando2 in variables:
        operando2_val = variables[operando2]
    else:
        print("Error en la línea", numero_linea, ": Operando 2 no es válido")
        return 1
    variables[var_nombre] = operando1_val * operando2_val
    return 0

def main(nombre_archivo):
    with open(nombre_archivo) as file_object:
        lista = file_object.readlines()

    i = 1
    hayerror = 0
    for linea in lista:
        if re.match(define, linea):
            hayerror = definir_variable(linea, i)
        elif re.match(asignacion, linea):
            hayerror = asignar_variable(linea, i)
        elif re.match(multiplicacion, linea):
            hayerror = multiplicacion_variables(linea, i)
        else:
            print("Hay un error de sintaxis en la linea", i )
            hayerror = 1
        
        if hayerror == 1:
            break
        
        i += 1

    archivo_output.close()

    if hayerror == 1:
        return 1  # Termina el programa si hay un error
    else:
        return 0

main("codigo.txt")