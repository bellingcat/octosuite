# LogRoller This class is where the main notification strings/messages are held, and are being used in two different
# cases (they're being used by logging to be written to log files, and being printed out to the screen).


ctrl_c = "Session terminated with Ctrl+C."
error = "An error occurred: {}"
session_opened = "Opened new session on {}:{}"
session_closed = "Session closed at {}."
viewing_logs = "Viewing logs"
viewing_csv = "Viewing CSV file(s)..."
deleted = "Deleted: {}"
reading = "Reading: {}"
file_downloading = "Downloading: {}"
file_downloaded = "Downloaded: downloads/{}"
info_not_found = "Information not found: {}, {}, {}"
user_not_found = "User not found: @{}"
org_not_found = "Organization not found: @{}"
repo_or_user_not_found = "Repository or User not found: {}, @{}"
prompt_log_csv = "Would you like to log this output to a .csv file?"
logged_to_csv = "Output logged: {}"
limit_output = "Limit '{}' output to how many? (1-100)"
