import json

def load_user_data():
    try:
        with open("user_data.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def filter_users(users, filters, details):
    filtered_users = []
    for user in users.values():
        match = True
        for key, value in filters.items():
            if isinstance(value, tuple):  # For range filters like age or income
                if not (value[0] <= user.get(key, 0) <= value[1]):
                    match = False
                    break
            elif str(user.get(key, "")).strip().lower() != str(value).strip().lower():
                match = False
                break
        if match:
            filtered_users.append({detail: user.get(detail, "N/A") for detail in details})
    return filtered_users

def demographic_analysis(users, filter_key, filter_value):
    filter_value = str(filter_value).strip().lower()
    filtered_users = [user for user in users.values() if str(user.get(filter_key, "")).strip().lower() == filter_value]
    total_users = len(filtered_users)
    if total_users == 0:
        return f"No data available for {filter_key}: {filter_value}"
    
    bjp_supporters = sum(1 for user in filtered_users if "BJP" in user.get("judgment", ""))
    congress_supporters = sum(1 for user in filtered_users if "Congress" in user.get("judgment", ""))
    neutral = total_users - (bjp_supporters + congress_supporters)
    
    return {
        "Total Users": total_users,
        "BJP Supporters": bjp_supporters,
        "Congress Supporters": congress_supporters,
        "Neutral": neutral,
        "BJP Influence (%)": round((bjp_supporters / total_users) * 100, 2),
        "Congress Influence (%)": round((congress_supporters / total_users) * 100, 2),
        "Neutral Percentage (%)": round((neutral / total_users) * 100, 2)
    }

def classify_financial_class(income):
    try:
        income = int(income)
        if income >= 5000000:
            return "Ultra Rich"
        elif income >= 1000000:
            return "Upper Class"
        elif income >= 500000:
            return "Upper Middle Class"
        elif income >= 200000:
            return "Middle Class"
        elif income >= 100000:
            return "Lower Middle Class"
        else:
            return "Below Poverty Line"
    except ValueError:
        return "Invalid Income"

def main():
    users = load_user_data()
    if not users:
        print("No user data available.")
        return
    
    while True:
        choice = input("Do you want a list of users? (yes/no/exit): ").strip().lower()
        if choice == "exit":
            break
        
        if choice == "yes":
            filters = {}
            details = []
            
            if input("Filter by age? (yes/no): ").strip().lower() == "yes":
                try:
                    min_age = int(input("Enter minimum age: "))
                    max_age = int(input("Enter maximum age: "))
                    filters["age"] = (min_age, max_age)
                except ValueError:
                    print("Invalid age input.")
                    continue
            
            if input("Filter by education? (yes/no): ").strip().lower() == "yes":
                filters["education"] = input("Enter education level: ").strip()
            
            if input("Filter by location? (yes/no): ").strip().lower() == "yes":
                filters["location"] = input("Enter location: ").strip()
            
            if input("Filter by category? (yes/no): ").strip().lower() == "yes":
                filters["category"] = input("Enter category: ").strip()
            
            if input("Filter by financial class? (yes/no): ").strip().lower() == "yes":
                income = input("Enter annual income: ")
                income_range = classify_financial_class(income)
                if income_range == "Invalid Income":
                    print("Invalid income input.")
                    continue
                filters["financial_class"] = income_range
            
            print("Select details to display (comma separated):")
            all_details = ["full_name", "age", "place", "annual_income", "education", "category", "location", "points", "judgment"]
            print(", ".join(all_details))
            details = [detail.strip() for detail in input("Enter details: ").strip().split(",")]
            
            result = filter_users(users, filters, details)
            print("Filtered Users:", json.dumps(result, indent=4))
            
        else:
            filter_type = input("Do you want a demographic analysis of a (place/category/age/financial class)?: ").strip().lower()
            filter_value = input(f"Enter the {filter_type} you want to analyze: ").strip()
            if filter_type == "financial class":
                filter_value = classify_financial_class(filter_value)
                if filter_value == "Invalid Income":
                    print("Invalid income input.")
                    continue
            
            report = demographic_analysis(users, filter_type, filter_value)
            print("Demographic Report:", json.dumps(report, indent=4))

if __name__ == "__main__":
    main()
