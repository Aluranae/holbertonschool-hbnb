document.addEventListener('DOMContentLoaded', () => {
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
                displayMessage(error.message || 'Une erreur inattendue est survenue.');
                console.error('Erreur capturée : ', error);
            }
        });
    }
    // Remplissage dynamique du menu déroulant de prix
    populatePriceFilter();

    // Vérifie le status de l'authentification au chargement d'index.html
    checkAuthentication();

    // Ecouteur d'événement sur le menu déroulant de prix
    // Chaque changement déclenche le filtrage dynamique des logements affichés
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', () => {
            const maxPrice = priceFilter.value;
            filterPlacesByPrice(maxPrice);
        });
    }

    if (document.body.classList.contains('place-detail-page')) {
        const placeId = getPlaceIdFromURL();
        console.log('PlaceId:', placeId);
        const token = getCookie('access_token');
        console.log('Token JWT trouvé :', token);
        console.log('ID du logement extrait de l’URL :', placeId);

        const addReviewSection = document.getElementById('add-review');
        if (!token && addReviewSection) {
            addReviewSection.style.display = 'none';
        } else if (addReviewSection) {
            addReviewSection.style.display = 'block';
        }
        fetchPlaceDetails(token, placeId);
    }

    // Ecouteur d’événement du formulaire
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        const token = getCookie('access_token');

    if (token) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const textReview = document.getElementById('review').value;
            const note = document.getElementById('rating').value;
            const idPlace = getPlaceIdFromURL();

            if (textReview.trim() === '' || note === '' || token === null || idPlace === null) {
                displayMessage('Tous les champs doivent être remplis');
                return;
            }

            console.log('Token JWT :', token);
            console.log('ID du logement :', idPlace);
            console.log('Texte de l’avis :', textReview);
            console.log('Note :', note);

            await submitReview(token, idPlace, textReview, note);
        });
    }
}


    const logoutButton = document.getElementById('logout-button');
    if (logoutButton) {
        logoutButton.addEventListener('click', logoutUser);
    }

    if (document.body.classList.contains('landing-page')) {
        const logo = document.querySelector('.logo-landing');
        const sound = document.getElementById('landing-sound');

        if (logo && sound) {
            logo.addEventListener('click', (event) => {
                event.preventDefault(); // bloque la redirection immédiate
                sound.currentTime = 0;
                sound.play();

                // Ajout de la classe visuelle
                logo.classList.add('glow-pulse');

                // Redirection après 0.6 seconde
                setTimeout(() => {
                    logo.classList.remove('glow-pulse'); // nettoyage
                    window.location.href = 'index.html';
                }, 600);
            });
        }
    }

});

/**
 * Fonction asynchrone de connexion.
 * @param {string} email - Adresse email saisie par l'utilisateur
 * @param {string} password - Mot de passe saisi par l'utilisateur
 * @throws {Error} en cas d'échec de requête, de réponse invalide ou de token manquant
 * Effectue la requête de connexion vers l'API et gère le stockage du token en cookie.
 * Le cookie est configuré avec ou sans 'Secure' selon l'environnement (localhost ou HTTPS).
 */
async function loginUser (email, password) {
    // Appel API pour authentification
    const response = await fetch('http://localhost:5000/api/v1/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password }) // envoie les identifiants sous forme JSON
    });

    // Gestion d’échec HTTP (ex: 401 ou 500)
    if (!response.ok) {
        const message = response.status === 401
            ? 'Identifiants incorrects. Veuillez réessayer.'
            : 'Erreur serveur lors de la connexion.';
        displayMessage(message);
        throw new Error(message);
    }

    let data;
    try {
        // Parsing JSON sécurisé
        data = await response.json();
    } catch (jsonError) {
        throw new Error('Réponse JSON invalide.');
    }

    // Vérification de la présence du token
    if (!data.access_token) {
        throw new Error('Token JWT manquant dans la réponse.');
    }

    // Préparation du cookie JWT via fonction dédiée
    const cookie = buildAuthCookie(data.access_token);

    // Stockage du cookie dans le navigateur
    document.cookie = cookie;

    // journalisation du cookie pour debug
    console.log('Connexion réussie. JWT stocké dans un cookie.');
    console.log('Cookies : ', document.cookie);

    // Redirection vers la page principale
    console.log('Redirection vers index.html déclenchée.');
    window.location.href = 'index.html';
}

