import re

# Lista para almacenar las gramáticas
grammars_list = []  

# Función para analizar una línea de gramática y agregarla a la lista de gramáticas
def parse_grammar_line(line):
    line = line.strip()
    if re.compile(r'Gramatica([0-9])*').match(line):
        # Si la línea contiene un encabezado de nueva gramática, agregamos una nueva lista
        grammars_list.append([])  # Agregar una nueva gramática a la lista
        print(f'Nueva gramática detectada: {line}')
    elif not line:
        return
    else:
        # Expresión regular para validar una producción gramatical
        exp_regular = re.compile(r'[A-Z]\s*->\s*(([A-Z])|([0-9A-Za-z]+(\s*\|\s*[0-9A-Za-z]+)*))')
        if exp_regular.match(line):
            grammars_list[-1].append(line)  # Agregar una producción válida a la gramática actual
            print(f'Producción válida: {line}')
        else:
            print(f'Producción inválida: {line}')

# Función para cargar y analizar las gramáticas desde un archivo
def load_and_parse_grammars(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()

        for linea in lineas:
            parse_grammar_line(linea)

    except FileNotFoundError:
        print(f"El archivo '{filename}' no se encontró.")
    except IOError as e:
        print(f"Error de E/S: {str(e)}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {str(e)}")

# Función para encontrar los símbolos anulables en una gramática
def find_nullable_symbols(grammar):
    nullable = set()
    changes = True
    while changes:
        changes = False
        for production in grammar:
            parts = production.split('->')
            non_terminal, production_body = parts[0].strip(), parts[1].strip()
            # Verificar si todos los símbolos en la producción son anulables
            if all(symbol in nullable for symbol in production_body):
                if non_terminal not in nullable:
                    nullable.add(non_terminal)
                    changes = True
    return nullable

# Función para eliminar producciones epsilon en una gramática
def eliminate_epsilon_productions(grammar):
    nullable = find_nullable_symbols(grammar)
    new_grammar = list(grammar)

    for i in range(len(new_grammar)):
        parts = new_grammar[i].split('->')
        non_terminal, production_body = parts[0].strip(), parts[1].strip()
        new_productions = []

        # Generar todas las combinaciones posibles sin símbolos anulables
        def generate_combinations(current, remaining):
            if not remaining:
                new_productions.append(current)
                return
            first_symbol = remaining[0]
            rest_symbols = remaining[1:]
            if first_symbol not in nullable:
                generate_combinations(current + first_symbol, rest_symbols)
            generate_combinations(current, rest_symbols)

        generate_combinations('', production_body)

        # Agregar las nuevas producciones al resultado
        new_grammar[i] = f"{non_terminal} -> {' | '.join(new_productions)}"

    return new_grammar

# Función para imprimir una gramática
def print_grammar(grammar):
    for production in grammar:
        print(production)

if __name__ == "__main__":
    filename = "gramatica.txt"  
    load_and_parse_grammars(filename)
    
    # Procesar y mostrar las gramáticas
    for i, grammar in enumerate(grammars_list):
        grammar_name = f"Gramática {i + 1}"
        print(f"Gramática original ({grammar_name}):")
        for production in grammar:
            print(production)
        new_grammar = eliminate_epsilon_productions(grammar)
        print(f"\nGramática sin producciones-𝜀 ({grammar_name}):")
        print_grammar(new_grammar)
