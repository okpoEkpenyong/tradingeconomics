document.getElementById('compareForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const indicator = document.getElementById('indicator').value.trim().toLowerCase();
    const country1 = document.getElementById('country1').value.trim();
    const country2 = document.getElementById('country2').value.trim();
    const freeCountries = ['Sweden', 'Mexico', 'New Zealand', 'Thailand'];

    const resultsDiv = document.getElementById('results');
    clearElement(resultsDiv);

    // Validate countries (case-insensitive)
    if (
        !freeCountries.map(c => c.toLowerCase()).includes(country1.toLowerCase()) || 
        !freeCountries.map(c => c.toLowerCase()).includes(country2.toLowerCase())
    ) {
        const errorMsg = createErrorMessage(
            `Invalid country selection. Please choose from: ${freeCountries.join(', ')}.`
        );
        resultsDiv.appendChild(errorMsg);
        return;
    }

    // Show loading spinner
    const spinner = createSpinner();
    resultsDiv.appendChild(spinner);

    try {
        const response = await fetch(`/api/compare?country1=${country1}&country2=${country2}&indicator=${indicator}`);
        const data = await response.json();

        clearElement(resultsDiv); // Clear spinner

        if (!response.ok) {
            const errorMsg = createErrorMessage(`Error: ${data.error || "Unexpected server error."}`);
            resultsDiv.appendChild(errorMsg);
            return;
        }

        // Create and display GDP comparison table
        const tableContainer = createTable(data.country1_data, data.country2_data, country1, country2, indicator);
        resultsDiv.appendChild(tableContainer);

        // Create and append "Plot Data" button
        const plotButton = createButton('Plot Data', 'plotButton');
        resultsDiv.appendChild(plotButton);

        // Create and append chart canvas (hidden by default)
        const chartCanvas = createCanvas('indicatorChart', 800, 400);
        resultsDiv.appendChild(chartCanvas);

        // Attach event listener to plot button
        plotButton.addEventListener('click', () => {
            plotIndicatorData(data.country1_data, data.country2_data, country1, country2, indicator);
        });
    } catch (error) {
        clearElement(resultsDiv);
        const errorMsg = createErrorMessage('An error occurred while fetching data.');
        resultsDiv.appendChild(errorMsg);
        console.error(error);
    }
});

/**
 * Clear all child elements from a given parent element.
 * @param {HTMLElement} element
 */
function clearElement(element) {
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
}

/**
 * Create a spinner element.
 * @returns {HTMLElement}
 */
function createSpinner() {
    const spinner = document.createElement('img');
    spinner.src = '/static/images/spinner.gif'; // Ensure this path exists
    spinner.alt = 'Loading...';
    spinner.setAttribute('role', 'status');
    return spinner;
}

/**
 * Create an error message element.
 * @param {string} message
 * @returns {HTMLElement}
 */
function createErrorMessage(message) {
    const errorMsg = document.createElement('p');
    errorMsg.className = 'error-message';
    errorMsg.textContent = message;
    errorMsg.setAttribute('role', 'alert');
    return errorMsg;
}

/**
 * Create a button element.
 * @param {string} text
 * @param {string} id
 * @returns {HTMLButtonElement}
 */
function createButton(text, id) {
    const button = document.createElement('button');
    button.id = id;
    button.textContent = text;
    button.className = 'action-button';
    return button;
}

/**
 * Create a canvas element.
 * @param {string} id
 * @param {number} width
 * @param {number} height
 * @returns {HTMLCanvasElement}
 */
function createCanvas(id, width, height) {
    const canvas = document.createElement('canvas');
    canvas.id = id;
    canvas.width = width;
    canvas.height = height;
    canvas.style.display = 'none';
    return canvas;
}

/**
 * Extract dates and values from data.
 * @param {Array} data
 * @returns {Object}
 */
function extractDatesAndValues(data) {
    return {
        dates: data.map(([date]) => date.split('T')[0]),
        values: data.map(([_, value]) => value),
    };
}

/**
 * Create a table element to display indicator data.
 * @param {Array} country1Data
 * @param {Array} country2Data
 * @param {string} country1Name
 * @param {string} country2Name
 * @param {string} indicator
 * @returns {HTMLElement}
 */
function createTable(country1Data, country2Data, country1Name, country2Name, indicator) {
    const combinedData = country1Data.map(([date, value1], index) => {
        const value2 = country2Data[index] ? country2Data[index][1] : 'N/A';
        return { date: date.split('T')[0], country1: value1, country2: value2 };
    });

    const tableContainer = document.createElement('div');
    tableContainer.style.overflowX = 'auto';
    tableContainer.style.maxHeight = '200px';

    const table = document.createElement('table');
    table.border = '1';
    table.style.width = '100%';
    table.style.borderCollapse = 'collapse';
    table.style.textAlign = 'center';

    // Add table headers
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    const headers = ['Date', `${capitalizeWords(country1Name)} ${indicator}`, `${capitalizeWords(country2Name)} ${indicator}`];
    headers.forEach((header) => {
        const th = document.createElement('th');
        th.textContent = header;
        th.style.position = 'sticky'; // Make header stationary
        th.style.top = '0';          // Stick to the top
        th.style.backgroundColor = '#f8f8f8'; // Background to prevent overlay issues
        th.style.zIndex = '1';       // Ensure it stays above other content
        thead.appendChild(th);
    });

    const tbody = document.createElement('tbody');
    combinedData.forEach((row) => {
        const tr = document.createElement('tr');
        ['date', 'country1', 'country2'].forEach((key) => {
            const td = document.createElement('td');
            td.textContent = row[key];
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });

    table.appendChild(thead);
    table.appendChild(tbody);
    tableContainer.appendChild(table);
    return tableContainer;
}

/**
 * Capitalize the first letter of each word in a string.
 * @param {string} str
 * @returns {string}
 */
function capitalizeWords(str) {
    return str
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
        .join(' ');
}

/**
 * Plot indicator data on a chart.
 * @param {Array} country1Data
 * @param {Array} country2Data
 * @param {string} country1
 * @param {string} country2
 * @param {string} indicator
 */
function plotIndicatorData(country1Data, country2Data, country1, country2, indicator) {
    const country1Info = extractDatesAndValues(country1Data);
    const country2Info = extractDatesAndValues(country2Data);

    const chartCanvas = document.getElementById('indicatorChart');
    chartCanvas.style.display = 'block';

    new Chart(chartCanvas, {
        type: 'line',
        data: {
            labels: country1Info.dates,
            datasets: [
                {
                    label: `${capitalizeWords(country1)} ${indicator}`,
                    data: country1Info.values,
                    borderColor: 'blue',
                },
                {
                    label: `${capitalizeWords(country2)} ${indicator}`,
                    data: country2Info.values,
                    borderColor: 'green',
                },
            ],
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: `${capitalizeWords(indicator)} Comparison`,
                },
            },
            scales: {
                x: { title: { display: true, text: 'Date' } },
                y: { title: { display: true, text: `${indicator}` } },
            },
        },
    });
}
