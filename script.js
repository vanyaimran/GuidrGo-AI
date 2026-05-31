async function searchCity() {

    const city =
    document.getElementById("city").value;

    const result =
    document.getElementById("result");

    result.innerHTML = "Loading...";

    try {

        const response =
        await fetch(`/travel/${city}`);

        const data =
        await response.json();

        result.innerHTML = `
            <h2>${data.city}</h2>

            <h3>Weather</h3>
            <p>Temperature:
            ${data.weather.temperature}°C</p>

            <p>Condition:
            ${data.weather.condition}</p>

            <p>Risk:
            ${data.risk_analysis}</p>

            <h3>Hotels</h3>

            <ul>
                ${data.hotels.map(
                    h =>
                    `<li>${h.name}
                    (${h.rating})</li>`
                ).join("")}
            </ul>

            <h3>Attractions</h3>

            <ul>
                ${data.attractions.map(
                    a =>
                    `<li>${a}</li>`
                ).join("")}
            </ul>
        `;

    } catch(error){

        result.innerHTML =
        "Error loading data";

    }
}
