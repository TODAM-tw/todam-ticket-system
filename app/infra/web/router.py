import gradio as gr
from fastapi import FastAPI

from app.views.dashboard import build_playground
from app.controllers.mock_ticket import mock_ticket_routes


def setup_routers(app: FastAPI) -> None:
    gr.mount_gradio_app(app, build_playground(), path="/playground")
    
    app.include_router(mock_ticket_routes)

