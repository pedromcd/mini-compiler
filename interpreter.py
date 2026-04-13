variables = {}

def interpret(tokens):
    # var x = 10
    if tokens[0][0] == "VAR":
        name = tokens[1][1]
        value = int(tokens[3][1])
        variables[name] = value

    # print(x)
    elif tokens[0][0] == "PRINT":
        name = tokens[2][1]

        if name in variables:
            print(variables[name])
        else:
            print("Erro: variável não definida")