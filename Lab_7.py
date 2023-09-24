import re

def load_grammars(filename):
    grammars = []
    current_grammar = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split('->')
                if len(parts) == 2:
                    non_terminal, productions = parts[0].strip(), parts[1].strip()
                    current_grammar[non_terminal] = productions.split('|')
                else:
                    if current_grammar:
                        grammars.append(current_grammar)
                    current_grammar = {}

    if current_grammar:
        grammars.append(current_grammar)

    return grammars

def find_nullable_symbols(grammar):
    nullable = set()
    changes = True
    while changes:
        changes = False
        for non_terminal, productions in grammar.items():
            for production in productions:
                if all(symbol in nullable for symbol in production):
                    if non_terminal not in nullable:
                        nullable.add(non_terminal)
                        changes = True
    return nullable

def eliminate_epsilon_productions(grammar):
    nullable = find_nullable_symbols(grammar)
    new_grammar = dict(grammar)

    for non_terminal, productions in grammar.items():
        for production in productions:
            for i, symbol in enumerate(production):
                if symbol in nullable:
                    new_production = production[:i] + production[i + 1:]
                    if new_production != '':
                        new_grammar[non_terminal].append(new_production)

    for non_terminal in nullable:
        for key, value in new_grammar.items():
            new_grammar[key] = [v.replace(non_terminal, '') for v in value]

    return new_grammar

def print_grammar(grammar):
    for non_terminal, productions in grammar.items():
        print(f"{non_terminal} -> {' | '.join(productions)}")

if __name__ == "__main__":
    filename = "gramatica.txt"  # Reemplaza con el nombre de tu archivo de gramática
    grammars = load_grammars(filename)

    for i, grammar in enumerate(grammars):
        grammar_name = f"Gramática {i + 1}"
        print(f"Gramática original ({grammar_name}):")
        print_grammar(grammar)

        new_grammar = eliminate_epsilon_productions(grammar)

        print(f"\nGramática sin producciones-𝜀 ({grammar_name}):")
        print_grammar(new_grammar)
