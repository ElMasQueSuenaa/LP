import re

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

    if re.match(define, linea):
        var_name = re.findall(r"\$_[A-Z][A-Za-z]*", linea)[0]
        if var_name in variables:
            archivo_output.write(f"Línea {numero_linea}: Variable Ya Definida: La variable '{var_name}' ya se encuentra definida.")
        variables[var_name] = None
        return None

    elif re.match(asignacion, linea):
        parts = linea.split()
        var_name = parts[1]
        value = parts[3]

        if var_name not in variables:
            archivo_output.write(f"Línea {numero_linea}: Variable No Definida: La variable '{var_name}' no ha sido definida o no se le ha asignado valor.")
        if value.startswith("#") and value.endswith("#"):
            variables[var_name] = value[1:-1] 
        elif value.isdigit():
            variables[var_name] = int(value)
        elif value in ["True", "False"]:
            variables[var_name] = value == "True"
        else:
            archivo_output.write(f"Línea {numero_linea}: Tipo Incompatible: El valor '{value}' es incompatible con la operación.")

        return None

    elif re.match(suma, linea) or re.match(multiplicacion, linea):
        parts = linea.split()
        var_name = parts[1]
        operand1 = parts[3]
        operand2 = parts[4]

        if var_name not in variables:
            archivo_output.write(f"Línea {numero_linea}: Variable No Definida: La variable '{var_name}' no ha sido definida o no se le ha asignado valor.")

        operand1_value = variables.get(operand1) if operand1.startswith("$_") else int(operand1)
        operand2_value = variables.get(operand2) if operand2.startswith("$_") else int(operand2)

        if operand1_value is None or operand2_value is None:
            archivo_output.write(f"Línea {numero_linea}: Variable No Definida: Alguno de los operandos no ha sido definido o no se le ha asignado valor.")

        if isinstance(operand1_value, int) and isinstance(operand2_value, int):
            if "+" in linea:
                variables[var_name] = operand1_value + operand2_value
            elif "*" in linea:
                variables[var_name] = operand1_value * operand2_value
        else:
            archivo_output.write(f"Línea {numero_linea}: Tipo Incompatible: La operación en la línea es incompatible con el tipo de dato.")

        return None

    elif re.match(leer_if, linea):
        var_name = re.findall(r"\$_[A-Z][A-Za-z]*", linea)[0]
        if var_name not in variables or variables[var_name] is None:
            archivo_output.write(f"Línea {numero_linea}: Variable No Definida: La variable '{var_name}' no ha sido definida o no se le ha asignado valor.")
        if not isinstance(variables[var_name], bool):
            archivo_output.write(f"Línea {numero_linea}: Tipo Incompatible: La variable '{var_name}' no es booleana.")
        return None

    elif re.match(mostrar, linea):
        var_name = re.findall(r"\$_[A-Z][A-Za-z]*", linea)[0]
        if var_name not in variables:
            archivo_output.write(f"Línea {numero_linea}: Variable No Definida: La variable '{var_name}' no ha sido definida.")
        return None

    archivo_output.write(f"Línea {numero_linea}: Mal Sintaxis: La línea no está bien escrita.")


with open("codigo.txt") as file_object:
    lista=file_object.readlines()
i = 1
for linea in lista:
    verificador_linea(linea, i)