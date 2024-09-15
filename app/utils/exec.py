import ast
import os
import docker


def normalize_data(key):
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
    elif key == "true":
        return True
    elif key == "false":
        return False
    else:
        return key


def get_test_cases(language: str, challenge: str) -> list:
    """
    Returns a list of all test cases contained in a challenge. Stored in list with tuples (input, expected)
    :param language:
    :param challenge:
    :return:
    """
    challenge_path = os.getcwd().replace('\\', '/') + f"/app/challenges/{language}/{challenge}"

    input_file = open(challenge_path + "/input.txt", "r")
    input_list = [normalize_data(line.rstrip('\n')) for line in input_file]
    input_file.close()

    output_file = open(challenge_path + "/output.txt", "r")
    output_list = [normalize_data(line.rstrip('\n')) for line in output_file]
    output_file.close()

    cases = [(input_list[i], output_list[i]) for i in range(len(input_list))]
    return cases


def run_test_cases(code: str, language: str, challenge: str):
    print(f"\n\nStarting {challenge}!")
    #
    # Syntax Check
    #
    try:
        ast.parse(code)
        print("Syntax Check Passed")
    except SyntaxError as error:
        return {
            "success": 3,
            "error": str(error),
            "description": "Syntax Error"
        }

    #
    # Defining challenge in local scope
    #
    scope = {}
    try:
        if language == "python":
            exec(code, {}, scope)
            print("Function Exec Passed")
    except Exception as error:
        return {
            "success": 4,
            "error": str(error),
            "description": "Code failed function declaration"
        }
    except:
        return {
            "success": 99,
            # "error": "",
            "description": "unknown error"
        }

    #
    # Running the test cases
    #

    cases = get_test_cases(language, challenge)
    data_collection = []
    total_success = 0
    total_runs = 0

    for inp, sol in cases:
        success = 0  # 0 Indicates a pass, 1 indicates a wrong value, 2 or other is an error
        error = ""
        try:
            print(inp)
            returned = scope["solution"](inp)

            if returned != sol:
                success = 1
            else:
                total_success += 1
        except Exception as e:
            success = 2
            error = str(e)
            returned = "ERROR"
        total_runs += 1
        data_collection.append({
            "success": success,
            "input": inp,
            "solution": sol,
            "returned": returned,
            "error": error})

    success = 0 if total_runs == total_success else 1
    print(success)
    print(total_success)
    print(total_runs)

    return {
        "success": success,
        "successful_runs": total_success,
        "total": total_runs,
        "data": data_collection
    }
