import os
import json
from datetime import date
from ddgs import DDGS
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

MODELO = "gpt-4o-mini"

TEMAS = [
    {
        "nome": "Bitcoin - análise de preço e mercado",
        "queries": [
            "Bitcoin preço hoje análise",
            "BTC valorização tendência mercado",
            "Bitcoin análise técnica resistência suporte",
        ],
    },
    {
        "nome": "Ethereum - atualizações e staking",
        "queries": [
            "Ethereum atualização novidades",
            "ETH staking rendimento validadores",
            "Ethereum layer 2 taxas escalabilidade",
        ],
    },
    {
        "nome": "DeFi - finanças descentralizadas",
        "queries": [
            "DeFi finanças descentralizadas tendências",
            "yield farming liquidez protocolos DeFi",
            "melhores plataformas DeFi rendimento",
        ],
    },
    {
        "nome": "Altcoins em destaque",
        "queries": [
            "altcoins em alta mercado cripto",
            "melhores criptomoedas para investir",
            "altseason tokens emergentes",
        ],
    },
    {
        "nome": "Regulamentação cripto no Brasil e no mundo",
        "queries": [
            "regulamentação criptomoedas Brasil",
            "legislação cripto governo SEC aprovação",
            "bitcoin impostos leis regulação",
        ],
    },
    {
        "nome": "Staking e renda passiva com cripto",
        "queries": [
            "staking criptomoedas rendimento passivo",
            "melhores criptos para staking yield",
            "como fazer staking Ethereum Cardano Solana",
        ],
    },
    {
        "nome": "Segurança: hacks, golpes e como se proteger",
        "queries": [
            "hacks golpes criptomoedas exchange",
            "roubo cripto phishing segurança",
            "como proteger carteira Bitcoin hardware wallet",
        ],
    },
    {
        "nome": "Solana - ecossistema e desempenho",
        "queries": [
            "Solana SOL notícias preço",
            "Solana DeFi NFT aplicações ecossistema",
            "Solana velocidade taxas comparação Ethereum",
        ],
    },
    {
        "nome": "Bitcoin ETF e investidores institucionais",
        "queries": [
            "Bitcoin ETF fluxo investidores institucionais",
            "empresas comprando Bitcoin reserva corporativa",
            "fundos hedge Bitcoin Wall Street",
        ],
    },
    {
        "nome": "Stablecoins e dólar digital",
        "queries": [
            "stablecoins USDT USDC mercado",
            "stablecoin regulamentação reservas laudo",
            "CBDC moeda digital banco central",
        ],
    },
    {
        "nome": "Cripto e tributação no Brasil",
        "queries": [
            "imposto renda criptomoedas Brasil Receita Federal",
            "como declarar bitcoin ganho capital",
            "tributação cripto regras obrigações",
        ],
    },
    {
        "nome": "Web3 e o futuro da internet",
        "queries": [
            "Web3 internet descentralizada aplicações",
            "dApps Web3 casos de uso",
            "identidade digital blockchain Web3",
        ],
    },
    {
        "nome": "Adoção cripto por empresas e países",
        "queries": [
            "empresas adotando bitcoin pagamento",
            "países legalizando criptomoedas moeda oficial",
            "adoção cripto varejo comércio",
        ],
    },
    {
        "nome": "Carteiras cripto: como guardar com segurança",
        "queries": [
            "carteira hardware cripto Ledger Trezor",
            "cold wallet hot wallet diferença segurança",
            "melhor carteira criptomoeda iniciantes",
        ],
    },
    {
        "nome": "Mineração de Bitcoin e energia",
        "queries": [
            "mineração Bitcoin energia renovável rentabilidade",
            "mineradores Bitcoin hashrate dificuldade",
            "mineração cripto consumo energia sustentabilidade",
        ],
    },
    {
        "nome": "Exchanges: mercado e comparação",
        "queries": [
            "Binance Coinbase Kraken notícias exchange",
            "exchange criptomoedas volume taxa",
            "melhores exchanges para comprar cripto Brasil",
        ],
    },
    {
        "nome": "Ripple XRP e pagamentos internacionais",
        "queries": [
            "Ripple XRP notícias parceria bancos",
            "XRP pagamentos internacionais remessas",
            "XRP preço análise regulação",
        ],
    },
    {
        "nome": "GameFi e play-to-earn",
        "queries": [
            "GameFi play-to-earn jogos blockchain",
            "jogos NFT ganhar criptomoeda",
            "melhores jogos cripto blockchain",
        ],
    },
    {
        "nome": "Cardano - contratos inteligentes e desenvolvimento",
        "queries": [
            "Cardano ADA atualização desenvolvimento",
            "Cardano contratos inteligentes DeFi ecossistema",
            "ADA preço análise adoção",
        ],
    },
    {
        "nome": "Bitcoin como reserva de valor e inflação",
        "queries": [
            "Bitcoin reserva de valor inflação proteção",
            "Bitcoin ouro digital economia",
            "macro economia Bitcoin ciclo halving",
        ],
    },
    {
        "nome": "Layer 2 e escalabilidade blockchain",
        "queries": [
            "layer 2 Ethereum Arbitrum Optimism Polygon",
            "soluções escalabilidade blockchain transações baratas",
            "Lightning Network Bitcoin micropagamentos",
        ],
    },
    {
        "nome": "Avalanche e blockchains de alta performance",
        "queries": [
            "Avalanche AVAX notícias ecossistema",
            "blockchains rápidas baixo custo EVM compatível",
            "AVAX DeFi NFT subnet",
        ],
    },
    {
        "nome": "DAOs e governança descentralizada",
        "queries": [
            "DAO governança descentralizada votação",
            "tokens governança protocolo",
            "maiores DAOs cripto projetos",
        ],
    },
    {
        "nome": "Cripto e inteligência artificial",
        "queries": [
            "criptomoedas inteligência artificial IA tokens",
            "projetos cripto IA blockchain",
            "agentes IA Web3 descentralizado",
        ],
    },
    {
        "nome": "Bitcoin halving e ciclos de mercado",
        "queries": [
            "Bitcoin halving impacto histórico preço",
            "bull market bear market cripto ciclo",
            "pós-halving altseason análise",
        ],
    },
    {
        "nome": "NFTs: mercado e casos de uso",
        "queries": [
            "NFT mercado volume notícias",
            "NFT arte digital coleções tokens",
            "NFT utilidade jogos música ingressos",
        ],
    },
    {
        "nome": "Polkadot e interoperabilidade entre blockchains",
        "queries": [
            "Polkadot DOT parachain interoperabilidade",
            "bridge blockchain cross-chain transferência",
            "DOT ecossistema projetos",
        ],
    },
    {
        "nome": "Cripto para iniciantes: primeiros passos",
        "queries": [
            "como comprar bitcoin iniciantes passo a passo",
            "primeiros passos criptomoedas investimento seguro",
            "guia cripto iniciante carteira exchange Brasil",
        ],
    },
    {
        "nome": "Cripto e bancos: o futuro das finanças",
        "queries": [
            "bancos criptomoedas integração serviços",
            "banco digital crypto custodia",
            "sistema bancário tradicional versus DeFi",
        ],
    },
    {
        "nome": "Análise de mercado: capitalização e dominância",
        "queries": [
            "capitalização total mercado cripto dominância",
            "Bitcoin dominância altcoins distribuição",
            "análise mercado cripto semana",
        ],
    },
    {
        "nome": "Bolsa de valores - Ibovespa e mercado brasileiro",
        "queries": [
            "Ibovespa hoje análise fechamento",
            "bolsa de valores Brasil B3 tendência",
            "Ibovespa alta baixa investidores",
        ],
    },
    {
        "nome": "Ações brasileiras - análise e recomendações",
        "queries": [
            "melhores ações para investir Brasil",
            "ações B3 dividendos recomendação analistas",
            "blue chips Brasil análise fundamentalista",
        ],
    },
    {
        "nome": "Ações internacionais e mercado americano",
        "queries": [
            "Wall Street S&P 500 Nasdaq hoje",
            "melhores ações americanas para investir",
            "mercado americano bolsa Nova York tendência",
        ],
    },
    {
        "nome": "Fundos Imobiliários (FIIs) - renda passiva",
        "queries": [
            "fundos imobiliários FIIs melhores",
            "FII dividendos rendimento mensal",
            "fundos imobiliários tijolo papel comparação",
        ],
    },
    {
        "nome": "Dividendos: ações e FIIs pagadores de renda",
        "queries": [
            "ações pagadoras de dividendos Brasil",
            "FIIs e ações dividend yield comparação",
            "carteira de dividendos renda passiva",
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


def gerar_conteudo_post() -> dict:
    """Pipeline completo: seleciona tema → pesquisa notícias → gera post."""
    tema = selecionar_tema()

    print("Pesquisando notícias...")
    noticias = pesquisar_noticias(tema)

    print("Gerando post...")
    post = gerar_post(noticias, tema)

    return post
