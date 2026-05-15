# ============================================================
# lexer.py — Analisador Léxico baseado em AFD explícito
# ============================================================
#
# O Autômato Finito Determinístico (AFD) é definido formalmente como:
#   M = (Q, Σ, δ, q0, F)
#
#   Q  = {INICIO, NUM, PALAVRA, OP, ERRO}
#   Σ  = caracteres ASCII imprimíveis
#   q0 = 'INICIO'
#   F  = {NUM, PALAVRA, OP}          (estados de aceitação)
#   δ  = dicionário TRANSITION_TABLE abaixo
#
# A cada caractere lido, o autômato consulta δ(estado_atual, tipo_char)
# e avança para o próximo estado. Ao detectar uma transição de volta a
# INICIO (fim de lexema), o token acumulado é classificado e emitido.
# ============================================================

# ------------------------------------------------------------------
# Classificação de caracteres (categorias do alfabeto de entrada)
# ------------------------------------------------------------------
def char_type(c):
    if c.isdigit():        return 'DIGIT'
    if c.isalpha():        return 'ALPHA'
    if c == '_':           return 'ALPHA'   # underscore válido em identificadores
    if c in '+-*/':        return 'OP'
    if c == '=':           return 'EQUAL'
    if c == '(':           return 'LPAREN'
    if c == ')':           return 'RPAREN'
    if c.isspace():        return 'SPACE'
    return 'INVALID'

# ------------------------------------------------------------------
# Tabela de transições δ: (estado_atual, tipo_char) → próximo_estado
# ------------------------------------------------------------------
#   'EMIT' significa: finalizar o token atual e reprocessar o char
# ------------------------------------------------------------------
TRANSITION_TABLE = {
    # Estado INICIO: ponto de partida e reset após cada token
    ('INICIO',  'DIGIT'):   'NUM',
    ('INICIO',  'ALPHA'):   'PALAVRA',
    ('INICIO',  'OP'):      'OP_SINGLE',
    ('INICIO',  'EQUAL'):   'EQUAL_SINGLE',
    ('INICIO',  'LPAREN'):  'PAREN_SINGLE',
    ('INICIO',  'RPAREN'):  'PAREN_SINGLE',
    ('INICIO',  'SPACE'):   'INICIO',       # ignora espaços
    ('INICIO',  'INVALID'): 'ERRO',

    # Estado NUM: acumulando dígitos
    ('NUM',     'DIGIT'):   'NUM',
    ('NUM',     'ALPHA'):   'EMIT',         # ex: "10x" → emite NUM, reinicia
    ('NUM',     'OP'):      'EMIT',
    ('NUM',     'EQUAL'):   'EMIT',
    ('NUM',     'LPAREN'):  'EMIT',
    ('NUM',     'RPAREN'):  'EMIT',
    ('NUM',     'SPACE'):   'EMIT',
    ('NUM',     'INVALID'): 'ERRO',

    # Estado PALAVRA: acumulando letras/dígitos (identificadores e keywords)
    ('PALAVRA', 'ALPHA'):   'PALAVRA',
    ('PALAVRA', 'DIGIT'):   'PALAVRA',
    ('PALAVRA', 'OP'):      'EMIT',
    ('PALAVRA', 'EQUAL'):   'EMIT',
    ('PALAVRA', 'LPAREN'):  'EMIT',
    ('PALAVRA', 'RPAREN'):  'EMIT',
    ('PALAVRA', 'SPACE'):   'EMIT',
    ('PALAVRA', 'INVALID'): 'ERRO',

    # Estados de token único (OP, EQUAL, PAREN): sempre emitem imediatamente
    ('OP_SINGLE',    'DIGIT'):   'EMIT',
    ('OP_SINGLE',    'ALPHA'):   'EMIT',
    ('OP_SINGLE',    'OP'):      'EMIT',
    ('OP_SINGLE',    'EQUAL'):   'EMIT',
    ('OP_SINGLE',    'LPAREN'):  'EMIT',
    ('OP_SINGLE',    'RPAREN'):  'EMIT',
    ('OP_SINGLE',    'SPACE'):   'EMIT',
    ('OP_SINGLE',    'INVALID'): 'EMIT',

    ('EQUAL_SINGLE', 'DIGIT'):   'EMIT',
    ('EQUAL_SINGLE', 'ALPHA'):   'EMIT',
    ('EQUAL_SINGLE', 'OP'):      'EMIT',
    ('EQUAL_SINGLE', 'EQUAL'):   'EMIT',
    ('EQUAL_SINGLE', 'LPAREN'):  'EMIT',
    ('EQUAL_SINGLE', 'RPAREN'):  'EMIT',
    ('EQUAL_SINGLE', 'SPACE'):   'EMIT',
    ('EQUAL_SINGLE', 'INVALID'): 'EMIT',

    ('PAREN_SINGLE', 'DIGIT'):   'EMIT',
    ('PAREN_SINGLE', 'ALPHA'):   'EMIT',
    ('PAREN_SINGLE', 'OP'):      'EMIT',
    ('PAREN_SINGLE', 'EQUAL'):   'EMIT',
    ('PAREN_SINGLE', 'LPAREN'):  'EMIT',
    ('PAREN_SINGLE', 'RPAREN'):  'EMIT',
    ('PAREN_SINGLE', 'SPACE'):   'EMIT',
    ('PAREN_SINGLE', 'INVALID'): 'EMIT',
}

