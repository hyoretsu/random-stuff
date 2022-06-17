import re
from interfaces import Grammar

# Validação dos símbolos
def symbol_validation(symbols: list[str] | str, casing: str):
    # Como só estamos esperando um único símbolo inicial (string), caso passe uma combinação (Ss) ou vários símbolos iniciais (S,A) o Python reconhecerá isto como uma lista de caractéres, e cada um deles iria passar nos testes mais adiante (ou cair em um erro indevido ou aumentar substancialmente o código). Portanto, precisamos checar que, caso seja inicial, não tenha mais de 1 caractére, independente se combinação ou símbolo
    if (casing == "initial") and (len(symbols) > 1):
        raise SystemExit("Só pode existir um símbolo inicial ou foi fornecida uma combinação. Tente novamente.")

    for symbol in symbols:
        if symbol == "":
            raise SystemExit("Por favor, forneça ao menos um símbolo para cada categoria.")

        # Símbolos não-terminais não aceitam dígitos
        if casing != "lower" and symbol.isnumeric():
            raise SystemExit("Um dos símbolos não-terminais fornecidos é um dígito. Tente novamente.")
        # Foi fornecida uma combinação (AB) ao invés de um símbolo (A)
        if len(symbol) > 1:
            raise SystemExit("Cada entrada deve conter apenas 1 símbolo. Tente novamente.")

        if (casing == "upper") | (casing == "initial"):
            correctCasing = symbol.isupper()
        elif casing == "lower":
            correctCasing = symbol.islower() or symbol.isnumeric()

        if not correctCasing:
            if casing == "initial":
                raise SystemExit("Um símbolo não-terminal foi fornecido como inicial. Tente novamente.")

            # Um não-terminal foi fornecido como terminal ou um terminal foi fornecido como não-terminal
            raise SystemExit("Um dos símbolos fornecidos está na categoria errada. Tente novamente.")


# Processamento das produções
def prod_processing(grammar: Grammar, productions: list[str]):
    grammar["productions"] = {}

    for prod in productions:
        [variable, terminals] = re.split(r"\s?->\s?", prod)

        if not variable.isupper():
            raise SystemExit("A parte esquerda da produção só pode conter símbolos não-terminais. Tente novamente.")

        if len(variable) > 1:
            raise SystemExit(
                "A parte esquerda da produção só pode conter um único símbolo não-terminal. Tente novamente."
            )

        # Inicializa o array da propriedade da variável caso não exista
        grammar["productions"].setdefault(variable, [])

        # Caso o usuário tenha incluído mais de uma substituição na mesma produção, separa cada uma
        terminals = terminals.split("|")

        # Percorre um array que terá ou uma posição ou várias, a depender da produção fornecida
        for result in terminals:
            grammar["productions"][variable].append(result)

    # Checa se todos os símbolos não-terminais possuem produções, caso contrário teríamos uma gramática inválida/incompleta
    for variable in grammar["variables"]:
        try:
            list(grammar["productions"].keys()).index(variable)
        except ValueError:
            raise SystemExit(f"Não há produções para o não-terminal {variable}. Tente novamente.")


# Reconhecimento da gramática e encaminhamento para suas respectivas funções de processamento
def grammar_parse(rawGrammar: str) -> Grammar:
    grammar = Grammar()

    # Coleta de símbolos, retirada de espaços e separação em uma lista pelas vírgulas (ou quebra de linha no caso das produções)

    grammar["terminals"] = re.search(r"terminais\s?=((?:.*,?)*)", rawGrammar).group(1).replace(" ", "").split(",")
    symbol_validation(grammar["terminals"], "lower")

    grammar["variables"] = re.search(r"variaveis\s?=((?:.*,?)*)", rawGrammar).group(1).replace(" ", "").split(",")
    symbol_validation(grammar["variables"], "upper")

    grammar["initial"] = re.search(r"inicial\s?=(.*)", rawGrammar).group(1).replace(" ", "")
    symbol_validation(grammar["initial"], "initial")

    productions = re.search(r"producoes\n((?:.*->.*(?:\n|$))*)", rawGrammar).group(1).replace(" ", "").split("\n")
    prod_processing(grammar, productions)

    return grammar
