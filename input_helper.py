def ask_contract_number():
    while True:
        contract_number = input("Vertragsnummer: ").strip()

        if contract_number:
            return contract_number

        print("Die Vertragsnummer darf nicht leer sein.")

def ask_description():
    while True:
        description = input("Beschreibe deinen Schaden: ").strip()

        if description:
            return description

        print("Die Beschreibung darf nicht leer sein.")
      


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
      


