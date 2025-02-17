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
                    disciplinaSelect.innerHTML += `<option value="${disciplina.id}">${disciplina.nome}</option>`;
                });
            });
    }

    // Funzione per caricare nazioni dal backend
    function caricaNazioni() {
        fetch("/api/nazioni")
            .then(response => response.json())
            .then(data => {
                nazioneSelect.innerHTML = '<option value="">-- Seleziona una nazione --</option>';
                data.forEach(nazione => {
                    nazioneSelect.innerHTML += `<option value="${nazione.id}">${nazione.nome}</option>`;
                });
            });
    }

    // Funzione per caricare gli atleti in base a disciplina e nazione
    function caricaAtleti() {
        const disciplina = disciplinaSelect.value;
        const nazione = nazioneSelect.value;

        if (!disciplina || !nazione) {
            listaAtleti.innerHTML = "<p>Seleziona una disciplina e una nazione.</p>";
            return;
        }

        fetch(`/api/atleti?disciplina=${disciplina}&nazione=${nazione}`)
            .then(response => response.json())
            .then(data => {
                if (data.length === 0) {
                    listaAtleti.innerHTML = "<p>Nessun atleta trovato.</p>";
                } else {
                    listaAtleti.innerHTML = "<ul>" + data.map(atleta => `<li>${atleta.nome} - ${atleta.nazione}</li>`).join("") + "</ul>";
                }
            });
    }

    // Caricare discipline e nazioni al caricamento della pagina
    caricaDiscipline();
    caricaNazioni();

    // Aggiornare gli atleti quando si cambia selezione
    disciplinaSelect.addEventListener("change", caricaAtleti);
    nazioneSelect.addEventListener("change", caricaAtleti);
});
