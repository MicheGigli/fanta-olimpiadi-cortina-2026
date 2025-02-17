document.addEventListener("DOMContentLoaded", function() {
    const disciplinaSelect = document.getElementById("disciplina-select");
    const nazioneSelect = document.getElementById("nazione-select");
    const listaAtleti = document.getElementById("lista-atleti");

    // Funzione per caricare discipline dal backend
    function caricaDiscipline() {
        fetch("/api/discipline")
            .then(response => response.json())
            .then(data => {
                disciplinaSelect.innerHTML = '<option value="">-- Seleziona una disciplina --</option>';
                data.forEach(disciplina => {
                    disciplinaSelect.innerHTML += `<option value="${disciplina.nome}">${disciplina.nome}</option>`;
                });
            })
            .catch(error => console.error("Errore nel caricamento delle discipline:", error));
    }

    // Funzione per caricare nazioni dal backend
    function caricaNazioni() {
        fetch("/api/nazioni")
            .then(response => response.json())
            .then(data => {
                nazioneSelect.innerHTML = '<option value="">-- Seleziona una nazione --</option>';
                data.forEach(nazione => {
                    nazioneSelect.innerHTML += `<option value="${nazione.nome}">${nazione.nome}</option>`;
                });
            })
            .catch(error => console.error("Errore nel caricamento delle nazioni:", error));
    }

    // Funzione per caricare gli atleti in base a disciplina e nazione
    function caricaAtleti() {
        const disciplina = disciplinaSelect.value;
        const nazione = nazioneSelect.value;

        if (!disciplina || !nazione) {
            listaAtleti.innerHTML = "<p>Seleziona una disciplina e una nazione.</p>";
            return;
        }

        fetch(`/api/atleti?disciplina=${encodeURIComponent(disciplina)}&nazione=${encodeURIComponent(nazione)}`)
            .then(response => response.json())
            .then(data => {
                if (data.length === 0) {
                    listaAtleti.innerHTML = "<p>Nessun atleta trovato.</p>";
                } else {
                    listaAtleti.innerHTML = "<ul>" + data.map(atleta => `<li>${atleta.nome} (${atleta.nazione})</li>`).join("") + "</ul>";
                }
            })
            .catch(error => {
                console.error("Errore nel caricamento degli atleti:", error);
                listaAtleti.innerHTML = "<p>Errore nel caricamento degli atleti.</p>";
            });
    }

    // Caricare discipline e nazioni al caricamento della pagina
    caricaDiscipline();
    caricaNazioni();

    // Aggiornare gli atleti quando si cambia selezione
    disciplinaSelect.addEventListener("change", caricaAtleti);
    nazioneSelect.addEventListener("change", caricaAtleti);
});
