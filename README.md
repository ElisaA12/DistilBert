Implementazione di un sistema di question answring in italiano.

Il programma parte chiedendo all'utente quale lingua scegliere, italiano o inglese, per poi settare quella scelta.
Successivamente si inserisce, sempre  da linea di codice, la pagina a cui si vuole fare la domanda. Il sistema stampa un elenco di pagine relative a quel nome e l'utente dovra' scegliere secondo il codice riportato sullo schermo.

Verra' estratta da wikepedia il contenuto la pagina corrispondente a quel nome, a quel codice, nella ingua scelta.
Sara' chiesto un ulteriore comando in input che andra' a selezionare dove si vuole eseguire a ricerca, se sul testo o se sulle tabelle della pagina wikipedia.
Con una serie di elaborazioni del testo, il sistema salva il testo in una cartella denominata text, per poi andarla a ricercare quando richiesta.

Successivamente si potra' inserire la domanda in questione.
Si procedera' ad una seconda puliza del testo, ovvero della frase di domanda, per estrarre le parole chiave.

Infine il sistema riportera' la domanda corretta.



```
# Creiamo un virtual environment
python -m venv bert
bert\Scripts\activate

#
Apriamo Visual Studio Code
code .

#Installiamo le dipendenze
pip install -U spacy
pip install wikipedia
pip install rank-bm25
pip install torch
pip install transformers
pip install lxml
python -m spacy download it_core_news_sm
```





