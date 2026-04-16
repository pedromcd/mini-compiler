# 🧠 Mini Compilador — Linguagens Formais e Autômatos

## 👨‍💻 Autores

- Pedro Marques Correa Domingues  
- Luiz Guilherme Silva Caride  
- João Matheus Veríssimo Francisco  
- Thiago Galli  

**Disciplina:** Linguagens Formais, autômatos e computabilidade  

---

## 📌 Descrição do Problema

O projeto implementa um **interpretador de uma linguagem de script minimalista**, capaz de declarar variáveis, realizar operações aritméticas e imprimir resultados. O problema escolhido é o de **reconhecimento e execução de linguagens formais estruturadas**, que é o cenário central de compiladores, interpretadores de configuração, validadores de expressões e DSLs (Domain-Specific Languages).

A escolha desse domínio é diretamente motivada pela disciplina: compiladores são a aplicação mais clássica e direta de Linguagens Formais e Autômatos, onde cada fase do pipeline teórico corresponde a uma fase real de software.

---

## 🎯 Justificativa das Teorias Escolhidas

### Por que Autômato Finito Determinístico (AFD) no Léxico?

O analisador léxico precisa reconhecer **padrões regulares** (números, identificadores, operadores). Linguagens regulares são exatamente o que os AFDs reconhecem. Um AFD é suficiente porque:

- Números são descritos pela expressão regular `[0-9]+`  
- Identificadores são descritos por `[a-zA-Z_][a-zA-Z0-9_]*`  
- Operadores e delimitadores são caracteres únicos fixos  

Nenhum desses padrões exige memória de pilha nem recursão — portanto, um **Autômato Finito** (sem pilha) é a ferramenta teórica correta e suficiente.

### Por que Gramática Livre de Contexto (GLC) no Sintático?

Expressões aritméticas com **precedência de operadores** (`*` e `/` antes de `+` e `-`) não podem ser descritas por uma gramática regular. A hierarquia de não-terminais `EXPR → TERMO → FATOR` é necessária para capturar essa precedência, e essa hierarquia **não é expressável com estados finitos**.

Formalmente, a linguagem das expressões aritméticas balanceadas pertence à classe das linguagens livres de contexto (Tipo 2 na hierarquia de Chomsky), e o reconhecedor natural dessa classe é o **Autômato com Pilha** — que é o que um parser descendente recursivo implementa implicitamente.

---

## 🔢 Modelagem Formal

### 1. AFD do Analisador Léxico

O autômato é definido como:

```
M = (Q, Σ, δ, q0, F)

Q  = { INICIO, NUM, PALAVRA, OP_SINGLE, EQUAL_SINGLE, PAREN_SINGLE, ERRO }
Σ  = { DIGIT, ALPHA, OP, EQUAL, LPAREN, RPAREN, SPACE, INVALID }
q0 = INICIO
F  = { NUM, PALAVRA, OP_SINGLE, EQUAL_SINGLE, PAREN_SINGLE }
```

**Tabela de transições δ (parcial — principais caminhos):**

| Estado atual   | DIGIT      | ALPHA      | OP          | EQUAL          | SPACE  | INVALID |
|----------------|------------|------------|-------------|----------------|--------|---------|
| INICIO         | NUM        | PALAVRA    | OP_SINGLE   | EQUAL_SINGLE   | INICIO | ERRO    |
| NUM            | NUM        | EMIT       | EMIT        | EMIT           | EMIT   | ERRO    |
| PALAVRA        | PALAVRA    | PALAVRA    | EMIT        | EMIT           | EMIT   | ERRO    |
| OP_SINGLE      | EMIT       | EMIT       | EMIT        | EMIT           | EMIT   | EMIT    |
| EQUAL_SINGLE   | EMIT       | EMIT       | EMIT        | EMIT           | EMIT   | EMIT    |

> `EMIT` = emitir o token acumulado e reprocessar o caractere atual a partir de `INICIO`.

**Diagrama de estados (ASCII):**

```
           DIGIT                  ALPHA
  ┌─────────────────┐    ┌──────────────────────┐
  │                 ▼    │                      ▼
  │   ┌─────────────────────────────────────────────────┐
  │   │                   INICIO (q0)                   │
  │   └─────────────────────────────────────────────────┘
  │      │DIGIT     │ALPHA    │OP       │=      │( )
  │      ▼          ▼         ▼         ▼       ▼
  │    [NUM]★    [PALAVRA]★  [OP_S]★  [EQ_S]★ [PAR_S]★
  │      │DIGIT    │ALPHA
  └──────┘         └──────(loop)
  
  ★ = estado de aceitação (emite token ao receber caractere que não pertence ao estado)
```

---

### 2. GLC do Analisador Sintático

A gramática é definida como:

```
G = (V, Σ, P, S)

V = { PROGRAMA, STMT, DECL, PRINT_STMT, EXPR, TERMO, FATOR }
Σ = { var, print, ID, NUM, =, +, -, *, /, (, ) }
S = PROGRAMA
```

**Produções P:**

```
PROGRAMA    → STMT

STMT        → DECL
            | PRINT_STMT

DECL        → var ID = EXPR

PRINT_STMT  → print ( ID )

EXPR        → TERMO
            | EXPR + TERMO
            | EXPR - TERMO

TERMO       → FATOR
            | TERMO * FATOR
            | TERMO / FATOR

FATOR       → NUM
            | ID
```

> A hierarquia `EXPR → TERMO → FATOR` garante que multiplicação e divisão tenham precedência maior que adição e subtração, refletindo as regras padrão da aritmética.

**Exemplo de derivação para `var x = 5 + 3 * 2`:**

