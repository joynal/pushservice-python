import signal

from pushservice import monitor
from pushservice.app import Application
from pushservice.settings import load_settings


# Properly handle stopping of your threads
# when you Ctrl+c on local
def signal_handler(sig, frame, app):
    print("Pressed: Ctrl+c - Stopping application...")
    app.stop()


def main():
    settings = load_settings("./settings.yaml")
    monitor.init(settings.monitor)
    monitor.App.publish_settings(settings.display)

    app = Application(settings=settings)
    signal.signal(signal.SIGINT, lambda sig, frame: signal_handler(sig, frame, app))
    app.run()


if __name__ == "__main__":
    main()
