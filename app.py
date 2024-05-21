import argparse
from typing import Any

from dotenv import load_dotenv

from app.views.dashboard import build_playground


def main(*args: Any, **kwargs: Any,) -> None:
    parser = argparse.ArgumentParser(
        prog="todam-ticket-system",
        description="Run the server in different modes."
    )
    parser.add_argument(
        "--prod", action="store_true", 
        help="Run the server in production mode."
    )
    parser.add_argument(
        "--test", action="store_true", 
        help="Run the server in test mode."
    )
    parser.add_argument(
        "--dev", action="store_true", 
        help="Run the server in development mode."
    )
    parser.add_argument(
        "-p", "--port", type=int, default=8080,
        help="Specify the server port. Default is 8080."
    )
    
    args = parser.parse_args()

    if args.prod:
        load_dotenv(".env.prod", override=True)
    elif args.test:
        load_dotenv(".env.test", override=True)
    elif args.dev:
        load_dotenv(".env.dev", override=True)
    else:
        load_dotenv(".env", override=True)

    demo = build_playground()
    demo.launch(
        server_port=args.port
    )

if __name__ == "__main__":
    main()