/**
 * Génère une chaîne de cookie JWT bien formée.
 * @param {string} token - Le JWT à stocker
 * @param {number} maxAgeSeconds - Durée de vie en secondes (défaut : 3600)
 * @returns {string} - La chaîne du cookie prête à être assignée à document.cookie
 */
function buildAuthCookie(token, maxAgeSeconds = 3600) {
    const encodedToken = encodeURIComponent(token);
    const expiry = new Date(Date.now() + maxAgeSeconds * 1000).toUTCString();
    const isLocalhost = ['localhost', '127.0.0.1'].includes(window.location.hostname);

    let cookie = `access_token=${encodedToken}; path=/; expires=${expiry}; SameSite=Lax`;
    if (!isLocalhost) {
        cookie += '; Secure';
    }

    return cookie;
}

/**
 * Affiche un message dans la div #message avec une couleur personnalisable.
 * Par défaut, le message est rouge pour signaler une erreur.
 * Cette fonction peut aussi afficher un succès (vert), une info (bleu), ou autre.
 *
 * @param {string} text - Le texte à afficher.
 * @param {string} color - La couleur du message rouge par défaut.
 */
function displayMessage (text, color = 'red') {
    const messageDiv = document.getElementById('message');
    if (!messageDiv) {
        console.warn("Aucune div avec l'id 'message' trouvée");
        return;
    }

    // Mise à jour du texte et de la couleur
    messageDiv.textContent = text;
    messageDiv.style.color = color;

    // visibilité automatique
    messageDiv.style.display = 'block';

    // masquage automatique après 5 secondes
    setTimeout(() => {
        messageDiv.textContent = '';
        messageDiv.style.display = 'none';
    }, 5000);
}

/**
 * Décode le payload d’un JWT (JSON Web Token) sans vérification de signature.
 * @param {string} token - Le token JWT complet (3 parties séparées par des points)
 * @returns {Object|null} - Le payload décodé (objet), ou null si erreur
 */
function parseJwt(token) {
    try {
        const payloadBase64 = token.split('.')[1]; // extraction du payload
        const payloadDecoded = atob(payloadBase64.replace(/-/g, '+').replace(/_/g, '/')); // décode base64
        return JSON.parse(payloadDecoded); // parse JSON
    } catch (error) {
        console.error('Échec du décodage du JWT :', error);
        return null;
    }
}

/**
 * Récupère la valeur d'un cookie à partir de son nom.
 * @param {string} name - Le nom du cookie à chercher
 * @returns {string|null} - La valeur du cookie, ou null s’il n’existe pas
 */
function getCookie(name) {
    const cookies = document.cookie.split('; ');
    for (let c of cookies) {
        const [key, value] = c.split('=');
        if (key === name) return decodeURIComponent(value);
    }
    return null;
}

// Vérification du token
function checkAuthentication() {
  const token = getCookie('access_token');
  const loginLink = document.getElementById('login-link');
  const logoutButton = document.getElementById('logout-button');

  if (!token) {
    if (loginLink) {
      loginLink.style.display = 'inline-block';
    }
    if (logoutButton) {
      logoutButton.style.display = 'none';
    }
  } else {
    if (loginLink) {
      loginLink.style.display = 'none';
    }
    if (logoutButton) {
      logoutButton.style.display = 'inline-block';
    }
  }

  // Appel de fetchPlaces dans tous les cas
  if (document.getElementById('places-list')) {
    fetchPlaces(token);
  }
}


/**
 * Récupère les données des logements via l'API.
 * @param {string} token - Le JWT à inclure dans la requête
 * Cette fonction appelle ensuite displayPlaces(data) pour afficher les logements.
 */
async function fetchPlaces(token) {
    try {
        // Appel API pour Places
        const response = await fetch('http://localhost:5000/api/v1/places/', {
            method: 'GET',
            headers: token
                ? {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                  }
                : {
                    "Content-Type": "application/json"
                  }
        });

        // Gestion d’échec HTTP (ex: 401 ou 500)
        if (!response.ok) {
            const message = response.status === 401
                ? 'Authentification requise pour accéder aux logements.'
                : response.status === 500
                    ? 'Erreur interne du serveur lors de la récupération des logements.'
                    : 'Impossible de récupérer les données. Réessayez plus tard.';
            displayMessage(message);
            throw new Error(message);
        }

        // Parsing JSON sécurisé
        let data
        try {
            data = await response.json();
            console.log('Données brutes reçues de l’API :', data);
        } catch (jsonError) {
            displayMessage('Erreur : la réponse du serveur n’est pas un JSON valide.');
            throw new Error('Réponse JSON invalide.');
        }

        // Vérifie que data.places est bien un tableau
        if (!Array.isArray(data.places)) {
            displayMessage('Erreur : données de logements invalides.');
            throw new Error('La clé "places" est absente ou incorrecte dans la réponse.');
        }
        
        displayPlaces(data.places);

    } catch (error) {
        console.error('Erreur lors de la récupération des logements : ', error);
        displayMessage('Erreur lors du chargement des logements');
    }    
}

