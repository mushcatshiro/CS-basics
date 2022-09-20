sql_ref = {
    "student_table": {
        "select": "SELECT (columns) FROM student_table st (join|where)",
        "insert": "INSERT INTO student_table (#1) VALUES (#2)",
        "update": "UPDATE student_table SET (#1) WHERE (#2)",
        "delete": "DELETE FROM student_table WHERE (#1)",
        "order": "ORDER BY (#1) (#2)"

    }
}

input_json = {
    "student_table": {
        "select": {
            "columns": "id, name, desc",
            "where": "st.id = 1",
            "where": "st.name = 'a'"
        }
    }
}