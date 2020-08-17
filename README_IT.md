## Language Detection

[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)


Questo progetto si occupa di *analizzare* e *classificare* le repository GitHub in base alla lingua utilizzata per la stesura del **README**.

### Requisiti
* python3
```
$ pip3 install six
$ pip3 install langdetect
$ pip3 install pytest
```

### Get Started
Per utilizzare Language Detector individualmente, se utilizzi MacOS o Linux digitare il comando:

`$ python3 detector.py` altrimenti: `$ python detector.py` su Windows.

#### Tasks

- [x] Classificazione di tutti i README all'interno della repository.
- [x] Spostamento delle repository in cartelle dedicate in base ai risultati della detection della lingua.
- [x] Generazione CSV in output contenente i risultati della classificazione e i nuovi path dopo lo spostamento.
- [ ] Generazione CSV in input contenente i path verso le repository.

#### Come Funziona?

Lo script prende in input un file CSV che deve contenere le informazioni sulla posizione delle repository da analizzare:

| Index    | Path                                  |
|:--------:|---------------------------------------|
| 0        | Path assoluto della repository        |
| 1        | Path assoluto di un'altra repository  |
| ...      | ...                                   |

È possibile fornire allo script il [*nome*](https://github.com/anasmounsif/Language_Detection/blob/master/config.ini#L16) del CSV mediante l'utilizzo del file di configurazione.

Language Detection utilizza la libreria [*langdetect*](https://github.com/Mimino666/langdetect) che implementa un classificatore Naive Bayes migliorato attraverso una normalizzazione dei caratteri e l'applicazione di specifici filtri, per più dettagli guarda: [*langdetect slideshare*](https://www.slideshare.net/shuyo/language-detection-library-for-java).

Per ogni repository vengono analizzati tutti i README presenti all'interno della struttura, anche se annidati, dunque ipotizzando che una repository contenga molti README scritti con varie lingue lo script si focalizza solamente su di una domanda;

> *"Quanto inglese c'è all'interno di tutta la repository?"*

Questo per evitare di saturare i risultati con innumerevoli codici.

I risultati vengono poi annotati nel CSV generato in output:

| Index    | Path                                           | Readme Analyzed | Language Detected | Code   | Percentage | Code   | Percentage |
|:--------:|------------------------------------------------|:---------------:|-------------------|:------:|:----------:|:------:|:----------:|
| 0        |  Path assoluto della repository                |  1              | `English`         | en     | 100%       | //     | //         |
| 1        |  Path assoluto di un'altra repository          |  2              | `Mixed`           | en     | 60%        | others | 40%        |
| 2        |  etc                                           |  1              | `Not English `    | others | 100%       | //     | //         |
| ...      | ...                                            |  ...            | ...               | ...    | ...        | ...    | ...        |

Dunque le repository possono essere classificate in:

* Inglese
* Non Inglese
* Misto

Le repository aventi il README assente, vuoto, con meno del [*numero minimo*](https://github.com/anasmounsif/Language_Detection/blob/master/config.ini#L10) di caratteri oppure con un'estensione non supportata verranno classificate come *Unknown*, e sarà poi cura dell'utente analizzarle manualmente.

Estensioni supportate:
* .markdown
* .mdown
* .mdwn
* .mkdn
* .mkd
* .md
* .txt

| Index    | Path                                           | Readme Analyzed | Language Detected | Code   | Percentage | Code   | Percentage |
|:--------:|------------------------------------------------|:---------------:|-------------------|:------:|:----------:|:------:|:----------:|
| 0        |  Path assoluto della repository analizzata     |  1              | `Unknown`         | //     | //         | //     | //         |
| 0        |  etc                                           |  0              | `Unknown`         | //     | //         | //     | //         |
| ...      | ...                                            | ...             | ...               | ...    | ...        | ...    | ...        |

GitHub :octocat: mette a disposizione numerosi *markdown*, quest'ultimi potrebbero influenzare la detection della lingua, perciò lo script dispone di un'ulteriore feature, ovvero quella di pulire il README analizzato dai seguenti markdown:

* Tabelle
* Immagini
* Link
* Code Snippet
* URLs
* HTML
* Caratteri Speciali

Di default *langdetect* utilizza un approccio **non deterministico**, questa funzionalità è parte del progetto originale di Google, se hai bisogno di forzare l'algoritmo ad utilizzare un approccio deterministico modifica la seguente [*linea*](https://github.com/anasmounsif/Language_Detection/blob/master/config.ini#L8) in `translation_type=0` nel file di configurazione.

Inoltre è possibile scegliere dove spostare le repository classificate:

```
[destinations]
destination_english = path
destination_not_english = path
destination_mixed = path
destination_unknown = path
```

Nonché [*disabilitare*](https://github.com/anasmounsif/Language_Detection/blob/master/config.ini#L6) lo spostamento; `moving_feature=0`, oppure [*disabilitare*](https://github.com/anasmounsif/Language_Detection/blob/master/config.ini#L14) la generazione del file CSV in output; `activate_csv_output=0`

Se utilizzato individualmente _sarebbe opportuno modificare con cautela i parametri all'interno del file di configurazione_.

Durante l'esecuzione lo script genera un file di log ove è possibile consultare tutte le operazioni compiute nonché i risultati della detection, ovviamente il logging è un'operazione costosa dunque per default il livello è configurato su INFO, se si ha necessità di un logging più dettagliato modificare la seguente [*riga*](https://github.com/anasmounsif/Language_Detection/blob/master/log.conf#L23) in `level=DEBUG` nel file di configurazione.

:warning: **Per una corretta esecuzione di Language Detector è necessario che le repository da analizzare siano state clonate!** :warning:

#### Test

Per eseguire i test digitare da terminale il comando: `$ pytest` all'interno della cartella root oppure è anche possibile eseguire test specifici digitando il comando: `$ py.test -k <test_name> -v`

Per ulteriori informazioni consultare la [*documentazione*](https://docs.pytest.org/en/stable/contents.html).

### Conclusioni

Language Detector *è parte integrante* del progetto [*G-Repo*](https://github.com/MatHeartGaming/G-Repo), sviluppato in collaborazione con l'Università Degli Studi Della Basilicata :top:
