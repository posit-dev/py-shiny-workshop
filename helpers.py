from pathlib import Path
import glob


def print_file(file_path: str, file_name: str = None):
    if file_name is not None:
        print(f"\n## file: {file_name}")

    with open(file_path, "r") as app_file:
        app_contents = app_file.read()
        print(app_contents)


def list_files(path):
    files = glob.glob(path + "/**", recursive=True)
    files = [file for file in files if not glob.os.path.isdir(file)]
    return files


def include_shiny_folder(
    path: str,
    file_name: str = "app.py",
    exclusions: list = [],
    components: str = "editor, viewer",
):
    folder_path = Path(__name__).parent / path

    # Start with the header
    header = f"```{{shinylive-python}}\n#| standalone: true\n#| components: [{components}]\n#| layout: horizontal\n#| viewerHeight: 800"
    print(header)
    # Print contents of app.py
    print_file(folder_path / file_name, None)

    exclude_list = ["__pycache__"] + [file_name] + exclusions

    files = list_files(path)

    path_list = [
        string
        for string in files
        if not any(exclusion in string for exclusion in exclude_list)
    ]

    file_names = [string.replace(f"{str(folder_path)}/", "") for string in path_list]

    # Additional files need to start with ## file:
    for x, y in zip(path_list, file_names):
        print_file(x, y)

    # Finish with the closing tag
    print("```")


def problem_tabs(path: str):
    print("\n:::: {.column-screen}\n::: {.panel-tabset}")

    print("## Goal")
    include_shiny_folder(path, "app.py", components="viewer")

    print("## Problem")
    include_shiny_folder(path, "app.py", exclusions=["app-solution.py"])
    print("## Solution")
    include_shiny_folder(path, "app-solution.py", exclusions=["app.py"])

    print(":::\n::::")
