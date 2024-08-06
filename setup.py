from setuptools import find_packages,setup

def get_packages(file_path):
    """
    The function `get_packages` reads a file containing package requirements and returns a list of
    stripped package names.
    
    :param file_path: The `get_packages` function reads a file located at the specified `file_path` and
    returns a list of package requirements listed in the file. The function reads each line from the
    file, strips any leading or trailing whitespaces, and then returns a list of the cleaned
    requirements
    :return: The function `get_packages` reads a file located at the specified `file_path`, extracts the
    lines of text from the file, removes any leading or trailing whitespace from each line, and returns
    a list of the cleaned requirements.
    : if: file is not present if can retrun the empty list.
    """
    try:
        with open(file_path,"r") as f:
           requirements=f.readlines()

           requirements=[req.strip() for req in requirements]
        return requirements
    except:
        return []



setup(
    author="Samiullah",
    author_email="sami606713@gmail.com",
    name="Data_Science_Tool",
    description="In this project our goal is to build a tool for data scince learner that can larn by simple click to gain a hand on experience.",
    long_description="This project aims to build a tool that helps data science learners by providing a simple interface to practice and gain hands-on experience. It is designed to be user-friendly and educational.",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=get_packages('requirements.txt'),
    python_requires='>=3.11'
)