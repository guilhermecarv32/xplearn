# XP Learn - API

Bem-vindo à API do XP Learn, o backend para uma plataforma de aprendizado gamificada. Esta API é construída com Python e FastAPI, fornecendo uma base robusta para gerenciar alunos, professores, turmas, atividades e elementos de gamificação.

## ✨ Funcionalidades

*   **Autenticação Segura**: Autenticação baseada em JWT para alunos e professores, com hash de senhas usando bcrypt.
*   **Gerenciamento de Usuários**: Endpoints para criar, ler e gerenciar perfis de alunos ([`app/models/aluno.py`](app/models/aluno.py)) e professores ([`app/models/professor.py`](app/models/professor.py)).
*   **Gestão de Turmas**: Crie turmas ([`app/models/turma.py`](app/models/turma.py)), associe professores e adicione alunos.
*   **Atividades e Notas**: Crie atividades ([`app/models/atividade.py`](app/models/atividade.py)) com notas, pontos e datas de entrega.
*   **Gamificação**:
    *   **Badges**: Conceda badges ([`app/models/badge.py`](app/models/badge.py)) aos alunos como recompensa.
    *   **XP e Níveis**: Acompanhe a progressão dos alunos através de pontos de experiência (XP) e níveis.
*   **Avatares**: Permite que os usuários personalizem seus perfis com avatares ([`app/models/avatar.py`](app/models/avatar.py)).

## 🛠️ Tecnologias Utilizadas

*   **Python 3**
*   **FastAPI**: Para a construção da API.
*   **SQLAlchemy**: ORM para interação com o banco de dados.
*   **Pydantic**: Para validação e serialização de dados.
*   **Uvicorn**: Servidor ASGI para rodar a aplicação.
*   **python-jose**: Para geração e validação de tokens JWT.
*   **passlib**: Para hashing de senhas.
*   **MySQL**: Banco de dados relacional.

## 🚀 Como Começar

Siga estas instruções para configurar e executar o projeto em seu ambiente local.

### Pré-requisitos

*   Python 3.8 ou superior
*   Um servidor de banco de dados MySQL em execução

### Instalação

1.  **Clone o repositório:**
    ```sh
    git clone <URL_DO_SEU_REPOSITORIO>
    cd xplearn-backend
    ```

2.  **Crie e ative um ambiente virtual:**
    ```sh
    python3 -m venv venv # No windows py -3.12 -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
    ```

3.  **Instale as dependências:**
    Crie um arquivo `requirements.txt` com as bibliotecas necessárias e instale-as.
    ```sh
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**
    Copie o arquivo de exemplo `.env.example` para um novo arquivo chamado `.env` e preencha as variáveis com suas credenciais.
    ```sh
    cp .env.example .env
    ```
    Edite o arquivo `.env`:
    ```
    DATABASE_URL=mysql+mysqlconnector://USER:PASSWORD@HOST:PORT/DATABASE_NAME
    SECRET_KEY=SUA_CHAVE_SECRETA_SUPER_SEGURA
    ```

5.  **Execute a aplicação:**
    ```sh
    uvicorn app.main:app --reload
    ```

A API estará disponível em `http://127.0.0.1:8000`. Você pode acessar a documentação interativa em `http://127.0.0.1:8000/docs`.

## 📁 Estrutura do Projeto

```
app/
├── models/      # Modelos de dados SQLAlchemy
├── routers/     # Lógica dos endpoints da API
├── schemas/     # Esquemas Pydantic para validação de dados
├── database.py  # Configuração da conexão com o banco de dados
├── main.py      # Ponto de entrada da aplicação FastAPI
└── security.py  # Funções de segurança e autenticação
```
