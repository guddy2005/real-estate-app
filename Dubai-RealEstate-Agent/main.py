from flask import Flask, render_template, request, jsonify
from google import genai
import json
import os
from datetime import datetime

app = Flask(__name__)

# Configure Gemini API
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("⚠️ GEMINI_API_KEY not found! Please add it in Replit Secrets.")

client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-2.5-flash"  # or "gemini-2.0-flash" if your key supports that

# Load property catalog
with open('property_catalog.json', 'r') as f:
    property_catalog = json.load(f)

# Load user database
with open('user_database.json', 'r') as f:
    user_database = json.load(f)

# Real Estate GPT Knowledge Base
REAL_ESTATE_KNOWLEDGE = """
# DUBAI REAL ESTATE EXPERT SYSTEM - COMPREHENSIVE KNOWLEDGE BASE

## CORE MARKET INTELLIGENCE (2026)

### Market Overview
- Dubai's property market recorded AED 559.4 billion in sales in 2025 (highest ever)
- Average residential prices rose 10-13% year-over-year in 2025
- Median housing price in Dubai 2026: AED 2.1 million (~$572,000)
- Average price per sqft: AED 1,925 (~$524/sqft or AED 20,700/sqm)
- 87% cash buyers dominate the market, keeping negotiations tight

### Price Ranges by Property Type (2026)
- **Studios**: AED 450,000 - 850,000 ($123K - $231K)
- **1-Bedroom**: AED 900,000 - 1.6M ($245K - $436K)
- **2-Bedroom**: AED 1.5M - 2.8M ($408K - $762K)
- **3-Bedroom Townhouses**: AED 2.2M - 4.5M ($599K - $1.23M)
- **4-5 Bedroom Villas**: AED 3.5M - 8M ($953K - $2.18M)
- **Prime Villas**: AED 12M+ (up to AED 100M+)
- **Penthouses (2BR)**: AED 4M - 8M in Dubai Marina
- **Penthouses (4BR)**: AED 20M - 30M in Downtown Dubai
- **Ultra-Luxury Penthouses**: AED 75M - 185M (Palm Jumeirah, Burj Khalifa)

### Regional Pricing Dynamics
- **Emirates Hills**: AED 14,500/sqft (most expensive)
- **Palm Jumeirah**: AED 28,000 - 45,000/sqm
- **Downtown Dubai & Dubai Marina**: AED 2,000 - 2,400/sqft
- **Discovery Gardens**: AED 9,000 - 12,000/sqm (most affordable)
- **Dubai Silicon Oasis**: AED 12,000 - 16,000/sqm

### Investment Hotspots & Rental Yields (2026)
1. **Dubai South**: 7-8% yields + 15-20% appreciation (Airport expansion AED 128B)
2. **Dubai Creek Harbour**: 6-7% yields + 10-15% appreciation (Downtown 2.0)
3. **JVC (Jumeirah Village Circle)**: 7.82% yields (risk: 10-15% correction)
4. **Business Bay**: 6-8% yields, highest liquidity (Metro + DIFC proximity)
5. **Palm Jumeirah**: 5-7% yields + 8-10% appreciation (luxury resilience)
6. **Dubai Hills Estate**: 5-6% yields + 7-9% growth (family-friendly)
7. **Dubai Marina**: 5.8-7.2% yields (60%+ growth 2020-2025)
8. **Arabian Ranches**: 4.5-5.5% yields + 6-8% appreciation (villa shortage)

### Transaction Costs (Important for Buyers)
- **DLD Transfer Fee**: 4% of purchase price
- **Agency Commission**: 2% of purchase price
- **Total Buying Costs**: 6-7% on top of purchase price

## REGIONAL EXPERTISE

### Downtown Dubai
- Heart of Dubai, home to Burj Khalifa & Dubai Mall
- Average: AED 2,200/sqft
- Target Audience: Ultra-high net worth individuals, luxury seekers
- Best For: Investment prestige, rental income from tourists/expats
- Connectivity: Dubai Mall Metro, Downtown Blvd, Sheikh Zayed Road

### Dubai Marina
- Waterfront lifestyle, vibrant community
- Average: AED 1,850/sqft
- Target Audience: Young professionals, expats, beach lovers
- Best For: Rental yields, lifestyle living
- Connectivity: Dubai Marina Metro, Tram, JBR Beach

### Palm Jumeirah
- Iconic man-made island, ultra-luxury beachfront
- Average: AED 3,200/sqft
- Target Audience: Ultra-wealthy, celebrities, families seeking exclusivity
- Best For: Luxury living, long-term appreciation
- Connectivity: Palm Monorail, Golden Mile

### Business Bay
- Central business district, canal views
- Average: AED 1,750/sqft
- Target Audience: Business professionals, investors
- Best For: Rental yields, capital appreciation, business proximity
- Connectivity: Business Bay Metro (direct), DIFC (5 min)

### Dubai Hills Estate
- Family-friendly master community with golf courses
- Average: AED 1,450/sqft
- Target Audience: Families, golf enthusiasts
- Best For: Long-term living, community lifestyle, schools
- Connectivity: Al Khail Road, Dubai Hills Mall

## PROPERTY TYPES EXPERTISE

### Villas
- Typical Size: 4,000 - 10,000 sqft
- Best Regions: Palm Jumeirah, Dubai Hills Estate, Arabian Ranches
- Investment Logic: Long-term appreciation, limited supply, family demand
- Rental Yields: 4-6%
- Key Features: Private pool, garden, parking, maid room

### Penthouses
- Typical Size: 3,500 - 7,000 sqft
- Best Regions: Downtown Dubai, Business Bay, Palm Jumeirah
- Investment Logic: Ultra-luxury segment, scarcity premium
- Rental Yields: 4-6%
- Key Features: Private elevator, rooftop terrace, sky pool, panoramic views

### Duplexes
- Typical Size: 2,500 - 4,000 sqft
- Best Regions: Dubai Marina, Business Bay, Dubai Hills Estate
- Investment Logic: Space efficiency, family appeal
- Rental Yields: 5-7%
- Key Features: Double height living, multiple levels, balconies

### Apartments
- Typical Size: 700 - 2,000 sqft
- Best Regions: Dubai Marina, JVC, Business Bay
- Investment Logic: High rental demand, affordability, liquidity
- Rental Yields: 6-8%
- Key Features: Modern amenities, community living

### Commercial Offices
- Typical Size: 1,500 - 5,000 sqft
- Best Regions: Business Bay, DIFC, Downtown Dubai
- Investment Logic: Business hub proximity, corporate demand
- Rental Yields: 7-9%
- Key Features: Fitted offices, parking, high-speed internet

## BUYER PSYCHOLOGY & PROBING LOGIC

### For First-Time Buyers
- Probe: Budget range, lifestyle preferences, family size
- Recommend: Dubai Marina apartments, JVC, Dubai Hills Estate
- Reason: Affordability, community, appreciation potential

### For Luxury Seekers
- Probe: Budget (AED 10M+), lifestyle (beach/city/golf)
- Recommend: Palm Jumeirah villas, Downtown penthouses
- Reason: Prestige, exclusivity, premium amenities

### For Investors
- Probe: Investment goal (yield vs appreciation), holding period
- Recommend: Dubai South, Business Bay, JVC
- Reason: High rental yields, infrastructure growth

### For Families
- Probe: Number of children, school proximity, outdoor space
- Recommend: Dubai Hills Estate, Arabian Ranches, Dubai South
- Reason: Family-friendly, schools, parks, safety

## INTELLIGENT RESPONSE PATTERNS

### When User Asks About Prices
1. Provide general market overview
2. Mention specific regional averages
3. If registered user: relate to their budget
4. Probe: "Are you looking in any specific area?"

### When User Asks for Recommendations
1. Check user type (guest vs registered)
2. If registered: analyze profile (budget, preferences, browsing history)
3. Match properties from catalog
4. Present 3-4 primary matches with reasoning
5. Offer alternative options with probing questions

### When User Shows Interest in Specific Property
1. Provide detailed property information
2. Highlight unique features
3. Mention nearby amenities
4. If registered: compare with saved/viewed properties
5. Probe: "Would you like to schedule a viewing?" or "Interested in similar options?"

### When User Asks About Investment
1. Discuss rental yields by area
2. Mention appreciation trends
3. Recommend based on user's investment horizon
4. Probe: "Are you looking for rental income or capital appreciation?"

## PERSONALIZATION RULES FOR REGISTERED USERS

### Profile-Based Matching
- Budget alignment (±10% flexibility)
- Location preference (primary regions, nearby alternatives)
- Property type preference
- Bedrooms requirement
- Must-have features

### Browsing History Intelligence
- Most viewed property type → recommend similar
- Time spent on property > 2 min → high interest signal
- Saved properties → compare and suggest upgrades/alternatives

### Contextual Probing Examples
- "I noticed you've been viewing villas in Palm Jumeirah. Your budget aligns perfectly with..."
- "Based on your preference for sea views and luxury amenities, I found..."
- "You saved the Palm Frond Villa last week. I have 2 similar options that just became available..."

## CONVERSATIONAL TONE RULES
- Professional yet warm and approachable
- Avoid repetitive patterns ("I found X properties...")
- Use varied sentence structures
- Natural transitions between topics
- Empathy: "I understand finding the perfect home is important..."
- Confidence: "Based on current market trends..." not "Maybe..."
- Proactive: Always end with a question or suggestion

## QUERY INTERPRETATION LOGIC

### Vague Queries
- "villa" → Probe: budget, location, family size
- "investment" → Probe: budget, goal (yield/appreciation), timeline
- "something in Dubai Marina" → Show overview, probe for specifics

### Specific Queries
- "luxury villa under 20 million" → Direct property matches
- "2 bedroom apartment for rent in Business Bay" → Targeted search
- "penthouses with sea views" → Filter and recommend

### Comparison Queries
- "Dubai Marina vs Palm Jumeirah" → Comparative analysis (price, lifestyle, yields)
- "villa or penthouse" → Pros/cons based on user profile

## ERROR HANDLING & EDGE CASES
- No matches in budget → Suggest nearby budget or alternative regions
- No data on specific micro-location → Provide regional insights
- Contradictory preferences → Ask clarifying questions
- Out of stock property → Recommend similar available options
"""


