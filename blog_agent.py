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
            "Bitcoin preço hoje análise 2026",
            "BTC valorização tendência mercado 2026",
            "Bitcoin análise técnica resistência suporte 2026",
        ],
    },
    {
        "nome": "Ethereum - atualizações e staking",
        "queries": [
            "Ethereum atualização novidades 2026",
            "ETH staking rendimento validadores 2026",
            "Ethereum layer 2 taxas escalabilidade 2026",
        ],
    },
    {
        "nome": "DeFi - finanças descentralizadas",
        "queries": [
            "DeFi finanças descentralizadas tendências 2026",
            "yield farming liquidez protocolos DeFi 2026",
            "melhores plataformas DeFi rendimento 2026",
        ],
    },
    {
        "nome": "Altcoins em destaque",
        "queries": [
            "altcoins em alta mercado cripto 2026",
            "melhores criptomoedas para investir 2026",
            "altseason tokens emergentes 2026",
        ],
    },
    {
        "nome": "Regulamentação cripto no Brasil e no mundo",
        "queries": [
            "regulamentação criptomoedas Brasil 2026",
            "legislação cripto governo SEC aprovação 2026",
            "bitcoin impostos leis regulação 2026",
        ],
    },
    {
        "nome": "Staking e renda passiva com cripto",
        "queries": [
            "staking criptomoedas rendimento passivo 2026",
            "melhores criptos para staking yield 2026",
            "como fazer staking Ethereum Cardano Solana 2026",
        ],
    },
    {
        "nome": "Segurança: hacks, golpes e como se proteger",
        "queries": [
            "hacks golpes criptomoedas exchange 2026",
            "roubo cripto phishing segurança 2026",
            "como proteger carteira Bitcoin hardware wallet 2026",
        ],
    },
    {
        "nome": "Solana - ecossistema e desempenho",
        "queries": [
            "Solana SOL notícias preço 2026",
            "Solana DeFi NFT aplicações ecossistema 2026",
            "Solana velocidade taxas comparação Ethereum 2026",
        ],
    },
    {
        "nome": "Bitcoin ETF e investidores institucionais",
        "queries": [
            "Bitcoin ETF fluxo investidores institucionais 2026",
            "empresas comprando Bitcoin reserva corporativa 2026",
            "fundos hedge Bitcoin Wall Street 2026",
        ],
    },
    {
        "nome": "Stablecoins e dólar digital",
        "queries": [
            "stablecoins USDT USDC mercado 2026",
            "stablecoin regulamentação reservas laudo 2026",
            "CBDC moeda digital banco central 2026",
        ],
    },
    {
        "nome": "Cripto e tributação no Brasil",
        "queries": [
            "imposto renda criptomoedas Brasil Receita Federal 2026",
            "como declarar bitcoin ganho capital 2026",
            "tributação cripto regras obrigações 2026",
        ],
    },
    {
        "nome": "Web3 e o futuro da internet",
        "queries": [
            "Web3 internet descentralizada aplicações 2026",
            "dApps Web3 casos de uso 2026",
            "identidade digital blockchain Web3 2026",
        ],
    },
    {
        "nome": "Adoção cripto por empresas e países",
        "queries": [
            "empresas adotando bitcoin pagamento 2026",
            "países legalizando criptomoedas moeda oficial 2026",
            "adoção cripto varejo comércio 2026",
        ],
    },
    {
        "nome": "Carteiras cripto: como guardar com segurança",
        "queries": [
            "carteira hardware cripto Ledger Trezor 2026",
            "cold wallet hot wallet diferença segurança 2026",
            "melhor carteira criptomoeda iniciantes 2026",
        ],
    },
    {
        "nome": "Mineração de Bitcoin e energia",
        "queries": [
            "mineração Bitcoin energia renovável rentabilidade 2026",
            "mineradores Bitcoin hashrate dificuldade 2026",
            "mineração cripto consumo energia sustentabilidade 2026",
        ],
    },
    {
        "nome": "Exchanges: mercado e comparação",
        "queries": [
            "Binance Coinbase Kraken notícias exchange 2026",
            "exchange criptomoedas volume taxa 2026",
            "melhores exchanges para comprar cripto Brasil 2026",
        ],
    },
    {
        "nome": "Ripple XRP e pagamentos internacionais",
        "queries": [
            "Ripple XRP notícias parceria bancos 2026",
            "XRP pagamentos internacionais remessas 2026",
            "XRP preço análise regulação 2026",
        ],
    },
    {
        "nome": "GameFi e play-to-earn",
        "queries": [
            "GameFi play-to-earn jogos blockchain 2026",
            "jogos NFT ganhar criptomoeda 2026",
            "melhores jogos cripto blockchain 2026",
        ],
    },
    {
        "nome": "Cardano - contratos inteligentes e desenvolvimento",
        "queries": [
            "Cardano ADA atualização desenvolvimento 2026",
            "Cardano contratos inteligentes DeFi ecossistema 2026",
            "ADA preço análise adoção 2026",
        ],
    },
    {
        "nome": "Bitcoin como reserva de valor e inflação",
        "queries": [
            "Bitcoin reserva de valor inflação proteção 2026",
            "Bitcoin ouro digital economia 2026",
            "macro economia Bitcoin ciclo halving 2026",
        ],
    },
    {
        "nome": "Layer 2 e escalabilidade blockchain",
        "queries": [
            "layer 2 Ethereum Arbitrum Optimism Polygon 2026",
            "soluções escalabilidade blockchain transações baratas 2026",
            "Lightning Network Bitcoin micropagamentos 2026",
        ],
    },
    {
        "nome": "Avalanche e blockchains de alta performance",
        "queries": [
            "Avalanche AVAX notícias ecossistema 2026",
            "blockchains rápidas baixo custo EVM compatível 2026",
            "AVAX DeFi NFT subnet 2026",
        ],
    },
    {
        "nome": "DAOs e governança descentralizada",
        "queries": [
            "DAO governança descentralizada votação 2026",
            "tokens governança protocolo 2026",
            "maiores DAOs cripto projetos 2026",
        ],
    },
    {
        "nome": "Cripto e inteligência artificial",
        "queries": [
            "criptomoedas inteligência artificial IA tokens 2026",
            "projetos cripto IA blockchain 2026",
            "agentes IA Web3 descentralizado 2026",
        ],
    },
    {
        "nome": "Bitcoin halving e ciclos de mercado",
        "queries": [
            "Bitcoin halving impacto histórico preço 2026",
            "bull market bear market cripto ciclo 2026",
            "pós-halving altseason análise 2026",
        ],
    },
    {
        "nome": "NFTs: mercado e casos de uso",
        "queries": [
            "NFT mercado volume notícias 2026",
            "NFT arte digital coleções tokens 2026",
            "NFT utilidade jogos música ingressos 2026",
        ],
    },
    {
        "nome": "Polkadot e interoperabilidade entre blockchains",
        "queries": [
            "Polkadot DOT parachain interoperabilidade 2026",
            "bridge blockchain cross-chain transferência 2026",
            "DOT ecossistema projetos 2026",
        ],
    },
    {
        "nome": "Cripto para iniciantes: primeiros passos",
        "queries": [
            "como comprar bitcoin iniciantes passo a passo 2026",
            "primeiros passos criptomoedas investimento seguro 2026",
            "guia cripto iniciante carteira exchange Brasil 2026",
        ],
    },
    {
        "nome": "Cripto e bancos: o futuro das finanças",
        "queries": [
            "bancos criptomoedas integração serviços 2026",
            "banco digital crypto custodia 2026",
            "sistema bancário tradicional versus DeFi 2026",
        ],
    },
    {
        "nome": "Análise de mercado: capitalização e dominância",
        "queries": [
            "capitalização total mercado cripto dominância 2026",
            "Bitcoin dominância altcoins distribuição 2026",
            "análise mercado cripto semana 2026",
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
                hits = list(ddgs.text(query, max_results=3))
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
