# pylint: disable=missing-module-docstring
# pylint: disable=exec-used
import logging
import os

import duckdb
import streamlit as st

if "exercises_sql_tables.duckdb" not in os.listdir("./data"):
    logging.error("Database not found. Rebuilding it.")
    with open("./init_db.py", 'r', encoding='utf-8') as f:
        exec(f.read())

con = duckdb.connect(database="./data/exercises_sql_tables.duckdb", read_only=False)

with st.sidebar:
    theme = st.selectbox(
        "What would you like to review?",
        ("cross_joins", "GroupBy", "Windows Functions"),
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
        try:
            result = con.execute(query).df()
            st.dataframe(result)
        except duckdb.CatalogException as e:
            st.write("This SQL request is not valid.")

        try:
            result = result[solution_df.columns]
            st.dataframe(result.compare(solution_df))
        except KeyError as e:
            st.write("Some columns are missing.")

        n_lines_difference = result.shape[0] - solution_df.shape[0]
        if n_lines_difference != 0:
            st.write(
                f"Result has a {n_lines_difference} lines difference with the solution_df."
            )

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
