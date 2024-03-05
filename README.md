## Introduction
The purpose of this Python code is to facilitate the importation of data from an Excel file into a SQLite database and to provide a flexible lookup mechanism for querying this data based on various criteria. The code is divided into two main scripts: import_agenda.py for data importation and lookup_agenda.py for data querying.

### import_agenda.py
The import_agenda.py script is designed to parse an Excel file (agenda.xls), extract relevant information about sessions, subsessions, and speakers, and then insert this data into a SQLite database according to a predefined schema. This process involves creating tables for sessions, subsessions, and speakers if they do not already exist and populating them with the data extracted from the Excel file.

### lookup_agenda.py
The lookup_agenda.py script, allows users to query the populated database for sessions and subsessions based on specific criteria such as date, location, and speaker name. It supports both single-criterion searches (e.g., all sessions in a specific room) and multi-criterion searches (e.g., all sessions in a specific room on a specific date). This script demonstrates the capability to handle complex queries by dynamically constructing SQL queries based on the input criteria.
Key Functionalities
* Data Importation: import_agenda.py reads from an Excel file and imports data into a SQLite database, creating necessary tables and ensuring data is correctly organized into sessions, subsessions, and associated speakers.
* Flexible Data Lookup: lookup_agenda.py enables querying the database for sessions and subsessions using single or multiple search criteria, enhancing data retrievability and user interaction with the stored information.
* Dynamic Query Construction: The code efficiently handles dynamic SQL query generation, allowing for flexible and complex searches without hard-coding query parameters, thereby accommodating a wide range of user queries.
* Data Relationship Handling: It carefully manages the relationships between sessions, subsessions, and speakers, ensuring that queries return accurate and comprehensive results, including hierarchical data relationships.

## Summary
This codebase significantly streamlines the process of importing event-related data from an Excel format into a structured database and subsequently querying this data based on various user-defined criteria. It exemplifies a practical application of Python programming for data manipulation and SQL database interaction, showcasing dynamic query construction and the handling of complex data relationships. The functionality to import data and then query it using single or multiple criteria addresses the need for versatile data management tools in organizing and retrieving event information effectively.##