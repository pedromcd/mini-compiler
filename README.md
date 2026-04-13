# 🧠 Mini Compilador com Linguagens Formais e Autômatos

## 📌 Descrição

Este projeto implementa um mini compilador/interprete desenvolvido como trabalho final da disciplina de Linguagens Formais e Autômatos.

O sistema é capaz de:
- Realizar análise léxica (tokenização)
- Validar a estrutura do código (análise sintática)
- Executar comandos simples (interpretação)

---

## 🎯 Objetivo

Aplicar conceitos teóricos da disciplina em um problema prático, utilizando:

- Autômatos Finitos Determinísticos (AFD)
- Gramáticas Livres de Contexto (GLC)
- Interpretação de linguagem

---

## ⚙️ Funcionalidades

✔️ Declaração de variáveis  
✔️ Expressões matemáticas (+, -, *, /)  
✔️ Impressão de valores  
✔️ Tratamento de erros léxicos e sintáticos  
✔️ Modo debug para análise interna  

---

## 🧩 Estrutura do Projeto

```
mini-compiler/
│
├── main.py          # Controle principal
├── lexer.py         # Analisador léxico (AFD)
├── parser.py        # Analisador sintático (GLC)
├── interpreter.py   # Execução semântica
```

---

## 🔍 Como funciona

### 1. Análise Léxica (AFD)
O código de entrada é transformado em tokens.

Exemplo:
```
var x = 10
```

Saída:
```
[('VAR','var'), ('ID','x'), ('EQUAL','='), ('NUM','10')]
```

---

### 2. Análise Sintática (GLC)

Valida se os tokens seguem a gramática da linguagem.

Regras principais:

```
DECL → var ID = EXPR
PRINT → print ( ID )
EXPR → NUM (OP NUM)*
```

---

### 3. Interpretação

Executa o código:

- Armazena variáveis
- Avalia expressões
- Imprime resultados

---

## ▶️ Como executar

### 1. Pré-requisitos
- Python 3 instalado

---

### 2. Executar o projeto

```bash
python main.py
```

---

### 3. Modo debug

Ao iniciar o programa:

```
Modo debug? (s/n):
```

- `s` → mostra tokens e validações  
- `n` → mostra apenas o resultado final  

---
## 💻 Exemplos de uso

### ✔️ Declaração
```
>> var x = 10
```
---
### ✔️ Expressão
```
>> var x = 5 + 3 * 2
```
---
### ✔️ Impressão
```
>> print(x)
11
```
---
### ❌ Erro léxico
```
>> @
Erro léxico: @
```
---
### ❌ Erro sintático
```
>> var = 10
Erro: esperado identificador
```
---

## 🧠 Conceitos aplicados

### 🔹 Autômato Finito Determinístico (AFD)
Implementado no `lexer.py` para reconhecimento de tokens.

---

### 🔹 Gramática Livre de Contexto (GLC)
Implementada no `parser.py` para validação da estrutura da linguagem.

---

### 🔹 Interpretação
Executa o significado do código, simulando um interpretador real.

---

## 👨‍💻 Autor(es)

- Pedro Marques Correa Domingues
- Luiz Guilherme Silva Caride
- João Matheus Veríssimo Francisco
- Thiago Galli

---

## 📚 Disciplina

Linguagens Formais e Autômatos