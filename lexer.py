def lexer(code):
    tokens = []
    i = 0  # ponteiro para percorrer a string

    while i < len(code):
        char = code[i]

        # Ignora espaços em branco
        if char.isspace():
            i += 1
            continue

        # 🔹 Reconhecimento de números (estado NUM)
        elif char.isdigit():
            num = char
            i += 1
            while i < len(code) and code[i].isdigit():
                num += code[i]
                i += 1
            tokens.append(("NUM", num))

        # 🔹 Reconhecimento de palavras (ID ou palavras-chave)
        elif char.isalpha():
            word = char
            i += 1
            while i < len(code) and code[i].isalnum():
                word += code[i]
                i += 1

            # Verifica se é palavra-chave
            if word == "var":
                tokens.append(("VAR", word))
            elif word == "print":
                tokens.append(("PRINT", word))
            else:
                tokens.append(("ID", word))  # identificador

        # 🔹 Operadores e símbolos
        elif char == "=":
            tokens.append(("EQUAL", "="))
            i += 1

        elif char == "+":
            tokens.append(("PLUS", "+"))
            i += 1

        elif char == "-":
            tokens.append(("MINUS", "-"))
            i += 1

        elif char == "*":
            tokens.append(("MULT", "*"))
            i += 1

        elif char == "/":
            tokens.append(("DIV", "/"))
            i += 1

        elif char == "(":
            tokens.append(("LPAREN", "("))
            i += 1

        elif char == ")":
            tokens.append(("RPAREN", ")"))
            i += 1

        # 🔹 Erro léxico (símbolo não reconhecido)
        else:
            raise Exception(f"Erro léxico: {char}")

    return tokens