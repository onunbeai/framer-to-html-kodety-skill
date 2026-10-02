# Verificação e entrega

## Primeiro carregamento

Inspecione a resposta HTML e o primeiro paint em recarga: o conteúdo principal e o layout final já devem existir. Teste com JS desativado quando a ferramenta permitir, ou inspecione HTML/CSS do build separadamente. Animações podem depender de JS; conteúdo básico não deve desaparecer.

Bloqueie/revise dependências Framer em execução e build. Assets originais copiados localmente são permitidos; bootstrap remoto ou iframe do original não são conversão concluída. Atenção a caminhos `/assets/...` que funcionam na home e quebram páginas aninhadas, `new URL` em módulos e imports de CSS que só chegam após JS.

## Aparência

Compare original hidratado e reprodução em condições iguais. Faça overlay/diferença por seção se houver ferramenta apropriada, sem usar uma métrica de pixels como único critério. Movimento, antialiasing e rasterização de fontes podem alterar pixels sem mudar geometria; por outro lado, uma pequena diferença de altura na navbar desloca a página inteira.

Priorize: estrutura e proporção → fontes/quebras de linha → gaps/bordas → recortes/máscaras → estados → movimento. Não aceite uma textura genérica no lugar de um shader original, um card redesenhado no lugar da variante real ou um footer abreviado.

## Completude de rotas

Cruze três fontes: rotas descobertas no original, arquivos/páginas implementados e links do produto. Para cada rota, verifique abertura direta, recarga, links de entrada/saída, título, conteúdo específico e estado de navegação ativo.

Execute `scripts/audit_site.py` e o validador do destino. O auditor considera HTML estático; rotas servidas só por JS precisam ser materializadas ou justificadas no contrato escolhido. Inspecione divergências em vez de silenciar todos os avisos.

Percorra a navegação global, detalhes de cada template, paginação/filtros e volta ao índice. Confirme todos os destinos locais do manifesto. Links externos funcionais devem continuar externos; não os “corrija” para rotas fictícias.

## Comportamento

Verifique controles acionáveis, teclado, foco, seleção/hover, menu mobile, carrossel, formatação, persistência e mensagens de falha pertinentes. Não faça envios reais, pagamentos ou autenticação apenas para produzir uma captura; use estado já disponível ou fixtures identificadas quando necessário.

Teste CMS longo e rotas com acentos. Ao inserir HTML gerado por substituição, preserve caracteres Unicode e sequências como `$&`, aspas e emoji; funções de substituição evitam interpretar conteúdo como substituição especial.

## Critério de conclusão

Entregue páginas conectadas, ativos locais, código organizado, estados relevantes reconstruídos e saída sem runtime Framer. Liste pendências concretas, distinguindo captura indisponível, serviço externo ausente e implementação ainda não verificada. Build aprovado prova compilação, não fidelidade. Não declare uma percentagem de fidelidade inventada.
