import json

from fastapi import APIRouter, status

mock_ticket_routes = APIRouter(
    tags=["mock_ticket"], prefix="/mock_ticket")

@mock_ticket_routes.get("", status_code=status.HTTP_200_OK)
async def get_log_segment(id: int):
    try:
        file_name = f"./mock-tickets/mock-ticket-{id}.json"
        with open(file_name) as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e)}

