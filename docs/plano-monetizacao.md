> Documento vivo (com gráfico de projeção e roadmap visual): https://claude.ai/code/artifact/0d10614f-b1e0-4a6a-8084-6546aae99b0d
>
> Esta é uma cópia em texto, salva no repositório para referência e versionamento. Os dois widgets (gráfico de estimativa de receita e roadmap de 90 dias) só são visualizáveis no link acima.

# Plano de Monetização — Blog Cripto

Sep 28, 2026 · @Marcelo Augusto

## Diagnóstico atual

O blog tem tráfego real, mas ainda pequeno demais para gerar renda relevante: 1.266 visualizações este mês, um crescimento de 7,5% sobre o mês anterior (1.178).

| Métrica | Valor |
| --- | --- |
| Postagens publicadas | 173 |
| Visualizações totais (histórico) | 27.461 |
| Visualizações este mês | 1.266 |
| Visualizações mês anterior | 1.178 |
| Crescimento mês a mês | +7,5% |
| Seguidores | 0 |
| Comentários totais | 9 |
| Cadência de publicação | 1 post/dia, rotação automática entre 30 temas (cripto, ações, FIIs) |

Dois sinais importam mais que o volume: zero seguidores e só 9 comentários em 173 posts indicam que o tráfego é quase todo de busca (Google), não de audiência recorrente. O conteúdo é gerado e publicado automaticamente por tema do dia, o que garante consistência de SEO mas ainda não tem estrutura voltada a conversão — não há, hoje, uma seção fixa de comparativos ou recomendações que puxe cliques de afiliado.

Base para as projeções abaixo: crescimento de tráfego e RPM combinado (anúncios + afiliados).

## Estimativa de ganhos

Hoje, com 1.266 visualizações/mês, a receita realista fica entre R$13 e R$89 por mês — dependendo de quanto do tráfego já clica em links de afiliado. Isso não é pouco por falta de qualidade do conteúdo: é porque o volume de tráfego ainda é pequeno para qualquer modelo de monetização.

&#91;embedded content: estimativa própria · RPM combinado R$10 / R$35 / R$70 por 1.000 visualizações · 6 meses\]

Os três cenários assumem crescimento composto de tráfego (5% / 12% / 20% ao mês) e RPM combinado (anúncios + comissões de afiliado) de R$10 / R$35 / R$70 por 1.000 visualizações — faixa típica para blogs de finanças no Brasil, conforme o quanto o conteúdo é escrito para converter (seções 4 a 8 deste plano). São estimativas, não garantias: o fator que mais pesa é o crescimento de tráfego, não o RPM.

## Programas de afiliados recomendados

Os 30 temas do blog já cobrem cripto e ações/FIIs, então os programas certos são os que esses posts já citam naturalmente — exchange, corretora, carteira, curso.

| Programa | Categoria | Comissão típica | Janela de conversão | Por que encaixa |
| --- | --- | --- | --- | --- |
| Binance Affiliate | Exchange cripto | até 50% do fee de trading, recorrente | vitalício na conta vinculada | Cobre Bitcoin, Ethereum, altcoins, staking — mais da metade dos temas |
| Bybit / OKX Affiliate | Exchange cripto | 20–40% do fee de trading | vitalício | Bom para posts de altcoins e derivativos |
| Ledger / Trezor | Hardware wallet | 10–12% por venda | 30 dias | Encaixa direto no tema "carteiras: como guardar com segurança" |
| XP / Rico / Clear (indicação de corretora) | Corretora de ações e FIIs | R$50–150 fixo por conta aberta e ativada | 30–90 dias | Encaixa com os 5 temas de ações, Ibovespa, FIIs e dividendos |
| Cursos de cripto/investimento (Hotmart) | Infoproduto | 30–50% do valor do curso | 30 dias | Converte bem no tema "cripto para iniciantes" |
| Amazon Associates | Livros e hardware | 1–8% | 24h | Ticket baixo, mas fácil de inserir em qualquer post |

Antes de colocar qualquer link no ar: a Lei brasileira (CDC) e as próprias regras dos programas exigem divulgar que o link é de afiliado. Um aviso curto no início ou fim do post ("este post contém links de afiliado") resolve — detalhe no checklist técnico, mais abaixo.

## Estratégia de conteúdo para conversão

O gerador atual roda 30 temas informativos em rotação — ótimo para SEO, mas nenhum formato foi desenhado para vender. Quatro formatos convertem melhor que análise de mercado genérica:

