from app.pipeline import Pipeline


class Application:
    """
    Application bootstrap.

    Responsible for:
    - Initializing application resources
    - Wiring dependencies
    - Starting the execution pipeline
    """

    def __init__(self) -> None:
        self.pipeline = Pipeline()

    def run(self) -> None:
        print("=" * 45)
        print("Fund Compliance Reporting Engine")
        print("=" * 45)

        print("[BOOT] Starting application...")

        self.pipeline.run()

        print("[BOOT] Application started successfully.")