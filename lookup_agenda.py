import sys
from db_table import db_table

def lookup_agenda(column, value):
    # Connect to the database tables
    session_table = db_table("session", {})
    sub_session_table = db_table("subsession", {})
    speaker_table = db_table("speaker", {})
    
    # For multiple criteria searching
    # Split criteria and values based on ',' and strip quotes if present
    criteria_list = [c.strip() for c in column.split(',')]
    values_list = [v.strip('"').strip("'") for v in value.split(',')]
    if len(criteria_list) != len(values_list):
        print("Error: The number of criteria must match the number of values.")
        sys.exit(1)

    results = []
    
    # Check session for specified speaker and return all the related (sub)session data 
    if "speaker" in criteria_list:        
        '''
        # Code below only support Single criteria handling
        # Find speakers matching the value
        speakers = speaker_table.select(where={"name": value})

        session_ids = [speaker["session_id"] for speaker in speakers if speaker["session_id"]]
        sub_session_ids = [speaker["subsession_id"] for speaker in speakers if speaker["subsession_id"]]

        # Lookup sessions and subsessions by IDs found
        for session_id in session_ids:
            results.extend(session_table.select(where={"id": session_id}))
        for sub_session_id in sub_session_ids:
            results.extend(sub_session_table.select(where={"id": sub_session_id}))
        '''

        # Revised Code below support Multiple criteria handling
        speaker_index = criteria_list.index("speaker")
        speaker_name = values_list[speaker_index]
        
        # Remove speaker from criteria for initial session query
        del criteria_list[speaker_index]
        del values_list[speaker_index]

        # Initial fetch of sessions based on speaker's name
        speakers = speaker_table.select(where={"name": speaker_name})
        session_ids = {speaker["session_id"] for speaker in speakers if speaker["session_id"]}
        sub_session_ids = {speaker["subsession_id"] for speaker in speakers if speaker["subsession_id"]}

        # If there are other criteria, filter these sessions/subsessions further
        if criteria_list:
            where_clause = " AND ".join(f"{c} = ?" for c in criteria_list)
            params = values_list
            
            # Filter session/subsession IDs based on additional criteria
            filtered_sessions = session_table.select(where={c: v for c, v in zip(criteria_list, values_list)}, additional_clause=where_clause, additional_params=params)
            session_ids = session_ids.intersection({session["id"] for session in filtered_sessions})

            filtered_subsessions = sub_session_table.select(where={c: v for c, v in zip(criteria_list, values_list)}, additional_clause=where_clause, additional_params=params)
            session_ids = session_ids.intersection({subsession["id"] for subsession in filtered_subsessions})

        # Fetch sessions' information by IDs
        for session_id in session_ids:
            results.extend(session_table.select(where={"id": session_id}))

        # Fetch subsessions' information by IDs
        for sub_session_id in sub_session_ids:
            results.extend(sub_session_table.select(where={"id": sub_session_id}))

    else:

        # Direct lookup for sessions on single criteria
        # session_results = session_table.select(where={column: value}) 

        # Direct lookup for sessions based on multiple criteria
        where_clause = " AND ".join(f"{c} = ?" for c in criteria_list)
        params = values_list
        session_results = session_table.select(where={c: v for c, v in zip(criteria_list, values_list)}, additional_clause=where_clause, additional_params=params)

        # Fetch related subsessions for each found session
        for session in session_results:
            # Append the session directly to results
            results.append(session)
            
            # Fetch related subsessions for this session
            subsession_results = sub_session_table.select(where={"session_parent_id": session["id"]})
            results.extend(subsession_results)
        # results = sorted(results, key=lambda x: x["id"])


    
    for i in range(len(results)):
        print(f"{1}, {results[i]}\n")
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
    criteria_list = [c.strip() for c in column.split(',')]
    for criteria in criteria_list:
        if criteria not in valid_columns:
            print("Invalid criteria. Please choose one or multiple criteria(s) from:" + str(valid_columns))
        else:
            lookup_agenda(column, value)