1. **Comparativos** ("Binance vs Bybit: qual exchange escolher em 2026", "XP vs Rico vs Clear para FIIs") — o leitor já está decidindo entre opções, o link de afiliado é a próxima ação natural.
2. **Guias de primeiro passo** ("como comprar Bitcoin pela primeira vez", "como abrir conta em corretora para FIIs") — já existem 2 temas assim na rotação; merecem virar posts fixos, atualizados e linkados no menu, não só posts do dia que somem no feed.
3. **Reviews de produto** (Ledger vs Trezor, melhores corretoras para dividendos) — intenção de compra alta, aceita 2–3 links de afiliado por post sem parecer forçado.
4. **Páginas de recursos fixas** ("Minhas ferramentas", "Onde eu compro cripto") — não dependem do algoritmo do dia, ficam no menu do blog e acumulam clique mês após mês.

Ação concreta: adicionar esses 4 formatos como novos itens da lista `TEMAS` em `blog_agent.py` (ou um gerador separado rodando 1–2x/semana), cada um com CTA e link de afiliado já no prompt de geração. Os 30 temas atuais continuam — eles tra çem tráfego; os novos formatos convertem esse tráfego.

## SEO e crescimento de tráfego

O tráfego é o multiplicador que mais pesa na projeção acima — é o que separa o cenário conservador do otimista, mais do que o RPM. Três frentes, em ordem de impacto:

- **Palavras-chave de cauda longa e intenção de compra.** "melhor exchange para iniciantes no Brasil" traz menos volume que "Bitcoin hoje", mas converte muito mais. Ajustar as `queries` de cada tema em `blog_agent.py` para incluir pelo menos uma versão "melhor X para Y" ou "como escolher X".
- **Link interno entre posts do mesmo tema.** Com 173 posts e 30 temas, cada tema novo devia linkar para os posts anteriores do mesmo assunto — hoje isso não existe no gerador. Isso mantém o visitante no blog por mais páginas e ajuda o Google a entender quais posts são mais relevantes.
- **Páginas pilar por tema.** Uma página fixa "Tudo sobre Bitcoin" ou "Guia de FIIs", atualizada periodicamente e linkada por todos os posts do tema, tende a rankear melhor que posts diários isolados — e é onde os links de afiliado de maior ticket devem ficar.

Zero seguidores hoje confirma que o tráfego é quase 100% orgânico de busca: qualquer ganho de SEO se reflete quase direto em mais visualizações, sem depender de redes sociais.

## Monetização complementar

Afiliados não precisa ser a única fonte:

- **Google AdSense via Blogger.** O menu "Ganhos" já aparece no painel do Blogger — confirmar se a conta já está aprovada ou se ainda precisa solicitar (exige tráfego mínimo e conteúdo original, que o blog já tem com 173 posts). Renda baixa no volume atual, mas soma à receita de afiliados sem esforço extra por post.
- **Newsletter.** Começar a capturar e-mail agora, mesmo com pouco tráfego, cria uma audiência própria que não depende do algoritmo do Google — e é o canal com maior taxa de clique em links de afiliado quando a lista cresce.
- **Produto próprio no médio prazo.** Com histórico de 173 posts sobre cripto e investimentos, um e-book ou mini-curso "como começar a investir" pode ser vendido diretamente, sem depender de comissão de terceiros — vale considerar depois que o tráfego mensal passar de \~5 mil visualizações.

## Plano de ação em fases

&#91;embedded content: roadmap · 3 fases de 30 dias · 2 gates intermediários + 1 final\]

Cada fase tem um critério de saída claro (o "gate"), não só uma data: a Fase 2 só começa quando todo post novo já sai com link de afiliado e disclosure, e a Fase 3 só quando os 4 novos formatos e a newsletter já estiverem no ar.

## Checklist técnico de implementação

- [ ] Cadastrar-se nos programas de afiliado da tabela acima e guardar os links/IDs
- [ ] Adicionar aviso de divulgação de afiliado (disclosure) no template do blog, em `tema-blogger.xml`
- [ ] Confirmar status do Google AdSense na aba "Ganhos" do Blogger — solicitar se ainda não está aprovado
- [ ] Criar as páginas pilar fixas ("Tudo sobre Bitcoin", "Guia de FIIs") como páginas do Blogger, não posts do dia
- [ ] Adicionar os 4 novos formatos de conteúdo (comparativos, guias, reviews, recursos) em `blog_agent.py`, com CTA e link de afiliado no próprio prompt de geração
- [ ] Ajustar as `queries` de cada tema em `TEMAS` para incluir pelo menos uma versão de cauda longa ("melhor X para Y")
- [ ] Adicionar link interno automático entre posts do mesmo tema no gerador
- [ ] Configurar captura de e-mail (formulário de newsletter) no template do blog
- [ ] Acompanhar cliques em links de afiliado (UTM ou encurtador com analytics) para medir qual formato converte mais
- [ ] Revisar esta projeção de receita a cada 30 dias com os números reais de tráfego e comissão
