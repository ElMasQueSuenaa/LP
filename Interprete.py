import re
import sys

#EBNF
define = r"^\s*DEFINE\s+\$_[A-Z][A-Za-z]*\s*$"
asignacion = r"^\s*DP\s+\$_[A-Z][A-Za-z]*\s+ASIG\s+(True|False|\d+|#[^#]*#)\s*$"
suma = r"^\s*DP\s+\$_[A-Z][A-Za-z]*\s+\+\s+(\$_[A-Z][A-Za-z]*|\d+|#[^#]*#)\s+(\$_[A-Z][A-Za-z]*|\d+|#[^#]*#)\s*$"
multiplicacion = r"^\s*DP\s+\$_[A-Z][A-Za-z]*\s+\*\s+(\$_[A-Z][A-Za-z]*|\d+)\s+(\$_[A-Z][A-Za-z]*|\d+)\s*$"
leer_if = r"^\s*if\s*\(\s*\$_[A-Z][A-Za-z]*\s*\)\s*\{\s*$"
leer_else = r"^\s*\}\s*else\s*\{\s*$"
mostrar = r"^\s*MOSTRAR\(\s*\$_[A-Z][A-Za-z]*\s*\)\s*$"
concatenacion_texto = r"^\s*DP\s+\$_[A-Z][A-Za-z]*\s+\+\s+(\$_[A-Z][A-Za-z]*|#[^#]*#)\s+(\$_[A-Z][A-Za-z]*|#[^#]*#)\s*$"

archivo_output=open("output.txt", "w")

variables = {}

def verificador_linea(linea, numero_linea):
    
    linea = linea.strip()
    error_encontrado = 0

    if re.match(define, linea):
        var_name = re.findall(r"\$_[A-Z][A-Za-z]*", linea)[0]
        if var_name in variables:
            print("Línea", numero_linea, ": Variable Ya Definida: La variable", var_name, "ya se encuentra definida.")
            error_encontrado = 1
        else:
            variables[var_name] = None
    elif re.match(asignacion, linea):
        parts = linea.split()
        var_name = parts[1]
        value = parts[3]

        if var_name not in variables:
            print("Línea", numero_linea, ": Variable No Definida: La variable", var_name, "no ha sido definida o no se le ha asignado valor.")
            error_encontrado = 1
        else:
            if value.startswith("#") and value.endswith("#"):
                variables[var_name] = value[1:-1] 
            elif value.isdigit():
                variables[var_name] = int(value)
            elif value in ["True", "False"]:
                variables[var_name] = value == "True"
            else:
                print("Línea", numero_linea, ": Tipo Incompatible: El valor", value, "es incompatible con la operación.")
                error_encontrado = 1
    elif re.match(suma, linea) or re.match(multiplicacion, linea):
        parts = linea.split()
        var_name = parts[1]
        operand1 = parts[3]
        operand2 = parts[4]

        if var_name not in variables:
            print("Línea", numero_linea, ": Variable No Definida: La variable", var_name, "no ha sido definida o no se le ha asignado valor.")
            error_encontrado = 1
        else:
            operand1_value = variables.get(operand1) if operand1.startswith("$_") else int(operand1)
            operand2_value = variables.get(operand2) if operand2.startswith("$_") else int(operand2)

            if operand1_value is None or operand2_value is None:
                print("Línea", numero_linea, ": Variable No Definida: Alguno de los operandos no ha sido definido o no se le ha asignado valor.")
                error_encontrado = 1
            elif isinstance(operand1_value, int) and isinstance(operand2_value, int):
                if "+" in linea:
                    variables[var_name] = operand1_value + operand2_value
                elif "*" in linea:
                    variables[var_name] = operand1_value * operand2_value
            else:
                print("Línea", numero_linea, ": Tipo Incompatible: La operación en la línea es incompatible con el tipo de dato.")
                error_encontrado = 1
    elif re.match(leer_if, linea):
        var_name = re.findall(r"\$_[A-Z][A-Za-z]*", linea)[0]
        if var_name not in variables or variables[var_name] is None:
            print("Línea", numero_linea, ": Variable No Definida: La variable", var_name, "no ha sido definida o no se le ha asignado valor.")
            error_encontrado = 1
        elif not isinstance(variables[var_name], bool):
            print("Línea", numero_linea, ": Tipo Incompatible: La variable", var_name, "no es booleana.")
            error_encontrado = 1
    elif re.match(mostrar, linea):
        var_name = re.findall(r"\$_[A-Z][A-Za-z]*", linea)[0]
        if var_name not in variables:
            print("Línea", numero_linea, ": Variable No Definida: La variable", var_name, "no ha sido definida.")
            error_encontrado = 1
    else:
        print("Línea", numero_linea, ": Mal Sintaxis: La línea no está bien escrita.")
        error_encontrado = 1

    return error_encontrado

def definir_variable(linea):
    linea = linea.strip()
    matches = re.findall(r"\$_[A-Z][A-Za-z]*", linea)
    nombre_var = matches[0]
    variables[0] = nombre_var
    variables[nombre_var] = None
    
with open("codigo.txt") as file_object:
    lista=file_object.readlines()
i = 1
hayerror = 0
for linea in lista:
    hayerror = verificador_linea(linea, i)
    if hayerror == 0:
        i = 1#mentira
    elif hayerror == 1:
        archivo_output.close()
        file_object.close()
        sys.exit()
    
    