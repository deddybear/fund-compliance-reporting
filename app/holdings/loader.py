
from __future__ import annotations
import csv
from collections.abc import Sequence
from decimal import Decimal, InvalidOperation
from pathlib import Path

from app.holdings.models import Holding


class HoldingsLoader:
    """
    Load and validate the assignment sample_holdings.csv file.
    """

    REQUIRED_COLUMNS = {
        "instrument_id",
        "instrument_name",
        "asset_class",
        "issuer_name",
        "issuer_type",
        "parent_issuer",
        "credit_rating",
        "downgraded_from",
        "market_value_sgd",
        "modified_duration",
    }

    REQUIRED_VALUES = {
        "instrument_id",
        "instrument_name",
        "asset_class",
        "issuer_name",
        "issuer_type",
        # "credit_rating",
        "market_value_sgd",
        "modified_duration",
    }

    NUMERIC_COLUMNS = {
        "market_value_sgd",
        "modified_duration",
    }

    def load(self, path: Path) -> list[Holding]:
        """
        Load holdings from a CSV file.
        """

        if not path.exists():
            raise FileNotFoundError(
                f"Holdings file not found: {path}"
            )

        if path.suffix.lower() != ".csv":
            raise ValueError(
                "Holdings file must be a CSV file."
            )

        with path.open(
            mode="r",
            encoding="utf-8-sig",
            newline="",
        ) as file:

            reader = csv.DictReader(file)

            if reader.fieldnames is None:
                raise ValueError(
                    "CSV header is missing."
                )

            self._validate_headers(reader.fieldnames)

            holdings: list[Holding] = []

            for row_number, row in enumerate(
                reader,
                start=2,
            ):
                holdings.append(
                    self._validate_row(
                        row=row,
                        row_number=row_number,
                    )
                )

        if not holdings:
            raise ValueError(
                "Holdings file is empty."
            )

        return holdings

    def _validate_headers(
        self,
        headers: Sequence[str],
    ) -> None:
        """
        Validate required CSV headers.
        """

        missing = self.REQUIRED_COLUMNS - set(headers)

        if missing:
            raise ValueError(
                "Missing required columns: "
                + ", ".join(sorted(missing))
            )

    def _validate_row(
        self,
        row: dict[str, str | None],
        row_number: int,
    ) -> Holding:
        """
        Validate and convert one CSV row into a Holding model.
        """

        values: dict[str, str | Decimal] = {}

        for column in self.REQUIRED_COLUMNS:

            value = (row.get(column) or "").strip()

            if (
                column in self.REQUIRED_VALUES
                and value == ""
            ):
                raise ValueError(
                    f"Row {row_number}: "
                    f"'{column}' is required."
                )

            if (
                column in self.NUMERIC_COLUMNS
                and value != ""
            ):
                try:
                    values[column] = Decimal(value)
                except InvalidOperation as exc:
                    raise ValueError(
                        f"Row {row_number}: "
                        f"'{column}' must be numeric."
                    ) from exc
            else:
                values[column] = value

        return Holding(
            instrument_id=str(values["instrument_id"]),
            instrument_name=str(values["instrument_name"]),
            asset_class=str(values["asset_class"]),
            issuer_name=str(values["issuer_name"]),
            issuer_type=str(values["issuer_type"]),
            parent_issuer=str(values["parent_issuer"]),
            credit_rating=str(values["credit_rating"]),
            downgraded_from=str(values["downgraded_from"]),
            market_value_sgd=Decimal(values["market_value_sgd"]),
            modified_duration=Decimal(values["modified_duration"]),
        )

