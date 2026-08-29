from claim import Claim


claim = Claim(
    contract_number="V-12345",
    description="Fahrrad wurde gestohlen",
    police_reported="yes"
)

print(claim.police_reported)
print(type(claim.police_reported))