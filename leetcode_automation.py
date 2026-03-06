import os
import datetime
import random

# --- Configuration ---
REPO_PATH = os.environ.get("GITHUB_WORKSPACE", ".") # Default to current directory if not in GitHub Actions
PROBLEMS_FILE = os.path.join(REPO_PATH, "problems.txt") # File to store problems already solved

# A curated list of beginner-friendly LeetCode problems (NeetCode 150 - Arrays & Hashing, Two Pointers)
# Format: (Problem Name, LeetCode URL, Topic)
BEGINNER_PROBLEMS = [
    ("Contains Duplicate", "https://leetcode.com/problems/contains-duplicate/", "Arrays & Hashing"),
    ("Valid Anagram", "https://leetcode.com/problems/valid-anagram/", "Arrays & Hashing"),
    ("Two Sum", "https://leetcode.com/problems/two-sum/", "Arrays & Hashing"),
    ("Group Anagrams", "https://leetcode.com/problems/group-anagrams/", "Arrays & Hashing"),
    ("Valid Palindrome", "https://leetcode.com/problems/valid-palindrome/", "Two Pointers"),
    ("Two Sum II - Input Array Is Sorted", "https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/", "Two Pointers"),
    ("3Sum", "https://leetcode.com/problems/3sum/", "Two Pointers"),
]

def get_solved_problems():
    """Reads the list of already solved problems from a file."""
    if not os.path.exists(PROBLEMS_FILE):
        return set()
    with open(PROBLEMS_FILE, "r") as f:
        return {line.strip() for line in f}

def add_solved_problem(problem_name):
    """Adds a solved problem to the file."""
    with open(PROBLEMS_FILE, "a") as f:
        f.write(f"{problem_name}\n")

def select_problem(solved_problems):
    """Selects a random problem from the beginner list that hasn\'t been solved yet."""
    available_problems = [p for p in BEGINNER_PROBLEMS if p[0] not in solved_problems]
    if not available_problems:
        print("All beginner problems solved! Consider adding more problems or moving to the next topic.")
        return None
    return random.choice(available_problems)

def generate_python_solution(problem_name, problem_url, topic):
    """Generates a basic Python solution file content."""
    class_name = "Solution"
    method_name = "solve"
    # Basic template for a LeetCode problem solution
    return f"""""""""
# LeetCode Problem: {problem_name}
# Link: {problem_url}
# Topic: {topic}

class {class_name}:
    def {method_name}(self, *args) -> any:
        """""""""
        # Write your solution here
        # Example:
        # return sum(args)
        pass

# Example Usage (for local testing)
# sol = {class_name}()
# print(sol.{method_name}(...))
"""""""""

def generate_markdown_description(problem_name, problem_url, topic):
    """Generates a Markdown file content for the problem description."""
    return f"""""""""
# {problem_name}

**Link:** [{problem_name}]({problem_url})

**Topic:** {topic}

## Problem Description (Summary)

[You can paste the problem description here from LeetCode, or just rely on the link.]

## Solution Approach

[Describe your thought process and approach to solving the problem here.]

## Time and Space Complexity

-   **Time Complexity:** O(N) or O(N log N) etc.
-   **Space Complexity:** O(1) or O(N) etc.
"""""""""

def main():
    solved_problems = get_solved_problems()
    problem = select_problem(solved_problems)

    if problem is None:
        print("No new problems to solve today.")
        return

    problem_name, problem_url, topic = problem
    sanitized_problem_name = problem_name.replace(" ", "_").replace("-", "_").replace("(", "").replace(")", "").replace(",", "")
    today_date = datetime.date.today().strftime("%Y-%m-%d")

    # Create directory structure: Leetcode/Topic/YYYY-MM-DD_ProblemName/
    problem_dir = os.path.join(REPO_PATH, topic.replace(" ", "_"), f"{today_date}_{sanitized_problem_name}")
    os.makedirs(problem_dir, exist_ok=True)

    # Generate Python solution file
    python_file_path = os.path.join(problem_dir, f"{sanitized_problem_name}.py")
    with open(python_file_path, "w") as f:
        f.write(generate_python_solution(problem_name, problem_url, topic))
    print(f"Generated solution file: {python_file_path}")

    # Generate Markdown description file
    markdown_file_path = os.path.join(problem_dir, "README.md")
    with open(markdown_file_path, "w") as f:
        f.write(generate_markdown_description(problem_name, problem_url, topic))
    print(f"Generated README file: {markdown_file_path}")

    # Add problem to solved list
    add_solved_problem(problem_name)

    # Git operations (will be handled by GitHub Actions, but for local testing)
    # os.system(f"cd {REPO_PATH} && git add . && git commit -m \"Daily LeetCode: {problem_name}\" && git push")
    print(f"Problem \'{problem_name}\' processed. Files created in {problem_dir}")
    print("Git operations will be handled by the GitHub Action.")

if __name__ == "__main__":
    main()
      
