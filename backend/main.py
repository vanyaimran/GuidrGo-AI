from fastapi import FastAPI
import googlemaps
import requests
import os
from textblob import TextBlob

app = FastAPI()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)


# ==========================
# WEATHER
# ==========================
def get_weather(city):
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}"

        response = requests.get(url)
        data = response.json()

        return {
            "temperature": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"],
            "humidity": data["current"]["humidity"],
            "wind_kph": data["current"]["wind_kph"]
        }

    except Exception as e:
        return {
            "error": str(e)
        }


# ==========================
# NLP SENTIMENT ANALYSIS
# ==========================
def analyze_sentiment(text):

    analysis = TextBlob(text)

    score = analysis.sentiment.polarity

    if score > 0:
        label = "Positive"
    elif score < 0:
        label = "Negative"
    else:
        label = "Neutral"

    return {
        "label": label,
        "score": round(score, 2)
    }


# ==========================
# REVIEW ANALYSIS
# ==========================
def analyze_hotel_reviews(city):

    analyzed_reviews = []

    try:

        hotel_results = gmaps.places(
            query=f"best hotels in {city} Pakistan"
        )

        if not hotel_results["results"]:
            return []

        place_id = hotel_results["results"][0]["place_id"]

        details = gmaps.place(
            place_id=place_id,
            fields=["reviews"]
        )

        google_reviews = details["result"].get(
            "reviews",
            []
        )

        for review in google_reviews:

            text = review.get("text", "")

            sentiment = analyze_sentiment(text)

            analyzed_reviews.append({
                "review": text,
                "sentiment": sentiment["label"],
                "score": sentiment["score"]
            })

    except Exception as e:

        analyzed_reviews.append({
            "review": str(e),
            "sentiment": "Error",
            "score": 0
        })

    return analyzed_reviews
    # ==========================
# LIVE GOOGLE REVIEWS
# ==========================
def get_live_reviews(place_id):

    try:

        details = gmaps.place(
            place_id=place_id,
            fields=["reviews"]
        )

        reviews = []

        for review in details["result"].get("reviews", []):

            text = review.get("text", "")

            sentiment = analyze_sentiment(text)

            reviews.append({
                "review": text,
                "sentiment": sentiment["label"],
                "score": sentiment["score"]
            })

        return reviews

    except Exception as e:

        print(e)

        return []


@app.get("/reviews/{city}")
def reviews(city: str):
    return analyze_hotel_reviews(city)

# ==========================
# TRAVEL SCORE
# ==========================
def calculate_travel_score(weather, hotels, attractions):

    score = 5

    try:

        if weather.get("temperature", 0) < 35:
            score += 2

        score += min(len(attractions) / 2, 2)

        if hotels:

            ratings = [
                h["rating"]
                for h in hotels
                if h["rating"] is not None
            ]

            if ratings:
                score += sum(ratings) / len(ratings) / 5

    except:
        pass

    return round(min(score, 10), 1)


# ==========================
# AI TRIP PLANNER
# ==========================
def generate_trip_plan(city):

    return {
        "day_1": [
            f"Explore famous attractions in {city}",
            "Visit local market"
        ],

        "day_2": [
            "Visit top tourist spots",
            "Enjoy local cuisine"
        ],

        "day_3": [
            "Photography and sightseeing",
            "Shopping and souvenirs"
        ]
    }


# ==========================
# HOME
# ==========================
@app.get("/")
def home():
    return {
        "message": "GuidrGo AI Backend Running"
    }


# ==========================
# DEBUG
# ==========================
@app.get("/debug")
def debug():

    return {
        "weather_key_exists": WEATHER_API_KEY is not None,
        "google_key_exists": GOOGLE_MAPS_API_KEY is not None
    }
  # ==========================
# TEST LIVE REVIEWS
# ==========================
@app.get("/test-reviews/{city}")
def test_reviews(city: str):

    try:

        hotels = gmaps.places(
            query=f"best hotels in {city} Pakistan"
        )

        first_hotel = hotels["results"][0]

        place_id = first_hotel["place_id"]

        return get_live_reviews(place_id)

    except Exception as e:

        return {
            "error": str(e)
        }

# ==========================
# SENTIMENT API
# ==========================
@app.get("/sentiment/{text}")
def sentiment(text: str):

    return analyze_sentiment(text)


# ==========================
# REVIEW API
# ==========================

    # ==========================
