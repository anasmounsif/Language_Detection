## Language Detection

[![Python versions](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-4682B4.svg?longCache=true&style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Build Status](https://travis-ci.com/anasmounsif/Language_Detection.svg?token=7m4zb6JD1gtxhrzEgWkG&branch=master)](https://travis-ci.com/anasmounsif/Language_Detection)

Questo progetto si occupa di *analizzare* e *classificare* le repository GitHub in base alla lingua utilizzata per la stesura del **README**.

### Requisiti

```
$ pip3 install six
$ pip3 install pytest
$ pip3 install langdetect
```

### Get Started
Per utilizzare lo script individualmente, se utilizzi MacOS o Linux digitare il comando:

`$ python language_detection.py`

#### Tasks

- [x]  Generazione CSV in output contenente i risultati della classificazione e i nuovi path dopo lo spostamento.
- [x]  Spostamento delle repository in cartelle dedicate in base ai risultati della detection della lingua.
- [x]  Classificazione di tutti i README all'interno della repository.
- [x]  Generazione CSV in input contenente i path verso le repository.

#### Come Funziona

Lo script prende in input un file CSV che deve contenere le informazioni sulla posizione delle repository da analizzare:

| Index    | Path                                  |
|:--------:|---------------------------------------|
| 0        | Path assoluto della repository        |
| 1        | Path assoluto di un'altra repository  |
| ...      | ...                                   |

È possibile fornire allo script il [*nome*](https://github.com/anasmounsif/Language_Detection/blob/master/config.ini#L16) del CSV mediante l'utilizzo del file di configurazione.

###### Non hai il file input.csv

Lo script è in grado di generare automaticamente il file input.csv a partire dalla cartella dove le repository sono state clonate, tutto ciò che devi fare è settare `input_generator=1` [*qui*](https://github.com/anasmounsif/Language_Detection/blob/master/config.ini#L20) ed [*inserire*](https://github.com/anasmounsif/Language_Detection/blob/master/config.ini#L21) il path dove sono presenti le repository.

---

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

-  Misto
-  Inglese
-  Non Inglese

Le repository aventi il README assente, vuoto, con meno del [*numero minimo*](https://github.com/anasmounsif/Language_Detection/blob/master/config.ini#L10) di caratteri oppure con un'estensione non supportata verranno classificate come *Unknown*, e sarà poi cura dell'utente analizzarle manualmente.

Estensioni supportate:
-  markdown
-  mdown
-  mdwn
-  mkdn
-  mkd
-  md
-  txt

| Index    | Path                                           | Readme Analyzed | Language Detected | Code   | Percentage | Code   | Percentage |
|:--------:|------------------------------------------------|:---------------:|-------------------|:------:|:----------:|:------:|:----------:|
| 0        |  Path assoluto della repository analizzata     |  1              | `Unknown`         | //     | //         | //     | //         |
| 0        |  etc                                           |  0              | `Unknown`         | //     | //         | //     | //         |
| ...      | ...                                            | ...             | ...               | ...    | ...        | ...    | ...        |

GitHub :octocat: mette a disposizione numerosi *markdown*, quest'ultimi potrebbero influenzare la detection della lingua, perciò lo script dispone di un'ulteriore feature, ovvero quella di pulire il README analizzato dai seguenti markdown:

-  Link
-  URLs
-  HTML
-  Tabelle
-  Immagini
-  Code Snippet
-  Caratteri Speciali

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

:warning: **Per una corretta esecuzione di *Language Detection* è necessario che le repository da analizzare siano state clonate!** :warning:

#### Test

Per eseguire i test digitare da terminale il comando: `$ pytest -v` all'interno della cartella root oppure è anche possibile eseguire test specifici digitando il comando: `$ py.test -k <test_name> -v`

Per ulteriori informazioni consultare la [*documentazione*](https://docs.pytest.org/en/stable/contents.html).

### Conclusioni

Language Detection *è parte integrante* del progetto [*G-Repo*](https://github.com/MatHeartGaming/G-Repo), sviluppato in collaborazione con l'Università Degli Studi Della Basilicata :top:

---
[![MIT license](https://img.shields.io/badge/License-MIT-red.svg)](https://github.com/anasmounsif/Language_Detection/blob/master/LICENSE)
