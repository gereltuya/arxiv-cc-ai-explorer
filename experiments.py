import arxiv
import pandas as pd
import streamlit as st
import plotly.express as px
import inspect
import textwrap


def intro():
    st.write("# Hello! 👋")
    st.markdown(
        """
        This is a sample app to explore arXiv pre-prints of AI papers for Climate action.
    """
    )


def search_arxiv(query: str, max_results: int, download: bool) -> pd.DataFrame:
    search = arxiv.Search(
        query=query, #"all:artificial intelligence AND all:climate change"
        max_results=max_results, #1000
        sort_by=arxiv.SortCriterion.Relevance,
        sort_order=arxiv.SortOrder.Descending,
    )

    arxiv_papers = []
    unavailable = []

    for result in search.results():
        temp = {}

        temp["entry_id"] = result.entry_id
        temp["updated"] = result.updated
        temp["published"] = result.published
        temp["title"] = result.title
        temp["authors"] = result.authors
        temp["summary"] = result.summary.replace("\n", " ")
        temp["comment"] = result.comment
        temp["journal_ref"] = result.journal_ref
        temp["doi"] = result.doi
        temp["primary_category"] = result.primary_category
        temp["categories"] = result.categories
        temp["links"] = result.links
        temp["pdf_url"] = result.pdf_url
        temp["links"] = result.links

        arxiv_papers.append(temp)

        if download is True:
            try:
                result.download_pdf(dirpath="./data/")
                print("paper downloaded\n")
            except:
                print("-----> paper not available\n")
                unavailable.append(result.title)
                pass
        else:
            pass

    # arxiv_df = pd.DataFrame.from_csv("./data/arxiv-cc-ai-papers.csv")
    arxiv_df = pd.DataFrame.from_records(arxiv_papers)
    return arxiv_df


def showcase_search_arxiv():
    st.subheader("0. Data collection")
    if st.checkbox("Show data collection code"):
        sourcelines, _ = inspect.getsourcelines(search_arxiv)
        st.code(textwrap.dedent("".join(sourcelines[1:])))


@st.cache
def read_data(data_filepath) -> pd.DataFrame:
    df = pd.read_csv(data_filepath)
    return df.loc[:, df.columns != "Unnamed: 0"]


def explore_data(data_filepath: str):
    def show_histogram_plot(selected_df: pd.DataFrame):
        st.subheader("2. Histogram")
        feature = st.selectbox(
            "Which feature?", selected_df.columns[:])
        fig2 = px.histogram(selected_df, x=feature,
                            color="primary_category", marginal="rug")
        st.plotly_chart(fig2)

    def show_scatter_plot(selected_df: pd.DataFrame):
        st.subheader("3. Scatter plot")
        feature_x = st.selectbox("Which feature on x?",
                                 selected_df.columns)
        feature_y = st.selectbox("Which feature on y?",
                                 selected_df.columns)

        fig3 = px.scatter(selected_df, x=feature_x,
                         y=feature_y, color="primary_category")
        st.plotly_chart(fig3)

    st.subheader("1. Source data")
    source_df = read_data(data_filepath)
    if st.checkbox("Show collected data"):
        st.write(source_df)

    show_histogram_plot(source_df)
    show_scatter_plot(source_df)

    st.subheader("4. Code")
    if st.checkbox("Show data exploration code"):
        sourcelines, _ = inspect.getsourcelines(explore_data)
        st.code(textwrap.dedent("".join(sourcelines[1:])))
