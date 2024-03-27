import logging
from collections import defaultdict

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set up logging
logging.basicConfig(level=logging.INFO)


def authorize_and_open_sheet():
    logging.info("Authorizing and opening Google Sheet...")
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "app/client_secret.json", scope
    )
    client = gspread.authorize(creds)

    try:
        sheet = client.open("My Test Sheet").sheet1
        return client, sheet
    except gspread.exceptions.SpreadsheetNotFound:
        logging.error("Spreadsheet not found.")
        return client, None
    except gspread.exceptions.APIError:
        logging.error("API error occurred.")
        return client, None
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return client, None


def format_data_for_sheet(result):
    logging.info("Formatting data for Google Sheet...")
    formatted_data = defaultdict(list)
    for i, segment_stats in enumerate(result, start=2):
        formatted_data[str(i)].append(segment_stats["id"])
        formatted_data[str(i)].append(segment_stats["name"])
        formatted_data[str(i)].append(segment_stats["effort_count"])
        formatted_data[str(i)].append(segment_stats["fetch_date"])
    return formatted_data


def update_google_sheet(sheet, formatted_data):
    logging.info("Updating Google Sheet...")
    if formatted_data:
        range_start = 2
        range_end = len(formatted_data) + 1
        data_range = f"A{range_start}:D{range_end}"
        try:
            cell_list = sheet.range(data_range)
            for cell in cell_list:
                row_num = cell.row
                col_num = cell.col
                cell.value = formatted_data[str(row_num)][col_num - 1]
            sheet.update_cells(cell_list)
            logging.info("Google Sheet updated successfully.")
        except Exception as e:
            logging.error(f"An error occurred while updating Google Sheet: {e}")
