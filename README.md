# Framer to HTML / Kodety — Pixel Perfect Skill

**Framer → HTML limpo + CSS editável + JavaScript independente → [Kodety.com](https://kodety.com).**

Skill da [Onunbe AI](https://github.com/onunbeai) para **Claude Code e Codex**, dedicada à conversão de sites Framer completos. Usa o site publicado e renderizado como referência para preservar o design, as páginas, a responsividade e as interações, com saída independente do runtime do Framer.

**Pixel perfect é o objetivo de fidelidade. Compatibilidade 100% com o Kodety é o critério de entrega no escopo validado.** Cada conversão precisa demonstrar esses resultados por comparação visual, validação estrutural e verificação no Builder. HTML limpo fornece a base; componentes, CMS e animações editáveis também precisam seguir os contratos nativos do Kodety.

## Instalar no Codex

No terminal, com Git instalado — comandos para macOS, Linux ou WSL:

```bash
mkdir -p "$HOME/.agents/skills"
git clone https://github.com/onunbeai/framer-to-html-kodety-skill.git \
  "$HOME/.agents/skills/framer-to-kodety"
```

Abra o Codex na pasta onde deseja salvar a conversão. Se a skill não aparecer, reinicie a sessão. Cole este comando no chat, substituindo a URL:

```text
$framer-to-kodety Converta https://seu-site.framer.app inteiro para HTML limpo, CSS editável e JavaScript independente em ./site-convertido. Preserve o visual pixel perfect como objetivo, descubra todas as rotas públicas, reconecte os links e valide desktop, tablet e mobile.
```

A pasta de instalação e a invocação com `$` seguem a [documentação oficial de skills do Codex](https://developers.openai.com/codex/skills/). O identificador da skill permanece `framer-to-kodety`.

## Instalar no Claude Code

No terminal, com Git instalado:

```bash
mkdir -p "$HOME/.claude/skills"
git clone https://github.com/onunbeai/framer-to-html-kodety-skill.git \
  "$HOME/.claude/skills/framer-to-kodety"
```

Abra o Claude Code na pasta onde deseja salvar a conversão e invoque a skill no chat:

```text
/framer-to-kodety Converta https://seu-site.framer.app inteiro para HTML limpo, CSS editável e JavaScript independente em ./site-convertido. Preserve o visual pixel perfect como objetivo, descubra todas as rotas públicas, reconecte os links e valide desktop, tablet e mobile.
```

A instalação pessoal e o comando `/framer-to-kodety` seguem a [documentação oficial de skills do Claude Code](https://code.claude.com/docs/en/skills). Estes comandos são para Claude Code local.

Se já existir uma pasta `framer-to-kodety`, preserve a instalação existente e compare os arquivos antes de substituí-los. Os exemplos de invocação acima são enviados no chat do agente, não executados no shell.

## Converter para o Kodety

No Codex:

```text
$framer-to-kodety Converta https://seu-site.framer.app inteiro para o Kodety.com. Use também a skill kodety-site-code, se disponível, e o contrato atual do Builder. Entregue um ZIP importável com HTML limpo, assets locais, rotas conectadas, componentes nativos e animações editáveis onde aplicável. Valide a fidelidade visual e a compatibilidade no Builder e relate qualquer pendência.
```

No Claude Code:

```text
/framer-to-kodety Converta https://seu-site.framer.app inteiro para o Kodety.com. Use também a skill kodety-site-code, se disponível, e o contrato atual do Builder. Entregue um ZIP importável com HTML limpo, assets locais, rotas conectadas, componentes nativos e animações editáveis onde aplicável. Valide a fidelidade visual e a compatibilidade no Builder e relate qualquer pendência.
```

Para sincronizar diretamente com um projeto aberto no Kodety, conecte o MCP do Builder ao agente e informe o projeto de destino. A skill complementar `kodety-site-code`, seu contrato e seu validador **não estão incluídos neste repositório**. Sem acesso a esses recursos e ao Builder, a entrega pode ser validada como HTML independente; a integração nativa permanece não verificada.

## O que a conversão preserva

- Todas as rotas públicas descobertas no escopo, páginas de detalhe, conteúdo CMS público, idiomas, redirects, menus e âncoras.
- Fontes e recursos OpenType, imagens e SVGs, proporções, espaçamentos, máscaras, breakpoints e estados visuais.
- Navegação e interações observáveis, reconstruídas com código independente.
- Conteúdo e layout presentes no HTML/CSS inicial, com assets locais e classes estáveis.
- Componentes reutilizáveis, variantes e motion editável quando implementados segundo os contratos do Kodety.

A skill orienta o agente a inspecionar, reconstruir e verificar o site. Requer um agente com acesso ao site público, ferramentas de navegador para comparar o resultado e permissão para escrever os arquivos de saída. Serviços externos, autenticação e backends exigem integrações próprias; código público não dá acesso ao projeto privado do Framer.

## Verificar uma conversão

O auditor incluído usa **Python 3.9+**, sem dependências externas. A partir da pasta instalada da skill:

```bash
python3 scripts/audit_site.py /caminho/do/site-convertido \
  --origin https://seu-site.framer.app \
  --routes /caminho/rotas.json
```

`--routes` é opcional. Exemplo de manifesto aceito:

```json
{"routes":[{"localPath":"/"},{"localPath":"/sobre"},{"localPath":"/blog/primeiro-post"}]}
```

O relatório JSON identifica arquivos, links, âncoras e páginas locais ausentes, links que escapam para o domínio original e referências conhecidas ao Framer. O processo retorna código `1` quando encontra problemas e `0` quando não há problemas detectados; avisos ainda exigem revisão.

O auditor é uma verificação estática: não executa a conversão, não mede fidelidade visual e não comprova compatibilidade com o Kodety. Também não cobre CSS `url()`, `srcset`, imports JavaScript, formulários ou comportamento no navegador. Complete a revisão visual e funcional e execute o validador atual do Kodety para esse destino.

Teste interno do auditor:

```bash
python3 scripts/audit_site.py --self-test
```

## Arquivos da skill

| Arquivo | Função |
| --- | --- |
| [SKILL.md](SKILL.md) | Contrato de conversão e fluxo de trabalho |
| [Inventário e extração](references/extraction.md) | Rotas, conteúdo CMS, assets e proveniência |
| [Estado renderizado](references/rendered-state.md) | Captura pós-hidratação, estados e responsividade |
| [HTML independente](references/native-output.md) | Arquitetura, componentes e integração Kodety |
| [Verificação](references/verification.md) | Fidelidade, navegação, comportamento e entrega |
| [Auditor](scripts/audit_site.py) | Verificações estáticas e self-test |
| [Metadados Codex](agents/openai.yaml) | Nome de exibição e prompt inicial |

Uma conversão concluída inclui o site conectado, o mapa de rotas, os assets, o código editável e o registro do que foi verificado. Qualquer divergência visual, integração indisponível ou funcionalidade ainda não validada deve acompanhar a entrega.
