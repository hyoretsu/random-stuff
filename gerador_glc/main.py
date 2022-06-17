from utils import clear, install

# Instalação automática das bibliotecas de terceiros utilizadas
install("simple-term-menu")
# clear()


from funcs import grammar_parse
from random import randint
from simple_term_menu import TerminalMenu


try:
    grammarFile = open("gramatica.txt").read()
except FileNotFoundError:
    raise SystemExit(
        """
Por favor, forneça uma grámatica em um arquivo chamado "gramatica.txt" no seguinte formato:
terminais=a,b
variaveis=S,A
inicial=S

producoes
S-> aA
A-> epsilon
        """
    )

# Processar a gramática
grammar = grammar_parse(grammarFile)

# Menu para escolher o modo de funcionamento da aplicação
modes = ["Rápido", "Detalhado"]
mode: str = modes[TerminalMenu(modes, title="Qual modo deseja executar?").show()]

# Por motivos de facilitar o código, é melhor guardar a cadeia de saída como uma lista e converter para string quando necessário
output = list(grammar["initial"])

quickPrints = []
pastOutputs = []
# Limite relativamente seguro de vezes para tentar gerar uma nova gramática, visto que contar exatamente quantas possiveis derivações uma gramática pode ter seria complicado dada uma gramática complexa. As exceções são para gramáticas gigantes ou infinitas
runLimit = 50
origLimit = runLimit

# Contador para achar a posição para as substituições
current = 0

while True:
    if runLimit == 0:
        print("É improvável que existam cadeias restantes na gramática fornecida.")

        break

    try:
        # Percorre o restante da saída até achar um não-terminal
        while True:
            # Se achou um símbolo terminal, passar para a próxima posição
            if not output[current].isupper():
                current += 1
            else:
                break
    # O último símbolo da cadeia de saída foi um terminal. Portanto, o programa terminou
    except IndexError:
        # No modo rápido, continuaremos gerando uma nova cadeia até o usuário não querer mais.
        if mode == "Rápido":
            alreadyGenerated = False

            # Se ele gerou uma cadeia igual a alguma das anteriores, reinicia o ciclo para gerar outra cadeia
            for past in pastOutputs:
                if past == "".join(output):
                    output = list(grammar["initial"])
                    current = 0
                    quickPrints = []

                    alreadyGenerated = True

            # Reinicia o ciclo e aumenta a contagem regressiva de iterações
            if alreadyGenerated:
                runLimit -= 1
                continue

            # Caso contrário, adiciona a cadeia resultante a uma lista para que não se repita mais e resetta a contagem
            pastOutputs.append("".join(output))
            runLimit = origLimit

            # Printa cadeia, substituição e resultado
            for message in quickPrints:
                print(message[0])
                print(message[1])

            print(f"A cadeia resultante foi: {''.join(output)}\n")

            # Menu para ver se o usuário quer continuar ou não
            yesNo = ["Sim", "Não"]
            answer = yesNo[
                TerminalMenu(
                    yesNo,
                    title="Deseja gerar outra cadeia?",
                ).show()
            ]

            # Para isso, basta reiniciarmos a cadeia de saída e a variável de posição e o ciclo continuará se repetindo do começo
            if answer == "Sim":
                output = list(grammar["initial"])
                current = 0
                quickPrints = []

                continue

        if mode == "Detalhado":
            print(f"A cadeia resultante é: {''.join(output)}\n")

        break

    # Possíveis substituições para o símbolo atual
    results = grammar["productions"][output[current]]

    prods: list[str] = []
    # Junta os símbolos em produções
    for symbol in results:
        if symbol == "epsilon":
            symbol = "ε"

        prods.append(f"{output[current]} -> {symbol}")

    # Modo de funcionamento do programa
    if mode == "Rápido":
        # Escolhe uma substituição aleatória dentre as possíveis. Fora isso, o programa já realiza derivação mais à esquerda por natureza
        choice = randint(0, len(prods) - 1)

        quickPrints.append([f"Cadeia: {''.join(output)}", f"Substituição: {prods[choice]}"])
    elif mode == "Detalhado":
        # Menu para o usuário escolher uma substituição
        choice = TerminalMenu(
            map(lambda prod: f"{prods.index(prod) + 1}. {prod}", prods),
            title=f"Esta é a saída atual: {''.join(output)}\nQual das seguintes substituições deseja realizar?",
        ).show()

    # Removemos o símbolo não-terminal para trocá-lo pela substituição escolhida
    output.pop(current)
    # Em caso de substituição para epsilon, simplesmente excluímos o não-terminal
    if results[choice] == "epsilon":
        # Derivou-se para um único símbolo e depois para epsilon, não produzindo nenhum símbolo terminal
        if len(output) == 0:
            output = "ε"

        continue
    else:
        # Caso contrário, adicionamos cada símbolo na posição atual (+1 por causa do list.insert())
        for index, symbol in enumerate(results[choice]):
            output.insert(current + (index + 1), symbol)
