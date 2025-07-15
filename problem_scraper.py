import pandas as pd
import json

from db_accessor import LeetCodeDB
from extractor import get_leetcode_question
from get_questions import GetQuestionsList
from llm_code_generation import generate_solution_with_deepseek
from supabase_accessor import SupabaseDB


class ProblemScraper:
    """
    A class to scrape LeetCode problems, generate solutions, and store them in a database.
    """

    def __init__(self, num_questions: int = 200, local = True):
        """
        Initializes the ProblemScraper with the number of questions to scrape.

        Args:
            num_questions (int): The number of questions to retrieve.
        """
        self.num_questions = num_questions
        self.get_questions_client = GetQuestionsList(self.num_questions)
        if local:
            self.db_manager = LeetCodeDB()
        else:
            self.db_manager = SupabaseDB()

        pd.set_option('display.max_columns', None)

    def scrape_and_store_problems(self):
        """
        Fetches the list of questions, retrieves data for each, and stores it in the database.
        """
        quest_df = self.get_questions_client._get_questions_df(self.num_questions)
        question_title_list = quest_df['titleSlug'].to_list()

        for title_slug in question_title_list:
            question_data = get_leetcode_question(title_slug)

            if question_data:
                question = json.dumps(question_data, indent=2)
                print(question)
                print("=== Generating Solution ===")
                # generated_code = generate_solution_with_deepseek(question_data)
                print("=== Final Generated Solution ===\n")
                # print(generated_code)

                # Insert the problem data
                print("\n--- Inserting Data ---")
                self.db_manager.insert_problem(question_data)
                print(f"Successfully inserted problem: {title_slug}")


if __name__ == "__main__":
    # Example: Initialize the scraper and run the process
    problem_scraper = ProblemScraper(200, False)
    problem_scraper.scrape_and_store_problems()
