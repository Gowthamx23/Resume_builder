import json

def load_profiles(file_path):
    """
    Load profiles from JSON file.
    """
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to load profiles: {e}")
        return {}

def save_profile(file_path, name, profile):
    """
    Save a new profile to JSON file.
    """
    try:
        profiles = load_profiles(file_path)
        profiles[name] = profile
        with open(file_path, "w") as f:
            json.dump(profiles, f, indent=4)
    except Exception as e:
        print(f"Failed to save profile: {e}")

def delete_profile(file_path, name):
    """
    Delete a profile from JSON file.
    """
    try:
        profiles = load_profiles(file_path)
        if name in profiles:
            del profiles[name]
            with open(file_path, "w") as f:
                json.dump(profiles, f, indent=4)
    except Exception as e:
        print(f"Failed to delete profile: {e}")

def get_ui_styles():
    """
    Custom CSS for dark theme.
    """
    return """
    <style>
        .stApp {
            background-color: #1a1a1a;
            font-family: Arial, sans-serif;
            color: #ffffff;
        }
        .title {
            color: #00ff00;
            font-size: 2em;
            text-align: center;
            margin-bottom: 20px;
        }
        .stTextInput, .stTextArea, .stSelectbox {
            background-color: #333333;
            color: #ffffff;
        }
        .stButton>button {
            background-color: #00ff00;
            color: #000000;
            border-radius: 5px;
            padding: 8px 16px;
        }
        .stButton>button:hover {
            background-color: #33ff33;
        }
        .stSpinner, .stText, .stError, .stSuccess, .stWarning {
            color: #ffffff !important;
        }
        .stError {
            background-color: #660000 !important;
        }
        .stSuccess {
            background-color: #006600 !important;
        }
        .stSidebar {
            background-color: #222222;
        }
    </style>
    """