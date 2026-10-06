import os
import json
from datetime import date
from html import escape
from ddgs import DDGS
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

MODELO = "gpt-4o-mini"
AFILIADOS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "afiliados.json")

TEMAS = [
    {
        "nome": "Bitcoin - análise de preço e mercado",
        "palavra_chave": "Bitcoin",
        "afiliado": "binance",
        "queries": [
            "Bitcoin preço hoje análise",
            "BTC valorização tendência mercado",
            "Bitcoin análise técnica resistência suporte",
            "melhor forma de comprar Bitcoin no Brasil",
        ],
    },
    {
        "nome": "Ethereum - atualizações e staking",
        "palavra_chave": "Ethereum",
        "afiliado": "binance",
        "queries": [
            "Ethereum atualização novidades",
            "ETH staking rendimento validadores",
            "Ethereum layer 2 taxas escalabilidade",
            "melhor exchange para fazer staking de Ethereum",
        ],
    },
    {
        "nome": "DeFi - finanças descentralizadas",
        "palavra_chave": "DeFi",
        "afiliado": "binance",
        "queries": [
            "DeFi finanças descentralizadas tendências",
            "yield farming liquidez protocolos DeFi",
            "melhores plataformas DeFi rendimento",
            "como começar no DeFi com segurança iniciantes",
        ],
    },
    {
        "nome": "Altcoins em destaque",
        "palavra_chave": "Altcoins",
        "afiliado": "binance",
        "queries": [
            "altcoins em alta mercado cripto",
            "melhores criptomoedas para investir",
            "altseason tokens emergentes",
            "melhor exchange para comprar altcoins no Brasil",
        ],
    },
    {
        "nome": "Regulamentação cripto no Brasil e no mundo",
        "palavra_chave": "Regulamentação",
        "afiliado": "binance",
        "queries": [
            "regulamentação criptomoedas Brasil",
            "legislação cripto governo SEC aprovação",
            "bitcoin impostos leis regulação",
            "exchanges regulamentadas no Brasil como escolher",
        ],
    },
    {
        "nome": "Staking e renda passiva com cripto",
        "palavra_chave": "Staking",
        "afiliado": "binance",
        "queries": [
            "staking criptomoedas rendimento passivo",
            "melhores criptos para staking yield",
            "como fazer staking Ethereum Cardano Solana",
            "melhor plataforma de staking para iniciantes",
        ],
    },
    {
        "nome": "Segurança: hacks, golpes e como se proteger",
        "palavra_chave": "Segurança",
        "afiliado": "binance",
        "queries": [
            "hacks golpes criptomoedas exchange",
            "roubo cripto phishing segurança",
            "como proteger carteira Bitcoin hardware wallet",
            "como escolher exchange segura para comprar cripto",
        ],
    },
    {
        "nome": "Solana - ecossistema e desempenho",
        "palavra_chave": "Solana",
        "afiliado": "binance",
        "queries": [
            "Solana SOL notícias preço",
            "Solana DeFi NFT aplicações ecossistema",
            "Solana velocidade taxas comparação Ethereum",
            "como comprar Solana no Brasil passo a passo",
        ],
    },
    {
        "nome": "Bitcoin ETF e investidores institucionais",
        "palavra_chave": "ETF",
        "afiliado": "binance",
        "queries": [
            "Bitcoin ETF fluxo investidores institucionais",
            "empresas comprando Bitcoin reserva corporativa",
            "fundos hedge Bitcoin Wall Street",
            "ETF de Bitcoin ou comprar Bitcoin direto qual melhor",
        ],
    },
    {
        "nome": "Stablecoins e dólar digital",
        "palavra_chave": "Stablecoins",
        "afiliado": "binance",
        "queries": [
            "stablecoins USDT USDC mercado",
            "stablecoin regulamentação reservas laudo",
            "CBDC moeda digital banco central",
            "como comprar USDT dólar digital no Brasil",
        ],
    },
    {
        "nome": "Cripto e tributação no Brasil",
        "palavra_chave": "Imposto",
        "afiliado": "binance",
        "queries": [
            "imposto renda criptomoedas Brasil Receita Federal",
            "como declarar bitcoin ganho capital",
            "tributação cripto regras obrigações",
            "como declarar criptomoedas comprada em exchange estrangeira",
        ],
    },
    {
        "nome": "Web3 e o futuro da internet",
        "palavra_chave": "Web3",
        "afiliado": "binance",
        "queries": [
            "Web3 internet descentralizada aplicações",
            "dApps Web3 casos de uso",
            "identidade digital blockchain Web3",
            "como começar a investir em tokens Web3",
        ],
    },
    {
        "nome": "Adoção cripto por empresas e países",
        "palavra_chave": "Adoção",
        "afiliado": "binance",
        "queries": [
            "empresas adotando bitcoin pagamento",
            "países legalizando criptomoedas moeda oficial",
            "adoção cripto varejo comércio",
            "como começar a usar criptomoedas para pagamentos",
        ],
    },
    {
        "nome": "Carteiras cripto: como guardar com segurança",
        "palavra_chave": "Carteiras",
        "afiliado": "binance",
        "queries": [
            "carteira hardware cripto Ledger Trezor",
            "cold wallet hot wallet diferença segurança",
            "melhor carteira criptomoeda iniciantes",
            "melhor carteira cripto para iniciantes exchange ou hardware wallet",
        ],
    },
    {
        "nome": "Mineração de Bitcoin e energia",
        "palavra_chave": "Mineração",
        "afiliado": "binance",
        "queries": [
            "mineração Bitcoin energia renovável rentabilidade",
            "mineradores Bitcoin hashrate dificuldade",
            "mineração cripto consumo energia sustentabilidade",
            "vale mais a pena minerar ou comprar Bitcoin",
        ],
    },
    {
        "nome": "Exchanges: mercado e comparação",
        "palavra_chave": "Exchanges",
        "afiliado": "binance",
        "queries": [
            "Binance Coinbase Kraken notícias exchange",
            "exchange criptomoedas volume taxa",
            "melhores exchanges para comprar cripto Brasil",
            "melhor exchange de criptomoedas para iniciantes no Brasil",
        ],
    },
    {
        "nome": "Ripple XRP e pagamentos internacionais",
        "palavra_chave": "XRP",
        "afiliado": "binance",
        "queries": [
            "Ripple XRP notícias parceria bancos",
            "XRP pagamentos internacionais remessas",
            "XRP preço análise regulação",
            "como comprar XRP no Brasil",
        ],
    },
    {
        "nome": "GameFi e play-to-earn",
        "palavra_chave": "GameFi",
        "afiliado": "binance",
        "queries": [
            "GameFi play-to-earn jogos blockchain",
            "jogos NFT ganhar criptomoeda",
            "melhores jogos cripto blockchain",
            "como comprar tokens de jogos blockchain",
        ],
    },
    {
        "nome": "Cardano - contratos inteligentes e desenvolvimento",
        "palavra_chave": "Cardano",
        "afiliado": "binance",
        "queries": [
            "Cardano ADA atualização desenvolvimento",
            "Cardano contratos inteligentes DeFi ecossistema",
            "ADA preço análise adoção",
            "como comprar e fazer staking de Cardano ADA",
        ],
    },
    {
        "nome": "Bitcoin como reserva de valor e inflação",
        "palavra_chave": "Bitcoin",
        "afiliado": "binance",
        "queries": [
            "Bitcoin reserva de valor inflação proteção",
            "Bitcoin ouro digital economia",
            "macro economia Bitcoin ciclo halving",
            "quanto investir em Bitcoin para proteger da inflação",
        ],
    },
    {
        "nome": "Layer 2 e escalabilidade blockchain",
        "palavra_chave": "Layer 2",
        "afiliado": "binance",
        "queries": [
            "layer 2 Ethereum Arbitrum Optimism Polygon",
            "soluções escalabilidade blockchain transações baratas",
            "Lightning Network Bitcoin micropagamentos",
            "como usar layer 2 para pagar taxas menores",
        ],
    },
    {
        "nome": "Avalanche e blockchains de alta performance",
        "palavra_chave": "Avalanche",
        "afiliado": "binance",
        "queries": [
            "Avalanche AVAX notícias ecossistema",
            "blockchains rápidas baixo custo EVM compatível",
            "AVAX DeFi NFT subnet",
            "como comprar AVAX no Brasil",
        ],
    },
    {
        "nome": "DAOs e governança descentralizada",
        "palavra_chave": "DAO",
        "afiliado": "binance",
        "queries": [
            "DAO governança descentralizada votação",
            "tokens governança protocolo",
            "maiores DAOs cripto projetos",
            "como participar de uma DAO com tokens de governança",
        ],
    },
    {
        "nome": "Cripto e inteligência artificial",
        "palavra_chave": "IA",
        "afiliado": "binance",
        "queries": [
            "criptomoedas inteligência artificial IA tokens",
            "projetos cripto IA blockchain",
            "agentes IA Web3 descentralizado",
            "melhores criptomoedas de inteligência artificial para investir",
        ],
    },
    {
        "nome": "Bitcoin halving e ciclos de mercado",
        "palavra_chave": "Halving",
        "afiliado": "binance",
        "queries": [
            "Bitcoin halving impacto histórico preço",
            "bull market bear market cripto ciclo",
            "pós-halving altseason análise",
            "melhor momento para comprar Bitcoin no ciclo",
        ],
    },
    {
        "nome": "NFTs: mercado e casos de uso",
        "palavra_chave": "NFT",
        "afiliado": "binance",
        "queries": [
            "NFT mercado volume notícias",
            "NFT arte digital coleções tokens",
            "NFT utilidade jogos música ingressos",
            "como comprar NFT com segurança iniciantes",
        ],
    },
    {
        "nome": "Polkadot e interoperabilidade entre blockchains",
        "palavra_chave": "Polkadot",
        "afiliado": "binance",
        "queries": [
            "Polkadot DOT parachain interoperabilidade",
            "bridge blockchain cross-chain transferência",
            "DOT ecossistema projetos",
            "como comprar Polkadot DOT no Brasil",
        ],
    },
    {
        "nome": "Cripto para iniciantes: primeiros passos",
        "palavra_chave": "Iniciantes",
        "afiliado": "binance",
        "queries": [
            "como comprar bitcoin iniciantes passo a passo",
            "primeiros passos criptomoedas investimento seguro",
            "guia cripto iniciante carteira exchange Brasil",
            "melhor exchange para comprar a primeira criptomoeda",
        ],
    },
    {
        "nome": "Cripto e bancos: o futuro das finanças",
        "palavra_chave": "Bancos",
        "afiliado": "binance",
        "queries": [
            "bancos criptomoedas integração serviços",
            "banco digital crypto custodia",
            "sistema bancário tradicional versus DeFi",
            "comprar cripto pelo banco ou pela exchange qual melhor",
        ],
    },
    {
        "nome": "Análise de mercado: capitalização e dominância",
        "palavra_chave": "Mercado",
        "afiliado": "binance",
        "queries": [
            "capitalização total mercado cripto dominância",
            "Bitcoin dominância altcoins distribuição",
            "análise mercado cripto semana",
            "como montar carteira de criptomoedas diversificada",
        ],
    },
    {
        "nome": "Bolsa de valores - Ibovespa e mercado brasileiro",
        "palavra_chave": "Ibovespa",
        "afiliado": None,
        "queries": [
            "Ibovespa hoje análise fechamento",
            "bolsa de valores Brasil B3 tendência",
            "Ibovespa alta baixa investidores",
            "melhor corretora para começar a investir na bolsa",
        ],
    },
    {
        "nome": "Ações brasileiras - análise e recomendações",
        "palavra_chave": "Ações",
        "afiliado": None,
        "queries": [
            "melhores ações para investir Brasil",
            "ações B3 dividendos recomendação analistas",
            "blue chips Brasil análise fundamentalista",
            "como escolher ações para iniciantes",
        ],
    },
    {
        "nome": "Ações internacionais e mercado americano",
        "palavra_chave": "Ações americanas",
        "afiliado": None,
        "queries": [
            "Wall Street S&P 500 Nasdaq hoje",
            "melhores ações americanas para investir",
            "mercado americano bolsa Nova York tendência",
            "melhor forma de investir em ações americanas do Brasil",
        ],
    },
    {
        "nome": "Fundos Imobiliários (FIIs) - renda passiva",
        "palavra_chave": "FIIs",
        "afiliado": None,
        "queries": [
            "fundos imobiliários FIIs melhores",
            "FII dividendos rendimento mensal",
            "fundos imobiliários tijolo papel comparação",
            "melhores FIIs para iniciantes como escolher",
        ],
    },
    {
        "nome": "Dividendos: ações e FIIs pagadores de renda",
        "palavra_chave": "Dividendos",
        "afiliado": None,
        "queries": [
            "ações pagadoras de dividendos Brasil",
            "FIIs e ações dividend yield comparação",
            "carteira de dividendos renda passiva",
            "como montar carteira de dividendos para iniciantes",
        ],
    },
]


