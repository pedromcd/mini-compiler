variables = {}

def interpret(tokens):
    print("DEBUG INTERPRETADOR NOVO")
def interpret(tokens):
    # Caso: var x = ...
    if tokens[0][0] == "VAR":
        name = tokens[1][1]

        # pega toda a expressão depois do '='
        expression_tokens = tokens[3:]

        # monta a expressão como string
        expression = ""
        for token in expression_tokens:
            expression += token[1]

        print("Expressão:", expression)  # debug (pode remover depois)

        try:
            value = eval(expression)
        except:
            raise Exception("Erro ao avaliar expressão")

        variables[name] = value

    # Caso: print(x)
    elif tokens[0][0] == "PRINT":
        name = tokens[2][1]

        if name in variables:
            print(variables[name])
        else:
            print("Erro: variável não definida")