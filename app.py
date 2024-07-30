# pylint: disable=missing-module-docstring

import duckdb
import streamlit as st

con = duckdb.connect(database="./data/exercises_sql_tables.duckdb", read_only=False)


# solution_df = duckdb.sql(ANSWER_STR).df()


with st.sidebar:
    theme = st.selectbox(
        "What would you like to review?",
        ("cross_joins", "GroupBy", "Windows Functions"),
        index=0,
        placeholder="Select a theme...",
    )
    st.write("You selected:", theme)
    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'").df()
    st.write(exercise["tables"])


st.header("enter your code:")
query = st.text_area(label="Votre code SQL ici", key="user_input")
if query:
    try:
        result = con.execute(query).df()
        st.dataframe(result)
    except duckdb.CatalogException as e:
        st.write("This SQL request is not valid.")
#
#     try:
#         result = result[solution_df.columns]
#         st.dataframe(result.compare(solution_df))
#     except KeyError as e:
#         st.write("Some columns are missing.")
#
#     n_lines_difference = result.shape[0] - solution_df.shape[0]
#     if n_lines_difference != 0:
#         st.write(
#             f"Result has a {n_lines_difference} lines difference with the solution_df."
#         )
#
tab2, tab3 = st.tabs(["Tables", "solution_df"])


with tab2:
    # print(exercise.loc[0, "tables"])
    # print(type(exercise.loc[0, "tables"]))
    exercise_tables = exercise.loc[0, "tables"]
    for table in exercise_tables:
        st.write(f"table: {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.write(df_table)
#     st.dataframe(beverages)
#     st.write("table: food_items")
#     st.dataframe(food_items)
#     st.write("expected result:")
#     st.dataframe(solution_df)
#
with tab3:
    exercise_name = exercise.loc[0, "exercise_name"]
    with open(f"./data/answers/{exercise_name}.sql", "r", encoding='utf-8') as f:
        l = f.readlines()[0]
        st.write(l)
