import pandas as pd
import streamlit as st
import pandasql as ps
if __name__ =="__main__":
    """
    return the result based on input SQL query by executing it on dataframe in streamlit
    """


    st.title("CSV extractor by SQL")

    data_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if data_file:
        st.write("Data preview:")
        df = pd.read_csv(data_file)
        st.dataframe(df)
        query = st.text_area("Enter SQL query with df", "SELECT * FROM df")
        if st.button("Execute"):
            try:
                result = ps.sqldf(query, {'df': df})
                st.write("Query Result:")
                st.dataframe(result)
            except Exception as e:
                st.error(f"An error occured:{e}")