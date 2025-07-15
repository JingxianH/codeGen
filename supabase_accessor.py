import os
from supabase import create_client, Client


class SupabaseDB:
    """
    A class to manage a Supabase database for LeetCode problems.
    It handles inserting, retrieving, and deleting problem data.
    """

    def __init__(self, supabase_url=None, supabase_key=None):
        """
        Initializes the Supabase client.

        It's recommended to store your URL and key as environment variables.

        Args:
            supabase_url (str): Your Supabase project URL.
            supabase_key (str): Your Supabase anon public key.
        """
        # It's best practice to use environment variables for credentials
        url = supabase_url or ""
        key = supabase_key or ""
        if not url or not key:
            raise ValueError("Supabase URL and Key must be provided either as arguments or environment variables.")

        # Initialize the client
        self.supabase: Client = create_client(url, key)
        print("Successfully connected to Supabase.")

    def insert_problem(self, problem_data):
        """
        Inserts a new problem into the 'problems' table in Supabase.

        Args:
            problem_data (dict): A dictionary containing the problem details.
                                 Must match the columns in your Supabase table.

        Returns:
            dict: The inserted data as returned by Supabase, or None on error.
        """
        try:
            # 'problems' is the name of the table we created
            # The insert method takes a dictionary or a list of dictionaries
            response = self.supabase.table('problems').insert(problem_data).execute()

            # The actual data is in the 'data' attribute of the response
            inserted_data = response.data
            if inserted_data:
                print(f"Successfully inserted problem '{problem_data.get('title', 'N/A')}'.")
                return inserted_data
            else:
                # Handle potential errors from Supabase (e.g., unique constraint violation)
                print(f"Failed to insert problem. Response: {response}")
                return None

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_problem_by_id(self, question_id):
        """
        Retrieves a problem from Supabase by its question_id.

        Args:
            question_id (int): The unique ID of the question.

        Returns:
            dict: The problem data if found, otherwise None.
        """
        try:
            response = self.supabase.table('problems').select('*').eq('question_id', question_id).execute()
            if response.data:
                print(f"Found problem with ID {question_id}.")
                return response.data[0]
            else:
                print(f"No problem found with ID {question_id}.")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def delete_problem_by_id(self, question_id):
        """
        Deletes a problem from Supabase by its question_id.

        Args:
            question_id (int): The unique ID of the question to delete.

        Returns:
            dict: The data of the deleted row, or None if not found or on error.
        """
        try:
            # The delete() method needs a filter like eq() to know what to delete
            response = self.supabase.table('problems').delete().eq('question_id', question_id).execute()
            if response.data:
                print(f"Successfully deleted problem with ID {question_id}.")
                return response.data
            else:
                print(f"Could not find problem with ID {question_id} to delete.")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


# --- Example Usage ---

if __name__ == '__main__':
    # Before running, make sure you have the supabase-py library installed:
    # pip install supabase

    # IMPORTANT:
    # Replace these with your actual Supabase URL and anon key,
    # or set them as environment variables named SUPABASE_URL and SUPABASE_KEY.
    SUPABASE_URL = "url"
    SUPABASE_KEY = "key"
    if SUPABASE_URL == "YOUR_SUPABASE_URL" or SUPABASE_KEY == "YOUR_SUPABASE_ANON_KEY":
        print("=" * 50)
        print(
            "⚠️  Please replace 'YOUR_SUPABASE_URL' and 'YOUR_SUPABASE_ANON_KEY' with your actual Supabase credentials before running!")
        print("=" * 50)
    else:
        # The dictionary containing the LeetCode problem data
        problem_to_add = {'title_slug': 'two-sum',
                          'title': 'Two Sum',
                          'question_id': 1,
                          'difficulty': 'Easy',
                          'content_html': '<p>Given an array of integers <code>nums</code>&nbsp;and an integer <code>target</code>, return <em>indices of the two numbers such that they add up to <code>target</code></em>.</p>\n\n<p>You may assume that each input would have <strong><em>exactly</em> one solution</strong>, and you may not use the <em>same</em> element twice.</p>\n\n<p>You can return the answer in any order.</p>\n\n<p>&nbsp;</p>\n<p><strong class="example">Example 1:</strong></p>\n\n<pre>\n<strong>Input:</strong> nums = [2,7,11,15], target = 9\n<strong>Output:</strong> [0,1]\n<strong>Explanation:</strong> Because nums[0] + nums[1] == 9, we return [0, 1].\n</pre>\n\n<p><strong class="example">Example 2:</strong></p>\n\n<pre>\n<strong>Input:</strong> nums = [3,2,4], target = 6\n<strong>Output:</strong> [1,2]\n</pre>\n\n<p><strong class="example">Example 3:</strong></p>\n\n<pre>\n<strong>Input:</strong> nums = [3,3], target = 6\n<strong>Output:</strong> [0,1]\n</pre>\n\n<p>&nbsp;</p>\n<p><strong>Constraints:</strong></p>\n\n<ul>\n\t<li><code>2 &lt;= nums.length &lt;= 10<sup>4</sup></code></li>\n\t<li><code>-10<sup>9</sup> &lt;= nums[i] &lt;= 10<sup>9</sup></code></li>\n\t<li><code>-10<sup>9</sup> &lt;= target &lt;= 10<sup>9</sup></code></li>\n\t<li><strong>Only one valid answer exists.</strong></li>\n</ul>\n\n<p>&nbsp;</p>\n<strong>Follow-up:&nbsp;</strong>Can you come up with an algorithm that is less than <code>O(n<sup>2</sup>)</code><font face="monospace">&nbsp;</font>time complexity?', 'code': 'class Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:\n        ',
                          'test_cases': '([2, 7, 11, 15], 9, [0, 1]), ([3, 2, 4], 6, [1, 2]), ([3, 3], 6, [0, 1])', 'parameter_map': 'nums, target, output'}


        # 1. Initialize the database class
        print("--- Initializing Supabase Connection ---")
        db_manager = SupabaseDB(supabase_url=SUPABASE_URL, supabase_key=SUPABASE_KEY)

        # 2. Insert the problem data
        print("\n--- Inserting Data ---")
        #db_manager.insert_problem(problem_to_add)

        # # Try inserting again (this should fail because of the UNIQUE constraint on question_id)
        # print("\n--- Attempting to Insert Duplicate ---")
        # db_manager.insert_problem(problem_to_add)
        #
        # # 3. Get data from the database
        # print("\n--- Retrieving Data ---")
        # retrieved_problem = db_manager.get_problem_by_id(1)
        # if retrieved_problem:
        #     print("Retrieved Data:", retrieved_problem['title'])
        #
        # # 4. Delete data from the database
        # print("\n--- Deleting Data ---")
        #db_manager.delete_problem_by_id(1)

        # # Verify deletion
        # print("\n--- Verifying Deletion ---")
        # db_manager.get_problem_by_id(1)
