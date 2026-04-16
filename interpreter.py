# ============================================================
# interpreter.py — Interpretador semântico
# ============================================================
#
# Responsável pela fase semântica: percorre os tokens já validados
# pelo parser e executa as operações, mantendo a tabela de variáveis.
#
# Diferença importante em relação à versão original:
#   - Expressões suportam tanto literais (NUM) quanto variáveis (ID).
#   - A avaliação é feita manualmente, respeitando precedência de
#     operadores (MULT/DIV antes de PLUS/MINUS), sem usar eval().
#   - Isso espelha exatamente a hierarquia EXPR → TERMO → FATOR da GLC.
# ============================================================

# Tabela de variáveis: { nome (str) → valor (int/float) }
variables = {}


# ------------------------------------------------------------------
# Avaliador de expressões (espelha a GLC do parser)
# ------------------------------------------------------------------

class ExprEvaluator:
    """Avalia uma sequência de tokens de expressão com precedência correta."""

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos    = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos][0]
        return None

    def consume(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def eval_expr(self):
        """EXPR → TERMO (( PLUS | MINUS ) TERMO)*"""
        result = self.eval_termo()
        while self.peek() in ('PLUS', 'MINUS'):
            op = self.consume()
            right = self.eval_termo()
            if op[0] == 'PLUS':
                result += right
            else:
                result -= right
        return result

    def eval_termo(self):
        """TERMO → FATOR (( MULT | DIV ) FATOR)*"""
        result = self.eval_fator()
        while self.peek() in ('MULT', 'DIV'):
            op = self.consume()
            right = self.eval_fator()
            if op[0] == 'MULT':
                result *= right
            else:
                if right == 0:
                    raise Exception("Erro semântico: divisão por zero")
                result = result / right
        return result

    def eval_fator(self):
        """FATOR → NUM | ID"""
        tok = self.consume()
        if tok[0] == 'NUM':
            # Tenta int primeiro, depois float
            return int(tok[1]) if '.' not in tok[1] else float(tok[1])
        if tok[0] == 'ID':
            if tok[1] not in variables:
                raise Exception(f"Erro semântico: variável '{tok[1]}' não declarada")
            return variables[tok[1]]
        raise Exception(f"Erro semântico: fator inválido '{tok[1]}'")


# ------------------------------------------------------------------
# Ponto de entrada público (compatível com o main.py original)
# ------------------------------------------------------------------

def interpret(tokens):
    # ── Declaração:  VAR ID EQUAL <expr...>
    if tokens[0][0] == 'VAR':
        name          = tokens[1][1]          # nome da variável
        expr_tokens   = tokens[3:]            # tudo após o '='
        evaluator     = ExprEvaluator(expr_tokens)
        value         = evaluator.eval_expr()

        # Formata: exibe inteiro se o resultado for inteiro
        variables[name] = value
        display = int(value) if isinstance(value, float) and value.is_integer() else value
        # Sem saída aqui — o print só ocorre via print(x)

    # ── Impressão:  PRINT LPAREN ID RPAREN
    elif tokens[0][0] == 'PRINT':
        name = tokens[2][1]
        if name not in variables:
            raise Exception(f"Erro semântico: variável '{name}' não foi declarada")
        value = variables[name]
        display = int(value) if isinstance(value, float) and value.is_integer() else value
        print(display)