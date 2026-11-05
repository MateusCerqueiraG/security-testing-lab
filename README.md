<div align="center">

# 🛡️ security-testing-lab

**Testes de Segurança / Controle de Acesso** &nbsp;·&nbsp; OWASP &nbsp;·&nbsp; IDOR &nbsp;·&nbsp; BOLA &nbsp;·&nbsp; Python

[![Security Tests](https://github.com/MateusCerqueiraG/security-testing-lab/actions/workflows/security.yml/badge.svg)](https://github.com/MateusCerqueiraG/security-testing-lab/actions/workflows/security.yml)
&nbsp;
[![Relatório Allure](https://img.shields.io/badge/📊_Relatório-Allure_ao_vivo-5fd0e6?style=flat&labelColor=103a4e)](https://mateuscerqueirag.github.io/security-testing-lab/)

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-0A9EDC?logo=pytest&logoColor=white)
![OWASP](https://img.shields.io/badge/OWASP-Top_10-000000?logo=owasp&logoColor=white)

</div>

---

Suíte de **testes de segurança** focada em **controle de acesso** — a classe de falha mais comum (e mais grave) em APIs. Prova, de forma automatizada, que um usuário **não consegue** ler, alterar ou apagar o que não é dele, nem alcançar áreas de administrador.

> 🎯 **Alvo sob teste:** uma **API própria** (`app/main.py`) com os controles de acesso corretos. O repo sobe o alvo localmente — segurança **só se testa em ambiente autorizado** (nunca num sistema de terceiro sem permissão). As mesmas técnicas se aplicam a labs como o **OWASP Juice Shop**.

## ✅ O que a suíte verifica

| Categoria OWASP | Ataque simulado | Esperado |
|:--|:--|:--|
| **A01** · Broken Access Control (IDOR) | Bob tenta ler a nota da Alice trocando o `id` na URL | **403** (bloqueado) |
| **A01** · BOLA | Bob tenta listar / apagar recurso da Alice | **403** / não aparece |
| **A01** · Escalonamento de privilégio | Usuário comum tenta acessar `/admin` | **403** |
| **A07** · Falha de autenticação | Requisição sem token / token inválido | **401** |
| **A05** · Misconfiguration | Resposta sem cabeçalhos de segurança | headers presentes |

<div align="center">

**9 testes &nbsp;·&nbsp; 5 categorias OWASP &nbsp;·&nbsp; 100% verde (controles seguram)**

</div>

## 🧰 Stack & práticas

- 🕵️ **Testes de abuso** — cada teste encena um atacante (Bob) tentando burlar o controle de acesso de outro usuário (Alice)
- 🔒 **Defesas no alvo** — ownership check (anti-IDOR/BOLA), role check (anti escalonamento), auth em toda rota protegida, headers de segurança
- 🗂️ **Mapeado ao OWASP** — cada arquivo de teste referencia a categoria (A01 / A05 / A07)
- ⚙️ **CI** — GitHub Actions sobe a API, roda a suíte e publica o relatório **Allure**

## 📁 Estrutura

```
app/main.py                      # API-alvo com os controles de acesso
tests/
├── test_authentication.py       # A07 — sem token / token inválido
├── test_idor.py                 # A01 — ler nota alheia pelo id
├── test_bola.py                 # A01 — listar / apagar recurso alheio
├── test_privilege_escalation.py # A01 — usuário comum na área de admin
└── test_security_headers.py     # A05 — cabeçalhos de segurança
.github/workflows/security.yml
```

## ▶️ Como rodar localmente

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 1) sobe a API-alvo
uvicorn app.main:app --port 8000
# 2) em outro terminal:
pytest
```

## 📊 Relatório Allure

### 👉 **[mateuscerqueirag.github.io/security-testing-lab](https://mateuscerqueirag.github.io/security-testing-lab/)**

---

<div align="center">
<sub>Projeto de portfólio · foco em testes de controle de acesso (OWASP) · alvo próprio e autorizado</sub>
</div>
