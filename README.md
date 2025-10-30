# 🚗 Sistema de Locadora de Carros (POO)

Projeto em Python que simula o funcionamento de uma locadora de carros, permitindo gerenciar carros, clientes e operações de aluguel/devolução. O sistema inclui exceções personalizadas, controle de disponibilidade e testes automatizados com **pytest**.

---

## 🧾 Sumário
- [Introdução](#introdução)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Uso](#uso)
- [Funcionalidades](#funcionalidades)
- [Testes](#testes)
- [Dependências](#dependências)
- [Contribuição](#contribuição)
- [Licença](#licença)

---

## 🚀 Introdução

Este projeto demonstra conceitos de Programação Orientada a Objetos (POO), exceções personalizadas e testes automatizados em Python aplicados a uma locadora de carros.  
Ele permite cadastrar carros e clientes, realizar locações e devoluções, calcular pagamentos e multas por atraso.

---

## 📁 Estrutura do Projeto

```text
locadora-projeto-oop-py/
├── locadora.py
├── test_locadora.py
├── pyproject.toml
├── uv.lock
├── .gitignore
└── README.md
```

---

## ⚙️ Instalação

1. **Clone este repositório**
   ```powershell
   git clone <url-do-repositorio>
   cd locadora-projeto-oop-py
   ```

2. **Crie e ative o ambiente usando `uv`**
   ```powershell
   # Cria/ativa o ambiente virtual gerenciado por uv
   uv venv
   ```

3. **Sincronize dependências (incluindo dependências de desenvolvimento)**
   ```powershell
   uv sync
   ```

---

## ▶️ Uso

Execute o módulo principal para ver uma simulação básica (o projeto contém um bloco de exemplo em `locadora.py`):

```powershell
uv run locadora.py
```

---

## ✅ Funcionalidades

- Cadastro simples de carros e clientes
- Aluguel de carros com verificação de disponibilidade
- Limite de carros por cliente
- Cálculo de valor total e multa por atraso
- Testes automatizados com pytest

---

## 🧪 Testes

Sincronize dependências (se ainda não fez) e execute os testes:

```powershell
uv sync
uv run pytest
```

---

## 📦 Dependências

As dependências e grupos de dependências (por exemplo, `dev` com `pytest`) estão definidas em `pyproject.toml` e o lockfile em `uv.lock`. Use `uv sync` para instalar tudo conforme especificado.

---

## 👤 Autor

Desenvolvido por Davi Patricio Gimenes

📧 RA: 2401557
