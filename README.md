Implementazione di un sistema di question answring in italiano.

Il programma parte chiedendo all'utente di inserire il nome della pagina a cui si vuole fare la domanda. Il sistema stampa un elenco di pagine relative a quel nome e l'utente dovra' scegliere il numero della pagina secondo l'ordine dell'elenco di output.

Verra' estratta da wikepedia il contenuto la pagina corrispondente a quel nome e a quel numero.
Sara' chiesto un ulteriore comando in input che andra' a selezionare dove si vuole eseguire la ricerca, se sul testo o se sulle tabelle della pagina wikipedia.
Con una serie di elaborazioni del testo, il sistema salva il testo in una cartella denominata text, per poi andarla a ricercare quando richiesta.

Successivamente si potra' inserire la domanda in questione.
Si procedera' ad una pulizia della frase di domanda, per estrarre le parole chiave.
Infine il sistema riportera' la risposta corretta.



```
# Creiamo un virtual environment
python -m venv bert
bert\Scripts\activate

#Apriamo Visual Studio Code
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





