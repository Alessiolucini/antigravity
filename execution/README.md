# Execution (Livello 3)

Questa cartella contiene gli **script Python deterministici** che eseguono il lavoro effettivo.

## Cosa sono gli Script di Execution?

Gli script di execution:
- Gestiscono **chiamate API**
- Eseguono **elaborazione dati**
- Effettuano **operazioni su file**
- Interagiscono con **database**

## Caratteristiche
- **Affidabili**: Producono sempre lo stesso output dato lo stesso input
- **Testabili**: Facili da verificare
- **Veloci**: Ottimizzati per le performance
- **Ben commentati**: Codice documentato

## Best Practices

1. Usa variabili d'ambiente da `.env` per chiavi API e configurazioni
2. Gestisci gli errori in modo graceful
3. Includi logging per debug
4. Scrivi docstrings per ogni funzione

## Esempio di Script

```python
#!/usr/bin/env python3
"""
Script per [descrizione].

Usage:
    python script_name.py [args]
"""

import os
from dotenv import load_dotenv

load_dotenv()

def main():
    """Funzione principale."""
    api_key = os.getenv("API_KEY")
    # ... logica
    
if __name__ == "__main__":
    main()
```