def get_user_context(user_type):
    """Generate user context string for the AI prompt"""
    if user_type == 'guest':
        return """
        USER TYPE: Guest User (Non-Registered)
        - No profile information available
        - Provide general market insights and property information
        - Encourage exploration of different options
        - No personalization capabilities
        """
    else:
        user = user_database['demo_user']
        profile = user['profile']

        browsing_summary = "\n".join([
            f"- Viewed {h['property_id']} on {h['viewed_on']} (spent {h['time_spent_seconds']}s)"
            for h in user['browsing_history'][-3:]
        ])

        return f"""
        USER TYPE: Registered User
        USER PROFILE:
        - Name: {user['name']}
        - Budget Range: AED {profile['budget_min_aed']:,} - AED {profile['budget_max_aed']:,}
        - Preferred Locations: {', '.join(profile['preferred_locations'])}
        - Property Type Preference: {', '.join(profile['property_type_preference'])}
        - Category Interest: {profile['category_interest']}
        - Listing Type: {profile['listing_type_interest']}
        - Bedrooms Required: {profile['bedrooms_min']} - {profile['bedrooms_max']}
        - Must-Have Features: {', '.join(profile['must_have_features'])}
        - Lifestyle Preferences: {', '.join(profile['lifestyle_preferences'])}

        RECENT BROWSING HISTORY (Last 3 properties):
        {browsing_summary}

        SAVED PROPERTIES: {', '.join(user['saved_properties'])}

        ⚠️ IMPORTANT: Use this profile information to provide HIGHLY PERSONALIZED recommendations.
        - Match properties to their budget and preferences
        - Reference their browsing history when relevant
        - Suggest properties similar to what they've viewed/saved
        - Be proactive in understanding their needs
        """


