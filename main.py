from __future__ import annotations
from pathlib import Path
from app.bootstrap import Bootstrap
from app.pipeline import Pipeline
from dotenv import load_dotenv
import traceback
import sys
import os


def main() -> None:
    
    """
    Application entry point.
    """
    load_dotenv()
    
    # Check Env file
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

    missing = [key for key, value in required_envs.items() if not value]

    if missing:
        print()
        print("=" * 80)
        print("APPLICATION ERROR")
        print("=" * 80)
        print(f"Missing env variables: {', '.join(missing)}")
        return

    bootstrap = Bootstrap()

    try:

        pipeline = Pipeline(
            bootstrap=bootstrap,
        )

        configuration_path = Path(
            "configs/firm_a.yaml"
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

        # print(narrative.content)

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

        print()
        print("=" * 80)
        print("APPLICATION ERROR")
        print("=" * 80)

    
        print(f"Error Message: {error_message}")
        print(f"File Name: {file_name}")
        print(f"Line Number: {line_no}")
        
    finally:
        bootstrap.shutdown()


if __name__ == "__main__":
    main()