/**
 * Affiche dynamiquement les logements dans la section #places-list
 * @param {Array} places - Liste des logements à afficher
 */
function displayPlaces(places) {
    // Sélectionner l'élément #places-list
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    // Vider le contenu existant pour éviter les doublons
    placesList.textContent = '';

    // Vérifier que places est bien un tableau
    if (!Array.isArray(places)) {
        displayMessage('Erreur inattendue : la liste des logements est corrompue.');
        throw new Error('Données inattendues : places devrait être un tableau.');
    }

    // Parcourir la liste des logements
    for (const place of places) {
        console.log(place); // pour debug

    // création de la carte pour un logement.
    const card = document.createElement('div');
    card.classList.add('place-card');

    // Ajout d'image
    const img = document.createElement('img');
    img.src = place.image_url || 'images/default.png';
    img.alt = place.title || place.name || 'Image logement';
    img.classList.add('place-image');
    card.appendChild(img);

    // Titre du logement (fallback : 'Logement sans nom')
    const title = document.createElement('h3');
    title.textContent = place.name || place.title || 'Logement sans nom';
    card.appendChild(title);

    // Prix par nuit (fallback : 'Non renseigné')
    const price = document.createElement('p');
    const priceValue = place.price || place.price_per_night || 'Non renseigné';
    price.innerHTML = `Prix par nuit: <strong>${priceValue} crédits</strong>`;
    card.appendChild(price);

    // Description du logement (fallback : 'Aucune description fournie.')
    const description = document.createElement('p');
    description.textContent = place.description || 'Aucune description fournie.';
    card.appendChild(description);

    // Bouton "Détails"
    const button = document.createElement('button');
    button.textContent = 'Détails';
    button.classList.add('details-button');
    button.setAttribute('data-id', place.id);
    button.addEventListener('click', (event) => {
        const id = event.target.dataset.id;
        console.log(`Vous avez cliqué sur le logoment avec l'id ${id}`);
        window.location.href = `place.html?id=${id}`;
    });
    card.appendChild(button);

    // ajout de la carte au DOM
    placesList.appendChild(card);
    }
}

/**
 * Remplit dynamiquement le menu déroulant de filtre de prix.
 * Doit être appelée au chargement de la page.
 */
function populatePriceFilter() {
  const priceFilter = document.getElementById('price-filter');
  if (!priceFilter) return;

  const options = [
    { value: '10', label: 'Max 10' },
    { value: '50', label: 'Max 50' },
    { value: '100', label: 'Max 100' },
    { value: 'all', label: 'All prices' }
  ];

  options.forEach(opt => {
    const optionElement = document.createElement('option');
    optionElement.value = opt.value;
    optionElement.textContent = opt.label;
    priceFilter.appendChild(optionElement);
  });
}

/**
 * Filtre les logements affichés selon le prix maximal sélectionné.
 * @param {string} maxPrice - Valeur sélectionnée dans le menu (ex: '10', '50', 'all')
 */
function filterPlacesByPrice(maxPrice) {
  const cards = document.querySelectorAll('.place-card');

  cards.forEach(card => {
    const priceText = card.querySelector('p').textContent;
    const match = priceText.match(/(\d+)/); // extrait le premier nombre (le prix)
    
    if (!match) return; // sécurité : ignore si aucun prix trouvé

    const price = parseInt(match[1]);

    if (maxPrice === 'all' || price <= parseInt(maxPrice)) {
      card.style.display = 'flex';
    } else {
      card.style.display = 'none';
    }
  });
}

/**
 * Extrait l'identifiant d’un logement depuis les paramètres de l’URL.
 * @returns {string|null} - L’ID du logement si présent, sinon null.
 */
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}


/**
 * Récupère les détails d’un logement (Place) via l’API.
 * @param {string} token - Le JWT pour l'autorisation
 * @param {string} placeId - L'ID du logement à récupérer
 */
