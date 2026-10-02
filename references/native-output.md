# HTML independente e arquitetura

## Saída visível desde o primeiro carregamento

Use páginas HTML geradas estaticamente, templates de build ou SSR que entregue o layout final. CSS crítico deve ser carregado antes do primeiro paint; reserve o tamanho de imagens/fontes para evitar mudança estrutural. A lógica interativa deve aprimorar esse DOM existente.

Remova da produção bootstrap/roteador Framer, módulos e carregadores hospedados da plataforma, hidratação Framer, analytics/editor do arquivo de referência e widgets de marca da plataforma que não pertençam ao conteúdo autoral. Preserve a implementação bruta para consulta fora do bundle final.

Ausência de runtime Framer não significa ausência de JavaScript. Menus, tabs, sliders, busca, shaders e estado de formulários podem ter JS próprio. Se o usuário pedir zero hidratação, não use React como pré-requisito para montar as páginas: materialize HTML e conecte eventos a ele. Se um app React existente for o destino explicitamente escolhido, separe a hidratação desse app da antiga dependência Framer e descreva com precisão o que permanece.

## Componentização

Extraia shell, navegação, dock, footer, card de cada tipo, detalhes CMS e efeitos em módulos/partials independentes. Dados de conteúdo ficam separados de markup e lógica. Use classes estáveis e tokens, não hashes gerados como API pública do novo site.

Evite copiar todo estilo computado para cada elemento. Computed style serve como evidência: reconstrua a regra, a herança, as variáveis e o breakpoint responsáveis. Prefira corrigir a origem da cascata a acrescentar overrides; no destino Kodety não use `!important`.

Não altere um componente global para resolver uma exceção de uma página. Declare variantes reais e preserve a estrutura. Em React solicitado, memoize fronteiras úteis com props estáveis; animação por frame não deve provocar rerender da árvore inteira.

## Integração Kodety

Consulte o contrato atual da skill `kodety-site-code` para a versão do ambiente. Camadas semânticas precisam de `data-label`; alvos de interação precisam de identidades únicas e estáveis. Componentes reutilizáveis exigem o pacote completo de manifest, CSS escopado, mestres/variantes e instâncias materializadas.

Use os contratos nativos de tabs e sliders quando aplicáveis. Motion editável pertence ao documento Interactions v2 por página. Não duplique a mesma animação em CSS/JS e Interactions. Preserve CSS no estado final visível; o runtime de interação pode aplicar estados de entrada.

Shaders ou lógica que não possam ser representados nativamente podem permanecer módulos JS independentes, desde que não reintroduzam Framer. Identifique o que será editável visualmente e o que requer código; não prometa que canvas virou elementos nativos de layout.

Assets compartilhados ficam em paths locais exatos. Não duplique os mesmos assets por componente. ZIP importável deve ter `index.html`, CSS/JS/assets e metadados na raiz, sem pasta envoltória desnecessária. No projeto conectado, confira o projeto e revisão antes de escrever, sincronize por seção semântica e valide por leitura após escrita. Publicar é uma ação separada.

## Reconexão multipágina

Construa um mapa explícito de URL fonte → rota/arquivo de destino. Use-o para anchors, menus, botões, cards, breadcrumbs, paginação e relações CMS. Resolva `#id` contra a rota de origem correta; preserve encoding e queries funcionais. Links absolutos que apontavam para o domínio fonte devem levar à rota local correspondente, não escapar de volta para o Framer.

Use o mecanismo de páginas/roteamento do destino, com HTML por rota. Servidores estáticos precisam resolver diretórios/index e 404 corretamente. Não transforme todos os destinos em `#`, nem faça uma rota desconhecida mostrar a home como se fosse válida. Preserve redirects e inclua-os no manifesto para que a navegação seja verificável.
