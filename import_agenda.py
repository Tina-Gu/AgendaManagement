import xlrd
# import sqlite3, sys
from db_table import db_table


def import_agenda(excel_file):
    # Open agenda.xls dataset and load the requested sheet if it is not already loaded
    workbook = xlrd.open_workbook(excel_file)
    sheet = workbook.sheet_by_index(0)
    
    # Define the database schema
    session = {
        "id": "integer PRIMARY KEY autoincrement",
        "date": "text",
        "time_start": "text",
        "time_end": "text",
        "session_title": "text",
        "location": "text",
        "description": "text",
        "speakers": "text"
    }

    sub_session = {
        "id": "integer PRIMARY KEY autoincrement",
        "date": "text",
        "time_start": "text",
        "time_end": "text",
        "session_title": "text",
        "location": "text",
        "description": "text",
        "speakers": "text",
        "session_parent_id": "integer", # foriegn key to connect parent session
        "FOREIGN KEY(session_parent_id)": "REFERENCES session(id)"
    }
    
    speaker = {
        "id": "integer PRIMARY KEY autoincrement",
        "name": "text",
        "session_id": "integer", # foriegn key to connect session
        "subsession_id": "integer", # foriegn key to connect subsession
        "FOREIGN KEY(session_id)": "REFERENCES session(id)", 
        "FOREIGN KEY(subsession_id)": "REFERENCES subsession(id)" 
    }

    # Initialize the database table
    session_table = db_table("session", session)
    sub_session_table = db_table('subsession', sub_session)
    speaker_table = db_table('speaker', speaker)


    session_table.db_conn.execute('BEGIN TRANSACTION')
    

    # Parse the Excel file and insert data into the table
    for row_idx in range(15, sheet.nrows):  # Start from row 16 as per the given file format
        row = sheet.row_values(row_idx)
        
        # Update Session Table
        if row[3] == "Session":
            session_parent_id = session_table.insert({
                "date": row[0],
                "time_start": row[1],
                "time_end": row[2],
                "session_title": row[4],
                "location": row[5],
                "description": row[6],
                "speakers": row[7]
            })

        # Update Subsession Table
        else: 
            if session_parent_id is None:
                raise ValueError("Sub-session found without a preceding main session")
            
            subsession_id = sub_session_table.insert({
                "date": row[0],
                "time_start": row[1],
                "time_end": row[2],
                "session_title": row[4],
                "location": row[5],
                "description": row[6],
                "speakers": row[7],
                "session_parent_id": session_parent_id
            })
        
        # Update Speaker Table
        speakers = row[7].split(';')
        for speaker_name in speakers:
            speaker_name = speaker_name.strip()  # Remove leading/trailing spaces
            if speaker_name: 
                speaker_entry = {
                    "name": speaker_name,
                    "session_id": session_parent_id if row[3] == "Session" else None,
                    "subsession_id": subsession_id if row[3] == "Sub" else None
                }
                speaker_table.insert(speaker_entry)

    session_table.db_conn.commit()

    # Close the database connection
    session_table.close()
    sub_session_table.close()
    speaker_table.close()
    
if __name__ == "__main__":
    
    import_agenda("agenda.xls") #sys.argv[1]