async function fetchPlaceDetails(token, placeId) {
    try {
        // Appel API pour récupérer un logement spécifique
        const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
        });

        // Vérifie que la réponse HTTP est valide (code 200-299). Affiche une erreur sinon
        if (!response.ok) {
            const message = response.status === 401
                ? 'Authentification requise pour accéder aux logements.'
                : response.status === 500
                    ? 'Erreur interne du serveur lors de la récupération des logements.'
                    : 'Impossible de récupérer les données. Réessayez plus tard.';
            displayMessage(message);
            throw new Error(message);
        }

        // Tentative de conversion de la réponse en JSON. Gère les erreurs de parsing.
        let place;
        try {
            place = await response.json();
            console.log('Données brutes reçues de l’API :', place);
        } catch (jsonError) {
            displayMessage('Erreur : la réponse du serveur n’est pas un JSON valide.');
            throw new Error('Réponse JSON invalide.');
        }

        // On passe directement l’objet place (car pas encapsulé dans { place: ... })
        displayPlaceDetails(place);

    } catch (error) {
        console.error('Erreur lors de la récupération des logements : ', error);
        displayMessage('Erreur lors du chargement des logements');
    }
}


/**
 * Affiche dynamiquement les détails d’un logement dans la page place.html
 * @param {Object} place - L’objet contenant toutes les données du logement
 */
function displayPlaceDetails(place) {
    const placeInfo = document.querySelector('.place-info')
    if (!placeInfo) return;

    // Vider son contenu pour éviter les doublons
    placeInfo.textContent = '';

    // Bloc titre
    const titleBlock = document.createElement('div');
    titleBlock.classList.add('title-block');

    const title = document.createElement('h2');
    title.textContent = place.name || place.title || 'Logement sans nom';

    titleBlock.appendChild(title);

    placeInfo.appendChild(titleBlock);

    // Image du logement
    const image = document.createElement('img');
    image.src = place.image_url || 'images/default.png';
    image.alt = place.title || place.name || 'Image du logement';
    image.classList.add('place-detail-image');
    placeInfo.appendChild(image);

    // Conteneur (prix + description)
    const infoRow = document.createElement('div');
    infoRow.classList.add('info-row');

    // Bloc prix
    const priceBlock = document.createElement('div');
    priceBlock.classList.add('price-block');

    const price = document.createElement('p');
    const priceValue = place.price || place.price_per_night || 'Non renseigné';
    price.innerHTML = `Prix par nuit: <strong>${priceValue} crédits</strong>`;

    priceBlock.appendChild(price);

    infoRow.appendChild(priceBlock);

    // Bloc description
    const descriptionBlock = document.createElement('div');
    descriptionBlock.classList.add('description-block');

    const description = document.createElement('p');
    description.textContent = place.description || 'Aucune description fournie.';

    descriptionBlock.appendChild(description);

    infoRow.appendChild(descriptionBlock);

    placeInfo.appendChild(infoRow);

    // Bloc commodités
    const amenitiesBlock = document.createElement('div');
    amenitiesBlock.classList.add('amenities-block');

    // Titre de la section des commodités
    const amenitiesTitle = document.createElement('h4');
    amenitiesTitle.textContent = 'Commodités disponibles';
    amenitiesBlock.appendChild(amenitiesTitle);

    // Conteneur des commodités
    const amenitiesList = document.createElement('ul');
    if (Array.isArray(place.amenities)) {
        for (const amenity of place.amenities) {
            const item = document.createElement('li');
            item.textContent = amenity.name || amenity.title || 'Commodité inconnue';
            amenitiesList.appendChild(item);
        }
        
    }
    amenitiesBlock.appendChild(amenitiesList);

    // Conteneur propriétaire
    const ownerBlock = document.createElement('div');
    ownerBlock.classList.add('owner-block');

    // Titre du bloc propriétaire
    const ownerTitle = document.createElement('h4');
    ownerTitle.textContent = 'Propriétaire :';
    ownerBlock.appendChild(ownerTitle);

    // Contenu du bloc
    const ownerContent = document.createElement('div');
    ownerContent.classList.add('owner-content');
    ownerBlock.appendChild(ownerContent);

    // Prénom + Nom
    const ownerName = document.createElement('p');
    ownerName.textContent = `${place.owner.first_name || ''} ${place.owner.last_name || ''}`;
    ownerContent.appendChild(ownerName);

    // Photo du propriétaire (ou image par défaut)
    const ownerImage = document.createElement('img');
    ownerImage.src = place.owner.profile_pic || 'images/default_user.png';
    ownerImage.alt = `${place.owner.first_name || 'Propriétaire'} ${place.owner.last_name || ''}`;
    ownerImage.classList.add('owner-photo');
    ownerContent.appendChild(ownerImage);

    // Conteneur aligné pour Commodités + Propriétaire
    const infoExtrasRow = document.createElement('div');
    infoExtrasRow.classList.add('info-extras-row');

    infoExtrasRow.appendChild(amenitiesBlock);
    infoExtrasRow.appendChild(ownerBlock);

    placeInfo.appendChild(infoExtrasRow);

    // Bloc avis
    const reviewsBlock = document.createElement('div');
    reviewsBlock.classList.add('reviews-block');

    if (Array.isArray(place.reviews)) {
        // Titre de la section des avis
        const reviewTitle = document.createElement('h4');
        reviewTitle.textContent = 'Avis des utilisateurs';
        reviewsBlock.appendChild(reviewTitle);

        // Affichage des avis
        for (const review of place.reviews) {
            const item = document.createElement('p');
            item.textContent = `${review.user?.first_name || 'Auteur'} ${review.user?.last_name || ''} : ${review.text || 'Aucun avis'}`;
            reviewsBlock.appendChild(item);
        }

        // Ajout du bloc des avis dans la nouvelle div
        const reviewsContainer = document.querySelector('#place-reviews');
        if (reviewsContainer) {
            reviewsContainer.textContent = ''; // vide avant de recharger
            reviewsContainer.appendChild(reviewsBlock);
        }
    }
}

