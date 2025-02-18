import json
from datetime import datetime

def calculate_points(user_data):
    points = 0
    decay_factor = 0.9  # Older interactions lose 10% weight per entry
    recent_weight = 1.2  # More weight for recent interactions
    max_recent = 10  # Consider last 10 interactions more

    interactions = user_data['interactions']
    recent_interactions = interactions[-max_recent:]

    for i, interaction in enumerate(interactions):
        color = interaction['color']
        multiplier = {
            "Green": 4, "Light Green": 3, "Yellow": 2, "Orange": -2, "Red": -4
        }.get(color, 0)
        
        platform_weights = {
            "Instagram": 1.0,
            "Facebook": 1.0,
            "Google": 1.5,
            "WhatsApp": 2.0,
            "Avenza": 1.2
        }
        
        weight = decay_factor ** (len(interactions) - i)
        if interaction in recent_interactions:
            weight *= recent_weight
        
        platform_weight = platform_weights.get(interaction['platform'], 1.0)
        
        points += (interaction['likes'] * (multiplier * 1) * weight * platform_weight)
        points += (interaction['comments'] * (multiplier * 2) * weight * platform_weight)
        points += (interaction['texts'] * (multiplier * 3) * weight * platform_weight)
        points += (interaction['calls'] * (multiplier * 3) * weight * platform_weight)
        points += (interaction['searches'] * (multiplier * 2) * weight * platform_weight)
        if interaction['follows']:
            points += (multiplier * 4 * weight * platform_weight)
    
    points += (user_data['scheme_benefits'] * 5 * decay_factor)
    points += (user_data['bjp_posts'] * 3 * decay_factor)
    points += (user_data['congress_posts'] * -3 * decay_factor)
    
    return points

def determine_color(points):
    if points >= 30:
        return "Green (Strong BJP)"
    elif 15 <= points < 30:
        return "Light Green (75% BJP)"
    elif -15 < points < 15:
        return "Yellow (Neutral)"
    elif -30 <= points <= -15:
        return "Orange (75% Congress)"
    else:
        return "Red (Strong Congress)"

def save_user_data(username, user_data):
    try:
        with open("user_data.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    
    data[username] = user_data
    with open("user_data.json", "w") as file:
        json.dump(data, file, indent=4)

def load_user_data(username):
    try:
        with open("user_data.json", "r") as file:
            data = json.load(file)
            return data.get(username, None)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def apply_decay(points, interactions):
    decay_rate = 0.95
    return points * (decay_rate ** len(interactions))

def main():
    while True:
        username = input("Enter user name: ")
        user_data = load_user_data(username)
        
        if user_data:
            print(f"Welcome back, {user_data['full_name']}!")
            user_data['scheme_benefits'] += int(input("Did you benefit from BJP schemes recently? (Enter count): "))
            
            new_bjp_posts = input("Did you post about BJP? (yes/no): ").strip().lower()
            if new_bjp_posts == 'yes':
                user_data['bjp_posts'] += 1
                
            new_congress_posts = input("Did you post about Congress? (yes/no): ").strip().lower()
            if new_congress_posts == 'yes':
                user_data['congress_posts'] += 1
        
        else:
            print(f"Welcome, {username}! Please enter your details.")
            user_data = {
                "full_name": input("Full Name: "),
                "age": int(input("Age: ")),
                "place": input("Place: "),
                "annual_income": int(input("Annual Income: ")),
                "education": input("Educational Background: "),
                "category": input("Category: "),
                "location": input("Location: "),
                "social_links": {
                    "Instagram": input("Want to connect Instagram? (yes/no): ").strip().lower() == 'yes',
                    "Facebook": input("Want to connect Facebook? (yes/no): ").strip().lower() == 'yes',
                    "X": input("Want to connect X? (yes/no): ").strip().lower() == 'yes',
                    "Google": input("Want to connect Google? (yes/no): ").strip().lower() == 'yes',
                    "WhatsApp": input("Want to connect WhatsApp? (yes/no): ").strip().lower() == 'yes'
                },
                "family_on_avenza": input("Are there any family members on Avenza? (yes/no): ").strip().lower() == 'yes',
                "scheme_benefits": int(input("Times benefited from BJP schemes: ")),
                "bjp_posts": int(input("Number of posts related to BJP: ")),
                "congress_posts": int(input("Number of posts related to Congress: ")),
                "interactions": []
            }
        
        points = calculate_points(user_data)
        points = apply_decay(points, user_data['interactions'])
        color = determine_color(points)
        
        user_data['points'] = points
        user_data['judgment'] = color
        save_user_data(username, user_data)
        
        next_action = input("Do you want to enter a new user? (yes/no): ").strip().lower()
        if next_action != 'yes':
            break

if __name__ == "__main__":
    main()
