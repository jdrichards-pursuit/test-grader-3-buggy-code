import os
import google.generativeai as genai
import json
from datetime import datetime
from dotenv import load_dotenv
from termcolor import colored
import textwrap



API_KEY = os.getenv("API_KEY")


genai.config(api_key=API_KEY)



SYSTEM_INSTRUCTIONS = """
You are a helpful Gardening Guide assistant. Provide advice on plant care, gardening techniques, and solving common gardening problems. You are not allowed to answer questions that are not related to gardening, plants, trees, or flowers.
"""

FEW_SHOT_EXAMPLES = """
Human: How often should I water my houseplants?
Assistant: The watering frequency for houseplants depends on several factors like the type of plant, pot size, and environmental conditions. As a general rule:
1. Check the soil moisture: Stick your finger about an inch into the soil. If it feels dry, it's time to water.
2. Most houseplants prefer to dry out slightly between waterings.
3. Water thoroughly until water drains from the bottom of the pot.
4. Adjust based on season: Water less frequently in winter when growth slows.
Remember, it's better to underwater than overwater. What type of houseplants are you growing?
"""

user_prompt =''

def get_plant_advice(user_input, topic="general", model_choice="gemini-1.5-flash", **kwargs):
    model = genai.GenerativeModel(model_choice)
   
    full_prompt = f"{SYSTEM_INSTRUCTIONS}\n\n{FEW_SHOT_EXAMPLES}\n\n{topic}\n\nHuman: {user_input}\nAssistant:"
    try:
        response = model.generate_content(full_prompt)
        # BUG 3: Wrong attribute access (should be .text)
        return response.content
    except Exception as e:
        return f"An error occurred: {e}"


TOPIC_KEYWORDS = {
    "watering": ["water", "irrigation", "drought", "moisture"]
    "pests": ["insects", "bugs", "aphids", "mites", "disease"],
    "soil": ["dirt", "compost", "fertilizer", "nutrients"],
    "planting": ["seed", "plant", "transplant", "sapling"],
}

def classify_topic(user_input):
    user_input = user_input.lower()
    for topic, keywords in TOPIC_KEYWORDS.items():
        if any(keyword in user_input for keyword in keywords):
            return topic
    return "general"


def main():
    print(colored("Welcome to your Gardening Guide Assistant! How Can I Help You? (Type 'quit' to exit)", 'green'))
    
    while True:
        user_input = input(colored("Type your question here or type 'quit' to exit: ", 'yellow')).strip()
        if user_input.lower() == 'quit':
            print(colored("Thank you for using the Gardening Guide Assistant.", 'green'))
            return
          
        else: 
            topic = classify_topic(user_input)
           
            response = get_plant_advice(user_input, topic)
            # BUG 5: Indentation error - print statement should be inside the else block
        print(f"\nASSISTANT RESPONSE:\n")
        print(colored(f"{response}", 'grey', 'on_cyan'))   
        
       
if __name__ == "__main__":
    main()