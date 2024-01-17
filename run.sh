#!/bin/bash

# Exécuter main.py dans un nouveau terminal
lxterminal -e python3 main.py &

# Exécuter apiManager.py dans un autre nouveau terminal
lxterminal -e python3 apiManager.py &
