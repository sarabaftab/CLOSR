import os
import json

# Define where the data files are located
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # goes up one folder from /chatbot to /backend
DATA_DIR = os.path.join(BASE_DIR, "data")

# A reusable function to load any JSON file from /data
def load_json(filename):
    with open(os.path.join(DATA_DIR, filename), "r") as f:
        return json.load(f)

# Specific loaders for each data file
def load_products():
    return load_json("products.json")

def load_faqs():
    return load_json("faqs.json")

def load_tone_profiles():
    return load_json("tone_profiles.json")
