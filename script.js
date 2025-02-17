document.addEventListener("DOMContentLoaded", function() {
    const disciplinaSelect = document.getElementById("disciplina-select");
    const nazioneSelect = document.getElementById("nazione-select");
    const listaAtleti = document.getElementById("lista-atleti");
    const filtraBtn = document.getElementById("filtra-btn");

    // Carica discipline dal backend
    function caricaDiscipline() {
        fetch("/api/discipline")
            .then(response => response.json())
            .then(data => {
                disciplinaSelect.innerHTML = '<option value="">Tutte le discipline</option>';
                data.forEach(disciplina => {
                    disciplinaSelect.innerHTML += `<option value="${disciplina.nome}">${disciplina.nome}</option>`;
                });
            })
            .catch(error => console.error("Errore nel caricamento delle discipline:", error));
    }

    // Carica nazioni dal backend
    function caricaNazioni() {
        fetch("/api/nazioni")
            .then(response => response.json())
            .then(data => {
                nazioneSelect.innerHTML = '<option value="">Tutte le nazioni</option>';
                data.forEach(nazione => {
                    nazioneSelect.innerHTML += `<option value="${nazione.nome}">${nazione.nome}</option>`;
                });
            })
            .catch(error => console.error("Errore nel caricamento delle nazioni:", error));
    }

    // Funzione per caricare atleti filtrati
    function caricaAtleti() {
        const disciplina = disciplinaSelect.value;
        const nazione = nazioneSelect.value;

        let url = "/api/atleti?";
        if (disciplina) url += `disciplina=${encodeURIComponent(disciplina)}&`;
        if (nazione) url += `nazione=${encodeURIComponent(nazione)}`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (data.length === 0) {
                    listaAtleti.innerHTML = "<p>Nessun atleta trovato.</p>";
                    return;
                }

                // Raggruppa gli atleti per nazione
                const atletiPerNazione = {};
                data.forEach(atleta => {
                    if (!atletiPerNazione[atleta.nazione]) {
                        atletiPerNazione[atleta.nazione] = [];
                    }
                    atletiPerNazione[atleta.nazione].push(atleta);
                });

                // Mostra gli atleti divisi per nazione
                listaAtleti.innerHTML = "";
                for (const nazione in atletiPerNazione) {
                    const sezione = document.createElement("div");
                    sezione.classList.add("nazione-sezione");
                    sezione.innerHTML = `<h3>${nazione}</h3><ul>` +
                        atletiPerNazione[nazione].map(atleta => `<li>${atleta.nome} (${atleta.disciplina})</li>`).join("") +
                        `</ul>`;
                    listaAtleti.appendChild(sezione);
                }
            })
            .catch(error => {
                console.error("Errore nel caricamento degli atleti:", error);
                listaAtleti.innerHTML = "<p>Errore nel caricamento degli atleti.</p>";
            });
    }

    // Carica le discipline e nazioni al caricamento della pagina
    caricaDiscipline();
    caricaNazioni();

    // Attiva il filtraggio solo al click sul pulsante
    filtraBtn.addEventListener("click", caricaAtleti);
});
