skills:
  - name: retrieve_policy
    description: Loads .txt policy file, returns content as structured numbered sections
    input: File path string to the .txt policy document.
    output: Structured data representation mapping each numbered clause to its original text.
    error_handling: Return an explicit error if the file cannot be accessed or parsing fails.

  - name: summarize_policy
    description: Takes structured sections, produces compliant summary with clause references
    input: Structured data mapping of numbered clauses.
    output: Summarized text referencing original clause numbers while strictly adhering to enforcement rules.
    error_handling: If a clause cannot be safely summarized without dropping conditions, fall back to quoting it verbatim and flag it.
