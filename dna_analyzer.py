"""
DNA Sequence Analyzer
Author: Ochai Moses Ameh

A beginner-friendly Python tool for analyzing DNA sequences.
"""

from collections import Counter


def clean_sequence(sequence):
    """Convert a sequence to uppercase and remove whitespace."""
    return "".join(sequence.split()).upper()


def validate_sequence(sequence):
    """Return characters that are not valid DNA bases."""
    valid_bases = set("ATGC")
    return sorted(set(sequence) - valid_bases)


def analyze_sequence(sequence):
    """Calculate basic statistics for a DNA sequence."""
    sequence = clean_sequence(sequence)

    if not sequence:
        return {"valid": False, "error": "Sequence is empty."}

    invalid_bases = validate_sequence(sequence)

    if invalid_bases:
        return {
            "valid": False,
            "error": "Invalid characters: " + ", ".join(invalid_bases),
        }

    counts = Counter(sequence)
    length = len(sequence)
    gc_content = (counts["G"] + counts["C"]) / length * 100

    if gc_content < 40:
        gc_category = "Low"
    elif gc_content <= 60:
        gc_category = "Moderate"
    else:
        gc_category = "High"

    return {
        "valid": True,
        "sequence": sequence,
        "length": length,
        "A": counts["A"],
        "T": counts["T"],
        "G": counts["G"],
        "C": counts["C"],
        "GC_content": round(gc_content, 2),
        "GC_category": gc_category,
    }


def parse_fasta(fasta_text):
    """Read sequences from text formatted as FASTA."""
    sequences = []
    sequence_id = None
    sequence_parts = []

    for line in fasta_text.splitlines():
        line = line.strip()

        if not line:
            continue

        if line.startswith(">"):
            if sequence_id is not None:
                sequences.append(
                    (sequence_id, "".join(sequence_parts))
                )

            sequence_id = line[1:].strip() or "Unnamed sequence"
            sequence_parts = []
        else:
            if sequence_id is None:
                raise ValueError(
                    "FASTA sequence data must begin with a > header."
                )

            sequence_parts.append(line)

    if sequence_id is not None:
        sequences.append((sequence_id, "".join(sequence_parts)))

    if not sequences:
        raise ValueError("No sequences were found in the FASTA text.")

    return sequences


def print_sequence_report(sequence_id, result):
    """Display the analysis of one sequence."""
    print("\n" + "=" * 40)
    print("Sequence ID:", sequence_id)

    if not result["valid"]:
        print("Status: INVALID")
        print("Reason:", result["error"])
        return

    print("Status: Valid DNA sequence")
    print("Sequence:", result["sequence"])
    print("Length:", result["length"], "bases")
    print("A:", result["A"])
    print("T:", result["T"])
    print("G:", result["G"])
    print("C:", result["C"])
    print("GC content:", result["GC_content"], "%")
    print("GC category:", result["GC_category"])


def print_summary(results):
    """Summarize the results from multiple sequences."""
    valid_results = [
        result for _, result in results if result["valid"]
    ]

    invalid_count = len(results) - len(valid_results)

    print("\n" + "=" * 40)
    print("PROJECT SUMMARY")
    print("=" * 40)
    print("Total sequences:", len(results))
    print("Valid sequences:", len(valid_results))
    print("Invalid sequences:", invalid_count)

    if valid_results:
        average_length = sum(
            result["length"] for result in valid_results
        ) / len(valid_results)

        average_gc = sum(
            result["GC_content"] for result in valid_results
        ) / len(valid_results)

        print("Average length:", round(average_length, 2), "bases")
        print("Average GC content:", round(average_gc, 2), "%")


def analyze_single_sequence():
    """Ask the user to analyze one DNA sequence."""
    sequence = input("Enter a DNA sequence: ")
    result = analyze_sequence(sequence)
    print_sequence_report("Single sequence", result)


def analyze_multiple_sequences():
    """Analyze example sequences in FASTA format."""
    fasta_data = """>Sequence_1
ATGCGTAC
>Sequence_2
AATTGGCC
>Sequence_3
GGGCCCAA
>Sequence_4
ATBXGCTA
"""

    try:
        sequences = parse_fasta(fasta_data)
    except ValueError as error:
        print("FASTA error:", error)
        return

    results = []

    for sequence_id, sequence in sequences:
        result = analyze_sequence(sequence)
        results.append((sequence_id, result))
        print_sequence_report(sequence_id, result)

    print_summary(results)


def main():
    """Display the program menu."""
    while True:
        print("\nDNA SEQUENCE ANALYZER")
        print("1. Analyze one DNA sequence")
        print("2. Analyze built-in FASTA examples")
        print("3. Exit")

        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            analyze_single_sequence()
        elif choice == "2":
            analyze_multiple_sequences()
        elif choice == "3":
            print("Thank you for using DNA Sequence Analyzer!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()