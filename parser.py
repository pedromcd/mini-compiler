# ============================================================
# parser.py — Analisador Sintático baseado em GLC explícita
# ============================================================
#
# A Gramática Livre de Contexto (GLC) da linguagem é definida como:
#   G = (V, Σ, P, S)
#
#   V  = {PROGRAMA, STMT, DECL, PRINT_STMT, EXPR, TERMO, FATOR, OP}
#   Σ  = {VAR, PRINT, ID, NUM, EQUAL, PLUS, MINUS, MULT, DIV, LPAREN, RPAREN}
#   S  = PROGRAMA
#
#   Produções P:
#     PROGRAMA     → STMT
#     STMT         → DECL | PRINT_STMT
#     DECL         → VAR ID EQUAL EXPR
#     PRINT_STMT   → PRINT LPAREN ID RPAREN
#     EXPR         → TERMO (( PLUS | MINUS ) TERMO)*
#     TERMO        → FATOR (( MULT | DIV ) FATOR)*
#     FATOR        → NUM | ID
#
# Por que GLC e não Gramática Regular?
#   A regra EXPR → TERMO (OP TERMO)* possui aninhamento implícito de
#   operações com precedência diferenciada (MULT/DIV antes de PLUS/MINUS),
#   o que exige uma hierarquia de não-terminais (EXPR → TERMO → FATOR)
#   impossível de capturar com uma gramática regular simples.
#
# Implementação: parser descendente recursivo (top-down, LL(1)).
#   Cada não-terminal da gramática corresponde a uma função Python.
# ============================================================

# ------------------------------------------------------------------
# Classe auxiliar: mantém o ponteiro de leitura sobre a lista de tokens
# ------------------------------------------------------------------
class TokenStream:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos    = 0

    def peek(self):
        """Retorna o tipo do token atual sem consumir."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos][0]
        return None

    def consume(self, expected_type=None):
        """Consome o token atual; lança exceção se o tipo não bater."""
        if self.pos >= len(self.tokens):
            raise Exception(f"Erro sintático: esperado '{expected_type}', mas a entrada terminou")
        tok = self.tokens[self.pos]
        if expected_type and tok[0] != expected_type:
            raise Exception(
                f"Erro sintático: esperado '{expected_type}', encontrado '{tok[1]}'"
            )
        self.pos += 1
        return tok

    def at_end(self):
        return self.pos >= len(self.tokens)


# ------------------------------------------------------------------
# Funções de parsing — uma por não-terminal da gramática
# ------------------------------------------------------------------

def parse_programa(stream):
    """PROGRAMA → STMT"""
    parse_stmt(stream)
    if not stream.at_end():
        tok = stream.tokens[stream.pos]
        raise Exception(f"Erro sintático: token inesperado '{tok[1]}' após fim do comando")


def parse_stmt(stream):
    """STMT → DECL | PRINT_STMT"""
    t = stream.peek()
    if t == 'VAR':
        parse_decl(stream)
    elif t == 'PRINT':
        parse_print_stmt(stream)
    else:
        tok = stream.tokens[stream.pos] if not stream.at_end() else ('?', '<vazio>')
        raise Exception(f"Erro sintático: comando desconhecido '{tok[1]}'")


def parse_decl(stream):
    """DECL → VAR ID EQUAL EXPR"""
    stream.consume('VAR')
    stream.consume('ID')
    stream.consume('EQUAL')
    parse_expr(stream)


def parse_print_stmt(stream):
    """PRINT_STMT → PRINT LPAREN ID RPAREN"""
    stream.consume('PRINT')
    stream.consume('LPAREN')
    stream.consume('ID')
    stream.consume('RPAREN')


def parse_expr(stream):
    """EXPR → TERMO (( PLUS | MINUS ) TERMO)*"""
    parse_termo(stream)
    while stream.peek() in ('PLUS', 'MINUS'):
        stream.consume()           # consome o operador
        parse_termo(stream)


def parse_termo(stream):
    """TERMO → FATOR (( MULT | DIV ) FATOR)*"""
    parse_fator(stream)
    while stream.peek() in ('MULT', 'DIV'):
        stream.consume()           # consome o operador
        parse_fator(stream)


def parse_fator(stream):
    """FATOR → NUM | ID"""
    t = stream.peek()
    if t == 'NUM':
        stream.consume('NUM')
    elif t == 'ID':
        stream.consume('ID')
    else:
        tok = stream.tokens[stream.pos] if not stream.at_end() else ('?', '<vazio>')
        raise Exception(
            f"Erro sintático: esperado número ou identificador, encontrado '{tok[1]}'"
        )


# ------------------------------------------------------------------
# Ponto de entrada público (compatível com o main.py original)
# ------------------------------------------------------------------
def parser(tokens):
    stream = TokenStream(tokens)
    parse_programa(stream)
    return True