import os
import zipfile
import pandas as pd
from io import TextIOWrapper

def strip_spaces(value):
    """Strip spaces from strings in a DataFrame column."""
    if isinstance(value, str):
        return value.strip()
    return value

def _find_in_zip(zf: zipfile.ZipFile, target_name: str) -> str:
    """
    Find a file by suffix inside a zip. Returns the internal path if found.
    Handles zips that have folder prefixes (e.g., 'gtfs/shapes.txt').
    """
    target_name = target_name.strip("/")
    for name in zf.namelist():
        if name.endswith("/"):  # skip directories
            continue
        if name.endswith(target_name):
            return name
    raise FileNotFoundError(f"Could not find '{target_name}' in zip archive.")

def load_and_clean_gtfs_file_from_zip(zf: zipfile.ZipFile, inner_path: str, selected_columns=None):
    """Load a GTFS file from a zip, rename columns, strip whitespace, and select relevant columns."""
    print(f"Loading {inner_path} from zip...")  # Debug logging

    with zf.open(inner_path, mode="r") as f:
        # Wrap binary handle into text for pandas
        df = pd.read_csv(TextIOWrapper(f, encoding="utf-8"), low_memory=False)

    print(f"Loaded {inner_path} with {len(df)} rows.")

    # Strip whitespace from column names
    df.columns = df.columns.str.strip()

    # Strip whitespace from all string columns
    str_cols = df.select_dtypes(include='object').columns
    df[str_cols] = df[str_cols].apply(lambda x: x.str.strip())

    # Select relevant columns if all are present
    if selected_columns:
        available_columns = set(df.columns)
        if all(col in available_columns for col in selected_columns):
            df = df[selected_columns]
        else:
            print(f"Warning: Missing selected columns in {inner_path}, using full DataFrame.")
    print(f"Finished processing {inner_path}.")
    return df

def load_gtfs_data_from_zip(zip_path, files_to_load=None):
    """
    Load and clean specified GTFS files from a zip archive.
    
    Args:
        zip_path (str): Path to the GTFS zip file.
        files_to_load (list, optional): List of file keys to load. Default is None (loads all files).

    Returns:
        dict: A dictionary {key: DataFrame} for the specified GTFS files.
    """
    gtfs_files = {
        "shapes": ('shapes.txt', None),
        "fare_rules": ('fare_rules.txt', None),
        "fare_attributes": ('fare_attributes.txt', ['fare_id', 'price']),
        "stop_times": ('stop_times.txt', ['trip_id', 'arrival_time', 'departure_time', 'stop_id', 'stop_sequence', 'stop_headsign']),
        "routes": ('routes.txt', ['route_id', 'route_long_name', 'route_short_name', 'route_type', 'route_color']),
        "trips": ('trips.txt', ['route_id', 'trip_id', 'route_variant', 'trip_headsign', 'trip_short_name', 'direction_id', 'shape_id']),
        "stops": ('stops.txt', ['stop_id', 'stop_name', 'stop_lat', 'stop_lon', 'zone_id'])
    }

    # Load all if no specific files are specified
    if files_to_load is None:
        files_to_load = gtfs_files.keys()

    gtfs_data = {}

    with zipfile.ZipFile(zip_path, mode="r") as zf:
        for key in files_to_load:
            if key in gtfs_files:
                file_name, columns = gtfs_files[key]
                # Locate the file inside the zip even if there's a folder prefix
                inner_path = _find_in_zip(zf, file_name)
                gtfs_data[key] = load_and_clean_gtfs_file_from_zip(zf, inner_path, selected_columns=columns)
            else:
                print(f"Warning: {key} is not a recognized GTFS file key.")

    return gtfs_data