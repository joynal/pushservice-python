import signal


def load(path):
    ...

def setup_logging(log_level:str =None):
    ...

def log_settings(settings: dict, logger=None):
    ...

# Properly handle stopping of your threads
# when you Ctrl+c on local
def signal_handler(sig, frame, app):
    print("Pressed: Ctrl+c - Stopping application...")
    app.stop()


def main():
    settings = load("./settings.yaml")
    logger = setup_logging(settings.log_level)

    log_settings(settings=settings.to_dict(), logger=logger)

    app = Application(settings=settings)
    signal.signal(signal.SIGINT, lambda sig, frame: signal_handler(sig, frame, app))
    app.run()


if __name__ == "__main__":
    main()
