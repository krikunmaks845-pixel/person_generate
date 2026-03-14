// static/js/main.js
// Приклад інтеграції з Flask бекендом

class CurrencyApp {
    constructor() {
        this.currencies = [];
        this.rates = {};
        this.init();
    }

    async init() {
        await this.loadCurrencies();
        this.setupEventListeners();
        this.populateSelects();
        this.populateCurrencyGrid();
    }

    setupEventListeners() {
        // Форма конвертації
        document.getElementById('converterForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.convertCurrency();
        });

        // Кнопка обміну валют
        document.getElementById('swapButton').addEventListener('click', () => {
            this.swapCurrencies();
        });

        // Пошук валют
        document.getElementById('searchInput').addEventListener('input', (e) => {
            this.filterCurrencies(e.target.value);
        });

        // Автоматична конвертація при зміні суми
        document.getElementById('fromAmount').addEventListener('input', () => {
            this.convertCurrency();
        });

        // Автоматична конвертація при зміні валюти
        document.getElementById('fromCurrency').addEventListener('change', () => {
            this.convertCurrency();
        });

        document.getElementById('toCurrency').addEventListener('change', () => {
            this.convertCurrency();
        });
    }

    async loadCurrencies() {
        try {
            const response = await fetch('/api/currencies');
            this.currencies = await response.json();
        } catch (error) {
            console.error('Помилка завантаження валют:', error);
        }
    }

    populateSelects() {
        const fromSelect = document.getElementById('fromCurrency');
        const toSelect = document.getElementById('toCurrency');

        // Зберігаємо поточні вибрані значення
        const fromValue = fromSelect.value;
        const toValue = toSelect.value;

        // Очищуємо селекти
        fromSelect.innerHTML = '';
        toSelect.innerHTML = '';

        // Заповнюємо селекти
        this.currencies.forEach(currency => {
            const option1 = new Option(
                `${currency.code} - ${currency.name}`,
                currency.code
            );
            const option2 = option1.cloneNode(true);

            fromSelect.add(option1);
            toSelect.add(option2);
        });

        // Відновлюємо вибрані значення
        fromSelect.value = fromValue;
        toSelect.value = toValue;
    }

    populateCurrencyGrid() {
        const grid = document.getElementById('currencyGrid');
        grid.innerHTML = '';

        this.currencies.forEach(currency => {
            const item = document.createElement('div');
            item.className = 'currency-item';
            item.innerHTML = `
                <div>
                    <div class="currency-code">${currency.code}</div>
                    <div class="currency-name">${currency.name}</div>
                </div>
                <div class="currency-rate">${currency.rate.toFixed(4)}</div>
            `;

            // Додаємо можливість вибору валюти з сітки
            item.addEventListener('click', () => {
                document.getElementById('toCurrency').value = currency.code;
                this.convertCurrency();
            });

            grid.appendChild(item);
        });
    }

    filterCurrencies(searchTerm) {
        const items = document.querySelectorAll('.currency-item');
        const term = searchTerm.toLowerCase();

        items.forEach(item => {
            const code = item.querySelector('.currency-code').textContent.toLowerCase();
            const name = item.querySelector('.currency-name').textContent.toLowerCase();

            if (code.includes(term) || name.includes(term)) {
                item.style.display = 'flex';
            } else {
                item.style.display = 'none';
            }
        });
    }

    async convertCurrency() {
        const amount = parseFloat(document.getElementById('fromAmount').value);
        const from = document.getElementById('fromCurrency').value;
        const to = document.getElementById('toCurrency').value;

        if (!amount || amount <= 0) {
            this.showPlaceholder();
            return;
        }

        try {
            const response = await fetch('/api/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ amount, from, to })
            });

            const data = await response.json();

            if (data.result) {
                this.displayResult(data);
                document.getElementById('toAmount').value = data.result.toFixed(2);
            }
        } catch (error) {
            console.error('Помилка конвертації:', error);
        }
    }

    displayResult(data) {
        const resultArea = document.getElementById('resultArea');
        resultArea.innerHTML = `
            <div class="result-value">${data.result.toFixed(2)} ${data.to}</div>
            <div class="result-rate">1 ${data.from} = ${data.rate.toFixed(4)} ${data.to}</div>
        `;
    }

    showPlaceholder() {
        const resultArea = document.getElementById('resultArea');
        resultArea.innerHTML = `
            <p class="placeholder-text">Введіть суму та виберіть валюти для конвертації</p>
        `;
        document.getElementById('toAmount').value = '';
    }

    swapCurrencies() {
        const fromSelect = document.getElementById('fromCurrency');
        const toSelect = document.getElementById('toCurrency');

        const temp = fromSelect.value;
        fromSelect.value = toSelect.value;
        toSelect.value = temp;

        this.convertCurrency();
    }
}

// Ініціалізація додатку при завантаженні сторінки
document.addEventListener('DOMContentLoaded', () => {
    new CurrencyApp();
});