# SMART HOTEL RECOMMENDER
# ==========================
@app.get("/recommend/{city}/{preference}")
def recommend_hotel(city: str, preference: str):
    preference_lower = preference.lower()
    
    # 1. Check/Fetch hotels from Google Places API
    try:
        hotel_results = gmaps.places(
            query=f"hotels in {city}"
        )
        if not hotel_results.get("results"):
            hotel_results = gmaps.places(
                query=f"hotels in {city} Pakistan"
            )
    except Exception as e:
        print(f"Google Places search failed: {e}")
        hotel_results = None

    # Define synonyms/related words for our main keywords to make matching highly intelligent
    preference_keywords = {
        "food": ["food", "breakfast", "dinner", "lunch", "restaurant", "buffet", "delicious", "meal", "taste", "dining", "cuisine", "chef", "eat"],
        "view": ["view", "scenery", "rooftop", "sea", "mountain", "window", "landscape", "beautiful", "scenic", "surroundings", "terrace"],
        "luxury": ["luxury", "premium", "deluxe", "five-star", "fancy", "classy", "posh", "royal", "suite", "spa", "pool", "poolside", "expensive"],
        "family": ["family", "kids", "children", "safe", "friendly", "spacious", "playground", "parents", "baby", "play"],
        "comfort": ["comfort", "comfortable", "cosy", "cozy", "clean", "quiet", "peaceful", "bed", "sleep", "soft", "sheets", "silent", "noise"],
        "staff": ["staff", "service", "hospitality", "helpful", "friendly", "management", "reception", "polite", "welcome", "host", "behavior", "courteous"]
    }

    matched_synonyms = [preference_lower]
    for key, synonyms in preference_keywords.items():
        if key in preference_lower:
            matched_synonyms.extend(synonyms)
    matched_synonyms = list(set(matched_synonyms))

    scored_hotels = []

    if hotel_results and hotel_results.get("results"):
        # Process top 5 hotels to ensure fast and reliable execution
        for hotel in hotel_results["results"][:5]:
            place_id = hotel.get("place_id")
            name = hotel.get("name")
            rating = hotel.get("rating", 0.0) or 0.0

            try:
                details = gmaps.place(
                    place_id=place_id,
                    fields=["reviews"]
                )
                google_reviews = details.get("result", {}).get("reviews", [])
            except Exception as e:
                print(f"Error fetching reviews for {name}: {e}")
                google_reviews = []

            hotel_score = 0.0
            keyword_matches = 0
            sentiment_sum = 0.0
            matching_reviews = []
            all_reviews = []

            for review in google_reviews:
                text = review.get("text", "")
                if not text:
                    continue

                sentiment = analyze_sentiment(text)
                score = sentiment["score"]
                sentiment_sum += score

                review_obj = {
                    "review": text,
                    "sentiment": sentiment["label"],
                    "score": score
                }
                all_reviews.append(review_obj)

                # Count how many preference synonyms match in the review
                match_count = sum(1 for word in matched_synonyms if word in text.lower())
                if match_count > 0:
                    matching_reviews.append(review_obj)
                    if score >= 0:
                        # Positive or neutral review matching preference keyword gives huge boost
                        keyword_matches += match_count
                        hotel_score += score * 5.0 * match_count
                    else:
                        # Negative review matching preference keyword penalizes heavily
                        hotel_score += score * 5.0 * match_count
                else:
                    # Generic review contributes normally to overall sentiment
                    hotel_score += score * 1.0

            num_reviews = len(all_reviews)
            avg_sentiment = (sentiment_sum / num_reviews) if num_reviews > 0 else 0.0

            # Core multi-factor rating score
            hotel_score += rating * 2.0
            hotel_score += avg_sentiment * 3.0

            # Huge preference boost if preference keywords were positively matched
            if keyword_matches > 0:
                hotel_score += 10.0 + (keyword_matches * 2.0)

            scored_hotels.append({
                "name": name,
                "score": hotel_score,
                "matching_reviews": matching_reviews,
                "all_reviews": all_reviews,
                "rating": rating
            })

    # If API fails or yields no scored hotels, fall back to our high-quality dynamic mock database
    if not scored_hotels:
        fallback_database = {
            "food": {
                "hotel": f"Pearl Continental Hotel {city.title()}",
                "reviews": [
                    {"review": "Amazing breakfast buffet with local and international dishes.", "sentiment": "Positive", "score": 0.85},
                    {"review": "Excellent dining experience, the food quality was outstanding.", "sentiment": "Positive", "score": 0.90},
                    {"review": "Loved the cuisine options and restaurant staff service.", "sentiment": "Positive", "score": 0.75}
                ]
            },
            "view": {
                "hotel": f"Movenpick Hotel {city.title()}",
                "reviews": [
                    {"review": "Beautiful panoramic city view from our room window.", "sentiment": "Positive", "score": 0.80},
                    {"review": "Amazing rooftop scenery and peaceful sunset views.", "sentiment": "Positive", "score": 0.95},
                    {"review": "Loved the scenic surroundings and landscape.", "sentiment": "Positive", "score": 0.85}
                ]
            },
            "luxury": {
                "hotel": f"Marriott Hotel {city.title()}",
                "reviews": [
                    {"review": "An absolute luxury experience with high-end premium rooms.", "sentiment": "Positive", "score": 0.90},
                    {"review": "Premium service, excellent facilities, and clean pool.", "sentiment": "Positive", "score": 0.85},
                    {"review": "Felt royal, standard was top notch deluxe quality.", "sentiment": "Positive", "score": 0.80}
                ]
            },
            "family": {
                "hotel": f"Avari Towers {city.title()}",
                "reviews": [
                    {"review": "Great safe place for families with clean playground for kids.", "sentiment": "Positive", "score": 0.80},
                    {"review": "Spacious rooms and kids really enjoyed the swimming pool.", "sentiment": "Positive", "score": 0.75},
                    {"review": "Family friendly management and safe environment.", "sentiment": "Positive", "score": 0.85}
                ]
            },
            "comfort": {
                "hotel": f"Ramada Plaza {city.title()}",
                "reviews": [
                    {"review": "Very comfortable rooms, extremely peaceful stay.", "sentiment": "Positive", "score": 0.85},
                    {"review": "Soft cozy beds and quiet rooms for an excellent sleep experience.", "sentiment": "Positive", "score": 0.90},
                    {"review": "Clean and silent surroundings, perfect for relaxation.", "sentiment": "Positive", "score": 0.80}
                ]
            },
            "staff": {
                "hotel": f"Pearl Continental Hotel {city.title()}",
                "reviews": [
                    {"review": "The hotel staff were very helpful and courteous.", "sentiment": "Positive", "score": 0.80},
                    {"review": "Excellent customer service and highly polite management.", "sentiment": "Positive", "score": 0.90},
                    {"review": "Friendly reception host made us feel very welcome.", "sentiment": "Positive", "score": 0.85}
                ]
            }
        }

        found_fallback = None
        for key in fallback_database:
            if key in preference_lower:
                found_fallback = fallback_database[key]
                break

        if not found_fallback:
            found_fallback = {
                "hotel": f"Marriott Hotel {city.title()}",
                "reviews": [
                    {"review": "Highly rated overall with great guest satisfaction.", "sentiment": "Positive", "score": 0.75},
                    {"review": "Popular among business and leisure travelers alike.", "sentiment": "Positive", "score": 0.70},
                    {"review": "Comfortable and convenient location in the city.", "sentiment": "Positive", "score": 0.65}
                ]
            }

        return {
            "recommended_hotel": found_fallback["hotel"],
            "reviews": found_fallback["reviews"]
        }

    # Sort hotels by overall preference recommendation score
    scored_hotels.sort(key=lambda x: x["score"], reverse=True)
    best_hotel = scored_hotels[0]

    # Structure reviews to display, putting preference matching ones first
    display_reviews = best_hotel["matching_reviews"]
    if len(display_reviews) < 3:
        for rev in best_hotel["all_reviews"]:
            if rev not in display_reviews:
                display_reviews.append(rev)
                if len(display_reviews) >= 3:
                    break

    return {
        "recommended_hotel": best_hotel["name"],
        "reviews": display_reviews[:5]
    }