def selecionar_tema() -> dict:
    """Seleciona o tema do dia de forma rotativa pelo dia do ano."""
    dia_do_ano = date.today().timetuple().tm_yday
    tema = TEMAS[dia_do_ano % len(TEMAS)]
    print(f"Tema do dia ({dia_do_ano}): {tema['nome']}")
    return tema


def pesquisar_noticias(tema: dict) -> str:
    """Busca notícias recentes do tema usando DuckDuckGo."""
    resultados = []
    with DDGS() as ddgs:
        for query in tema["queries"]:
            try:
                hits = list(ddgs.text(query, max_results=3, timelimit="y"))
                for h in hits:
                    resultados.append(f"- {h['title']}: {h['body']}")
            except Exception:
                continue

    if not resultados:
        return "Sem notícias disponíveis no momento."

    return "\n".join(resultados)


def gerar_post(noticias: str, tema: dict) -> dict:
    """Usa GPT-4o-mini para gerar o post estruturado sobre o tema."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""Com base nas notícias abaixo, crie um post sobre o tema "{tema['nome']}" para um blog de finanças e criptomoedas em português brasileiro.

NOTÍCIAS DO DIA:
{noticias}

REQUISITOS DO POST:
- Ano atual: 2026. Nunca mencione 2024 ou 2025 como presente
- Foco exclusivo no tema: {tema['nome']}
- Entre 500 e 600 palavras
- Tom informativo, acessível para iniciantes mas interessante para quem já investe
- Use dados e números das notícias quando disponíveis
- Estrutura: introdução chamativa, desenvolvimento com subtítulos, conclusão com call-to-action
- Formatação HTML usando: <h2>, <p>, <strong>, <em>, <ul>, <li>
- NÃO use markdown, apenas HTML
- NÃO inclua links nem URLs no texto

Retorne um JSON com exatamente estes campos:
- "title": título atraente e específico para o tema (sem HTML, sem aspas)
- "content": corpo completo do post em HTML
- "labels": lista de 3-5 tags relevantes ao tema (ex: ["Bitcoin", "Análise", "Mercado"])"""

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


