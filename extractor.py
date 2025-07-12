import pandas as pd
from leetscrape import GetQuestion, ExtractSolutions, GenerateCodeStub
import json


def get_leetcode_question(title_slug: str):
    """
    Fetches a LeetCode question, its visible test cases, code stubs, and solution
    using a title slug.

    Args:
        title_slug: The part of the URL that identifies the question
                    (e.g., "two-sum" for the problem at
                    https://leetcode.com/problems/two-sum/).

    Returns:
        A dictionary containing the question details, code stub, test cases, and solution,
        or None if an error occurs.
    """
    try:
        # Initialize and scrape question
        question = GetQuestion(titleSlug=title_slug)
        question_data = question.scrape()

        # Initialize solution extractor and get solutions

        # Construct result
        question_info = {
            "title_slug": title_slug,
            "title": question_data.title,
            "question_id": question_data.QID,
            "difficulty": question_data.difficulty,
            "content_html": question_data.Body,
            "code": question_data.Code,

        }
        solution = GenerateCodeStub(title_slug, question_info['question_id'])
        code_stub = solution._get_code_stub()
        problem_statement = solution._get_problem_statement()
        problem_statement_code_blocks = solution._extract_codeblocks_in_problem_statement(
            problem_statement
        )
        input_string, output_string = solution._get_parameters(problem_statement_code_blocks)
        question_info = {
            "title_slug": title_slug,
            "title": question_data.title,
            "question_id": question_data.QID,
            "difficulty": question_data.difficulty,
            "content_html": question_data.Body,
            "code": question_data.Code,
            "test_cases": input_string,
            "parameter_map": output_string

        }
        # print(solution._extract_codeblocks_in_problem_statement(code_stub))


        #solution_data = solution.generate()
        # print(solution_data)
        return question_info

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    # Example: Get the "Two Sum" problem
    two_sum_slug = "two-sum"
    question_data = get_leetcode_question(two_sum_slug)

    if question_data:
        q = json.dumps(question_data, indent=2)
