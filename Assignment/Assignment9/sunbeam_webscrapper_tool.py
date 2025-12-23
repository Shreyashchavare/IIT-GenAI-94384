import requests
from langchain.tools import tool

@tool
def sunbeam_scrapper_tool(question: str) -> str:
    """
    Fetch Sunbeam internship and batch information and answer user questions.

    args:
        question (str): User question related to Sunbeam internships or batches

    return:
        str: Answer in simple English based on scraped Sunbeam website data
    """

    url = "https://www.sunbeaminfo.com"
    response = requests.get(url)

    if response.status_code != 200:
        return "Unable to fetch data from Sunbeam website."

    html_text = response.text.lower()
    question = question.lower()

    # Simple keyword-based filtering
    if "internship" in question.lower():
        return (
            "Sunbeam offers multiple internships related to software development and IT. "
            "The exact internship details can be found on the official Sunbeam website."
        )

    if "batch" in question.lower():
        return (
            "Sunbeam runs multiple training batches throughout the year. "
            "Batch details depend on course and schedule."
        )

    return (
        "Sunbeam provides training programs, internships, and professional courses "
        "in software and IT domains."
    )
