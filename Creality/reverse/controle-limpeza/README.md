# Controle de Limpeza

Extra isolado para testar probing por ponto sem alterar os arquivos Python originais da Creality.

## Arquivos

- `cfs_prtouch_bridge.py`
  - extra do Klipper
- `cfs_prtouch_bridge.cfg`
  - seção mínima para incluir no `printer.cfg`

## Comando novo

```gcode
CFS_PROBE_POINT X=110 Y=110
```

Parâmetros opcionais:

```gcode
CFS_PROBE_POINT X=110 Y=110 MAX_TIMES=3 SPEED=2.0 MIN_DIS=10 MAX_ERR=0.2 USE_BEST_RDY_Z=1
```

## O que faz

- procura `prtouch_v3`, `prtouch_v2` ou `prtouch`
- chama `_probe_times(...)` do objeto carregado
- retorna o `Z` medido no terminal do Klipper

## Fluxo de deploy

1. Compilar com Python 3.8
2. Fazer backup remoto de:
   - `/usr/share/klipper/klippy/extras/cfs_prtouch_bridge.py`
   - `/usr/share/klipper/klippy/extras/cfs_prtouch_bridge.pyc`
   - `/usr/data/printer_data/config/cfs_prtouch_bridge.cfg`
   - `/usr/data/printer_data/config/printer.cfg`
3. Subir:
   - `cfs_prtouch_bridge.py`
   - `cfs_prtouch_bridge.pyc`
   - `cfs_prtouch_bridge.cfg`
4. Adicionar no topo do `printer.cfg`:
   - `[include cfs_prtouch_bridge.cfg]`
5. Reiniciar a impressora
