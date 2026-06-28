from __future__ import annotations
from pathlib import Path
from app.bootstrap import Bootstrap
from app.pipeline import Pipeline
import traceback
import sys

def main() -> None:
    """
    Application entry point.
    """

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

        computation, reconciliation = pipeline.run( 
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

        if reconciliation.passed:
            print("✅ Reconciliation PASSED")
        else:
            print("❌ Reconciliation FAILED")

    except Exception as e :
        # Get the current exception traceback
        exc_type, exc_value, exc_tb = sys.exc_info()
        tb = traceback.extract_tb(exc_tb)
        last_frame = tb[-1]  # frame paling akhir = lokasi error terjadi
    
        # Extract filename and line number
        file_name = last_frame.filename
        line_no = last_frame.lineno
        error_message = str(e)
    
        print(f"Error Message: {error_message}")
        print(f"File Name: {file_name}")
        print(f"Line Number: {line_no}")
        
    finally:
        bootstrap.shutdown()


if __name__ == "__main__":
    main()
