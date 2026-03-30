# skills.md
# INSTRUCTIONS: Generate a draft by prompting AI, then manually refine this file.
# Delete these comments before committing.

skills:
  - name: classify_complaint
    description: Classifies a single citizen complaint into category, priority, reason, and flag based on the description.
    input: A single complaint row (dictionary or object with description field).
    output: A dictionary with category, priority, reason, and flag fields.
    error_handling: If description is missing or invalid, return category: Other, priority: Low, reason: "Invalid input", flag: NEEDS_REVIEW.

  - name: batch_classify
    description: Reads an input CSV file, applies classify_complaint to each row, and writes the results to an output CSV file.
    input: Input CSV file path and output CSV file path.
    output: The output CSV file with added classification columns.
    error_handling: If input file is not found or unreadable, raise an error; if output path is invalid, raise an error.
