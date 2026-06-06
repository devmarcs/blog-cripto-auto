# Guia de Configuração — Blog Cripto Automático

Automação que pesquisa notícias de criptomoedas e finanças diariamente e publica posts no Blogger usando agno + GPT-4o-mini.

---

## Pré-requisitos

- Python 3.10+
- Conta Google com um blog no [Blogger](https://www.blogger.com)
- Conta na [OpenAI](https://platform.openai.com) com saldo (mínimo ~$1)

---

## Passo 1 — Instalar dependências

```bash
cd blog-cripto
pip install -r requirements.txt
```

---

## Passo 2 — Configurar a Blogger API no Google Cloud

1. Acesse [console.cloud.google.com](https://console.cloud.google.com)
2. Clique em **Selecionar projeto → Novo projeto**
   - Nome: `blog-cripto` (ou qualquer nome)
   - Clique em **Criar**
3. Com o projeto selecionado, vá em **APIs e Serviços → Biblioteca**
4. Busque por **Blogger API v3** e clique em **Ativar**
5. Vá em **APIs e Serviços → Tela de consentimento OAuth**
   - Tipo de usuário: **Externo** → Criar
   - Preencha o nome do app (ex: `blog-cripto`) e seu e-mail
   - Clique em **Salvar e continuar** até o final (pode deixar os campos opcionais em branco)
6. Vá em **APIs e Serviços → Credenciais**
   - Clique em **Criar credenciais → ID do cliente OAuth 2.0**
   - Tipo de aplicativo: **App para computador**
   - Nome: `blog-cripto-local`
   - Clique em **Criar**
7. Clique no botão de **download (⬇)** ao lado da credencial criada
8. Renomeie o arquivo baixado para `credentials.json` e mova para dentro da pasta `blog-cripto/`

---

## Passo 3 — Obter o Blog ID

1. Acesse [blogger.com](https://www.blogger.com) e entre no painel do seu blog
2. Clique em **Configurações**
3. Na URL do navegador você verá algo como:
   ```
   https://www.blogger.com/blog/settings/1234567890123456789
   ```
4. O número longo é o seu **Blog ID** — copie ele

---

## Passo 4 — Criar o arquivo .env

Copie o arquivo de exemplo e preencha com seus dados:

```bash
cp .env.example .env
```

Edite o `.env`:

```env
OPENAI_API_KEY=sk-...          # sua chave da OpenAI
BLOGGER_BLOG_ID=1234567890     # o Blog ID do passo anterior
```

---

## Passo 5 — Autenticar com o Google (apenas uma vez)

```bash
python auth_blogger.py
```

- O navegador abrirá automaticamente
- Faça login com sua conta Google
- Clique em **Permitir**
- Um arquivo `token.json` será criado na pasta — ele renova sozinho, não precisa repetir este passo

---

## Passo 6 — Testar sem publicar

```bash
python main.py --dry-run
```

Isso pesquisa e gera o post mas **não publica**. Útil para verificar se tudo está funcionando.

---

## Passo 7 — Publicar manualmente

```bash
python main.py
```

---

## Passo 8 — Agendar publicação diária (cron)

Para publicar automaticamente todo dia às 8h da manhã:

```bash
crontab -e
```

Adicione a linha abaixo (ajuste o caminho se necessário):

```
0 8 * * * cd "/home/marcelo/Área de trabalho/Projetos/automacoes/blog-cripto" && python main.py >> log.txt 2>&1
```

Para ver os logs de execução:

```bash
cat log.txt
```

---

## Estrutura do projeto

```
blog-cripto/
├── credentials.json   # baixado do Google Cloud (não versionar)
├── token.json         # gerado pelo auth_blogger.py (não versionar)
├── .env               # suas chaves secretas (não versionar)
├── .env.example       # modelo do .env
├── requirements.txt   # dependências Python
├── auth_blogger.py    # autenticação Google (rode uma vez)
├── blog_agent.py      # agente de pesquisa e geração de conteúdo
├── blogger_client.py  # cliente da Blogger API
├── main.py            # ponto de entrada
└── CONFIGURACAO.md    # este arquivo
```

---

## Custo estimado

| Item | Custo |
|------|-------|
| DuckDuckGo (busca) | Grátis |
| GPT-4o-mini por post | ~$0,0015 |
| Blogger API | Grátis |
| **Total por dia** | **~$0,0015** |

Com $3 de saldo na OpenAI, a automação roda por aproximadamente **5 anos** de posts diários.

---

## Solução de problemas

**`credentials.json não encontrado`**
→ Certifique-se de que baixou e renomeou o arquivo corretamente (Passo 2).

**`Token inválido ou expirado`**
→ Delete o `token.json` e rode `python auth_blogger.py` novamente.

**`BLOGGER_BLOG_ID não definido`**
→ Verifique se o arquivo `.env` existe e contém o Blog ID correto.

**`Erro de quota da OpenAI`**
→ Verifique seu saldo em [platform.openai.com/usage](https://platform.openai.com/usage).
