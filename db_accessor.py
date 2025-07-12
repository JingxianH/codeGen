from tinydb import TinyDB, Query
import os

class LeetCodeDB:
    """
    A class to manage a TinyDB database for LeetCode problems.
    It handles inserting, retrieving, updating, and deleting problem data.
    """

    def __init__(self, db_path='leetcode_problems.json'):
        """
        Initializes the database connection.

        Args:
            db_path (str): The path to the database file.
                           Defaults to 'leetcode_problems.json'.
        """
        self.db = TinyDB(db_path)
        self.Problem = Query()
        print(f"Database initialized at '{os.path.abspath(db_path)}'")

    def insert_problem(self, problem_data):
        """
        Inserts a new problem into the database.

        Checks for duplicates based on 'question_id' before insertion.

        Args:
            problem_data (dict): A dictionary containing the problem details.
                                 Must include a 'question_id'.

        Returns:
            int: The document ID of the inserted problem, or None if it already exists.
        """
        if 'question_id' not in problem_data:
            print("Error: 'question_id' is a required field.")
            return None

        # Check if a problem with this ID already exists
        if self.db.search(self.Problem.question_id == problem_data['question_id']):
            print(f"Error: Problem with ID {problem_data['question_id']} already exists.")
            return None

        # Insert the new problem data
        doc_id = self.db.insert(problem_data)
        print(f"Successfully inserted problem '{problem_data.get('title', 'N/A')}' with doc_id {doc_id}.")
        return doc_id

    def get_problem_by_id(self, question_id):
        """
        Retrieves a problem from the database by its question_id.

        Args:
            question_id (int): The unique ID of the question.

        Returns:
            dict: The problem data if found, otherwise None.
        """
        result = self.db.get(self.Problem.question_id == question_id)
        if result:
            print(f"Found problem with ID {question_id}.")
        else:
            print(f"No problem found with ID {question_id}.")
        return result

    def get_problem_by_title_slug(self, title_slug):
        """
        Retrieves a problem from the database by its title (case-insensitive).

        Args:
            title (str): The title of the question.

        Returns:
            dict: The problem data if found, otherwise None.
        """
        # Using a test function for case-insensitive search
        result = self.db.get(self.Problem.title_slug.test(lambda val: val.lower() == title_slug.lower()))
        if result:
            print(f"Found problem with title '{title_slug}'.")
        else:
            print(f"No problem found with title '{title_slug}'.")
        return result

    def get_problem_by_title(self, title):
        """
        Retrieves a problem from the database by its title (case-insensitive).

        Args:
            title (str): The title of the question.

        Returns:
            dict: The problem data if found, otherwise None.
        """
        # Using a test function for case-insensitive search
        result = self.db.get(self.Problem.title.test(lambda val: val.lower() == title.lower()))
        if result:
            print(f"Found problem with title '{title}'.")
        else:
            print(f"No problem found with title '{title}'.")
        return result

    def delete_problem_by_id(self, question_id):
        """
        Deletes a problem from the database by its question_id.

        Args:
            question_id (int): The unique ID of the question to delete.

        Returns:
            list: A list of document IDs that were removed. Returns an empty
                  list if no document was found to delete.
        """
        removed_docs = self.db.remove(self.Problem.question_id == question_id)
        if removed_docs:
            print(f"Successfully deleted problem with ID {question_id}.")
        else:
            print(f"Could not find problem with ID {question_id} to delete.")
        return removed_docs

    def get_all_problems(self):
        """
        Retrieves all problems from the database.

        Returns:
            list: A list of all problem dictionaries.
        """
        return self.db.all()

    def close_db(self):
        """
        Closes the database connection.
        """
        self.db.close()
        print("Database connection closed.")


# --- Example Usage ---

if __name__ == '__main__':
    # The dictionary containing the LeetCode problem data
    problem_to_add = {
        "title_slug": "two-sum",
        "title": "Two Sum",
        "question_id": 1,
        "difficulty": "Easy",
        "content_html": "<p>Given an array of integers...</p>",
        "code": "class Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:\n        "
    }

    # 1. Initialize the database class
    print("--- Initializing Database ---")
    db_manager = LeetCodeDB()

    # 2. Insert the problem data
    print("\n--- Inserting Data ---")
    db_manager.insert_problem(problem_to_add)

    # Try inserting the same problem again to see the duplicate check
    db_manager.insert_problem(problem_to_add)

    # 3. Get data from the database
    print("\n--- Retrieving Data ---")
    # By ID
    retrieved_problem = db_manager.get_problem_by_id(1)
    # print("Retrieved by ID:", retrieved_problem)

    # By Title
    retrieved_problem_by_title = db_manager.get_problem_by_title_slug("two-sum")
    print(retrieved_problem_by_title)
    # print("Retrieved by Title:", retrieved_problem_by_title)

    # 4. Delete data from the database
    print("\n--- Deleting Data ---")
    db_manager.delete_problem_by_id(1)

    # Verify deletion
    retrieved_problem_after_delete = db_manager.get_problem_by_id(1)


    # 5. Close the database connection
    db_manager.close_db()
