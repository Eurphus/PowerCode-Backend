import ast
import os

bad_code = """
for i in range(0, 4):
    print + l)
"""

good_code = """
def solution(inp):
    sum = 0
    for num in inp:
        if num % 2 == 0:
            sum += num
    return sum
"""

language = "Python"


def ingest_input(key):
    """
    Normalizes inputs to match python program output
    :param key:
    :return:
    """
    if key.isnumeric() or (key[0] == "-" and key[1:].isnumeric()):
        return int(key)
    if " " in key:
        lst = key.split(" ")
        if lst[0].isnumeric() or (lst[0][0] == "-" and lst[0][1:].isnumeric()):
            return [int(num) for num in lst]
        else:
            return lst
    else:
        return key


def get_test_cases(challenge: str) -> list:
    """
    Returns a list of all test cases contained in a challenge. Stored in list with tuples (input, expected)
    :param challenge:
    :return:
    """

    cases = []
    submission_path = os.getcwd().replace('\\', '/') + "/submissions/" + challenge
    for file_name in os.listdir(submission_path + "/input/"):
        input_file = open(submission_path + "/input/" + file_name, "r")
        input_digest = ingest_input(input_file.read())

        output_file = open(submission_path + "/output/output" + file_name[-6:], "r")
        output_digest = ingest_input(output_file.read())

        cases.append((input_digest, output_digest))
        output_file.close()
        input_file.close()
    return cases

def run_test_cases(code: str, challenge: str):
    print(f"\n\nStarting {challenge}!")
    #
    # Syntax Check
    #
    try:
        ast.parse(code)
        response = (True, 0)
        print("Syntax Check Passed")
    except SyntaxError as error:
        response = (False, error)
        print("Syntax Check Failed")

    #
    # Defining submission in local scope
    #
    if response[0]:
        try:
            if language == "Python":
                scope = {}
                exec(code, {}, scope)
                print("Function Exec Passed")
        except SyntaxError as error:
            print(f"): Error:\n{error}")
            print("Function Exec Failed")
    else:
        print(f"""There is a syntax error. Please try again. \nError Below \n{str(response[1])}:""")
        return 1

    #
    # Running the test cases
    #

    cases = get_test_cases(challenge)
    data_collection = []

    for inp, sol in cases:
        success = 0 # 0 Indicates a pass, 1 indicates a wrong value, 2 or other is an error
        error = ""
        try:
            print(inp)
            returned = scope["solution"](inp)

            if returned != sol:
                success = 1
        except Exception as e:
            success = 2
            error = str(e)

        data_collection.append((success, inp, sol, error))

    print(data_collection)

run_test_cases(good_code, "sum-even")
