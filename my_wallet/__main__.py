import argparse

import config

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host", "-H", default="127.0.0.1", help="webserver host"
    )
    parser.add_argument("--port", "-p", default=5000, help="webserver host")
    parser.add_argument(
        "--debug", "-v", action="store_true", help="run in debug mode"
    )
    args = parser.parse_args()
    config.update_config_from_args(args)

    import logging

    logging.basicConfig(
        level=logging.INFO if not args.debug else logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    from my_wallet import app

    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
