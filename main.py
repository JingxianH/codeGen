import pandas as pd
import json

from db_accessor import LeetCodeDB
from extractor import get_leetcode_question
from get_questions import GetQuestionsList
from llm_code_generation import generate_solution_with_deepseek

if __name__ == "__main__":
    # Example: Get the "Two Sum" problem
    get_questions_client = GetQuestionsList(200)

    quest_df = get_questions_client._get_questions_df(200)
    pd.set_option('display.max_columns', None)
    db_manager = LeetCodeDB()

    question_title_list = quest_df['titleSlug'].to_list()
    for title_slug in question_title_list:
        question_data = get_leetcode_question(title_slug)

        if question_data:
            question = json.dumps(question_data, indent=2)
            print(question)
            print("=== Generating Solution ===")
            #generated_code = generate_solution_with_deepseek(question_data)
            print("=== Final Generated Solution ===\n")
            #print(generated_code)

            # 2. Insert the problem data
            print("\n--- Inserting Data ---")
            db_manager.insert_problem(question_data)