# Conjunto de estados de aceitação F
ACCEPT_STATES = {'NUM', 'PALAVRA', 'OP_SINGLE', 'EQUAL_SINGLE', 'PAREN_SINGLE'}

# Palavras-chave da linguagem
KEYWORDS = {'var', 'print'}

# ------------------------------------------------------------------
# Função de classificação do lexema acumulado → tipo de token
# ------------------------------------------------------------------
def classify(state, lexeme):
    if state == 'NUM':
        return ('NUM', lexeme)
    if state == 'PALAVRA':
        if lexeme in KEYWORDS:
            return (lexeme.upper(), lexeme)   # VAR ou PRINT
        return ('ID', lexeme)
    if state == 'OP_SINGLE':
        names = {'+': 'PLUS', '-': 'MINUS', '*': 'MULT', '/': 'DIV'}
        return (names[lexeme], lexeme)
    if state == 'EQUAL_SINGLE':
        return ('EQUAL', lexeme)
    if state == 'PAREN_SINGLE':
        return ('LPAREN' if lexeme == '(' else 'RPAREN', lexeme)
    return None

# ------------------------------------------------------------------
# Máquina do AFD — percorre a entrada dirigida pela tabela δ
# ------------------------------------------------------------------
def lexer(code):
    tokens  = []
    state   = 'INICIO'
    lexeme  = ''
    i       = 0

    while i <= len(code):
        # Sentinela: ao fim da string, forçamos um SPACE para emitir o
        # último token pendente (se houver) sem duplicar lógica.
        c = code[i] if i < len(code) else ' '
        ctype = char_type(c)

        next_state = TRANSITION_TABLE.get((state, ctype)),

        print(f"[{state}] -- {c} --> [{next_state}]")

        if next_state is None:
            raise Exception(f"Erro léxico: caractere inesperado '{c}'")

        if next_state == 'ERRO':
            raise Exception(f"Erro léxico: '{c}' não pertence ao alfabeto da linguagem")

        if next_state == 'EMIT':
            # Emite o token acumulado, reinicia e reprocessa o char atual
            if state in ACCEPT_STATES and lexeme:
                tok = classify(state, lexeme)
                if tok:
                    tokens.append(tok)
            state  = 'INICIO'
            lexeme = ''
            # NÃO avança i — o char atual será reprocessado no próximo ciclo
        else:
            # Transição normal: acumula o char e avança
            if next_state != 'INICIO':
                lexeme += c
            state = next_state
            i += 1

    return tokens