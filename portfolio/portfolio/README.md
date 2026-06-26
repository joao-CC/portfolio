# Portfólio Acadêmico + Microsserviço de Notificação

Este repositório contém o **Portfólio do Aluno** (Django, porta **8000**), com:

- Páginas em **Templates** (Início, Projetos, Contato)
- **API REST** (DRF + JWT) para editar o perfil sem precisar passar pelo admin
- Um **sino de notificações** no menu, que consome um **microsserviço externo**

O microsserviço de notificação é um **projeto Django separado** (porta **8001**),
em **outro repositório**. Os dois precisam estar rodando ao mesmo tempo para o
sino funcionar.

> Repositório do microsserviço: `COLOQUE_AQUI_O_LINK_DO_SEU_REPO_NOTIFICACAO_MS`

---

## Pré-requisitos

- Python 3.10+ instalado (`python3 --version`)
- Git instalado
- Dois terminais abertos (um para cada projeto)

---

## Estrutura esperada ao final

Os dois projetos são independentes, mas para facilitar, organize-os como
pastas irmãs:

```
Projetos/
├── portfolio/            ← este repositório (porta 8000)
└── notificacao_ms/        ← repositório do microsserviço (porta 8001)
```

---

# PARTE 1 — Rodando o Portfólio (porta 8000)

## 1.1 Clonar o repositório

```bash
cd ~/Projetos
git clone COLOQUE_AQUI_O_LINK_DO_SEU_REPO_PORTFOLIO portfolio
cd portfolio
```

## 1.2 Criar e ativar o ambiente virtual

```bash
python3 -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows (cmd)
venv\Scripts\activate.bat

# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

## 1.3 Instalar as dependências

```bash
pip install -r requirements.txt
```

## 1.4 Aplicar as migrações

```bash
python manage.py migrate
```

## 1.5 Criar um superusuário

```bash
python manage.py createsuperuser
```

Siga as instruções (username, e-mail, senha). Vamos usar esse usuário para
logar e testar o "Editar Perfil" e o sino de notificações.

## 1.6 Subir o servidor

```bash
python manage.py runserver
```

Acesse: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

> Nesse momento o site já carrega, mas o **sino vai aparecer cinza com "X"**
> (sem conexão), porque o microsserviço (Parte 2) ainda não está rodando, e
> ainda **não tem perfil cadastrado**. Isso é esperado — vamos configurar tudo
> nos próximos passos.

**Deixe esse terminal aberto e rodando.** Abra um **segundo terminal** para a Parte 2.

---

# PARTE 2 — Rodando o Microsserviço de Notificação (porta 8001)

## 2.1 Clonar o repositório (em outra pasta, fora do portfolio)

```bash
cd ~/Projetos
git clone COLOQUE_AQUI_O_LINK_DO_SEU_REPO_NOTIFICACAO_MS notificacao_ms
cd notificacao_ms
```

## 2.2 Criar e ativar o ambiente virtual

```bash
python3 -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows (cmd)
venv\Scripts\activate.bat
```

## 2.3 Instalar as dependências

```bash
pip install -r requirements.txt
```

## 2.4 Aplicar as migrações

```bash
python manage.py migrate
```

## 2.5 Criar um superusuário (do microsserviço — é um banco separado, então é outro usuário)

```bash
python manage.py createsuperuser
```

## 2.6 Subir o servidor na porta 8001

```bash
python manage.py runserver 8001
```

**Deixe esse terminal também aberto e rodando.**

## 2.7 Criar a Empresa "Portfolio" no admin do microsserviço

1. Acesse [http://127.0.0.1:8001/admin/](http://127.0.0.1:8001/admin/) e faça login
   com o superusuário criado no passo 2.5.
2. Em **Notificacoes → Empresas**, clique em **Add Empresa**.
3. Em "Nome", coloque algo como `Portfolio UAST` e salve.
4. O campo **hash** é gerado automaticamente. **Copie esse hash** (16 caracteres) —
   ele é a "senha" que o portfolio vai usar para falar com o microsserviço.

---

# PARTE 3 — Ligando os dois projetos

## 3.1 Configurar o hash da Empresa no portfolio

No projeto **portfolio**, abra `site_repertorio/settings.py` e procure por:

```python
NOTIFICACAO_MS_API_KEY = 'COLOQUE_AQUI_O_HASH_DA_EMPRESA'
```

Substitua pelo hash copiado no passo 2.7:

```python
NOTIFICACAO_MS_API_KEY = 'a1b2c3d4e5f6a7b8'  # exemplo — use o seu hash real
```

Salve o arquivo. Como o `runserver` do portfolio recarrega automaticamente,
não precisa reiniciar nada.

## 3.2 Descobrir o ID do seu usuário no portfolio

No terminal do **portfolio** (com o venv ativado), rode:

```bash
python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.get(username='SEU_USERNAME').id)"
```

Anote esse número (vamos chamar de `SEU_USER_ID`).

## 3.3 Criar um Target e algumas Notificações de teste

No admin do **microsserviço** ([http://127.0.0.1:8001/admin/](http://127.0.0.1:8001/admin/)):

1. Em **Notificacoes → Targets**, clique em **Add Target**.
2. Selecione a empresa `Portfolio UAST` e em `user_id` coloque o `SEU_USER_ID` do passo 3.2.
3. Salve.
4. Em **Notificacoes → Notificacoes**, crie 2 ou 3 notificações de teste, selecionando esse
   Target, com `is_read` desmarcado.

> Alternativa: você pode criar notificações **pela API** com curl, simulando um
> terceiro sistema enviando avisos (substitua `SEU_HASH` e `SEU_USER_ID`):
>
> ```bash
> curl -X POST http://127.0.0.1:8001/api/notificacoes/criar/ \
>      -H "X-Api-Key: SEU_HASH" \
>      -H "Content-Type: application/json" \
>      -d '{"user_id": SEU_USER_ID, "mensagem": "Bem-vindo ao sistema de notificacoes!"}'
> ```

---

# PARTE 4 — Testando tudo junto

Com os **dois servidores rodando** (porta 8000 e porta 8001):

## 4.1 Testar o sino de notificações

1. Acesse [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) e faça login
   com o superusuário do **portfolio** (passo 1.5). Isso cria a sessão logada.
2. Volte para [http://127.0.0.1:8000/](http://127.0.0.1:8000/). O **sino** deve
   aparecer no menu, no canto direito, com o número de notificações não lidas
   (criadas no passo 3.3).
3. Clique no sino: deve abrir um dropdown com a lista de notificações.
4. Clique em uma notificação não lida: ela deve perder o destaque azul e a
   contagem do sino deve diminuir.
5. Crie uma nova notificação pelo admin do microsserviço (ou via curl, como no
   passo 3.3). Em até **5 segundos**, o número do sino deve atualizar
   sozinho (sem recarregar a página) — isso é o polling.
6. Pare o servidor do microsserviço (`Ctrl+C` no terminal da Parte 2). Em até
   5 segundos, o badge do sino deve virar **X** cinza (sem conexão). Suba o
   servidor de novo (`python manage.py runserver 8001`) e o número volta a
   aparecer.

## 4.2 Testar a edição do perfil via API (Exercício 1)

1. Ainda logado, acesse a home do portfolio.
2. Se ainda não existir um perfil, a página vai mostrar "Perfil não cadastrado" —
   isso é normal, o formulário de edição cria o perfil automaticamente na
   primeira vez que você salva.
3. Clique em **"Editar Perfil"**.
4. Um modal de login vai aparecer (é a autenticação via JWT, diferente da
   sessão do admin). Entre com o mesmo usuário/senha do passo 1.5.
5. O formulário deve abrir preenchido com os dados atuais (vazios na primeira vez).
6. Preencha nome, descrição, curso, período, e-mail, GitHub, LinkedIn e a URL
   de uma imagem, depois clique em **Salvar**.
7. A mensagem "Perfil atualizado!" deve aparecer, e a página recarrega
   sozinha mostrando os dados novos.

## 4.3 Testar a API por curl (opcional, mais rápido para depurar)

```bash
# 1. Obter token JWT
curl -X POST http://127.0.0.1:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "SEU_USERNAME", "password": "SUA_SENHA"}'

