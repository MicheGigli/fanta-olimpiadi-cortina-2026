document.addEventListener("DOMContentLoaded", function () {
    const apiBaseUrl = "https://fanta-olimpiadi-cortina-2026.onrender.com/api";

    const disciplinaSelect = document.getElementById("disciplina-select");
    const nazioneSelect = document.getElementById("nazione-select");
    const listaAtleti = document.getElementById("lista-atleti");
    const filtraBtn = document.getElementById("filtra-btn");
    const loadingIndicator = document.getElementById("loading");

    // Carica discipline dal backend
    async function caricaDiscipline() {
        try {
            const response = await fetch(`${apiBaseUrl}/discipline`);
            const data = await response.json();
            disciplinaSelect.innerHTML = '<option value="">Tutte le discipline</option>';
            data.forEach(disciplina => {
                disciplinaSelect.innerHTML += `<option value="${disciplina.id}">${disciplina.nome}</option>`;
            });
        } catch (error) {
            console.error("Errore nel caricamento delle discipline:", error);
        }
    }

    // Carica nazioni dal backend
    async function caricaNazioni() {
        try {
            const response = await fetch(`${apiBaseUrl}/nazioni`);
            const data = await response.json();
            nazioneSelect.innerHTML = '<option value="">Tutte le nazioni</option>';
            data.forEach(nazione => {
                nazioneSelect.innerHTML += `<option value="${nazione.id}">${nazione.nome}</option>`;
            });
        } catch (error) {
            console.error("Errore nel caricamento delle nazioni:", error);
        }
    }

    // Funzione per caricare atleti filtrati
    async function caricaAtleti() {
        const disciplinaId = disciplinaSelect.value;
        const nazioneId = nazioneSelect.value;

        let url = `${apiBaseUrl}/atleti`;
        const params = new URLSearchParams();
        if (disciplinaId) params.append("disciplina", disciplinaId);
        if (nazioneId) params.append("nazione", nazioneId);
        if (params.toString()) url += `?${params.toString()}`;

        try {
            loadingIndicator.style.display = "block"; // Mostra il caricamento
            listaAtleti.innerHTML = ""; // Pulisce la lista

            const response = await fetch(url);
            const data = await response.json();

            loadingIndicator.style.display = "none"; // Nasconde il caricamento

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
        } catch (error) {
            console.error("Errore nel caricamento degli atleti:", error);
            listaAtleti.innerHTML = "<p>Errore nel caricamento degli atleti.</p>";
        } finally {
            loadingIndicator.style.display = "none"; // Nasconde il caricamento in caso di errore
        }
    }

    // Inizializzazione
    caricaDiscipline();
    caricaNazioni();

    // Filtra atleti al click del pulsante
    filtraBtn.addEventListener("click", caricaAtleti);
});
