# ============================================================
# lexer.py — Analisador Léxico baseado em AFD explícito
# ============================================================
#
# O Autômato Finito Determinístico (AFD) é definido formalmente como:
#
#   M = (Q, Σ, δ, q0, F)
#
#   Q  = conjunto de estados
#   Σ  = alfabeto de entrada
#   δ  = função de transição
#   q0 = estado inicial
#   F  = conjunto de estados finais
#
# ============================================================

# ------------------------------------------------------------
# Classificação dos caracteres do alfabeto
# ------------------------------------------------------------
def char_type(c):

    if c.isdigit():
        return 'DIGIT'

    if c.isalpha():
        return 'ALPHA'

    if c == '_':
        return 'ALPHA'

    if c in '+-*/':
        return 'OP'

    if c == '=':
        return 'EQUAL'

    if c == '(':
        return 'LPAREN'

    if c == ')':
        return 'RPAREN'

    if c.isspace():
        return 'SPACE'

    return 'INVALID'


# ------------------------------------------------------------
# Tabela de transições δ
# (estado_atual, tipo_char) → próximo_estado
# ------------------------------------------------------------
TRANSITION_TABLE = {

    # Estado inicial
    ('INICIO', 'DIGIT'):   'NUM',
    ('INICIO', 'ALPHA'):   'PALAVRA',
    ('INICIO', 'OP'):      'OP_SINGLE',
    ('INICIO', 'EQUAL'):   'EQUAL_SINGLE',
    ('INICIO', 'LPAREN'):  'PAREN_SINGLE',
    ('INICIO', 'RPAREN'):  'PAREN_SINGLE',
    ('INICIO', 'SPACE'):   'INICIO',
    ('INICIO', 'INVALID'): 'ERRO',

    # Estado NUM
    ('NUM', 'DIGIT'):   'NUM',
    ('NUM', 'ALPHA'):   'EMIT',
    ('NUM', 'OP'):      'EMIT',
    ('NUM', 'EQUAL'):   'EMIT',
    ('NUM', 'LPAREN'):  'EMIT',
    ('NUM', 'RPAREN'):  'EMIT',
    ('NUM', 'SPACE'):   'EMIT',
    ('NUM', 'INVALID'): 'ERRO',

    # Estado PALAVRA
    ('PALAVRA', 'ALPHA'):   'PALAVRA',
    ('PALAVRA', 'DIGIT'):   'PALAVRA',
    ('PALAVRA', 'OP'):      'EMIT',
    ('PALAVRA', 'EQUAL'):   'EMIT',
    ('PALAVRA', 'LPAREN'):  'EMIT',
    ('PALAVRA', 'RPAREN'):  'EMIT',
    ('PALAVRA', 'SPACE'):   'EMIT',
    ('PALAVRA', 'INVALID'): 'ERRO',

    # Operadores
    ('OP_SINGLE', 'DIGIT'):   'EMIT',
    ('OP_SINGLE', 'ALPHA'):   'EMIT',
    ('OP_SINGLE', 'OP'):      'EMIT',
    ('OP_SINGLE', 'EQUAL'):   'EMIT',
    ('OP_SINGLE', 'LPAREN'):  'EMIT',
    ('OP_SINGLE', 'RPAREN'):  'EMIT',
    ('OP_SINGLE', 'SPACE'):   'EMIT',
    ('OP_SINGLE', 'INVALID'): 'EMIT',

    # Igual
    ('EQUAL_SINGLE', 'DIGIT'):   'EMIT',
    ('EQUAL_SINGLE', 'ALPHA'):   'EMIT',
    ('EQUAL_SINGLE', 'OP'):      'EMIT',
    ('EQUAL_SINGLE', 'EQUAL'):   'EMIT',
    ('EQUAL_SINGLE', 'LPAREN'):  'EMIT',
    ('EQUAL_SINGLE', 'RPAREN'):  'EMIT',
    ('EQUAL_SINGLE', 'SPACE'):   'EMIT',
    ('EQUAL_SINGLE', 'INVALID'): 'EMIT',

    # Parênteses
    ('PAREN_SINGLE', 'DIGIT'):   'EMIT',
    ('PAREN_SINGLE', 'ALPHA'):   'EMIT',
    ('PAREN_SINGLE', 'OP'):      'EMIT',
    ('PAREN_SINGLE', 'EQUAL'):   'EMIT',
    ('PAREN_SINGLE', 'LPAREN'):  'EMIT',
    ('PAREN_SINGLE', 'RPAREN'):  'EMIT',
    ('PAREN_SINGLE', 'SPACE'):   'EMIT',
    ('PAREN_SINGLE', 'INVALID'): 'EMIT',
}

# ------------------------------------------------------------
# Estados finais F
# ------------------------------------------------------------
ACCEPT_STATES = {
    'NUM',
    'PALAVRA',
    'OP_SINGLE',
    'EQUAL_SINGLE',
    'PAREN_SINGLE'
}

# ------------------------------------------------------------
# Palavras-chave da linguagem
# ------------------------------------------------------------
KEYWORDS = {
    'var',
    'print'
}


# ------------------------------------------------------------
# Classificação do token reconhecido
# ------------------------------------------------------------
def classify(state, lexeme):

    if state == 'NUM':
        return ('NUM', lexeme)

    if state == 'PALAVRA':

        if lexeme in KEYWORDS:
            return (lexeme.upper(), lexeme)

        return ('ID', lexeme)

    if state == 'OP_SINGLE':

        names = {
            '+': 'PLUS',
            '-': 'MINUS',
            '*': 'MULT',
            '/': 'DIV'
        }

        return (names[lexeme], lexeme)

    if state == 'EQUAL_SINGLE':
        return ('EQUAL', lexeme)

    if state == 'PAREN_SINGLE':

        if lexeme == '(':
            return ('LPAREN', lexeme)

        return ('RPAREN', lexeme)

    return None


# ------------------------------------------------------------
# Execução do AFD
# ------------------------------------------------------------
def lexer(code, debug=False):

    tokens = []

    state = 'INICIO'

    lexeme = ''

    i = 0

    while i <= len(code):

        # Sentinela de fim de entrada
        c = code[i] if i < len(code) else ' '

        ctype = char_type(c)

        # Consulta δ
        next_state = TRANSITION_TABLE.get((state, ctype))

        # Debug do autômato
        if debug:
            print(f"[{state}] -- '{c}' ({ctype}) --> [{next_state}]")

        # Estado inválido
        if next_state is None:
            raise Exception(f"Caractere inesperado: '{c}'")

        # Estado de erro
        if next_state == 'ERRO':
            raise Exception(f"'{c}' não pertence ao alfabeto da linguagem")

        # Emissão de token
        if next_state == 'EMIT':

            if state in ACCEPT_STATES and lexeme:

                tok = classify(state, lexeme)

                if tok:

                    tokens.append(tok)

                    if debug:
                        print(f"  TOKEN EMITIDO: {tok}")

            # Reinicia o autômato
            state = 'INICIO'

            lexeme = ''

            # NÃO avança o índice
            continue

        # Transição normal
        else:

            if next_state != 'INICIO':
                lexeme += c

            state = next_state

            i += 1

    return tokens