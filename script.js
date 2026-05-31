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

        // Main Travel Information

        document.getElementById("result").innerHTML = `
            <h2>📍 ${data.city}</h2>

            <h3>🌤 Weather</h3>
            <p>Temperature: ${data.weather.temperature}°C</p>
            <p>Condition: ${data.weather.condition}</p>
            <p>Humidity: ${data.weather.humidity}%</p>

            <h3>⚠ Risk Analysis</h3>
            <p>${data.risk_analysis}</p>

            <h3>🏨 Hotels</h3>
            <ul>
                ${data.hotels.map(h =>
                    `<li>${h.name} ⭐ ${h.rating}</li>`
                ).join("")}
            </ul>

            <h3>📸 Tourist Attractions</h3>
            <ul>
                ${data.attractions.map(a =>
                    `<li>${a}</li>`
                ).join("")}
            </ul>
        `;

        // Travel Score

        document.getElementById("score").innerHTML = `
            <h3>🏆 Travel Score</h3>
            <h1>${data.travel_score}/10</h1>
        `;

        // Review Analysis

        document.getElementById("reviews").innerHTML = `
            ${data.reviews.map(r => `
                <div style="
                    padding:10px;
                    margin:10px 0;
                    background:#1e293b;
                    border-radius:8px;
                ">
                    <p>${r.review}</p>

                    <strong style="
                    color:${r.sentiment==="Positive" ? "lime" : "red"};
                    ">
                        ${r.sentiment}
                    </strong>

                    <p>Score: ${r.score}</p>
                </div>
            `).join("")}
        `;

        // AI Trip Planner

        document.getElementById("trip").innerHTML = `
            <h3>Day 1</h3>
            <ul>
                ${data.trip_plan.day_1.map(x =>
                    `<li>${x}</li>`
                ).join("")}
            </ul>

            <h3>Day 2</h3>
            <ul>
                ${data.trip_plan.day_2.map(x =>
                    `<li>${x}</li>`
                ).join("")}
            </ul>

            <h3>Day 3</h3>
            <ul>
                ${data.trip_plan.day_3.map(x =>
                    `<li>${x}</li>`
                ).join("")}
            </ul>
        `;

    } catch (error) {

        console.error(error);

        document.getElementById("result").innerHTML =
            `<p style="color:red;">Error loading city data</p>`;
    }
}


// NLP SENTIMENT ANALYSIS

async function checkSentiment() {

    const text =
        document.getElementById("sentimentText").value;

    if (!text) {
        alert("Please enter text");
        return;
    }

    const response =
        await fetch(`/sentiment/${encodeURIComponent(text)}`);

    const data =
        await response.json();

    document.getElementById("sentimentResult").innerHTML = `
        <div style="
            background:#1e293b;
            padding:20px;
            margin-top:15px;
            border-radius:10px;
        ">
            <h3>${data.label}</h3>
            <p>Score: ${data.score}</p>
        </div>
    `;
}
