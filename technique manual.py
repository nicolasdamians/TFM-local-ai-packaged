import json
import datetime

def read_multiline_text(prompt):
    """
    Reads multi-line text until the user enters two consecutive blank lines.
    Returns the text as a single string.
    """
    print(prompt)
    print("(Type your text. Press Enter twice consecutively to finish.)")
    lines = []
    consecutive_blank = 0
    while True:
        line = input()
        if line == "":
            consecutive_blank += 1
            if consecutive_blank == 2:
                break
        else:
            consecutive_blank = 0
            lines.append(line)
    return "\n".join(lines)

def read_multiline_list(prompt):
    """
    Reads multi-line input (each line as an item in a list) until two consecutive blank lines.
    Returns a list of entered lines.
    """
    print(prompt)
    print("(Type each item on a new line. Press Enter twice consecutively to finish.)")
    items = []
    consecutive_blank = 0
    while True:
        line = input("- ")
        if line == "":
            consecutive_blank += 1
            if consecutive_blank == 2:
                break
        else:
            consecutive_blank = 0
            items.append(line)
    return items

def show_summary(data):
    """
    Prints the JSON data in a formatted way.
    """
    print("\n--- Current JSON Data ---")
    print(json.dumps(data, indent=4))
    print("-------------------------\n")

def edit_field(data, field):
    """
    Allows user to edit a field of the JSON data.
    Handles both simple string fields and multi-line list/text fields.
    """
    if field in ["technique_id", "title", "category", "last_updated", "author"]:
        new_value = input(f"Enter new value for {field} (current: {data[field]}): ")
        if new_value.strip() != "":
            data[field] = new_value.strip()
    elif field == "description":
        new_value = read_multiline_text(f"Enter new value for {field} (current value will be replaced):")
        if new_value.strip() != "":
            data[field] = new_value
    elif field in ["requirements", "enumeration_steps", "validation", "references"]:
        new_value = read_multiline_list(f"Enter new values for {field} (current items will be replaced):")
        data[field] = new_value
    elif field == "exploitation_steps":
        new_steps = read_multiline_list("Enter new exploitation steps (each step on a new line):")
        # Ensure exploitation_steps includes technique_id matching the main technique_id
        data["exploitation_steps"] = {"technique_id": data["technique_id"], "steps": new_steps}
    elif field == "detection":
        new_tools = read_multiline_list("Enter new detection tools (each tool on a new line):")
        data["detection"] = {"tools": new_tools}
    else:
        print("Field not recognized. Please check the field name.")
    return data

def main():
    print("=== Technique JSON Data Entry ===\n")
    # Collect basic fields
    technique_id = input("Enter technique_id: ").strip()
    title = input("Enter title: ").strip()
    category = input("Enter category: ").strip()

    # Multi-line description
    description = read_multiline_text("Enter description:")

    # Multi-line list fields
    requirements = read_multiline_list("Enter requirements:")
    enumeration_steps = read_multiline_list("Enter enumeration_steps:")

    # Exploitation steps: we ask for the list of steps.
    exploitation_steps_list = read_multiline_list("Enter exploitation_steps (list of steps):")
    exploitation_steps = {
        "technique_id": technique_id,
        "steps": exploitation_steps_list
    }

    validation = read_multiline_list("Enter validation steps:")
    detection_tools = read_multiline_list("Enter detection tools:")
    detection = {"tools": detection_tools}
    references = read_multiline_list("Enter references:")

    # Last updated: default to today's date if not provided
    default_date = datetime.date.today().isoformat()
    last_updated = input(f"Enter last_updated (default {default_date}): ").strip()
    if last_updated == "":
        last_updated = default_date

    # Author: default to Nico
    author = input("Enter author (default Nico): ").strip()
    if author == "":
        author = "Nico"

    # Assemble the data into a dictionary
    data = {
        "technique_id": technique_id,
        "title": title,
        "category": category,
        "description": description,
        "requirements": requirements,
        "enumeration_steps": enumeration_steps,
        "exploitation_steps": exploitation_steps,
        "validation": validation,
        "detection": detection,
        "references": references,
        "last_updated": last_updated,
        "author": author
    }

    # Show summary and allow editing
    while True:
        show_summary(data)
        edit_choice = input("Do you want to edit any field? (y/n): ").strip().lower()
        if edit_choice == "y":
            field_to_edit = input("Enter the field name you want to edit (e.g., technique_id, description, requirements, exploitation_steps, detection, etc.): ").strip()
            if field_to_edit in data:
                data = edit_field(data, field_to_edit)
            else:
                print("Field not found in data. Please check the field name.")
        else:
            break

    # Save JSON to file named with the technique_id
    filename = f"{data['technique_id']}.json"
    with open(filename, "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)
    print(f"\nJSON data saved to {filename}")

if __name__ == "__main__":
    main()
