# 🧠 Analisador Léxico com AFD — LFA

## Autores

- Pedro Marques Correa Domingues  
- Luiz Guilherme Silva Caride  
- João Matheus Veríssimo Francisco  
- Thiago Galli  
- Lucas Bucci Borges

**Disciplina:** Linguagens Formais, Autômatos e Computabilidade  

---

# 📌 Objetivo

O projeto implementa um **Analisador Léxico baseado em Autômato Finito Determinístico (AFD)**.

O sistema recebe uma entrada textual e identifica tokens da linguagem, como:

- números;
- identificadores;
- operadores;
- palavras-chave;
- parênteses.

O foco principal é demonstrar a aplicação prática de **Linguagens Regulares** e **Autômatos Finitos Determinísticos**.

---

# 🧠 Fundamentação Teórica

A análise léxica consiste em reconhecer padrões regulares na entrada.

Exemplos:

```text
Número:          [0-9]+
Identificador:   [a-zA-Z_][a-zA-Z0-9_]*
```

Esses padrões pertencem às **Linguagens Regulares (Tipo 3)** da Hierarquia de Chomsky, portanto podem ser reconhecidos por um:

# ✅ Autômato Finito Determinístico (AFD)

Não foi necessário utilizar pilha ou gramáticas livres de contexto, pois o projeto trabalha apenas com reconhecimento léxico.

---

# 🔢 Modelagem Formal

O autômato é definido como:

```text
M = (Q, Σ, δ, q0, F)
```

Onde:

```text
Q  = { INICIO, NUM, PALAVRA, OP_SINGLE, EQUAL_SINGLE, PAREN_SINGLE, ERRO }

Σ  = { DIGIT, ALPHA, OP, EQUAL, LPAREN, RPAREN, SPACE }

q0 = INICIO

F  = { NUM, PALAVRA, OP_SINGLE, EQUAL_SINGLE, PAREN_SINGLE }
```

---

# 🔄 Tabela de Transições

| Estado Atual | Entrada | Próximo Estado |
|---|---|---|
| INICIO | DIGIT | NUM |
| INICIO | ALPHA | PALAVRA |
| INICIO | OP | OP_SINGLE |
| NUM | DIGIT | NUM |
| NUM | SPACE | EMIT |
| PALAVRA | ALPHA | PALAVRA |
| PALAVRA | SPACE | EMIT |

---

# 🌳 Diagrama Simplificado

```text
INICIO
 ├── DIGIT ──► NUM
 ├── ALPHA ──► PALAVRA
 ├── OP ────► OP_SINGLE
 ├── = ─────► EQUAL_SINGLE
 └── ( ) ──► PAREN_SINGLE
```

---

# 🧩 Estrutura do Projeto

```text
mini-compiler/
│
├── main.py
├── lexer.py
└── README.md
```

---

# 📄 Arquivos

## `main.py`

- interface do usuário;
- loop principal;
- modo debug;
- exibição de tokens.

## `lexer.py`

- implementação do AFD;
- tabela de transições;
- classificação de caracteres;
- emissão de tokens;
- tratamento de erros léxicos.

---

# 💻 Tokens Reconhecidos

| Token | Exemplo |
|---|---|
| NUM | `123` |
| ID | `variavel` |
| VAR | `var` |
| PRINT | `print` |
| PLUS | `+` |
| MINUS | `-` |
| MULT | `*` |
| DIV | `/` |
| EQUAL | `=` |

---

# ▶️ Execução

## Requisitos

- Python 3.8+

## Rodar o projeto

```bash
python main.py
```

---

# 🔍 Exemplos

## Entrada

```text
>> var x = 10
```

## Saída

```text
('VAR', 'var')
('ID', 'x')
('EQUAL', '=')
('NUM', '10')
```

---

# 🐞 Modo Debug

```text
[INICIO] -- 'v' --> [PALAVRA]
[PALAVRA] -- 'a' --> [PALAVRA]
[PALAVRA] -- 'r' --> [PALAVRA]

TOKEN EMITIDO: ('VAR', 'var')
```

---

# ❌ Tratamento de Erros

## Entrada inválida

```text
>> @
```

## Saída

```text
Erro léxico: '@' não pertence ao alfabeto da linguagem
```

---

# 🧠 Conceitos Aplicados

| Conceito | Aplicação |
|---|---|
| Linguagens Regulares | Reconhecimento léxico |
| AFD | Implementação principal |
| Função δ | Tabela de transições |
| Estados Finais | Emissão de tokens |
| Hierarquia de Chomsky | Linguagens Tipo 3 |