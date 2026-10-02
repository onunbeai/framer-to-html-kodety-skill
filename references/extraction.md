# Inventário e extração

## Cobertura de páginas

Comece pelo sitemap (incluindo índices e sitemaps por idioma), links do HTML, navegação após hidratação, rodapé, menus, paginação, índice de busca e rotas/coleções públicas declaradas nos módulos publicados. Acompanhe links do mesmo site até não surgirem novas rotas do escopo. Slugs de CMS não se limitam aos primeiros cards visíveis.

Normalize para deduplicar sem perder significado: resolva URLs relativas, remova fragmentos apenas da identidade da página, preserve queries quando alterarem conteúdo e registre aliases/redirects. Evite multiplicar infinitamente páginas de busca/filtros: represente essas combinações como estados de uma rota quando esse for o comportamento original.

Manifesto sugerido, adaptável ao projeto:

```json
{"sourceOrigin":"https://exemplo.framer.app","capturedAt":"ISO-8601","routes":[{"sourceUrl":"https://exemplo.framer.app/notas/estreia","localPath":"/notas/estreia","outputFile":"notas/estreia/index.html","template":"article","status":"captured","links":["/notas","/#contato"]}]}
```

Não misture páginas não descobertas com páginas deliberadamente fora do escopo. Um link externo para uma ferramenta não concede acesso ao código privado dessa ferramenta. Documente o comportamento e integre/reconstrua apenas o que foi autorizado e é observável.

## Arquivo bruto de referência

Guarde o HTML recebido, CSS, imports estáticos/dinâmicos públicos, módulos de página/componente, fontes, SVG, imagens, vídeo e dados CMS públicos úteis. Registre URL, arquivo local, tamanho, hash SHA-256 e erro de captura, se houver. Preserve esse arquivo bruto separado dos arquivos de produção.

Inspecione os módulos para encontrar tokens, variantes, props, fórmulas e assets reais. Classes geradas e minificação dificultam leitura, mas não justificam redesenhar por aproximação. Não execute indiscriminadamente JavaScript extraído no host para descobrir valores: prefira leitura, AST, dados serializados ou o navegador de referência.

Uma cópia local do build original pode ajudar na comparação quando a rede é instável. Identifique-a como referência dependente; nunca a entregue como saída independente. Reescrita de imports, `new URL(..., import.meta.url)` e caminhos CMS precisa preservar semântica. Não remova hashes ou query de transformação de imagens sem guardar a associação ao asset.

## CMS e assets

- Preserve todos os registros, ordem, IDs e relações relevantes; confira contagens e paginação.
- Para formatos binários públicos, use o schema/decoder observado no bundle. Valide offsets, bytes consumidos e IDs únicos; não invente registros para preencher a grade.
- Mantenha conteúdo rico e links dos artigos. O título e a capa sozinhos não reproduzem uma página de detalhe.
- Preserve SVG vetorial real e fontes originais. Verifique eixo de peso, subset Unicode, ligaduras, `calt`, `ssXX`, `unicode-range` e fallbacks antes de “corrigir” uma diferença tipográfica.
- Arquive tamanhos adequados de mídia e mantenha proporção, recorte, `object-position`, opacidade, máscara e dimensões intrínsecas.
- Documente dependências de autenticação, formulários, embeds, busca ou pagamentos. Uma réplica visual não equivale a uma integração funcional; mantenha estados honestos quando o serviço não estiver disponível.
