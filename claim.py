class Claim:
    def __init__(self, contract_number, description, police_reported): #läuft jedes Mal, wenn neue Schadenmeldung erstelt wird.
        self.contract_number = contract_number
        self.description = description
        self.police_reported = police_reported