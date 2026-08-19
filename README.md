# hass-blueprints

Blueprints de automação do Home Assistant que eu mantenho e uso em várias
instâncias. Publicadas para que o próprio Home Assistant consiga importá-las e
oferecer atualização depois — é o que o `source_url` em cada arquivo permite.

## Instalar

| Blueprint | Nome no HA | Instalar |
|---|---|---|
| `SyncNStates.yaml` | Synchronize Multiple Switches (or Lights) | [![Add to your Home Assistant](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Frickard2014%2Fhass-blueprints%2Fmain%2Fblueprints%2Fautomation%2Frickard2014%2FSyncNStates.yaml) |
| `idlelights.yaml` | Timed Lights Shutdown | [![Add to your Home Assistant](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Frickard2014%2Fhass-blueprints%2Fmain%2Fblueprints%2Fautomation%2Frickard2014%2Fidlelights.yaml) |
| `idleshutdown.yaml` | Motion Activated Lights - Idle Shutdown Automation | [![Add to your Home Assistant](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Frickard2014%2Fhass-blueprints%2Fmain%2Fblueprints%2Fautomation%2Frickard2014%2Fidleshutdown.yaml) |
| `occupancylights.yaml` | Motion-Activated Devices with Time and State Conditions | [![Add to your Home Assistant](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Frickard2014%2Fhass-blueprints%2Fmain%2Fblueprints%2Fautomation%2Frickard2014%2Foccupancylights.yaml) |
| `switch_temperature_mode_controller.yaml` | RGCC - Switch Temperature Mode Controller | [![Add to your Home Assistant](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Frickard2014%2Fhass-blueprints%2Fmain%2Fblueprints%2Fautomation%2Frickard2014%2Fswitch_temperature_mode_controller.yaml) |

Ou: **Configurações → Automações e Cenas → Blueprints → Importar Blueprint** e
cole a URL do arquivo `.yaml` deste repositório.

## As blueprints

### `SyncNStates` — sincronizar N entidades

Mantém várias luzes ou tomadas no mesmo estado — o "paralelo", o three-way
emulado. É a **única** blueprint de sincronismo daqui: `SyncStatesTwo`, `Three`
e `Four` eram o mesmo problema escrito três vezes com 2, 3 e 4 inputs fixos, e
foram removidas em 2026-08-19 depois que toda a frota migrou.

Quatro guardas, nesta ordem, e o cabeçalho do arquivo explica cada uma:

1. o estado-alvo, **lido ao vivo**, é `on`/`off`;
2. quem volta de queda obedece ao grupo, não o comanda;
3. nenhum membro `unavailable`/`unknown`;
4. **divergência real** — é esta que fecha o laço: quando os estados já batem, o
   eco morre na condição em vez de virar mais uma chamada de serviço.

O alvo nunca inclui a entidade que disparou, e inclui apenas as que de fato
discordam.

> **Por que isso importa.** Em 2026-08-19 uma instância entrou em laço de
> verdade: um grupo de três entidades acumulou 4671 mudanças de estado em
> 45 min, a luz piscou, e alguém acabou cortando a energia pela fiação —
> queimando um interruptor. A blueprint em produção comandava todas as entidades
> do grupo, inclusive a que tinha disparado, e não checava divergência. Esse
> desenho é um **amplificador**: qualquer discordância momentânea vira comando
> no grupo inteiro, e cada confirmação reentra como gatilho novo.

> **Correção de uma explicação errada.** Uma versão anterior deste README e do
> cabeçalho do arquivo culpava a topologia Zigbee — dizia que End Device
> (TS0601 sem neutro) confirma "segundos depois e fora de ordem" e que era isso
> que sustentava o laço. Medido depois no histórico do incidente, com o grupo
> parado 38 min e um toque físico iniciando: **+49 ms** o End Device, **+238 ms**
> o Router do mesmo grupo — o End Device foi 5x mais rápido, e em ordem. Na
> mesma janela, outros dois grupos que também misturavam End Device com Router
> foram usados e sincronizaram normalmente. **O tipo do dispositivo não explica
> o incidente; o desenho da blueprint explica.** O que disparou aquele grupo
> específico segue indeterminado, e está registrado como tal.

`settle_time` (padrão 0.3 s) é uma janela de não-reentrada aplicada **depois** da
chamada de serviço — não atrasa a luz, e **não é** a proteção contra laço. O
padrão serve para qualquer grupo: está medido que o tipo Zigbee do dispositivo
não muda o quadro. Só mexa com medição própria na mão.

`mode: queued` com `max: 2`: um toque dentro da janela é enfileirado e honrado,
não descartado — é o que preserva "liguei sem querer, quero desligar já".

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
