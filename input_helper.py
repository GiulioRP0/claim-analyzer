def ask_contract_number():
    while True:
        contract_number = input("Vertragsnummer: ").strip()

        if len(contract_number) >= 3:
            return contract_number

        print("Die Vertragsnummer muss mindestens 3 Zeichen lang sein.")


def ask_description():
    while True:
        description = input("Beschreibe deinen Schaden: ").strip()

        if len(description) >= 10:
            return description

        print("Die Beschreibung muss mindestens 10 Zeichen lang sein.")


def ask_police_reported():
    while True:
        police_answer = input(
            "Wurde der Schaden der Polizei gemeldet? (j/n): "
        ).strip().lower()

        if police_answer == "j":
            return True

        elif police_answer == "n":
            return False

        print("Ungültige Eingabe. Bitte j oder n eingeben.")