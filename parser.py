def parser(tokens):
    i = 0

    if tokens[i][0] == "VAR":
        i += 1

        if tokens[i][0] != "ID":
            raise Exception("Erro: esperado identificador")
        i += 1

        if tokens[i][0] != "EQUAL":
            raise Exception("Erro: esperado '='")
        i += 1

        if tokens[i][0] != "NUM":
            raise Exception("Erro: esperado número")

    elif tokens[i][0] == "PRINT":
        i += 1

        if tokens[i][0] != "LPAREN":
            raise Exception("Erro: esperado '('")
        i += 1

        if tokens[i][0] != "ID":
            raise Exception("Erro: esperado identificador")
        i += 1

        if tokens[i][0] != "RPAREN":
            raise Exception("Erro: esperado ')'")

    else:
        raise Exception("Erro sintático")

    return True