/**
 * Envoie un avis utilisateur pour un logement donné à l’API.
 * @param {string} token - Le token JWT pour l’authentification
 * @param {string} placeId - L’ID du logement concerné
 * @param {string} reviewText - Le texte de l’avis saisi par l’utilisateur
 * @param {string|number} rating - La note attribuée (1 à 5)
 */
async function submitReview(token, placeId, reviewText, rating) {
    try {

        // Décoder le token pour extraire l’ID utilisateur
        const tokenPayload = parseJwt(token);
        const userId = tokenPayload.sub || tokenPayload.id;

        if (!userId) {
            throw new Error('Impossible d’extraire l’ID utilisateur depuis le token.');
        }

        console.log('userId extrait du token :', userId);

        // Appel API pour récupérer un logement spécifique
        const response = await fetch(`http://localhost:5000/api/v1/reviews/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: reviewText,
                rating: parseInt(rating),
                user_id: userId,
                place_id: placeId,
            })
        });
        // Vérifie que la réponse HTTP est valide. Affiche une erreur sinon
        if (!response.ok) {
            const message = response.status === 401
                ? 'Authentification requise pour accéder aux logements.'
                : response.status === 500
                    ? 'Erreur interne du serveur lors de la récupération des logements.'
                    : 'Impossible de récupérer les données. Réessayez plus tard.';
            displayMessage(message);
            throw new Error(message);
        }

        // Tentative de conversion de la réponse en JSON. Gère les erreurs de parsing.
        let place;
        try {
            place = await response.json();
            console.log('Données brutes reçues de l’API :', place);
        } catch (jsonError) {
            displayMessage('Erreur : la réponse du serveur n’est pas un JSON valide.');
            throw new Error('Réponse JSON invalide.');
        }

        displayMessage('Avis soumis avec succès !', 'green');
        document.getElementById('review-form').reset();

        // Tentative de rafrachissement des avis dynamiquement
        try {
            fetchPlaceDetails(token, placeId);
        } catch (refreshError) {
            console.warn("L'avis a bien été envoyé, mais le rafraîchissement automatique a échoué :", refreshError);
        }

    } catch (error) {
        console.error('Erreur lors de la récupération des logements : ', error);
        displayMessage('Erreur lors du chargement des logements');
    }
}

/**
 * Déconnecte l'utilisateur en supprimant le cookie JWT
 * puis redirige vers la page de connexion.
 */
function logoutUser() {
    // Expire le cookie immédiatement
    document.cookie = 'access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC; SameSite=Lax';

    // journalisation
    console.log('Déconnexion effectuée. Cookie supprimé.');

    // Redirection vers la page de login
    window.location.href = 'login.html';
}