# 2. Usar o "access" retornado acima
TOKEN="cole_o_access_token_aqui"

# 3. Ver o perfil
curl http://127.0.0.1:8000/api/perfil/ -H "Authorization: Bearer $TOKEN"

# 4. Atualizar parcialmente
curl -X PATCH http://127.0.0.1:8000/api/perfil/ \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"nome": "Meu Nome Atualizado", "periodo": "6"}'
```

---

## Resolução de problemas comuns

| Sintoma | Causa provável |
|---|---|
| Sino sempre com **X** cinza | Microsserviço (porta 8001) não está rodando, ou o `NOTIFICACAO_MS_API_KEY` no `settings.py` do portfolio está errado/com o placeholder |
| Sino não aparece no menu | Você não está logado no portfolio (`user.is_authenticated` precisa ser `True` — faça login em `/admin/`) |
| `401`/`403` ao chamar `/api/perfil/` | Token JWT expirado ou ausente — faça login de novo pelo botão "Editar Perfil" |
| `403` ao chamar a API do microsserviço | Header `X-Api-Key` ausente ou hash incorreto |
| Erro de CORS no console do navegador | Confirme que `django-cors-headers` está instalado e que `CORS_ALLOWED_ORIGINS` no `settings.py` do microsserviço inclui `http://127.0.0.1:8000` |
| `ModuleNotFoundError` ao rodar `manage.py` | Esqueceu de ativar o `venv` antes de rodar o comando, ou esqueceu o `pip install -r requirements.txt` |

---

## Resumo dos endpoints

### Portfólio (porta 8000)

| Endpoint | Método | Auth | Descrição |
|---|---|---|---|
| `/` | GET | — | Página inicial |
| `/projetos/` | GET | — | Lista de projetos |
| `/contato/` | GET | — | Página de contato |
| `/api/token/` | POST | — | Login (retorna JWT) |
| `/api/perfil/` | GET/PUT/PATCH | JWT | Ver/editar o perfil do usuário logado |

### Microsserviço de Notificação (porta 8001)

| Endpoint | Método | Auth | Descrição |
|---|---|---|---|
| `/api/notificacoes/nao-lidas/` | GET | `X-Api-Key` + `X-User-Id` | Conta notificações não lidas |
| `/api/notificacoes/` | GET | `X-Api-Key` + `X-User-Id` | Lista notificações (aceita `?is_read=true/false`) |
| `/api/notificacoes/<id>/lida/` | PATCH | `X-Api-Key` + `X-User-Id` | Marca uma notificação como lida |
| `/api/notificacoes/criar/` | POST | `X-Api-Key` | Cria notificação (usado por outros sistemas) |
