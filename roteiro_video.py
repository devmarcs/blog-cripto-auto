"""
Gera roteiros de vídeo para YouTube a partir dos posts publicados no blog.

Uso:
  python roteiro_video.py                    → roteiro do post mais recente (vídeo longo, 16:9)
  python roteiro_video.py --short            → versão Shorts (vertical, até 60s)
  python roteiro_video.py --post 3           → o 3º post mais recente
  python roteiro_video.py --todos 5          → os 5 mais recentes

Os arquivos saem em roteiros/ (Markdown). Cole o conteúdo da seção
"PROMPT PARA O CLAUDE DESIGN" no Claude Design, ou use o roteiro/narração no DaVinci Resolve.
"""
import os
import re
import sys
import json
from html import unescape
from openai import OpenAI
from dotenv import load_dotenv
from blogger_client import listar_posts

load_dotenv()

MODELO = "gpt-4o-mini"
PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "roteiros")

FORMATOS = {
    "longo": {
        "descricao": "vídeo horizontal 16:9, 4 a 6 minutos (cerca de 600 a 800 palavras de narração)",
        "cenas": "6 a 9 cenas",
    },
    "short": {
        "descricao": "vídeo vertical 9:16 para Shorts, no máximo 55 segundos (cerca de 120 a 140 palavras de narração)",
        "cenas": "4 a 6 cenas rápidas",
    },
}


def html_para_texto(html: str) -> str:
    """Remove o rodapé de afiliado/Leia também e as tags, devolvendo texto puro."""
    html = re.split(r'<div style="border:2px solid #f0b90b', html)[0]
    html = re.split(r"<h3>Leia também</h3>", html)[0]
    texto = re.sub(r"</(p|h2|li)>", "\n", html)
    texto = re.sub(r"<[^>]+>", "", texto)
    return unescape(texto).strip()


def gerar_roteiro(post: dict, formato: str) -> dict:
    fmt = FORMATOS[formato]
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""Transforme o post de blog abaixo em um roteiro de vídeo para YouTube em português brasileiro.

FORMATO: {fmt['descricao']}, com {fmt['cenas']}.

POST:
Título: {post['title']}
{html_para_texto(post['content'])}

REGRAS:
- Ano atual: 2026. Nunca trate 2024 ou 2025 como presente
- Gancho forte nos primeiros 3 segundos; fechamento com chamada para inscrição/comentário
- Narração em linguagem falada, frases curtas, sem jargão não explicado
- Use apenas dados presentes no post; não invente números
- Sem promessa de ganho e sem recomendação de investimento; inclua aviso "conteúdo informativo" na última cena
- Cada cena descreve o visual de forma concreta (gráfico, texto animado, ícones, transição), pensando em animação gerada por design e/ou edição no DaVinci Resolve

Retorne JSON com exatamente estes campos:
- "titulo_youtube": título (até 70 caracteres, atrativo, sem clickbait enganoso)
- "descricao_youtube": descrição de 2-3 linhas, com marcador [LINK_DO_POST] e aviso de conteúdo informativo
- "tags": lista de 8-12 tags
- "cenas": lista de objetos com "numero", "duracao_seg", "narracao", "visual", "texto_na_tela"
- "prompt_claude_design": um prompt único e autocontido, em português, para colar no Claude Design, pedindo a criação do vídeo animado completo: formato/proporção, duração, paleta e estilo (fintech/cripto, escuro, destaque dourado #f0b90b), tipografia, e a lista de cenas com narração, visuais, textos na tela e transições"""

    resposta = client.chat.completions.create(
        model=MODELO,
        messages=[
            {
                "role": "system",
                "content": "Você é roteirista de vídeos de finanças e criptomoedas para YouTube. Sempre responde com JSON válido.",
            },
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.7,
    )
    return json.loads(resposta.choices[0].message.content)


def montar_markdown(post: dict, r: dict, formato: str) -> str:
    linhas = [
        f"# {r['titulo_youtube']}",
        "",
        f"- Post de origem: {post['title']} ({post['url']})",
        f"- Formato: {FORMATOS[formato]['descricao']}",
        "",
        "## Descrição do YouTube",
        r["descricao_youtube"].replace("[LINK_DO_POST]", post["url"]),
        "",
        "## Tags",
        ", ".join(r["tags"]),
        "",
        "## Roteiro por cena",
    ]
    for c in r["cenas"]:
        linhas += [
            "",
            f"### Cena {c['numero']} ({c['duracao_seg']}s)",
            f"**Narração:** {c['narracao']}",
            f"**Visual:** {c['visual']}",
            f"**Texto na tela:** {c['texto_na_tela']}",
        ]
    linhas += ["", "## PROMPT PARA O CLAUDE DESIGN", "", r["prompt_claude_design"], ""]
    return "\n".join(linhas)


def slug(texto: str) -> str:
    texto = re.sub(r"[^a-z0-9]+", "-", texto.lower().encode("ascii", "ignore").decode())
    return texto.strip("-")[:60]


def main():
    formato = "short" if "--short" in sys.argv else "longo"

    def arg(nome, padrao):
        return int(sys.argv[sys.argv.index(nome) + 1]) if nome in sys.argv else padrao

    quantidade = arg("--todos", 0)
    posicao = arg("--post", 1)

    posts = listar_posts(max(quantidade, posicao))
    if not posts:
        print("Nenhum post publicado encontrado.")
        return
    alvos = posts[:quantidade] if quantidade else [posts[posicao - 1]]

    os.makedirs(PASTA, exist_ok=True)
    for post in alvos:
        print(f"Gerando roteiro ({formato}): {post['title']}")
        r = gerar_roteiro(post, formato)
        caminho = os.path.join(PASTA, f"{slug(post['title'])}-{formato}.md")
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(montar_markdown(post, r, formato))
        print(f"  salvo em {caminho}")


if __name__ == "__main__":
    main()
