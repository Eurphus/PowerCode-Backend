# import tempfile
# import docker
# import os
#
# client = docker.from_env()
#
#
# def init_docker(language, challenge, user_id):
#     path = os.getcwd().replace('\\', '/') + f"tmp/"
#     temp_dir = tempfile.mkdtemp(dir=path)
#
#     image, ending, run_command = "", "", ""
#     if language == 'python':
#         ending = "py"
#         image = "python:latest"
#         run_command = "python3 /code/main.py"
#     elif language == 'javascript':
#         ending = "js"
#         image = "node:latest"
#         run_command = "node /code/main.js"
#     elif language == 'c':
#         ending = "c"
#         image = "gcc:latest"
#         run_command = "gcc /code/main.c -o /code/a.out && /code/a.out"
#
#     open(f"{temp_dir}/main.{ending}").close()
#     eval_file = open(f"{temp_dir}/eval.txt")
#     eval_file.write(run_command)
#     eval_file.close()
#
#     container = client.containers.run(
#         image=image,
#         detach=True,
#         stdin_open=True, tty=True,
#         volumes={"temp_dir": {"bind": "/tmp", "mode": "rw"}},
#         working_dir=temp_dir,
#     )
#
#     return (temp_dir, container, run_command)
#
#
# init_docker("Python", "even-sum")