def search_properties(query_params, user_type='guest'):
    """Search properties based on query parameters"""
    matches = []

    for region_key, region_data in property_catalog['regions'].items():
        for prop in region_data['properties']:
            score = 0
            reasons = []

            # Basic matching logic
            if user_type == 'registered':
                user = user_database['demo_user']
                profile = user['profile']

                # Budget matching
                if 'price_aed' in prop:
                    if profile['budget_min_aed'] <= prop['price_aed'] <= profile['budget_max_aed']:
                        score += 10
                        reasons.append("within your budget")

                # Location matching
                if region_data['name'] in profile['preferred_locations']:
                    score += 8
                    reasons.append(f"in your preferred area ({region_data['name']})")

                # Property type matching
                if prop['type'] in profile['property_type_preference']:
                    score += 7
                    reasons.append(f"matches your preference for {prop['type'].lower()}s")

                # Listing type matching
                if prop['listing_type'] == profile['listing_type_interest']:
                    score += 5

                # Bedrooms matching
                if 'bedrooms' in prop and profile['bedrooms_min'] <= prop['bedrooms'] <= profile['bedrooms_max']:
                    score += 5
                    reasons.append("suitable bedroom count")

                # Feature matching
                for feature in profile['must_have_features']:
                    if feature in prop.get('features', []):
                        score += 3
                        reasons.append(f"includes {feature}")

            # General keyword matching
            prop_text = json.dumps(prop).lower()
            query_lower = json.dumps(query_params).lower() if isinstance(query_params, dict) else str(query_params).lower()

            keywords = ['villa', 'penthouse', 'duplex', 'apartment', 'office', 'luxury', 'sea view', 'pool', 'beach']
            for keyword in keywords:
                if keyword in query_lower and keyword in prop_text:
                    score += 2

            if score > 0:
                matches.append({
                    'property': prop,
                    'region': region_data['name'],
                    'score': score,
                    'reasons': reasons
                })

    # Sort by score
    matches.sort(key=lambda x: x['score'], reverse=True)
    return matches[:7]  # Return top 7 matches


