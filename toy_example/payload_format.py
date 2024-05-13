payload = {
    "ticket_subject": "Send by Hugo",
    "ticket_description": "M3 6666```'';;;`ls -al`",
    "department_id": "20000183827401924640",
    "segment_id": "fajl13289jl"
}

payload_string = "{\r\n"
for key, value in payload.items():
    payload_string += f"    \"{key}\": \"{value}\",\r\n"
payload_string += "}"
print(payload_string)

payload = {
    "ticket_subject": "test by Hugo",
    "ticket_description": "M3 666 666```'';;;`ls -al`",
    "department_id": "238409",
    "segment_id": "239807"
}

print(str(payload))