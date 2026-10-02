---
name: framer-to-kodety
description: Converta sites Framer completos para HTML limpo, CSS editável e JavaScript independente, com fidelidade pixel perfect como objetivo e integração validada com o Kodety.com. Preserve páginas, componentes, estados e navegação a partir do visual real após a hidratação. Use para importar ou migrar um site publicado do Framer; não para editar o projeto dentro do Framer.
---

# Framer to HTML / Kodety — Pixel Perfect Skill

Converta o site inteiro, usando o estado publicado após a hidratação como fonte visual. Entregue HTML real desde a primeira resposta, assets locais, CSS editável e interações independentes. A saída não deve carregar o runtime do Framer para adquirir o design correto.

O objetivo é uma conversão pixel perfect para HTML limpo e uma entrega 100% compatível com o Kodety.com no escopo contratado. Esses são critérios de aceitação por projeto: comprove a fidelidade por comparação visual e a compatibilidade pelo contrato atual, pelo validador e pela verificação no Builder. HTML limpo é a base da integração; por si só, não comprova suporte nativo a componentes, CMS ou Interactions. Registre qualquer diferença ou recurso ainda não validado antes de declarar a conversão concluída.

## Contrato da conversão

- Uma URL inicial é a entrada do inventário do site, não um limite à home. Descubra e reconecte todas as rotas públicas do escopo, incluindo páginas CMS, detalhes, idiomas, redirects, menus e âncoras.
- Preserve decisões autorais: fontes e seus recursos OpenType, geometria, textos, imagens, espaçamento, estados de hover/ativo/foco, breakpoints, carrosséis, máscaras e efeitos. Refinamento significa reproduzir melhor a referência; redesenhe apenas quando solicitado.
- Extraia e use o código público compilado como evidência quando disponível. Não descreva isso como acesso ao projeto privado editável, ao código-fonte original indisponível ou a um backend.
- A captura pós-hidratação orienta a reconstrução. Salvar HTML com os mesmos scripts Framer cria uma cópia dependente, não conclui a conversão.
- Conteúdo e layout final devem estar presentes no HTML/CSS inicial. JavaScript próprio pode operar menus, sliders, filtros, canvas e outras funções. Não esconda a página até um `ready`, nem apresente uma versão provisória para trocá-la depois.
- Não use screenshot como página, iframe do site original como implementação, um componente monolítico ou milhares de estilos computados inline como código final.

## Fluxo

### 1. Inventarie o site e o destino

Leia [inventário e extração](references/extraction.md). Preserve o trabalho existente e identifique o destino: pasta/ZIP importável ou projeto Kodety conectado. Para o Builder, combine com a skill `kodety-site-code`, quando disponível, e leia seu contrato atual antes de gerar metadados/componentes/Interactions. Sem esse contrato, produza primeiro o HTML independente e declare a compatibilidade específica do Builder ainda não verificada; não invente schemas proprietários.

Mantenha um manifesto com URL fonte, rota local, tipo de página, template/CMS, título, arquivo de saída, links e estado de verificação. Inventarie também assets e dependências externas. Compartilhe as lacunas reais; não peça confirmações para decisões de implementação já autorizadas.

### 2. Registre a versão visual verdadeira

Leia [captura pós-hidratação e estados](references/rendered-state.md). Navegue pelas rotas em navegador real com as ferramentas disponíveis e espere evidências de estabilidade: fontes carregadas, dimensões finais, conteúdo lazy e estado de entrada concluído. `networkidle` ou uma espera fixa não provam isso.

Registre screenshots, DOM renderizado e medidas focadas nos elementos decisivos. Compare o HTML inicial com o DOM final para identificar conteúdo, estilos e efeitos que dependiam da hidratação. Capture ao menos as variantes relevantes de templates, shell, hover, menu, mobile e conteúdo longo.

### 3. Reconstrua o shell e uma página representativa

Leia [HTML independente e arquitetura](references/native-output.md). Extraia os tokens efetivos e assets originais, normalize classes e faça navbar, dock, footer, tipografia e um componente repetido. Compare essa fatia no navegador antes de repetir uma interpretação errada em todas as páginas.

Use HTML semântico, CSS externo organizado por componentes e módulos JS pequenos quando necessários. Componentes nativos Kodety devem ter instâncias materializadas em HTML. Não copie automaticamente elementos comerciais da plataforma, como “Made in Framer”, para a implementação nova; preserve marcas e créditos do autor/conteúdo.

### 4. Complete as rotas e reconecte os links

Implemente cada template e seus registros reais. Reescreva apenas links internos pertencentes ao site migrado. Preserve destinos externos, `mailto:`, `tel:`, downloads, parâmetros funcionais e âncoras. Não faça replace global do domínio em todo o código.

Páginas de detalhe precisam abrir diretamente e após recarregar; não podem depender de visitar a home primeiro. Resolva caminhos UTF-8, percent-encoding e trailing slashes de modo consistente. Redirecionamentos também entram no mapa, com destino explícito. Nenhuma rota descoberta pode sumir silenciosamente: marque concluída, redirect ou bloqueada com motivo.

### 5. Valide a conversão completa

Leia [verificação e entrega](references/verification.md). Compare o original hidratado com o resultado no mesmo viewport, zoom, scroll e estado. Verifique aparência, comportamento e carregamento separadamente.

Execute o auditor offline, usando o caminho da pasta instalada desta skill:

```sh
python3 /caminho/da/skill/scripts/audit_site.py /caminho/do/site --origin https://fonte.framer.app --routes /caminho/rotas.json
```

O argumento `--routes` é opcional e aceita uma lista de rotas locais ou um objeto `{"routes":[{"localPath":"/notes"}]}`. Esse auditor identifica links/arquivos/âncoras locais ausentes e referências carregadas conhecidas do Framer. Ocorrências em código são avisos para revisão: uma string não prova execução. Inspecione os avisos antes de declarar independência. O auditor não prova fidelidade visual, execução de JS ou compatibilidade Kodety. Execute também o validador Kodety quando esse for o destino.

Entregue o site completo e conectado, o mapa de rotas, a proveniência necessária e as limitações concretas. Reporte o que foi visualmente conferido; não declare “100%” ou “todas as páginas” sem a respectiva evidência. Não publique ou altere serviços externos sem autorização para essa ação.
