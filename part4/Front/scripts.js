ocument.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            // Récupérer les valeurs du formulaire
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                // Appel de la fonction loginUser avec les identifiants
                await loginUser(email, password);
            } catch (error) {
                // Affichage de l’erreur dans l’interface utilisateur
                const messageDiv = document.getElementById('message');
                messageDiv.textContent = error.message || "Erreur inconnue lors de la connexion.";
                messageDiv.style.color = "red";
                console.error("Erreur capturée : ", error);
            }
        });
    }
});

/**
 * Fonction asynchrone de connexion.
 * @param {string} email - Adresse email saisie par l'utilisateur
 * @param {string} password - Mot de passe saisi par l'utilisateur
 * @throws {Error} en cas d'échec de requête, de réponse invalide ou de token manquant
 */
async function loginUser(email, password) {
    // Appel API pour authentification
    const response = await fetch('http://localhost:5000/api/v1/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password }) // On envoie les identifiants sous forme JSON
    });

    // Gestion d’échec HTTP (ex: 401 ou 500)
    if (!response.ok) {
        const message = response.status === 401
            ? "Identifiants incorrects. Veuillez réessayer."
            : "Erreur serveur lors de la connexion.";
        throw new Error(message);
    }

    let data;
    try {
        // Parsing JSON sécurisé
        data = await response.json();
    } catch (jsonError) {
        throw new Error("Réponse JSON invalide.");
    }

    // Vérification de la présence du token
    if (!data.access_token) {
        throw new Error("Token JWT manquant dans la réponse.");
    }

    // Stockage du token dans un cookie (encodé, pour 1 heure)
    document.cookie = `access_token=${encodeURIComponent(data.access_token)}; path=/; max-age=3600`;

    // Optionnel : journalisation du cookie pour debug
    console.log("Connexion réussie. JWT stocké dans un cookie.");
    console.log("Cookies : ", document.cookie);

    // Redirection vers la page principale
    console.log("Redirection vers index.html déclenchée.");
    window.location.href = "index.html";
}
