# Documentação em Português

## 🎓 Contexto

- Este repositório contém a implementação desenvolvida para meu **Trabalho de Conclusão de Curso (TCC)** em Ciência da Computação.
- O objetivo foi **definir uma malha aérea regional e selecionar tipos de aeronaves para uma nova companhia aérea regional com hub em Chapecó (Brasil)** usando um **modelo de Programação Linear Inteira**.

**TCC completo (PDF, em Português):** [`tcc2_leonardo_brancalione.pdf`](tcc2_leonardo_brancalione.pdf)

## 🧩 Visão Geral

- **Linguagem:** Python 3.11
- **Solver:** Gurobi (licença acadêmica)
- **Principais libs:** `gurobipy`, `pandas`, `numpy`, `openpyxl`
- **Entradas:** arquivos `.xlsx` e `.json` (especificações de aeronaves, aeroportos, demanda, tarifas)
- **Saídas:** tabela `.csv` de rotas, fluxos de passageiros e decisões binárias

## 🗂️ Estrutura

<details>
<summary>Clique para expandir</summary>

```bash
.
├── main_project/
│   ├── src/
│   │   ├── consts.py
│   │   ├── optimization.py
│   │   ├── __init__.py
│   │   ├── models/
│   │   │   ├── airplane.py
│   │   │   ├── airport.py
│   │   │   ├── model_vars.py
│   │   │   ├── route.py
│   │   │   └── __init__.py
│   │   └── utils/
│   │       ├── file_utils.py
│   │       ├── print_utils.py
│   │       ├── str_utils.py
│   │       ├── utils.py
│   │       └── __init__.py
│   ├── input/
│   │   ├── 2019.xlsx
│   │   ├── 2024.xlsx
│   │   ├── AerodromosPublicos.json
│   │   └── airplanes.xlsx
│   ├── output/
│   ├── requirements.txt
│   └── main.py
└── .gitignore
```
</details>

## 🚀 Início Rápido

**1. Clone e acesse**
```bash
git clone https://github.com/mactaviish/tcc.git
cd tcc\main_project
```

**2. Configuração do ambiente**
```bash
python -m venv .venv
# Windows:
.venv/Scripts/activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
```

**3. Execute o solver**
```bash
python main.py
```

**4. Veja os resultados**
```bash
cd output
ls
```
