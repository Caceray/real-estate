document.addEventListener('DOMContentLoaded', function() {
    const currencyInputs = document.querySelectorAll('.currency-input');

    function formatCurrency(value) {
        const number = parseFloat(value.replace(/[^\d]/g, '') || 0);
        return new Intl.NumberFormat('fr-FR', { minimumFractionDigits: 0 }).format(number);
    }

    function parseCurrency(value) {
        return parseFloat(value.replace(/[^\d]/g, '') || 0);
    }

    function updateDisplay(e) {
        const cursorPosition = e.target.selectionStart;
        e.target.value = formatCurrency(e.target.value);
        e.target.setSelectionRange(cursorPosition, cursorPosition);
    }

    function handleFormSubmission(event) {
        event.preventDefault(); // Empêche la soumission par défaut

        currencyInputs.forEach(input => {
            input.value = parseCurrency(input.value); // Convertit en nombre avant soumission
        });

        event.target.submit(); // Soumet le formulaire
    }

    // Ajoute les écouteurs d'événements
    currencyInputs.forEach(input => {
        input.addEventListener('input', updateDisplay);
    });

    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', handleFormSubmission);
    }

    // Fonction pour formater les champs au chargement de la page
    function formatInputsOnLoad() {
        const inputs = document.querySelectorAll('.currency-input');
        inputs.forEach(input => {
            const plainValue = input.value.replace(/[^\d]/g, '');
            input.value = formatCurrency(plainValue);
        });
    }
    
    // Formate les champs au chargement de la page
    formatInputsOnLoad();
});

document.addEventListener("DOMContentLoaded", function() {
    const tabLinks = document.querySelectorAll(".tab-links a");
    const tabs = document.querySelectorAll(".tab-content .tab");

    tabLinks.forEach(function(link) {
        link.addEventListener("click", function(e) {
            e.preventDefault();

            const activeTab = document.querySelector(".tab-content .tab.active");
            const activeLink = document.querySelector(".tab-links li.active");

            if (activeTab) {
                activeTab.classList.remove("active");
            }
            if (activeLink) {
                activeLink.classList.remove("active");
            }

            this.parentNode.classList.add("active");
            const targetTab = document.querySelector(this.getAttribute("href"));
            targetTab.classList.add("active");
        });
    });
});
