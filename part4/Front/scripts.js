/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            // Récupérer les valeurs du formulaire
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                // Construction de la requête POST vers l’API
                const response = await fetch('http://localhost:5000/api/v1/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password }) // On envoie les identifiants en JSON
                });

                // Sélection du bloc de message dans la page
                const messageDiv = document.getElementById('message');

                if (!response.ok) {
                    // Cas d’échec : affichage d’un message rouge personnalisé
                    if (response.status === 401) {
                        messageDiv.textContent = "Identifiants incorrects. Veuillez réessayer.";
                    } else {
                        messageDiv.textContent = "Une erreur inattendue est survenue.";
                    }
                    messageDiv.style.color = "red";
                    return; // On arrête ici, inutile d'aller plus loin
                }

                try {
                    // Connexion réussie : on extrait le contenu JSON
                    const data = await response.json();

                    // Vérification explicite : le champ 'access_token' est-il présent ?
                    if (data.access_token) {
                        // Stockage du token JWT dans un cookie (encodé pour éviter les caractères spéciaux problématiques)
                        document.cookie = `access_token=${encodeURIComponent(data.access_token)}; path=/; max-age=3600`;
                        console.log('Connexion réussie ! JWT stocké dans un cookie.');
                        console.log('Tous les cookies actuels :', document.cookie);

                        // Redirection vers la page d'accueil
                        console.log('Redirection vers index.html déclenchée');
                        window.location.href = "index.html";
                    } else {
                        // Cas rare : la réponse est OK mais ne contient pas de token
                        console.error("Réponse valide, mais aucun token JWT trouvé dans la réponse.");
                        messageDiv.textContent = "Erreur : Token manquant dans la réponse.";
                        messageDiv.style.color = "red";
                    }

                } catch (jsonError) {
                    // Erreur lors du parsing JSON (ex. JSON mal formé)
                    console.error('Erreur lors du parsing JSON :', jsonError);
                }

            } catch (error) {
                // Erreur générale lors de la requête (serveur inaccessible, etc.)
                console.error('Erreur lors de la requête :', error);
            }
        });
    }
});
