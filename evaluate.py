from evaluation_cases import evaluation_cases
from llm_classifier import classify_claim


correct = 0

for case in evaluation_cases:
    description = case["description"]
    expected = case["expected_category"]

    classification = classify_claim(description)
    actual = classification.category

    print(f"Beschreibung: {description}")
    print(f"Erwartet:     {expected}")
    print(f"Qwen:         {actual}")

    if actual == expected:
        print("Ergebnis:     RICHTIG")
        correct += 1
    else:
        print("Ergebnis:     FALSCH")

    print()


total = len(evaluation_cases)
accuracy = correct / total * 100

print("--------------------")
print(f"Richtig: {correct} von {total}")
print(f"Accuracy: {accuracy:.1f} %")