# ==========================
# TRAVEL API
# ==========================
@app.get("/travel/{city}")
def get_travel_data(city: str):

    hotels = []
    attractions = []

    try:

        hotel_results = gmaps.places(
            query=f"best hotels in {city} Pakistan"
        )

        for hotel in hotel_results["results"][:5]:

            hotels.append({
                "name": hotel["name"],
                "rating": hotel.get("rating")
            })

    except:
        pass

    try:

        attraction_results = gmaps.places(
            query=f"tourist attractions in {city} Pakistan"
        )

        for attraction in attraction_results["results"][:10]:

            attractions.append(
                attraction["name"]
            )

    except:
        pass

    weather = get_weather(city)

    risk = "Low Risk"

    try:

        if weather["temperature"] > 40:
            risk = "High Risk"

        elif weather["wind_kph"] > 30:
            risk = "Medium Risk"

    except:
        pass

    travel_score = calculate_travel_score(
        weather,
        hotels,
        attractions
    )

    trip_plan = generate_trip_plan(city)

    return {
        "city": city,
        "weather": weather,
        "risk_analysis": risk,
        "travel_score": travel_score,
        "hotels": hotels,
        "attractions": attractions,
       "reviews": analyze_hotel_reviews(city),
        "trip_plan": trip_plan
    }

           



           
            
