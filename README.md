# 📘 Gerenciador de Turmas

## 👥 Integrantes do Grupo



Diogo Pereira Almeida - 210126

Gustavo Torres Belini - 200008

João Victor Oliveira Moreira - 211359

João Victor Rosa Tagliarini - 210124

José Antônio Soares Pinto - 210430

Lucas Ribeiro Bonfílio de Lemos - 210442

Matheus Aparecido de Oliveira Ramos - 210388

---

# 📚 Sobre o Projeto

Este projeto implementa um sistema distribuído composto por:

1. **Backend gRPC**
   Responsável pela lógica de negócios e persistência, incluindo:

* CRUD de alunos
* CRUD de professores
* CRUD de matérias
* CRUD de turmas
* Inscrição de aluno em turma
* Filtrar turmas por professor

### 🔹 Regras implementadas:
- Professor pode listar apenas suas matérias.  
- Professor pode criar turmas somente para matérias que ele leciona.  
- Professor pode listar turmas apenas das suas matérias.  
- Aluno pode listar todas as turmas.  
- Aluno pode se inscrever em qualquer turma.

2. **API REST (Flask)**
   Interface que recebe requisições HTTP em JSON do frontend e se comunica com o backend via gRPC.

Oferece endpoints para:

- /students  
- /teachers  
- /subjects  
- /classes  
- /teachers/id/subjects  
- /teachers/id/classes  
- /subjects/id/classes  
- /classes/id/enroll

3. **Módulo de Testes**
   Verifica o funcionamento completo da aplicação simulando o fluxo real:

* criar professor  
* criar duas matérias associadas ao professor  
* listar todas as matérias  
* listar matérias filtradas pelo professor  
* criar aluno  
* criar turma vinculada a uma matéria do professor  
* listar turmas (geral, por professor e por matéria)  
* inscrever aluno na turma  
* validar que a inscrição foi aplicada ao consultar novamente as turmas

---

# 🏗️ Arquitetura da Aplicação

```
FRONTEND (HTTP JSON)
         ↓
Flask API (REST → gRPC)
         ↓
Backend gRPC (CRUD + Banco)
         ↓
      SQLite
```

---

# ▶️ Como Rodar o Projeto

## 1️⃣ Criar e ativar o ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

## 2️⃣ Instalar as dependências

```bash
pip install -r backend/requirements.txt
pip install -r front/requirements.txt
pip install -r test/requirements.txt
```


## 3️⃣ Iniciar o servidor gRPC (backend)

```bash
python backend/grpc_server.py
```

## 4️⃣  Iniciar o servidor Flask (API REST)

(Em outro terminal com o venv ativado)

```bash
python front/api.py
```

## 5️⃣ Rodar os testes automáticos

```bash
python test/test_api.py
```

Se tudo estiver correto, você verá:

```
=== TODOS OS TESTES FINALIZADOS COM SUCESSO ===
```