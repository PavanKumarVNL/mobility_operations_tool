import csv
from datetime import datetime


class DataValidator:

    DRIVER_COLUMNS = {
        "driver_id",
        "driver_name",
        "city",
        "vehicle_type",
        "rating",
        "status"
    }

    TRIP_COLUMNS = {
        "trip_id",
        "driver_id",
        "rider_id",
        "city",
        "pickup_zone",
        "drop_zone",
        "request_time",
        "pickup_time",
        "drop_time",
        "distance_km",
        "fare",
        "status",
        "cancellation_reason"
    }

    ACTIVITY_COLUMNS = {
        "driver_id",
        "timestamp",
        "status"
    }

    def validate_file(self, file_path, file_type):
        errors = []

        required_columns = self._get_required_columns(file_type)

        try:
            with open(file_path, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                if reader.fieldnames is None:
                    return ["CSV file has no header"]

                missing_columns = required_columns - set(reader.fieldnames)

                if missing_columns:
                    errors.append(
                        f"Missing columns: {sorted(missing_columns)}"
                    )

                if errors:
                    return errors

                for row_number, row in enumerate(reader, start=2):
                    if file_type == "drivers":
                        errors.extend(
                            self._validate_driver_row(row, row_number)
                        )

                    elif file_type == "trips":
                        errors.extend(
                            self._validate_trip_row(row, row_number)
                        )

                    elif file_type == "activity":
                        errors.extend(
                            self._validate_activity_row(row, row_number)
                        )

        except FileNotFoundError:
            errors.append("File not found")

        except Exception as error:
            errors.append(f"Unable to read file: {error}")

        return errors

    def _get_required_columns(self, file_type):

        if file_type == "drivers":
            return self.DRIVER_COLUMNS

        if file_type == "trips":
            return self.TRIP_COLUMNS

        if file_type == "activity":
            return self.ACTIVITY_COLUMNS

        return set()

    def _validate_driver_row(self, row, row_number):
        errors = []

        if not row["driver_id"]:
            errors.append(
                f"Row {row_number}: driver_id is missing"
            )

        if not row["driver_name"]:
            errors.append(
                f"Row {row_number}: driver_name is missing"
            )

        try:
            rating = float(row["rating"])

            if rating < 0 or rating > 5:
                errors.append(
                    f"Row {row_number}: invalid rating"
                )

        except ValueError:
            errors.append(
                f"Row {row_number}: rating must be numeric"
            )

        return errors

    def _validate_trip_row(self, row, row_number):
        errors = []

        if not row["trip_id"]:
            errors.append(
                f"Row {row_number}: trip_id is missing"
            )

        if not row["driver_id"]:
            errors.append(
                f"Row {row_number}: driver_id is missing"
            )

        errors.extend(
            self._validate_datetime(
                row["request_time"],
                "request_time",
                row_number
            )
        )

        if row["pickup_time"]:
            errors.extend(
                self._validate_datetime(
                    row["pickup_time"],
                    "pickup_time",
                    row_number
                )
            )

        if row["drop_time"]:
            errors.extend(
                self._validate_datetime(
                    row["drop_time"],
                    "drop_time",
                    row_number
                )
            )

        if row["pickup_time"] and row["drop_time"]:

            pickup_time = datetime.strptime(
                row["pickup_time"],
                "%Y-%m-%d %H:%M:%S"
            )

            drop_time = datetime.strptime(
                row["drop_time"],
                "%Y-%m-%d %H:%M:%S"
            )

            # if drop_time < pickup_time:
            #     errors.append(
            #         f"Row {row_number}: invalid trip duration"
            #     )
        
        try:
            distance = float(row["distance_km"])

            if distance < 0:
                errors.append(
                    f"Row {row_number}: negative distance"
                )

        except ValueError:
            errors.append(
                f"Row {row_number}: distance_km must be numeric"
            )

        try:
            fare = float(row["fare"])

        except ValueError:
            errors.append(
                f"Row {row_number}: fare must be numeric"
            )

        return errors

    def validate_trip_driver_references(self, trip_file, driver_file):
        errors = []

        with open(driver_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            driver_ids = {row["driver_id"] for row in reader}

        with open(trip_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row_number, row in enumerate(reader, start=2):

                if row["driver_id"] not in driver_ids:
                    errors.append(
                        f"Row {row_number}: unknown driver_id {row['driver_id']}"
                    )

        return errors
    
    def _validate_activity_row(self, row, row_number):
        errors = []

        if not row["driver_id"]:
            errors.append(
                f"Row {row_number}: driver_id is missing"
            )

        errors.extend(
            self._validate_datetime(
                row["timestamp"],
                "timestamp",
                row_number
            )
        )

        valid_statuses = {
            "Online",
            "Busy",
            "Idle",
            "Offline"
        }

        if row["status"] not in valid_statuses:
            errors.append(
                f"Row {row_number}: invalid activity status"
            )

        return errors

    def _validate_datetime(self, value, field_name, row_number):
        if not value:
            return [
                f"Row {row_number}: {field_name} is missing"
            ]

        try:
            datetime.strptime(
                value,
                "%Y-%m-%d %H:%M:%S"
            )

        except ValueError:
            return [
                f"Row {row_number}: invalid {field_name}"
            ]

        return []