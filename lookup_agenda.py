import sys
from db_table import db_table

def lookup_agenda(column, value):
    # Connect to the database tables
    session_table = db_table("session", {})
    sub_session_table = db_table("subsession", {})
    speaker_table = db_table("speaker", {})

    results = []
    
    # Check session for specified speaker and return all the related (sub)session data 
    if column == "speaker":
        # Find speakers matching the value
        speakers = speaker_table.select(where={"name": value})

        session_ids = [speaker["session_id"] for speaker in speakers if speaker["session_id"]]
        sub_session_ids = [speaker["subsession_id"] for speaker in speakers if speaker["subsession_id"]]

        # Lookup sessions and subsessions by IDs found
        for session_id in session_ids:
            results.extend(session_table.select(where={"id": session_id}))
        for sub_session_id in sub_session_ids:
            results.extend(sub_session_table.select(where={"id": sub_session_id}))
    else:
        # Direct lookup for sessions 
        session_results = session_table.select(where={column: value})
        # results.extend(session_results)

        # Fetch related subsessions for each found session
        for session in session_results:
            # Append the session directly to results
            results.append(session)
            
            # Fetch related subsessions for this session
            session_parent_id = session["id"]
            subsession_results = sub_session_table.select(where={"session_parent_id": session_parent_id})
            
            # Extend results with the found subsessions
            results.extend(subsession_results)
        # results = sorted(results, key=lambda x: x["id"])

    
    for i in range(len(results)):
        print(i+1, results[i],"\n")
    print(f"{value} attended {len(results)} sessions in total") if column == "speaker" else print(f"{value} have {len(results)} record(s) in total")

    # Close database connections
    session_table.close()
    sub_session_table.close()
    speaker_table.close()

if __name__ == "__main__":
    #  Check user has provided both a <column> and a <value>
    if len(sys.argv) != 3:
        print("Usage: lookup_agenda.py <column> <value>")
        sys.exit(1)
    
    column, value = sys.argv[1], sys.argv[2]
    valid_columns = ["date", "time_start", "time_end", "session_title", "location", "description", "speaker"]
    if column not in valid_columns:
        print("Invalid column. Please choose from:" + str(valid_columns))
    else:
        lookup_agenda(column, value)

