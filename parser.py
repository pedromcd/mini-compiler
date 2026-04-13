def parser(tokens):
    i = 0  # ponteiro na lista de tokens

    # 🔹 Regra: DECL → var ID = EXPR
    if tokens[i][0] == "VAR":
        i += 1

        # Espera um identificador
        if tokens[i][0] != "ID":
            raise Exception("Erro: esperado identificador")
        i += 1

        # Espera '='
        if tokens[i][0] != "EQUAL":
            raise Exception("Erro: esperado '='")
        i += 1

        # Espera um número (início da expressão)
        if tokens[i][0] != "NUM":
            raise Exception("Erro: esperado número")
        i += 1

        # 🔹 Regra simplificada de expressão: NUM (OP NUM)*
        while i < len(tokens):
            if tokens[i][0] in ["PLUS", "MINUS", "MULT", "DIV"]:
                i += 1

                if i >= len(tokens) or tokens[i][0] != "NUM":
                    raise Exception("Erro: esperado número após operador")
                i += 1
            else:
                break

    # 🔹 Regra: PRINT → print ( ID )
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

    # 🔹 Caso não reconheça nenhuma estrutura válida
    else:
        raise Exception("Erro sintático")

    return True