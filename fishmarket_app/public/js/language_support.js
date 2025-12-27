i18next
    .use(i18nextBrowserLanguageDetector)
    .init({
        fallbackLng: "en",
        resources: {
            en: {
                translation: {
                    title: "Billingsgate Fish Market",
                    hamburger: {
                        settings: "Settings",
                        account: "My Account",
                        help: "Help",
                        logout: "Log Out"
                    },
                    settings: {
                        title: "Settings",
                        dark_mode_button: "Dark Mode",
                        font_size_label: "Font Size",
                        normal_size: "Normal",
                        large_size: "Large",
                        extra_large_size: "Extra Large",
                        language_label: "Language",
                        english_option: "English",
                        spanish_option: "Spanish",
                        french_option: "French",
                        text_to_speech: "Text to Speech"
                    },
                    dock: {
                        market: "Market",
                        reserve: "Reserve",
                        checkout: "Checkout",
                        trends: "Trends",
                        messages: "Messages",
                        mylistings: "My Listings",
                        add_listing: "Add Listing"
                    }
                }
            },
            fr: {
                translation: {
                    title: "Marché aux poissons de Billingsgate",
                    hamburger: {
                        settings: "Paramètres",
                        account: "Mon compte",
                        help: "Aide",
                        logout: "Se déconnecter"
                    },
                    settings: {
                        title: "Paramètres",
                        dark_mode_button: "Mode sombre",
                        font_size_label: "Taille de la police",
                        normal_size: "Normal",
                        large_size: "Grand",
                        extra_large_size: "Très grand",
                        language_label: "Langue",
                        english_option: "Anglais",
                        spanish_option: "Espagnol",
                        french_option: "Français",
                        text_to_speech: "Texte en parole"
                    },
                    dock: {
                        market: "Marché",
                        reserve: "Réserve",
                        checkout: "Caisse",
                        trends: "Tendances",
                        messages: "Messages",
                        mylistings: "Mes annonces",
                        add_listing: "Ajouter une annonce"
                    }
                }
            },
            es: {
                translation: {
                    title: "Mercado de Pescado Billingsgate",
                    hamburger: {
                        settings: "Configuraciones",
                        account: "Mi cuenta",
                        help: "Ayuda",
                        logout: "Cerrar sesión"
                    },
                    settings: {
                        title: "Configuraciones",
                        dark_mode: "Modo oscuro",
                        font_size_label: "Tamaño de fuente",
                        normal_size: "Normal",
                        large_size: "Grande",
                        extra_large_size: "Extra grande",
                        language_label: "Idioma",
                        english_option: "Inglés",
                        spanish_option: "Español",
                        french_option: "Francés",
                        text_to_speech: "Texto a voz"
                    },
                    dock: {
                        market: "Mercado",
                        reserve: "Reservar",
                        checkout: "Pagar",
                        trends: "Tendencias",
                        messages: "Mensajes",
                        mylistings: "Mis anuncios",
                        add_listing: "Agregar anuncio"
                    }
                }
            }
        },
        detection: {
            order: ["localStorage", "navigator"],
            caches: ["localStorage"]
        }
    }, updateContent);

function updateContent() {
    document.querySelectorAll("[data-i18n]").forEach(el => {
        const key = el.dataset.i18n;
        const attr = el.dataset.i18nAttr;

        if (attr) el.setAttribute(attr, i18next.t(key));
        else el.textContent = i18next.t(key);
    });

    const langSelect = document.getElementById("lang");
    if (langSelect) langSelect.value = i18next.language;
}

document.addEventListener("DOMContentLoaded", () => {

    const langSelect = document.getElementById("lang");

    if (!langSelect) return;

    langSelect.addEventListener("change", e => {
        i18next.changeLanguage(e.target.value, updateContent);
    });

});
