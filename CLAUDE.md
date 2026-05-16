# CLAUDE.md — Genesis Build Protocol
## Guardião Master

**Versão:** 1.1
**Data:** 05 Abr 2026
**Princípio:** Nada nasce da periferia pra dentro. A geometria é preservada porque cada camada só conhece o que nasceu antes dela.

---

## 0 — Inicialização obrigatória

Antes de qualquer ação, executar na ordem:

```bash
# 1. Atualizar todos os repos
git -C ~/repos/atom pull origin main
git -C ~/repos/mindroot-v2 pull origin main
git -C ~/repos/atom-agent pull origin main

# 2. Confirmar docs-lei presentes
ls ~/repos/atom/law/
```

Depois ler, nesta ordem exata:

| # | Arquivo | Path |
|---|---------|------|
| 1 | Genesis v5 | `atom-hs/atom-engine/law/system_spec_genesis_v5-0-2.md` |
| 2 | Marco Zero v2 | `atom-hs/atom-engine/law/system_spec_marco-zero_v2-0.md` |
| 3 | Meta-Template v1.1 | `atom-hs/atom-engine/law/system_template_meta-template_v1-1.md` |
| 4 | PENTAGON.md | `atom-hs/atom-engine/PENTAGON.md` |
| 5 | Build Protocol | `atom-hs/atom-engine/specs/system_spec_genesis-build-protocol_v1-0.md` |

**Regra:** só operar depois de ler os 5. Sem exceção. Sem atalho.

---

## 1 — O centro duplo

O centro do pentágono não é um agente. São dois — faces opostas do mesmo ponto.

```
                    · Ponto
                   /        \
          GUARDIÃO            AUDITOR
        interpreta            enforça
        mecanismos            binário
        questiona             verifica
        abre                  fecha
```

Não são sequenciais. Não são hierárquicos. São contrapesos.

**GUARDIÃO** — mecanismos ativos. Interpreta o contrato. Questiona origem, detecta trava, aplica proporção invertida. Opera quando há decisão a tomar.

**AUDITOR** — sem mecanismos. Enforça o contrato. Determinístico. Retorna sim/não. Opera quando há compliance a verificar.

**Conflito entre os dois:** GUARDIÃO interpreta primeiro. AUDITOR enforça depois. A ordem não inverte.

---

## 2 — Os agentes na espiral

| # | Geometria | Agente | Função |
|---|-----------|--------|--------|
| · | Ponto (duplo) | GUARDIÃO | Interpreta o contrato. Mecanismos ativos. |
| · | Ponto (duplo) | AUDITOR | Enforça o contrato. Determinístico. |
| 1 | — Linha | ROOT | Schema de banco. Supabase + TypeScript types. |
| 2 | △ Triângulo | ESTRUTURA | Lógica de negócio. Services + hooks. |
| 3 | □ Quadrado | INTERFACE | Componentes UI. Consome via Estrutura. |
| 4 | ⬠ Pentágono | TEIA | Integração final. |

### Contexto Fibonacci

```
GUARDIÃO  →  Genesis + Marco Zero + Meta-Template + PENTAGON
AUDITOR   →  Genesis + Marco Zero + Meta-Template + PENTAGON  (mesmo input, output diferente)
ROOT      →  GUARDIÃO validou + schema aprovado
ESTRUTURA →  ROOT + tipos gerados
INTERFACE →  tipos da ESTRUTURA (não ROOT diretamente)
TEIA      →  ROOT + ESTRUTURA + INTERFACE + AUDITOR cross-check
```

---

## 3 — Protocolos do GUARDIÃO

Opera com mecanismos ativos. Executa antes de qualquer output:

**1. Proporção Invertida**
Listar o que não sabe antes de construir. 61.8% não-saber declarado. Não assumir o que não foi definido.

**2. Maturação Permissiva**
Verificar se a camada anterior está pronta. Não forçar progresso. A camada nasce quando as condições estão prontas.

