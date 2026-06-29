from __future__ import annotations
from pathlib import Path
from app.bootstrap import Bootstrap
from app.pipeline import Pipeline
from dotenv import load_dotenv
from app.audit.events import AuditEventType 
from app.audit.events import AuditStatus
from app.audit.database import AuditDatabase
from app.audit.repository import AuditRepository
from app.audit.service import AuditService
from app.configuration.profiles import (
    available_profiles,
    profile_exists,
)
import traceback
import sys
import os
import argparse

def main() -> None:
    """
    Application entry point.
    """

    #
    # Audit Logger with SQLite
    #
    audit_database = AuditDatabase(
        database_path=Path(
            "storage/audit/audit.db"
        ),
    )

    audit_database.initialize()

    audit_repository = AuditRepository(
        database=audit_database,
    )

    audit_service = AuditService(
        repository=audit_repository,
    )


    #
    # Load File ENV
    #
    load_dotenv()

    #
    # Initialize Bootstrap
    #
    bootstrap: Bootstrap | None = None
    
    #
    # Get Value Env File
    #
    neo4j_uri=os.getenv("NEO4J_URI", "")
    neo4j_username=os.getenv("NEO4J_USERNAME", "")
    neo4j_password=os.getenv("NEO4J_PASSWORD", "")
    openai_api_key=os.getenv("OPENAI_API_KEY", "")
    openai_model=os.getenv("OPENAI_API_MODEL", "")

    required_envs = {
        "NEO4J_URI": neo4j_uri,
        "NEO4J_USERNAME": neo4j_username,
        "NEO4J_PASSWORD": neo4j_password,
        "OPENAI_API_KEY": openai_api_key,
        "OPENAI_API_MODEL": openai_model,
    }

    #
    # Check Value Env File
    #
    missing = [key for key, value in required_envs.items() if not value]

    if missing:
        error_message = f"Missing env variables: {', '.join(missing)}"

        audit_service.log( 
            event_type=AuditEventType.ERROR, 
            status=AuditStatus.FAILED, 
            trigger_name="main", 
            message=error_message, 
            payload={}, 
        )

        print()
        print("=" * 80)
        print("APPLICATION ERROR")
        print("=" * 80)
        print(error_message)
        return


    #
    # Check file on folders configs exist or not if not will be retunr error
    #
    if not available_profiles():

        error_message = "configs yaml for firm not found !"

        audit_service.log( 
            event_type=AuditEventType.ERROR, 
            status=AuditStatus.FAILED, 
            trigger_name="main", 
            message=error_message, 
            payload={}, 
        )

        print()
        print("=" * 80)
        print("APPLICATION ERROR")
        print("=" * 80)
        print()
        print(error_message)
        return


    try:

        parser = argparse.ArgumentParser(
            add_help=False,
        )

        parser.add_argument(
            "--profile",
            type=str,
        )

        args = parser.parse_args()

        if not args.profile:

            error_message = "Missing required argument: --profile"

            audit_service.log( 
                event_type=AuditEventType.ERROR, 
                status=AuditStatus.FAILED, 
                trigger_name="main", 
                message=error_message, 
                payload={}, 
            )


            print()
            print("=" * 80)
            print("APPLICATION ERROR")
            print("=" * 80)
            print()
            print(error_message)
            print()
            print("Example:")
            print("    uv run python main.py --profile firm_a")
            print()
            print("Available profiles:")
            print(available_profiles())
            return
        
        configuration_path = Path(
            f"configs/{args.profile}.yaml"
        )

        if not configuration_path.exists():
        
            print()
            print("=" * 80)
            print("APPLICATION ERROR")
            print("=" * 80)
            print()
            print(f"Profile '{args.profile}' not found.")
            print()
            print("Available profiles:")
            print(available_profiles())
            return

        bootstrap = Bootstrap()

        bootstrap.audit_service.log( 
            event_type=AuditEventType.APPLICATION_STARTED, 
            status=AuditStatus.INFO, 
            trigger_name="main", 
            message="Application started."
        )

        pipeline = Pipeline(
            bootstrap=bootstrap,
        )

        holdings_path = Path(
            "data/sample_holdings.csv"
        )

        answer_key_path = Path(
            "data/firm_A_answer_key.xlsx"
        )

        computation, reconciliation, narrative, report_path = pipeline.run( 
            configuration_path=configuration_path, 
            holdings_path=holdings_path, 
            answer_key_path=answer_key_path, 
        )

        print()
        print("=" * 80)
        print("Computed Figures")
        print("=" * 80)
        print()

        for figure in computation.figures: 
            print( 
                f"{figure.section:<18}" 
                f"{figure.figure:<45}" 
                f"{figure.value}" 
            )
        
        print() 
        print("=" * 80) 
        print("Reconciliation") 
        print("=" * 80)

        for item in reconciliation.items:

            symbol = "✓" if item.matched else "✗"

            print(
                f"{symbol} "
                f"{item.figure:<45}"
                f"Expected={item.expected_value:<10}"
                f"Actual={item.actual_value:<10}"
            )

        print()

        print(
            f"Matched : {reconciliation.matched_count}"
        )

        print(
            f"Failed  : {reconciliation.failed_count}"
        )

        print()
        print("=" * 80)
        print("Traceability")
        print("=" * 80)

        for figure in computation.figures:
            print("=" * 60)
            print(figure.figure)
            print("Graph :", figure.graph_path)
            print("Citation :", figure.citation)

        #
        # Narrative
        #
        print()
        print("=" * 80)
        print("Narrative")
        print("=" * 80)

        print(narrative.content)

        #
        # Report Information
        #
        print()
        print("=" * 80)
        print("Report")
        print("=" * 80)

        print(f"Saved To : {report_path}")
        print(f"Model    : {narrative.model}")

        # if narrative.prompt_tokens is not None:
        #     print(f"Prompt Tokens     : {narrative.prompt_tokens}")

        # if narrative.completion_tokens is not None:
        #     print(f"Completion Tokens : {narrative.completion_tokens}")

        # if narrative.total_tokens is not None:
        #     print(f"Total Tokens      : {narrative.total_tokens}")


    except Exception as e :
        # Get the current exception traceback
        exc_type, exc_value, exc_tb = sys.exc_info()
        tb = traceback.extract_tb(exc_tb)
        last_frame = tb[-1]  # frame paling akhir = lokasi error terjadi
    
        # Extract filename and line number
        file_name = last_frame.filename
        line_no = last_frame.lineno
        error_message = str(e)

        audit_service.log( 
            event_type=AuditEventType.ERROR, 
            status=AuditStatus.FAILED, 
            trigger_name="main", 
            message=error_message, 
            payload={ 
                "exception": type(e).__name__, 
                "file": file_name, 
                "line": line_no, 
                "traceback": traceback.format_exc(), 
            }, 
        )

        print()
        print("=" * 80)
        print("APPLICATION ERROR")
        print("=" * 80)

    
        print(f"Error Message: {error_message}")
        print(f"File Name: {file_name}")
        print(f"Line Number: {line_no}")
        
    finally:

        audit_service.log( 
            event_type=AuditEventType.APPLICATION_SHUTDOWN, 
            status=AuditStatus.INFO, 
            trigger_name="main", 
            message="Application shutdown.", 
        )


        if bootstrap is not None: 
            

            bootstrap.shutdown()


if __name__ == "__main__":
    main()
