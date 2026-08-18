# hass-blueprints

Blueprints de automação do Home Assistant que eu mantenho e uso em várias
instâncias. Publicadas para que o próprio Home Assistant consiga importá-las e
oferecer atualização depois — é o que o `source_url` em cada arquivo permite.

## Instalar

| Blueprint | Nome no HA | Instalar |
|---|---|---|
| `SyncNStates.yaml` | Synchronize Multiple Switches (or Lights) | [![Add to your Home Assistant](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Frickard2014%2Fhass-blueprints%2Fmain%2Fblueprints%2Fautomation%2Frickard2014%2FSyncNStates.yaml) |
| `SyncStatesFour.yaml` | Synchronize Switches and Lights | [![Add to your Home Assistant](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Frickard2014%2Fhass-blueprints%2Fmain%2Fblueprints%2Fautomation%2Frickard2014%2FSyncStatesFour.yaml) |
| `SyncStatesThree.yaml` | Synchronize Three Switches (or Lights) | [![Add to your Home Assistant](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Frickard2014%2Fhass-blueprints%2Fmain%2Fblueprints%2Fautomation%2Frickard2014%2FSyncStatesThree.yaml) |
| `SyncStatesTwo.yaml` | Synchronize Two Switches (or Lights) | [![Add to your Home Assistant](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Frickard2014%2Fhass-blueprints%2Fmain%2Fblueprints%2Fautomation%2Frickard2014%2FSyncStatesTwo.yaml) |
| `idlelights.yaml` | Timed Lights Shutdown | [![Add to your Home Assistant](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Frickard2014%2Fhass-blueprints%2Fmain%2Fblueprints%2Fautomation%2Frickard2014%2Fidlelights.yaml) |
| `idleshutdown.yaml` | Motion Activated Lights - Idle Shutdown Automation | [![Add to your Home Assistant](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Frickard2014%2Fhass-blueprints%2Fmain%2Fblueprints%2Fautomation%2Frickard2014%2Fidleshutdown.yaml) |
| `occupancylights.yaml` | Motion-Activated Devices with Time and State Conditions | [![Add to your Home Assistant](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Frickard2014%2Fhass-blueprints%2Fmain%2Fblueprints%2Fautomation%2Frickard2014%2Foccupancylights.yaml) |
| `switch_temperature_mode_controller.yaml` | RGCC - Switch Temperature Mode Controller | [![Add to your Home Assistant](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Frickard2014%2Fhass-blueprints%2Fmain%2Fblueprints%2Fautomation%2Frickard2014%2Fswitch_temperature_mode_controller.yaml) |

Ou: **Configurações → Automações e Cenas → Blueprints → Importar Blueprint** e
cole a URL do arquivo `.yaml` deste repositório.

## As blueprints

### `SyncNStates` — sincronizar N entidades

Mantém várias luzes ou tomadas no mesmo estado. O gatilho é restrito a
`to: ["on", "off"]`, então nem chega a executar quando a entidade cai para
`unavailable`/`unknown` — a condição de estado continua ali como segunda linha
de defesa. É a que substitui as três
variantes antigas (`SyncStatesTwo`/`Three`/`Four`), e a única que **exclui do
alvo a entidade que disparou**, o que corta o laço de re-disparo na origem em
vez de mascará-lo com atrasos. Tem guarda para `unavailable`/`unknown`, para não
chamar `homeassistant.turn_unavailable`, e `max_exceeded: silent`.

Prefira esta. `SyncStatesTwo`, `Three` e `Four` seguem publicadas apenas porque
automações antigas ainda as referenciam.

### `switch_temperature_mode_controller` — termostato com modos

Controla uma tomada por temperatura, com modos Auto, On Demand e Off, alvos
distintos para casa/ausente, histerese configurável e opção de operar só de dia.
Reavalia a cada 5 minutos além dos gatilhos de estado.

### `occupancylights` — luzes por presença, com horário

Liga dispositivos por movimento, entre o pôr e o nascer do sol, ou quando foram
desligados há pouco por inatividade.

> Reescrita em 2026-08-18. A versão anterior usava uma variável `inputs`, que
> **não existe no Home Assistant**, e falhava com
> `UndefinedError: 'inputs' is undefined` em toda execução. O cabeçalho do
> arquivo lista os cinco defeitos corrigidos. O schema de inputs foi preservado,
> então automações que já usavam a versão antiga continuam válidas.

### `idleshutdown` / `idlelights` — desligar por inatividade

`idleshutdown` desliga dispositivos após um sensor de movimento ficar inativo
por N minutos. `idlelights` desliga após ficarem ligados por N minutos.

> `idlelights` desliga **todos** os dispositivos da lista quando **qualquer um**
> completa o tempo, não apenas o que disparou. Pode ser o que você quer, ou não.

## Terceiros

`edwardtfn/` é de outro autor, mantida aqui só para manter minhas instâncias na
mesma versão. O `source_url` dela aponta para a origem — instale pela origem,
não por aqui.

## Desenvolvimento

```sh
python3 scripts/validate.py     # YAML, bloco blueprint, coerência domain/pasta
python3 scripts/gen-badges.py   # regera a tabela de instalação acima
```

Os nomes de arquivo são estáveis por contrato: o `automations.yaml` referencia a
blueprint pelo caminho, então renomear quebra as automações de quem já usa.
