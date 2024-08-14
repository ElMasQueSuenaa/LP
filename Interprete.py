import re
file = open('codigo.txt','r')

#EBNF
define = r"^\s*DEFINE\s+\$_[A-Z][A-Za-z]*\s*$"
asignacion = r"^\s*DP\s+\$_[A-Z][A-Za-z]*\s+ASIG\s+(True|False|\d+|#[^#]*#)\s*$"
suma = r"^\s*DP\s+\$_[A-Z][A-Za-z]*\s+\+\s+(\$_[A-Z][A-Za-z]*|\d+|#[^#]*#)\s+(\$_[A-Z][A-Za-z]*|\d+|#[^#]*#)\s*$"
multiplicacion = r"^\s*DP\s+\$_[A-Z][A-Za-z]*\s+\*\s+(\$_[A-Z][A-Za-z]*|\d+)\s+(\$_[A-Z][A-Za-z]*|\d+)\s*$"
leer_if = r"^\s*if\s*\(\s*\$_[A-Z][A-Za-z]*\s*\)\s*\{\s*$"
leer_else = r"^\s*\}\s*else\s*\{\s*$"
mostrar = r"^\s*MOSTRAR\(\s*\$_[A-Z][A-Za-z]*\s*\)\s*$"