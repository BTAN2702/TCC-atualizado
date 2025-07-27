#!/usr/bin/env python3
"""
Arquivo principal para execução do sistema de telemonitoramento CEUB
"""

import sys
import os

# Adiciona o diretório telemonitoramento ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'telemonitoramento'))

from telemonitoramento.app import main

if __name__ == "__main__":
    main() 