# pylint: disable=missing-module-docstring
# pylint: disable=possibly-used-before-assignment
import logging
import os
import subprocess
import sys

import duckdb
import streamlit as st

if "exercises_sql_tables.duckdb" not in os.listdir("./data"):
    logging.error("Database not found. Rebuilding it.")
    with open("./init_db.py", "r", encoding="utf-8") as f:
        subprocess.run(sys.executable, stdin=f, check=True)

con = duckdb.connect(database="./data/exercises_sql_tables.duckdb", read_only=False)


def compare_results_user(query_user: str) -> None:
    """
    Check that user's SQL query generates the right output by
    1) Checking the number of rows and columns
    2) Checking the values inside the table
    :param query_user: The query retrieved from the user interface.
    """
    try:
        result = con.execute(query_user).df()
        st.dataframe(result)
    except duckdb.CatalogException:
        st.write("This SQL request is not valid.")
    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
    except KeyError:
        st.write("Some columns are missing.")
    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(
            f"Result has a {n_lines_difference} lines difference with the solution_df."
        )


with st.sidebar:
    list_themes = con.execute("SELECT DISTINCT theme FROM memory_state").df()

    theme = st.selectbox(
        "What would you like to review?",
        list_themes,
        index=None,
        placeholder="Select a theme...",
    )
    st.write("You selected:", theme)
    if theme:
        exercise = (
            con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'")
            .df()
            .sort_values("last_reviewed")
            .reset_index()
        )
        st.write(exercise["tables"])

        exercise_name = exercise.loc[0, "exercise_name"]
        with open(f"./data/answers/{exercise_name}.sql", "r", encoding="utf-8") as f:
            solution = f.readlines()[0]

        solution_df = con.execute(solution).df()


if theme:
    st.header("enter your code:")
    query = st.text_area(label="Votre code SQL ici", key="user_input")
    if query:
        compare_results_user(query)

    tab2, tab3 = st.tabs(["Tables", "solution_df"])

    with tab2:
        # print(exercise.loc[0, "tables"])
        # print(type(exercise.loc[0, "tables"]))
        exercise_tables = exercise.loc[0, "tables"]
        for table in exercise_tables:
            st.write(f"table: {table}")
            df_table = con.execute(f"SELECT * FROM {table}").df()
            st.write(df_table)

    with tab3:
        st.write(solution)
