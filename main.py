from lexer import lexer
from parser import parser
from interpreter import interpret

BANNER = """
╔══════════════════════════════════════════════╗
║         Mini Compilador — LFA 2025           ║
║  Linguagens Formais e Autômatos              ║
╚══════════════════════════════════════════════╝
Comandos disponíveis:
  var <id> = <expr>   → declara/atualiza variável
  print(<id>)         → imprime o valor de uma variável
  sair                → encerra o interpretador

Expressões suportam: +  -  *  /  e variáveis já declaradas.
Exemplo: var z = x + y * 2
"""

print(BANNER)

# Configuração do modo debug
while True:
    escolha = input("Modo debug? (s/n): ").strip().lower()
    if escolha == 's':
        DEBUG = True
        break
    elif escolha == 'n':
        DEBUG = False
        break
    else:
        print("Digite apenas 's' ou 'n'.")

print()

# Loop principal REPL
while True:
    try:
        code = input(">> ").strip()

        if not code:
            continue

        if code.lower() == 'sair':
            print("Encerrando...")
            break

        # ── FASE 1: Análise Léxica (AFD) ──────────────────────────
        tokens = lexer(code)
        if DEBUG:
            print(f"  [LEX] Tokens: {tokens}")

        # ── FASE 2: Análise Sintática (GLC) ───────────────────────
        parser(tokens)
        if DEBUG:
            print("  [SYN] Estrutura válida")

        # ── FASE 3: Interpretação (Semântica) ─────────────────────
        interpret(tokens)
        if DEBUG:
            from interpreter import variables
            print(f"  [SEM] Memória: {variables}")

    except Exception as e:
        print(f"  Erro: {e}")