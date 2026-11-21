
import os
from google import genai


def generate_food_description(food_name, quantity, location):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "Gemini API key is missing. Please check your .env file."

    try:
        client = genai.Client(api_key=api_key)

        prompt = f"""
        You are an assistant for FoodBridge, a food donation platform.

        Write a short and attractive food donation description.

        Food Name: {food_name}
        Quantity: {quantity}
        Location: {location}

        Write 3 to 4 simple sentences.
        Do not invent ingredients, freshness, or food safety details.
        Encourage NGOs to request this donation.
        """

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        return response.text.strip()

    except Exception as e:
        return f"AI service error: {str(e)}"


def suggest_food_category(food_name):
    api_key = os.getenv("GEMINI_API_KEY")

    food = food_name.lower().strip()

    # Recognize common food names first
    cooked_keywords = [
        'biriyani', 'biryani', 'rice', 'meals',
        'curry', 'fried rice', 'pulao', 'pasta',
        'chicken', 'fish curry', 'sambar', 'dal'
    ]

    bakery_keywords = [
        'cake', 'bread', 'bun', 'pastry', 'cookie'
    ]

    dairy_keywords = [
        'milk', 'cheese', 'butter', 'yogurt', 'curd'
    ]

    fruit_keywords = [
        'apple', 'banana', 'orange', 'mango',
        'grapes', 'vegetables', 'fruits'
    ]

    packaged_keywords = [
        'biscuit', 'chips', 'packed food', 'snacks'
    ]

    if any(word in food for word in cooked_keywords):
        return "COOKED"

    if any(word in food for word in bakery_keywords):
        return "BAKERY"

    if any(word in food for word in dairy_keywords):
        return "DAIRY"

    if any(word in food for word in fruit_keywords):
        return "FRUITS"

    if any(word in food for word in packaged_keywords):
        return "PACKAGED"

    if not api_key:
        return "OTHER"

    try:
        client = genai.Client(api_key=api_key)

        prompt = f"""
        Classify this food: {food_name}

        Choose exactly one:
        COOKED, FRUITS, BAKERY, PACKAGED, DAIRY, OTHER.

        Return only the category code.
        """

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        answer = response.text.strip().upper()

        if answer.startswith("COOKED"):
            return "COOKED"
        elif answer.startswith("FRUITS"):
            return "FRUITS"
        elif answer.startswith("BAKERY"):
            return "BAKERY"
        elif answer.startswith("PACKAGED"):
            return "PACKAGED"
        elif answer.startswith("DAIRY"):
            return "DAIRY"

        return "OTHER"

    except Exception as e:
        print("AI category error:", e)
        return "OTHER"
