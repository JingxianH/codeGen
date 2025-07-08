import pandas as pd
import requests
import os

# --- Dependencies from ._constants (mocked for this example) ---
# In a real application, you would import these from your project's constant file.
CATEGORIES = [
    {"name": "Algorithms", "slug": "algorithms"},
    {"name": "Database", "slug": "database"},
    {"name": "Shell", "slug": "shell"},
]

TOPIC_TAGS = [
    {"name": "Array", "slug": "array"},
    {"name": "String", "slug": "string"},
    {"name": "Hash Table", "slug": "hash-table"},
    {"name": "Dynamic Programming", "slug": "dynamic-programming"},
    {"name": "Math", "slug": "math"},
]


# --- Provided Library Code ---

class GetQuestionsList:
    """A class to scrape the list of questions, their topic tags, and company tags.

    Args:
        limit (int, optional): The maximum number of questions to query for from Leetcode's graphql API. Defaults to 10,000.
    """

    def __init__(self, limit: int = 10_000):
        self.limit = limit
        self.questions = pd.DataFrame()
        self.companies = pd.DataFrame()
        self.questionTopics = pd.DataFrame()
        self.categories = pd.DataFrame()
        self.topicTags = pd.DataFrame()
        self.questionCategory = pd.DataFrame()

    def scrape(self):
        """Scrapes LeetCode data including company tags, questions, question topics,
        and categories.
        """
        self._scrape_companies()
        self._scrape_questions_list()
        self._extract_question_topics()
        self._get_categories_and_topicTags_lists()
        self._scrape_question_category()
        self._add_category_to_questions_list()

    def to_csv(self, directory: str) -> None:
        """A method to export the scraped data into csv files in preparation for
        injection into a database.

        Args:
            directory (str): The directory path to export the scraped data into.
        """
        if not os.path.exists(directory):
            os.makedirs(directory)

        self.companies.to_csv(os.path.join(directory, "companies.csv"), index=False)
        self.questions["QID"] = self.questions["QID"].astype(int)
        self.questions.to_csv(os.path.join(directory, "questions.csv"), index=False)
        self.questionTopics.to_csv(
            os.path.join(directory, "questionTopics.csv"), index=True, index_label="id"
        )
        self.categories.to_csv(os.path.join(directory, "categories.csv"), index=False)
        self.topicTags.to_csv(os.path.join(directory, "topicTags.csv"), index=False)
        self.questionCategory.to_csv(
            os.path.join(directory, "questionCategory.csv"), index=True, index_label="id"
        )
        print(f"\nAll data successfully exported to the '{directory}' directory.")

    def _scrape_companies(self):
        """Scrape the company tags of each question. This always returns an empty
        dataframe as this is a paid only feature."""
        print("Scraping companies ... ", end="")
        data = {
            "query": """query questionCompanyTags {
                    companyTags {
                        name
                        slug
                        questionCount
                    }
                }
            """,
            "variables": {},
        }
        r = requests.post("https://leetcode.com/graphql", json=data).json()
        self.companies = pd.json_normalize(r["data"]["companyTags"])
        print("Done")

    def _scrape_questions_list(self):
        """
        Scrapes the list of questions from leetcode.com and store them in the 'questions' dataframe.
        """
        print("Scraping questions list ... ", end="")
        data = {
            "query": """query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
                    problemsetQuestionList: questionList(
                        categorySlug: $categorySlug
                        limit: $limit
                        skip: $skip
                        filters: $filters
                    ) {
                        total: totalNum
                        questions: data {
                            acceptanceRate: acRate
                            difficulty
                            QID: questionFrontendId
                            paidOnly: isPaidOnly
                            title
                            titleSlug
                            topicTags {
                                slug
                            }
                        }
                    }
                }
            """,
            "variables": {
                "categorySlug": "",
                "skip": 0,
                "limit": self.limit,
                "filters": {},
            },
        }

        r = requests.post("https://leetcode.com/graphql", json=data).json()
        self.questions = pd.json_normalize(
            r["data"]["problemsetQuestionList"]["questions"]
        )[
            [
                "QID",
                "title",
                "titleSlug",
                "difficulty",
                "acceptanceRate",
                "paidOnly",
                "topicTags",
            ]
        ]
        self.questions["topicTags"] = self.questions["topicTags"].apply(
            lambda w: [tag["slug"] for tag in w]
        )
        print("Done")

    def _extract_question_topics(self):
        """Create a table with the edge list of questions and topic tags."""
        print("Extracting question topics ... ", end="")
        self.questionTopics = (
            self.questions[["QID", "topicTags"]]
            .rename(columns={"topicTags": "tagSlug"})
            .explode("tagSlug", ignore_index=True)
        ).dropna()
        print("Done")

    def _get_categories_and_topicTags_lists(self):
        """Get the categories and topic tags of LeetCode problems."""
        print("Getting Categories ... ", end="")
        self.categories = pd.DataFrame.from_records(CATEGORIES)
        print("Done")
        print("Getting Topic Tags ... ", end="")
        self.topicTags = pd.DataFrame.from_records(TOPIC_TAGS)
        print("Done")

    def _scrape_question_category(self):
        """Scrape the category of each question."""
        print("Extracting question category ... ", end="")
        categories_data = []
        for category in self.categories["slug"].values:
            data = {
                "query": """query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
                        problemsetQuestionList: questionList(
                            categorySlug: $categorySlug
                            limit: $limit
                            skip: $skip
                            filters: $filters
                        ) {
                            questions: data {
                                QID: questionFrontendId
                            }
                        }
                    }
                """,
                "variables": {
                    "categorySlug": category,
                    "skip": 0,
                    "limit": self.limit,
                    "filters": {},
                },
            }

            r = requests.post("https://leetcode.com/graphql", json=data).json()
            if r.get("data") and r["data"].get("problemsetQuestionList"):
                categories = pd.json_normalize(
                    r["data"]["problemsetQuestionList"]["questions"]
                )
                if not categories.empty:
                    categories["categorySlug"] = category
                    categories_data.append(categories)

        if categories_data:
            self.questionCategory = pd.concat(categories_data, axis=0, ignore_index=True)
        print("Done")

    def _add_category_to_questions_list(self):
        """Adds the category and formatted topic tags to the main questions DataFrame."""
        self.questions["topicTags"] = self.questions["topicTags"].apply(
            lambda w: ",".join(w)
        )
        if not self.questionCategory.empty:
            self.questions = self.questions.merge(
                self.questionCategory, on="QID", how="left"
            )

    def _get_questions_df(self, limit=100, difficulties='ALL'):
        leetcode_scraper = GetQuestionsList(limit=limit)
        leetcode_scraper.scrape()
        questions_df = leetcode_scraper.questions

        if 'difficulty' in questions_df.columns and difficulties != 'ALL':
            print('*****')
            # Split into three DataFrames by difficulty
            by_difficulty_df = questions_df[questions_df['difficulty'] == difficulties]
            return by_difficulty_df
        else:
            print("Column 'difficulty' not found in DataFrame")
        return questions_df

# --- Main Execution Script ---
if __name__ == "__main__":
    # 1. Instantiate the scraper. A smaller limit is used for a quick demo.
    print("Initializing LeetCode scraper...")
    leetcode_scraper = GetQuestionsList(limit=100)

    # 2. Call the main 'scrape' method to fetch and process all data.
    leetcode_scraper.scrape()

    # 3. Access the final questions DataFrame.
    questions_df = leetcode_scraper.questions

    # 4. Display the first 10 results.
    print("\n✅ Successfully fetched LeetCode questions.")
    print("Displaying the first 10 questions:")
    print(questions_df.head(10).to_string())

    # 5. (Optional) Export all DataFrames to CSV files.
    # leetcode_scraper.to_csv(directory="leetcode_data")