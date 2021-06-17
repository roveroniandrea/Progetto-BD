# Progetto Basi di Dati

[Andrea Roveroni](https://github.com/roveroniandrea) mat 880092

[Leonardo Fasolato](https://github.com/leon-204863) mat 880653

[Matteo Checchin](https://github.com/MChecchin) mat 879904

# Introduzione

Come tema per il progetto abbiamo realizzato una web app per la creazione di questionari.

L'applicazione utilizza flask come framework server side e si interfaccia con il dbms Postgres tramite SQLAlchemy ORM. Si utilizza poi Flask-Login per l'autenticazione. Lato client si utilizza Bootstrap e alcune liberie javascript, quali Google Charts e Huebee JS.
L'applicazione è configurata per la connessione con un database in Postgres hostato sulla piattaforma Heroku, per la presentazione del progetto si è però utilizzato un db locale a causa di alcune limitazioni imposte da Heroku.

# Funzionalità principali

L'applicazione permette ad un utente registrato di creare questionari e condividerli con altri utenti. E' possibile scegliere tra quattro tipologie di domande da inserire:

-   domande a risposta aperta
-   domande a risposta chiusa (scelta singola)
-   domande a risposta chiusa (scelta multipla)
-   domande che accettano una risposta di tipo Date

E' inoltre possibile segnare determinate domande come "required" per far si che richiedano sempre una risposta da parte degli altri utenti.

Nella pagina home, ogni utente può visualizzare i propri questionari e quelli a cui ha accesso. Per i propri questionari inoltre, è disponibile una pagina per visualizzare le statistiche sulle risposte, come la percentuale di utenti che hanno risposto, le varie opzioni scelte e le risposte aperte fornite. E' inoltre possibile scaricare tali statistiche in formato csv.

# Progettazione della base di dati

## Schema

Lo schema della base di dati è composto da alcune tabelle:

-   Users(<ins>email</ins>, salt, digest)

    Oltre all'email che identifica univocamente un utente, la tabella contiene anche le informazioni sulla password dell'utente attraverso l'uso di digest e di un corrispondente salt. Si utilizza la funzione di hash **blake2b**. La funzione di generazione del salt è inoltre segnata come crittograficamente sicura. Si veda il paragrafo **"Autenticazione degli utenti"** per altre informazioni

-   Forms(<ins>id</ins>, title, owner\*, color, creation_date)

    Contiene le informazioni di base del questionario, tra cui il proprietario

-   Accesses(<ins>user*</ins>, <ins>form*</ins>, access_id)

    Questa tabella contiene le informazioni di accesso ai questionari. Un utente ha accesso (visualizzare e rispondere) ad un questionario se è presente la coppia (email, form_id) nella tabella. Vi è poi un terzo attributo, access_id, che se presente indica che l'utente ha già fornito una risposta al questionario, e permette di recuperare le sue risposte.

-   Questions(<ins>id</ins>, question, required, type, options, form\*)

    Le domande di ogni questionario. Vi è un campo per specificare il tipo della domanda ed eventuali opzioni in caso di domanda a risposta chiusa. Si è scelto di utilizzare una sola tabella per tutti i tipi di domande

-   Answers(<ins>id</ins>, access*, question*)

    L'attributo access è chiave esterna verso Accesses.access_id, e permette quindi di recuperare tutte le risposte di un utente dato un questionario. Vi è inoltre la chiave esterna verso la domanda a cui si riferisce questa risposta.

-   Open_answers(<ins>id\*</ins>, answer)

    A differenza della tabella Questions, si è scelto di suddividere le risposte fornite in base al loro tipo, in modo da evitare di convertire il tipo effettivo della risposta con un unico tipo di attributo. Questa tabella e le successive contengono quindi i rispettivi tipi di risposte, e puntano tutte alla tabella Answers.

-   Multiple_answers(<ins>id\*</ins>, answer)
-   Single_answers(<ins>id\*</ins>, answer)
-   Date_answers(<ins>id\*</ins>, answer)

## Sicurezza

### Ruoli

Si è definito un ruolo apposito, flask_application, che dispone solamente dei permessi minimi richiesti dall'applicazione. In particolare, tale ruolo ha i permessi di select, insert, write, update, delete sulle tabelle viste prima (solo i permessi necessari per ogni tabella) e sui vari tipi sequenza (utilizzati per assegnare un valore univoco ad alcuni attributi id delle tabelle).

Si è dovuto utilizzare un db locale poichè il piano gratuito di Heroku Postgres non permetteva la creazione di altri utenti nel db, fornendo un unico utente con permessi di admin sullo schema.

### SQL-injection

L'uso di SQLAlchemy ORM offre una protezione automatica dalla SQL injection

### Autenticazione degli utenti

Si utilizza Flask Login per l'autenticazione degli utenti. Il token della sessione è salvato in forma di cookie con le seguenti proprietà:

-   HttpOnly: il cookie non è accessibile via javascript
-   Secure: il cookie viene allegato solo su richieste effettuate tramite https
-   Expires Session: il cookie viene eliminato al termine della sessione, generalmente corrispondente alla chiusura del browser

Come visto prima, il db non salva le password degli utenti, bensì genera un salt crittograficamente sicuro (unico per ogni utente) e utilizza la funzione di hash **blake2b** per generare il digest. Digest e salt sono poi salvati assieme alla mail dell'utente. Al momento del login dell'utente viene controllato se il digest generato dal salt e dalla password inserita corrisponde a quello salvato nel db.

## Query principali

Vi sono alcune query eseguite di frequente:

-   Recupero dei questionari a cui l'utente ha accesso. Eseguita nella home page.
    ```sql
    select *
    from forms f join accesses a on f.id = a.form
    where a.user = user_email
    ```
-   Accesso al questionario dato il suo id. Eseguita quando si risponde al questionario, quando si visualizza il riepilogo delle risposte e la pagina delle statistiche. La query varia a seconda delle informazioni che si vogliono ottenere, ma un esempio potrebbe essere:

    ```sql
    select q.*,
    from forms f join accesses a on f.id = a.form join questions q on q.form = f.id
    where a.user = user_email and f.id = form_id
    ```

    Si utilizza anche la tabella Accesses in quanto si limita l'accesso al questionario solamente agli utenti specificati dal proprietario del questionario

-   Login dell'utente. La seguente query ritorna l'utente data la sua email solo se il digest corrisponde

    ```sql
    select *
    from 'users'
    where email = inserted_email and digest = computed_digest
    ```

-   Creazione del questionario. Viene effettuata un'unica transazione da SQLAlchemy ORM, che effettua gli inserimenti corretti sulle tabelle Forms, Questions e Accesses

## Performance

Analizzando la struttura dell'applicazione e le query più frequenti, abbiamo deciso di utilizzare una serie di indici sui seguenti attributi:

-   Users.email: utilizzato per il login dell'utente
-   Forms.id: utilizzato per l'accesso al questionario
-   Questions.form: utilizzato per il recupero delle domande dato il questionario
-   Accesses.user e Accesses.form: una delle tabelle più utilizzate è probabilmente Accesses. Utilizziamo quindi due vincoli, il primo per il recupero dei questionari a cui l'utente loggato ha accesso, il secondo per il recupero di tutti gli utenti che hanno accesso ad un certo questionario.

## Astrazione dal DBMS e transazioni

L'uso di SQLALchemy permette di astrarre l'applicazione dal tipo di DBMS e implementa in modo automatico le transazioni. Qualsiasi operazione al DB avviene quindi tramite transazione.

Un esempio potrebbe essere la creazione di un questionario: in caso di violazione dei vincoli di integrità (ad esempio una domanda a risposta multipla senza nessuna opzione), l'intera sequenza di operazioni viene annullata.

## Integrità

Abbiamo inserito alcuni check constraint e trigger per assicurare l'integrità dei dati. Alcuni dei vincoli sono:

-   La domanda deve avere delle opzioni tra cui scegliere solo nel caso sia a risposta chiusa. Vincolo realizzato tramite check
-   Le opzioni di una domanda devono essere distinte tra loro. Vincolo realizzato tramite check.
-   Alla risposta di un questionario, tutte le domande required devono avere una loro risposta
-   Un questionario deve avere almeno una domanda

Gli ultimi due vincoli sono stati realizzati tramite trigger DEFERRABLE INITIALLY DEFERRED. Tali trigger vengono eseguiti in seguito al commit della transazioni e possono quindi accedere a tutte le righe aggiunte/modificate. Ad esempio:

```sql
create constraint trigger tr_check_at_least_one_answer
after insert on forms
DEFERRABLE
INITIALLY DEFERRED
for each row execute function check_at_least_one_question();
```

## TODO:

"ulteriori informazioni"
