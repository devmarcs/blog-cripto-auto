import os
from datetime import datetime, timezone
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/blogger"]
TOKEN_FILE = "token.json"
CREDENTIALS_FILE = "credentials.json"


def _obter_credenciais():
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(TOKEN_FILE, "w") as f:
                f.write(creds.to_json())
        else:
            raise RuntimeError(
                "Token inválido ou expirado. Execute auth_blogger.py primeiro."
            )

    return creds


def post_ja_publicado_hoje() -> bool:
    """Verifica se já existe um post publicado hoje no Blogger."""
    blog_id = os.getenv("BLOGGER_BLOG_ID")
    if not blog_id:
        raise ValueError("BLOGGER_BLOG_ID não definido no .env")

    creds = _obter_credenciais()
    service = build("blogger", "v3", credentials=creds)

    hoje = datetime.now(timezone.utc).date()
    inicio = f"{hoje.isoformat()}T00:00:00Z"
    fim = f"{hoje.isoformat()}T23:59:59Z"

    resultado = service.posts().list(
        blogId=blog_id,
        startDate=inicio,
        endDate=fim,
        maxResults=1,
    ).execute()

    return len(resultado.get("items", [])) > 0


def publicar_post(titulo: str, conteudo_html: str, labels: list = None) -> str:
    """Publica um post no Blogger e retorna a URL do post."""
    blog_id = os.getenv("BLOGGER_BLOG_ID")
    if not blog_id:
        raise ValueError("BLOGGER_BLOG_ID não definido no .env")

    creds = _obter_credenciais()
    service = build("blogger", "v3", credentials=creds)

    corpo = {
        "kind": "blogger#post",
        "title": titulo,
        "content": conteudo_html,
    }

    if labels:
        corpo["labels"] = labels

    post = service.posts().insert(blogId=blog_id, body=corpo, isDraft=False).execute()

    return post.get("url", "URL não disponível")
