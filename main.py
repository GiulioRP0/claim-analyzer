from pydantic import ValidationError

from claim import Claim
from input_helper import (
    ask_contract_number,
    ask_description,
    ask_police_reported,
)


print("=== Insurance Claim Analyzer ===")

contract_number = ask_contract_number()
description = ask_description()
police_reported = ask_police_reported()


try:
    claim = Claim(
        contract_number=contract_number,
        description=description,
        police_reported=police_reported
    )

except ValidationError as error:
    print("Die Schadenmeldung enthält ungültige Daten.")

    for validation_error in error.errors():
        field = validation_error["loc"][0]
        message = validation_error["msg"]

        print(f"Fehler bei {field}: {message}")

else:
    print()
    print("--- Schadenmeldung ---")
    print()
    print(f"Vertragsnummer: {claim.contract_number}")
    print(f"Beschreibung: {claim.description}")

    if claim.police_reported:
        print("Polizei informiert: Ja")
    else:
        print("Polizei informiert: Nein")