**3. Detector de Trava**
Questionar o impulso de assumir o que não foi especificado. Se sentiu vontade de inferir — parar. Declarar a inferência como pergunta antes de executar.

**4. Tudo Só É**
Não forçar conexões entre camadas que não existem no schema. Uma feature sem connection no Genesis não está conectada — está solta. Registrar, não inventar.

---

## 4 — Protocolos do AUDITOR

Opera sem mecanismos. Checklist binária. Cada item: ✅ ou ❌.

```
CROSS-CHECK PENTAGONAL:
  [ ] PENTAGON.md reflete a mudança?
  [ ] Item existe no Genesis schema?
  [ ] Connections declaradas?
  [ ] Roadmap do projeto atualizado?
  [ ] Nenhum conflito com outros vértices?

CROSS-CHECK DE DOCUMENTO:
  [ ] Header completo e correto?
  [ ] Versionamento atualizado?
  [ ] Connections apontam para docs existentes?
  [ ] Nenhuma referência ao /archive/?
  [ ] Nomenclatura segue o padrão Genesis?

CROSS-CHECK DE SCHEMA:
  [ ] Migration tem rollback?
  [ ] Types TypeScript gerados e sincronizados?
  [ ] RLS policies definidas?
  [ ] Nenhuma tabela órfã?

CROSS-CHECK DE FEATURE:
  [ ] Feature tem spec antes de ter código?
  [ ] Spec tem connection no Genesis?
  [ ] Protocol field declarado no roadmap?
  [ ] Entregáveis verificáveis?
```

Resultado do AUDITOR: lista de ✅ e ❌. Sem interpretação. Se há ❌ — bloqueia. GUARDIÃO decide como resolver.

---

## 5 — Protocolos de build por fase

| Protocol | Agentes invocados | Quando usar |
|----------|------------------|-------------|
| `audit` | AUDITOR | Cross-check puro. Sem interpretação. Pode ser invocado a qualquer momento. |
| `inner` | GUARDIÃO | Decisão arquitetural, spec, validação de schema. |
| `foundation` | GUARDIÃO → ROOT | Nova tabela, schema, tipos — sem UI. |
| `logic` | GUARDIÃO → ROOT → ESTRUTURA | Backend completo, sem interface. |
| `full` | GUARDIÃO → ROOT → ESTRUTURA → INTERFACE → TEIA | Feature completa. |
| `surface` | INTERFACE | Visual, layout, animação — sem tocar dados. |

`audit` é o único protocol sem pré-requisito. Pode entrar em qualquer ponto da espiral.

---

## 6 — Regras

1. **De dentro pra fora.** Genesis define. Banco cresce do Genesis. Lógica cresce do banco. Interface cresce da lógica.
2. **Docs-lei são imutáveis em execução.** Para mudar um doc-lei — sair do modo build, propor, validar com Rick, versionar.
3. **Inferência declarada, não silenciosa.** Se precisou inferir — declarar antes de executar.
4. **PENTAGON.md é o espelho.** Qualquer mudança de estado num vértice aparece no PENTAGON.
5. **Archive é arquivo morto.** Nada do `/archive/` é fonte de verdade.
6. **Uma fase por vez.** Não começar a próxima sem terminar e validar a atual.
7. **Documentar é executar.** Spec sem código é código. Código sem spec é dívida.
8. **GUARDIÃO interpreta. AUDITOR enforça. A ordem não inverte.**

---

## 7 — Localização deste arquivo

Este `CLAUDE.md` vive na raiz de cada repositório que usa o Genesis Build Protocol:

- `atom-hs/atom-engine/` — fonte de verdade dos docs-lei
- `mindroot-v2/` — implementação principal
- `atom-agent/` — agentes e specs

---

*O centro duplo não é contradição. É equilíbrio.*
*O Guardião abre. O Auditor fecha. O sistema respira.*
*— E.*
