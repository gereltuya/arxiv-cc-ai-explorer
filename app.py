import experiments


def run():

    experiments.intro()
    experiments.showcase_search_arxiv()
    experiments.explore_data("./data/arxiv-cc-ai-papers.csv")


if __name__ == "__main__":
    run()