def carregar_afiliado(chave: str | None) -> dict | None:
    """Retorna os dados do programa de afiliado do tema, ou None se não houver."""
    if not chave or not os.path.exists(AFILIADOS_FILE):
        return None
    with open(AFILIADOS_FILE, encoding="utf-8") as f:
        return json.load(f).get(chave)


def montar_rodape(afiliado: dict | None, relacionados: list) -> str:
    """Monta o HTML anexado ao fim do post: CTA de afiliado com divulgação e "Leia também"."""
    partes = []

    if afiliado:
        partes.append(
            '<div style="border:2px solid #f0b90b;border-radius:8px;padding:16px;margin:24px 0;">'
            f"<h3>{escape(afiliado['cta_titulo'])}</h3>"
            f"<p>{escape(afiliado['cta_texto'])}</p>"
            f'<p><a href="{escape(afiliado["link"])}" target="_blank" rel="sponsored noopener">'
            f"<strong>{escape(afiliado['cta_botao'])} &rarr;</strong></a></p>"
            '<p style="font-size:0.85em;opacity:0.8;"><em>Divulgação: este post contém link de indicação. '
            "Se você abrir uma conta por ele, o blog pode receber uma comissão, sem custo extra para você. "
            "Este conteúdo é informativo e não constitui recomendação de investimento.</em></p>"
            "</div>"
        )

    if relacionados:
        itens = "".join(
            f'<li><a href="{escape(p["url"])}">{escape(p["title"])}</a></li>' for p in relacionados
        )
        partes.append(f"<h3>Leia também</h3><ul>{itens}</ul>")

    return "".join(partes)


def gerar_conteudo_post(buscar_relacionados=None) -> dict:
    """Pipeline completo: seleciona tema → pesquisa notícias → gera post → anexa rodapé.

    buscar_relacionados: função opcional (termo) -> [{"title", "url"}] para a seção "Leia também".
    """
    tema = selecionar_tema()

    print("Pesquisando notícias...")
    noticias = pesquisar_noticias(tema)

    print("Gerando post...")
    post = gerar_post(noticias, tema)

    chave = tema["palavra_chave"]
    labels = post.get("labels", [])
    if chave not in labels:
        post["labels"] = [chave] + labels

    relacionados = []
    if buscar_relacionados:
        try:
            relacionados = buscar_relacionados(chave)
        except Exception as e:
            print(f"Aviso: falha ao buscar posts relacionados ({e}). Seguindo sem 'Leia também'.")

    afiliado = carregar_afiliado(tema.get("afiliado"))
    post["content"] += montar_rodape(afiliado, relacionados)

    return post
