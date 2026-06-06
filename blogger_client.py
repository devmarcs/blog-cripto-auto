import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
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
