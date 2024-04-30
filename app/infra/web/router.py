import gradio as gr
from fastapi import FastAPI

from app.views.dashboard import build_playground


def setup_routers(app: FastAPI) -> None:
    gr.mount_gradio_app(app, build_playground(), path="/playground")