def format_property_card(property_data, region_name, reasons=None):
    """Format property information as HTML"""
    prop = property_data

    price_display = f"AED {prop['price_aed']:,}" if 'price_aed' in prop else ""
    if 'rent_annual_aed' in prop:
        price_display += f" | Rent: AED {prop['rent_annual_aed']:,}/year"
    if 'lease_annual_aed' in prop:
        price_display += f" | Lease: AED {prop['lease_annual_aed']:,}/year"

    bedrooms_display = f"{prop['bedrooms']} BR | " if 'bedrooms' in prop else ""

    status_emoji = "✅" if prop['status'] == 'Ready' else "🏗️"

    features_list = ', '.join(prop['features'][:4]) if 'features' in prop else ''

    reasons_html = ""
    if reasons:
        reasons_html = f"<p><strong>Why this matches:</strong> {', '.join(reasons[:3])}</p>"

    return f"""
    <div class="property-card">
        <h4>{status_emoji} {prop['name']} - {region_name}</h4>
        <p><strong>{prop['type']}</strong> | {bedrooms_display}{prop['area_sqft']} sqft | <span class="price">{price_display}</span></p>
        <p>{prop['description'][:120]}...</p>
        <p><strong>Features:</strong> {features_list}</p>
        {reasons_html}
    </div>
    """


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        user_type = data.get('user_type', 'guest')

        if not user_message:
            return jsonify({'response': 'Please enter a message.'})

        # Build comprehensive prompt for Gemini
        user_context = get_user_context(user_type)

        # Search for relevant properties
        property_matches = search_properties(user_message, user_type)

        # Format property data for context
        properties_context = ""
        if property_matches:
            properties_context = "\n\nRELEVANT PROPERTIES FROM CATALOG:\n"
            for i, match in enumerate(property_matches[:5], 1):
                prop = match['property']
                properties_context += f"\n{i}. {prop['name']} ({match['region']})\n"
                properties_context += f"   Type: {prop['type']} | Area: {prop['area_sqft']} sqft\n"
                if 'price_aed' in prop:
                    properties_context += f"   Price: AED {prop['price_aed']:,}\n"
                if 'bedrooms' in prop:
                    properties_context += f"   Bedrooms: {prop['bedrooms']}\n"
                properties_context += f"   Status: {prop['status']}\n"
                properties_context += f"   Match Score: {match['score']}\n"
                if match['reasons']:
                    properties_context += f"   Reasons: {', '.join(match['reasons'])}\n"

        prompt = f"""
{REAL_ESTATE_KNOWLEDGE}

{user_context}

{properties_context}

USER QUERY: "{user_message}"

INSTRUCTIONS:
1. You are a professional Dubai Real Estate GPT advisor
2. Provide accurate, helpful, and personalized responses
3. If registered user: use their profile data to personalize recommendations
4. Reference specific properties from the catalog when relevant
5. Use natural, varied conversational tone (avoid repetitive patterns)
6. Be proactive with follow-up questions and suggestions
7. Format property recommendations clearly
8. Keep responses concise but informative (300-500 words max)
9. Use emojis sparingly for better readability
10. ALWAYS end with a probing question or actionable suggestion

RESPONSE:
"""

        # Generate response using Gemini (new GenAI SDK)
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        ai_response = response.text


        # If properties matched, append property cards
        if property_matches and any(keyword in user_message.lower() for keyword in ['show', 'find', 'recommend', 'suggest', 'looking for', 'villa', 'penthouse', 'apartment', 'duplex', 'office']):
            properties_html = ""
            for match in property_matches[:4]:  # Show top 4
                properties_html += format_property_card(
                    match['property'],
                    match['region'],
                    match['reasons'] if user_type == 'registered' else None
                )

            if properties_html:
                ai_response += f"\n\n<strong>Here are some properties that match your criteria:</strong>\n{properties_html}"

        return jsonify({'response': ai_response})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'response': f'I apologize, but I encountered an error: {str(e)}. Please try again.'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
