# **Desenvolvendo sua Primeira API com FastAPI, Python e Docker**

Este repositório contém a resolução do desafio prático "Desenvolvendo sua Primeira API com FastAPI, Python e Docker" da plataforma **DIO (Digital Innovation One)**. O projeto consiste na criação de uma API RESTful completa para uma academia, permitindo o registo e a consulta de atletas, categorias e centros de treinamento.

O objetivo principal foi aplicar os conceitos aprendidos durante o curso, construindo uma aplicação robusta, desde a configuração do ambiente até à implementação dos endpoints, passando pela interação com a base de dados e a gestão de migrações.

## **A Jornada de Desenvolvimento: Desafios e Soluções**

A construção deste projeto foi um processo de aprendizagem intenso e realista, que envolveu a superação de diversos desafios de configuração e depuração. Esta seção documenta os principais obstáculos encontrados e as soluções aplicadas, refletindo o trabalho real de um desenvolvedor de software.

### **1\. Configuração do Ambiente de Desenvolvimento**

* **Desafio:** A configuração inicial do ambiente em Windows apresentou vários desafios, desde a instalação de ferramentas como pyenv e make, que não são nativas do sistema, até conflitos com a versão do Python instalada através da Microsoft Store.  
* **Solução Implementada:**  
  * **Python:** Foi realizada uma instalação limpa do Python diretamente do site oficial (python.org), eliminando os conflitos causados pela versão da Microsoft Store.  
  * **Ferramentas:** O make foi instalado utilizando o gerenciador de pacotes nativo do Windows, winget, com o comando winget install GnuWin32.Make.  
  * **Makefile:** Os comandos no Makefile foram ajustados para serem compatíveis com o PowerShell do Windows, removendo a sintaxe PYTHONPATH=. (específica de Linux/macOS) e garantindo que a indentação usasse o caractere TAB em vez de espaços.

### **2\. Migrações com Alembic**

* **Desafio:** O Alembic inicialmente não conseguia encontrar os módulos da aplicação (ex: workout\_api), resultando num ModuleNotFoundError. Posteriormente, ocorreram erros de NoReferencedTableError ao tentar criar as relações entre as tabelas.  
* **Solução Implementada:**  
  * Foi adicionado um código ao topo do ficheiro alembic/env.py para incluir o diretório raiz do projeto no sys.path, permitindo que o Alembic "enxergasse" todos os pacotes.  
  * O erro de referência de tabela foi resolvido garantindo que todos os modelos do SQLAlchemy fossem importados no env.py antes de o target\_metadata ser definido. Isto assegurou que o Alembic conhecia todas as tabelas antes de tentar criar as chaves estrangeiras.

### **3\. Lógica de Criação de Atletas (POST)**

* **Desafio:** O endpoint POST /atletas/ retornava um erro genérico 500 Internal Server Error, escondido por um bloco try...except Exception. Testes com o Postman provaram que o backend estava funcional, apontando para um problema subtil de serialização ou lógica.  
* **Solução Implementada:**  
  * A lógica dentro da função post no atleta/controller.py foi refatorada. Em vez de criar um schema de saída (AtletaOut) e depois um modelo da base de dados, a abordagem foi simplificada:  
    1. O AtletaModel é criado diretamente com os dados de entrada (AtletaIn).  
    2. Os objetos de relacionamento (categoria e centro\_treinamento) são associados diretamente ao modelo.  
    3. Após o commit, o próprio atleta\_model é retornado. O FastAPI encarrega-se da conversão para o AtletaOut (graças à configuração from\_attributes=True no BaseSchema), tornando o código mais limpo e robusto.

### **4\. Tratamento de Erros de Integridade**

* **Desafio:** Ao tentar criar um atleta com dados que violavam uma restrição unique (como um CPF ou nome já existente), a API retornava uma mensagem de erro enganadora, culpando sempre o CPF.  
* **Solução Implementada:**  
  * O bloco except IntegrityError foi aprimorado para inspecionar a mensagem de erro original da base de dados (e.orig). Isto permite que a API retorne uma mensagem de erro específica e correta, diferenciando entre um CPF duplicado e outra violação de integridade, como um nome duplicado.

## **Tecnologias Utilizadas**

* **Framework:** FastAPI  
* **Base de Dados:** PostgreSQL (a correr num container Docker)  
* **ORM:** SQLAlchemy (com suporte asyncio)  
* **Gestão de Migrações:** Alembic  
* **Validação de Dados:** Pydantic  
* **Servidor ASGI:** Uvicorn  
* **Automação:** Make  
* **Ambiente:** Pyenv, Venv  
* **Ferramentas de Teste:** Postman, DBeaver

## 🧠 Desafio Final: Funcionalidades Implementadas

Durante o desenvolvimento, foram implementadas as seguintes funcionalidades específicas do desafio:

### 1. Query Parameters nos Endpoints

- O endpoint `GET /atletas` permite filtrar atletas por `nome` e `cpf` via query string.
- Exemplo: `/atletas?nome=Joao&cpf=12345678900`

### 2. Customização da Resposta

- A resposta do endpoint `GET /atletas` foi ajustada para retornar apenas os campos:
  - `nome`
  - `categoria`
  - `centro_treinamento`
- Isso foi feito utilizando o schema `AtletaListOut`.

### 3. Tratamento de Exceções de Integridade

- O endpoint `POST /atletas` captura exceções do tipo `IntegrityError` (SQLAlchemy).
- Quando um CPF duplicado é enviado, a API retorna:
  - Status code: `303`
  - Mensagem: `"Já existe um atleta cadastrado com esse código: 303"`

### 4. Paginação com fastapi-pagination

- A biblioteca `fastapi-pagination` foi integrada ao projeto.
- O endpoint `GET /atletas` agora suporta paginação com `limit` e `offset`.
- Exemplo de resposta paginada:

```json
{
  "items": [...],
  "total": 42,
  "page": 1,
  "size": 10
}
