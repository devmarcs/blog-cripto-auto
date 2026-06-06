import os
import json
from ddgs import DDGS
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

MODELO = "gpt-4o-mini"


def pesquisar_noticias() -> str:
    """Busca notícias recentes de cripto usando DuckDuckGo diretamente."""
    queries = [
        "Bitcoin preço hoje 2026",
        "Ethereum criptomoedas notícias 2026",
        "mercado cripto altcoins junho 2026",
    ]

    resultados = []
    with DDGS() as ddgs:
        for query in queries:
            try:
                hits = list(ddgs.text(query, max_results=3))
                for h in hits:
                    resultados.append(f"- {h['title']}: {h['body']}")
            except Exception:
                continue

    if not resultados:
        return "Sem notícias disponíveis no momento."

    return "\n".join(resultados)


def gerar_post(noticias: str) -> dict:
    """Usa GPT-4o-mini com response_format JSON para gerar o post estruturado."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""Com base nas notícias abaixo, crie um post completo para um blog de finanças e criptomoedas em português brasileiro.

NOTÍCIAS DO DIA:
{noticias}

REQUISITOS DO POST:
- Ano atual: 2026. Nunca mencione 2024 ou 2025 como presente
- Entre 500 e 600 palavras (seja conciso para economizar tokens)
- Tom informativo, acessível para iniciantes mas interessante para quem já investe
- Use dados e números das notícias pesquisadas
- Estrutura: introdução chamativa, desenvolvimento com subtítulos, conclusão com call-to-action
- Formatação HTML usando: <h2>, <p>, <strong>, <em>, <ul>, <li>
- NÃO use markdown, apenas HTML

Retorne um JSON com exatamente estes campos:
- "title": título atraente para o post (sem HTML)
- "content": corpo completo do post em HTML
- "labels": lista de 3-5 tags relevantes (ex: ["Bitcoin", "Criptomoedas", "Finanças"])"""

    resposta = client.chat.completions.create(
        model=MODELO,
        messages=[
            {
                "role": "system",
                "content": "Você é um escritor especialista em finanças e criptomoedas. Sempre responde com JSON válido.",
            },
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.7,
    )

    return json.loads(resposta.choices[0].message.content)


def gerar_conteudo_post() -> dict:
    """Pipeline completo: pesquisa → geração do post."""
    print("Pesquisando notícias...")
    noticias = pesquisar_noticias()

    print("Gerando post...")
    post = gerar_post(noticias)

    return post