```
PROGRAMA
  └─ STMT
       └─ DECL
            ├─ var
            ├─ ID (x)
            ├─ =
            └─ EXPR
                 ├─ TERMO → FATOR → NUM (5)
                 ├─ +
                 └─ TERMO
                      ├─ FATOR → NUM (3)
                      ├─ *
                      └─ FATOR → NUM (2)
```

---

## ⚙️ Funcionalidades

| Recurso | Suportado |
|--------|-----------|
| Declaração de variáveis (`var x = 10`) | ✅ |
| Expressões aritméticas (`+`, `-`, `*`, `/`) | ✅ |
| Variáveis em expressões (`var z = x + y`) | ✅ |
| Precedência de operadores | ✅ |
| Impressão de valores (`print(x)`) | ✅ |
| Tratamento de erros léxicos | ✅ |
| Tratamento de erros sintáticos | ✅ |
| Erros semânticos (variável não declarada, divisão por zero) | ✅ |
| Modo debug (exibe tokens e memória) | ✅ |

---

## 🧩 Estrutura do Projeto

```
mini-compiler/
│
├── main.py          # Loop REPL principal
├── lexer.py         # Analisador léxico (AFD via tabela de transições)
├── parser.py        # Analisador sintático (GLC via parser descendente recursivo)
└── interpreter.py   # Interpretador semântico (avaliação com precedência)
```

---

## 🔍 Como funciona — Pipeline

```
Entrada (string)
      │
      ▼
 ┌─────────┐     tokens      ┌──────────┐    validado    ┌───────────────┐
 │  Léxico │ ─────────────►  │ Sintático│ ─────────────► │ Interpretador │
 │  (AFD)  │                 │  (GLC)   │                │  (Semântico)  │
 └─────────┘                 └──────────┘                └───────────────┘
      │                            │                            │
  Erro léxico               Erro sintático               Erro semântico
  (char inválido)           (estrutura inválida)         (variável não declarada,
                                                          divisão por zero)
```

### Fase 1 — Análise Léxica (AFD)

O `lexer.py` implementa o AFD com uma tabela de transições Python (`TRANSITION_TABLE`). A cada caractere lido, o estado atual e o tipo do caractere determinam o próximo estado. Quando a transição retorna `EMIT`, o lexema acumulado é classificado e emitido como token.

Exemplo:

```
Entrada: "var x = 10 + 3"
Tokens:  [('VAR','var'), ('ID','x'), ('EQUAL','='), ('NUM','10'), ('PLUS','+'), ('NUM','3')]
```

### Fase 2 — Análise Sintática (GLC)

O `parser.py` implementa um **parser descendente recursivo LL(1)**. Cada função corresponde a um não-terminal da gramática:

- `parse_programa()` → `parse_stmt()` → `parse_decl()` ou `parse_print_stmt()`
- `parse_expr()` → `parse_termo()` → `parse_fator()`

### Fase 3 — Interpretação

O `interpreter.py` avalia as expressões respeitando a mesma hierarquia da GLC (EXPR → TERMO → FATOR), sem usar `eval()`. Variáveis já declaradas podem ser usadas em novas expressões.

---

## ▶️ Como executar

### Pré-requisitos

- Python 3.8 ou superior (sem dependências externas)

### Executar

```bash
python main.py
```

---

## 💻 Exemplos de uso

### ✅ Declaração simples

```
>> var x = 10
```

### ✅ Expressão com precedência

```
>> var x = 5 + 3 * 2
>> print(x)
11
```

> `3 * 2` é avaliado primeiro (resultado 6), depois `5 + 6 = 11`.

### ✅ Variáveis em expressões

```
>> var a = 4
>> var b = 6
>> var c = a + b * 2
>> print(c)
16
```

### ✅ Modo debug

```
Modo debug? (s/n): s
>> var x = 10
  [LEX] Tokens: [('VAR', 'var'), ('ID', 'x'), ('EQUAL', '='), ('NUM', '10')]
  [SYN] Estrutura válida
  [SEM] Memória: {'x': 10}
```

### ❌ Erro léxico

```
>> var x = @
  Erro: Erro léxico: '@' não pertence ao alfabeto da linguagem
```

### ❌ Erro sintático

```
>> var = 10
  Erro: Erro sintático: esperado 'ID', encontrado '='
```

### ❌ Erro semântico — variável não declarada

```
>> var z = w + 1
  Erro: Erro semântico: variável 'w' não declarada
```

### ❌ Erro semântico — divisão por zero

```
>> var r = 10 / 0
  Erro: Erro semântico: divisão por zero
```

---

## 🧠 Conceitos Aplicados

| Conceito | Onde | Como |
|---------|------|------|
| AFD (Autômato Finito Determinístico) | `lexer.py` | `TRANSITION_TABLE`: dicionário `(estado, tipo_char) → próximo_estado` |
| GLC (Gramática Livre de Contexto) | `parser.py` | Uma função Python por não-terminal; produções como comentários formais |
| Parser descendente recursivo (LL(1)) | `parser.py` | Cada função consome tokens e chama funções filhas |
| Hierarquia de Chomsky | Projeto inteiro | Léxico = Tipo 3 (regular); Sintático = Tipo 2 (livre de contexto) |
| Tabela de símbolos | `interpreter.py` | Dicionário `variables` com nome → valor |
| Avaliação com precedência | `interpreter.py` | `eval_expr` → `eval_termo` → `eval_fator` (espelha a GLC) |

---

## 🔗 Referências

- SIPSER, Michael. *Introduction to the Theory of Computation*. 3. ed. Cengage, 2012.  
- AHO, Alfred V. et al. *Compilers: Principles, Techniques, and Tools*. 2. ed. Pearson, 2006.  
- HOPCROFT, John E.; ULLMAN, Jeffrey D. *Introduction to Automata Theory, Languages, and Computation*. Pearson, 2006.