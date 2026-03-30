"""
UC-0A — Complaint Classifier
Built using RICE → agents.md → skills.md → CRAFT workflow.
"""
import argparse
import csv
import re

# Classification schema from agents.md enforcement
CATEGORIES = [
    "Pothole", "Flooding", "Streetlight", "Waste", "Noise", 
    "Road Damage", "Heritage Damage", "Heat Hazard", "Drain Blockage", "Other"
]

URGENT_KEYWORDS = [
    "injury", "child", "school", "hospital", "ambulance", "fire", "hazard", "fell", "collapse"
]

# Keyword mappings for categories (simple rule-based classification)
CATEGORY_KEYWORDS = {
    "Pothole": ["pothole", "hole", "bump", "crater", "dip"],
    "Flooding": ["flood", "water", "rain", "overflow", "submerged"],
    "Streetlight": ["streetlight", "light", "lamp", "bulb", "dark"],
    "Waste": ["waste", "garbage", "trash", "dump", "litter"],
    "Noise": ["noise", "loud", "sound", "music", "party"],
    "Road Damage": ["road", "crack", "damage", "pavement", "broken"],
    "Heritage Damage": ["heritage", "monument", "historical", "vandal", "damage"],
    "Heat Hazard": ["heat", "hot", "temperature", "sun", "burn"],
    "Drain Blockage": ["drain", "block", "clog", "sewer", "pipe"],
}

def classify_complaint(row: dict) -> dict:
    """
    Classify a single complaint row based on description.
    Returns: dict with keys: complaint_id, category, priority, reason, flag
    
    Follows RICE enforcement rules from agents.md.
    """
    description = row.get('description', '').lower()
    complaint_id = row.get('complaint_id', '')
    
    # Determine category
    category = "Other"
    matched_keywords = []
    for cat, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in description:
                category = cat
                matched_keywords.append(keyword)
                break
        if category != "Other":
            break
    
    # If no clear match, flag as NEEDS_REVIEW
    flag = ""
    if not matched_keywords:
        flag = "NEEDS_REVIEW"
    
    # Determine priority
    priority = "Standard"  # Default
    urgent_match = False
    for keyword in URGENT_KEYWORDS:
        if keyword in description:
            priority = "Urgent"
            urgent_match = True
            matched_keywords.append(keyword)
            break
    
    # If not urgent and category is Other, set to Low
    if priority == "Standard" and category == "Other":
        priority = "Low"
    
    # Create reason sentence citing specific words
    if matched_keywords:
        reason = f"The description contains '{matched_keywords[0]}' which indicates {category.lower()}"
        if urgent_match:
            reason += f" and '{matched_keywords[-1]}' which requires urgent priority"
        reason += "."
    else:
        reason = "The description does not contain clear indicators for classification."
    
    return {
        'complaint_id': complaint_id,
        'category': category,
        'priority': priority,
        'reason': reason,
        'flag': flag
    }


def batch_classify(input_path: str, output_path: str):
    """
    Read input CSV, classify each row, write results CSV.
    
    Handles errors gracefully, produces output even if some rows fail.
    """
    results = []
    try:
        with open(input_path, 'r', newline='', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                try:
                    classified = classify_complaint(row)
                    results.append(classified)
                except Exception as e:
                    # On failure, add a row with Other category and NEEDS_REVIEW
                    results.append({
                        'complaint_id': row.get('complaint_id', ''),
                        'category': 'Other',
                        'priority': 'Low',
                        'reason': f'Classification failed: {str(e)}',
                        'flag': 'NEEDS_REVIEW'
                    })
    except FileNotFoundError:
        print(f"Error: Input file {input_path} not found.")
        return
    except Exception as e:
        print(f"Error reading input file: {str(e)}")
        return
    
    # Write output CSV
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as outfile:
            fieldnames = ['complaint_id', 'category', 'priority', 'reason', 'flag']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
    except Exception as e:
        print(f"Error writing output file: {str(e)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UC-0A Complaint Classifier")
    parser.add_argument("--input",  required=True, help="Path to test_[city].csv")
    parser.add_argument("--output", required=True, help="Path to write results CSV")
    args = parser.parse_args()
    batch_classify(args.input, args.output)
    print(f"Done. Results written to {args.output}")
