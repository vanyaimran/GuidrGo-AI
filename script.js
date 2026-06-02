async function searchCity() {
    const city = document.getElementById("city").value;
    const budget = document.getElementById("budget").value;
const duration = document.getElementById("duration").value;

    if (!city) {
        alert("Please enter a city");
        return;
    }

    document.getElementById("result").innerHTML = "<p>Loading...</p>";
    const reviewsContainer = document.getElementById("reviews");
    if (reviewsContainer) {
        reviewsContainer.innerHTML = "<p>Loading live reviews...</p>";
    }

    try {
 const response = await fetch(
    `/travel/${city}?budget=${budget}&duration=${duration}`
);
        const data = await response.json();

        document.getElementById("cityMap").src =
        `https://maps.google.com/maps?q=${city}&t=&z=13&ie=UTF8&iwloc=&output=embed`;

        document.getElementById("result").innerHTML = `
            <h2>📍 ${data.city}</h2>
            <p><strong>Budget Type:</strong> ${data.budget_category}</p>
<p><strong>Duration:</strong> ${data.duration} Days</p>

            <h3>🌤 Weather</h3>
            <p>Temperature: ${data.weather.temperature}°C</p>
            <p>Condition: ${data.weather.condition}</p>
            <p>Humidity: ${data.weather.humidity}%</p>

            <h3>⚠ Risk Analysis</h3>
            <p>${data.risk_analysis}</p>

            <h3>🏨 Hotels</h3>
            <ul>
                ${data.hotels.map(h =>
                    `<li>${h.name} ⭐ ${h.rating || 'N/A'}</li>`
                ).join("")}
            </ul>

            <h3>📸 Tourist Attractions</h3>
            <ul>
                ${data.attractions.map(a =>
                    `<li>${a}</li>`
                ).join("")}
            </ul>
        `;

        document.getElementById("score").innerHTML = `
            <h3>🏆 Travel Score</h3>
            <h1>${data.travel_score}/10</h1>
        `;

        document.getElementById("trip").innerHTML = `
<div class="trip-day">
    <h3>Day 1</h3>
    <ul>
        ${data.trip_plan.day_1.map(x =>
            `<li>${x}</li>`
        ).join("")}
    </ul>
</div>

<div class="trip-day">
    <h3>Day 2</h3>
    <ul>
        ${data.trip_plan.day_2.map(x =>
            `<li>${x}</li>`
        ).join("")}
    </ul>
</div>

<div class="trip-day">
    <h3>Day 3</h3>
    <ul>
        ${data.trip_plan.day_3.map(x =>
            `<li>${x}</li>`
        ).join("")}
    </ul>
</div>
`;

        // Render Live Reviews
        if (reviewsContainer) {
            if (data.reviews && data.reviews.length > 0) {
                if (data.reviews.length === 1 && data.reviews[0].sentiment === "Error") {
                    reviewsContainer.innerHTML = `<p style="color: #ef4444; background: rgba(239, 68, 68, 0.1); padding: 15px; border-radius: 8px; border: 1px solid rgba(239, 68, 68, 0.2);">Error fetching reviews: ${data.reviews[0].review}</p>`;
                } else {
                    reviewsContainer.innerHTML = `
                        <div class="reviews-list">
                            ${data.reviews.map(r => {
                                const badgeClass = r.sentiment === 'Positive' ? 'badge-positive' : r.sentiment === 'Negative' ? 'badge-negative' : 'badge-neutral';
                                return `
                                    <div class="review-card" style="border-left-color: ${r.sentiment === 'Positive' ? 'var(--success)' : r.sentiment === 'Negative' ? 'var(--danger)' : 'var(--text-secondary)'};">
                                        <p style="margin: 0 0 10px 0; font-style: italic; font-size: 1.05rem;">"${r.review}"</p>
                                        <span class="badge ${badgeClass}">
                                            Sentiment: ${r.sentiment} (${r.score >= 0 ? '+' : ''}${r.score.toFixed(2)})
                                        </span>
                                    </div>
                                `;
                            }).join("")}
                        </div>
                    `;
                }
            } else {
                reviewsContainer.innerHTML = "<p>No live hotel reviews available for this city.</p>";
            }
        }

    } catch (error) {
        console.error(error);
        document.getElementById("result").innerHTML =
        `<p style="color:red;">Error loading city data</p>`;
        if (reviewsContainer) {
            reviewsContainer.innerHTML = `<p style="color:red;">Failed to load reviews.</p>`;
        }
    }
}

async function checkSentiment() {

    const text = document.getElementById("sentimentText").value;

    if (!text) {
        alert("Please enter text");
        return;
    }

    const response =
        await fetch(`/sentiment/${encodeURIComponent(text)}`);

    const data = await response.json();

    const badgeClass = data.label === 'Positive' ? 'badge-positive' : data.label === 'Negative' ? 'badge-negative' : 'badge-neutral';

    document.getElementById("sentimentResult").innerHTML = `
        <div style="
            background:#161d30;
            padding:20px;
            margin-top:15px;
            border-radius:12px;
            border: 1px solid #334155;
        ">
            <h3>Sentiment Result</h3>
            <span class="badge ${badgeClass}" style="font-size: 1.1rem; padding: 6px 12px;">
                ${data.label} (${data.score >= 0 ? '+' : ''}${data.score.toFixed(2)})
            </span>
        </div>
    `;
}

async function recommendHotel() {

    const city =
        document.getElementById("recommendCity").value;

    const preference =
        document.getElementById("hotelPreference").value;

    if (!city || !preference) {
        alert("Please enter city and preference");
        return;
    }

    document.getElementById("hotelRecommendation").innerHTML = "<p>Analyzing reviews and scoring hotels...</p>";

    try {
        const response =
            await fetch(`/recommend/${city}/${encodeURIComponent(preference)}`);

        const data =
            await response.json();

        if (data.error) {
            document.getElementById("hotelRecommendation").innerHTML = `<p style="color:red;">Error: ${data.error}</p>`;
            return;
        }

        document.getElementById("hotelRecommendation").innerHTML = `
            <h3>🏨 Recommended Hotel for "${preference}"</h3>

            <p>
                <strong>${data.recommended_hotel}</strong>
            </p>

            <h3>💬 Relevant Guest Reviews:</h3>
            <ul>
                ${data.reviews.map(review => {
                    if (typeof review === 'object' && review !== null) {
                        const badgeClass = review.sentiment === 'Positive' ? 'badge-positive' : review.sentiment === 'Negative' ? 'badge-negative' : 'badge-neutral';
                        return `
                            <li style="margin-bottom: 12px; border-left: 4px solid ${review.sentiment === 'Positive' ? 'var(--success)' : review.sentiment === 'Negative' ? 'var(--danger)' : 'var(--text-secondary)'};">
                                <p style="margin: 0 0 8px 0; font-style: italic;">"${review.review}"</p>
                                <span class="badge ${badgeClass}">
                                    ${review.sentiment} (${review.score >= 0 ? '+' : ''}${review.score.toFixed(2)})
                                </span>
                            </li>
                        `;
                    } else {
                        return `<li>${review}</li>`;
                    }
                }).join("")}
            </ul>
        `;
    } catch (error) {
        console.error(error);
        document.getElementById("hotelRecommendation").innerHTML = `<p style="color:red;">Failed to get hotel recommendations.</p>`;
    }
}


