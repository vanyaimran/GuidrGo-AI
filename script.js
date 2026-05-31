async function searchCity() {

    const city = document.getElementById("city").value;

    if (!city) {
        alert("Please enter a city");
        return;
    }

    document.getElementById("result").innerHTML =
        "<p>Loading...</p>";

    try {

        const response = await fetch(`/travel/${city}`);

        const data = await response.json();

        document.getElementById("result").innerHTML = `
            <h2>${data.city}</h2>

            <h3>Weather</h3>
            <p>Temperature: ${data.weather.temperature}°C</p>
            <p>Condition: ${data.weather.condition}</p>
            <p>Humidity: ${data.weather.humidity}%</p>

            <h3>Risk Analysis</h3>
            <p>${data.risk_analysis}</p>

            <h3>Hotels</h3>
            <ul>
                ${data.hotels.map(h =>
                    `<li>${h.name} ⭐ ${h.rating}</li>`
                ).join("")}
            </ul>

            <h3>Tourist Attractions</h3>
            <ul>
                ${data.attractions.map(a =>
                    `<li>${a}</li>`
                ).join("")}
            </ul>
        `;

    } catch (error) {

        console.error(error);

        document.getElementById("result").innerHTML =
            `<p style="color:red;">Error loading city data</p>`;
    }
}
