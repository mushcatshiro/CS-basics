"""

"""
import json
import os
import random

exclude_files = [
    "amzn.md",
    "myassistant.md",
    "role.md"
]

def read_file(file_name):
    with open(file_name, 'r') as file:
        data = file.read()
    
    data_list = data.split('\n\n')
    data_list = [data for data in data_list if (not data.startswith("#") and not data.startswith("```") and not data.startswith("!["))]
    data_list = [data for data in data_list if data != '']
    data = " ".join([" ".join(data.split('\n')).replace("  ", " ") for data in data_list])

    return data

def n_gram(data, n):
    """
    should have a way to link to the section
    """
    n_gram_list = []
    data_list = data.split(' ')
    for i in range(len(data_list)-n+1):
        n_gram_list.append(data_list[i:i+n])
    return n_gram_list

def summary(n_gram_list, file_count):
    print(f"Number of n-gram: {len(n_gram_list)}")
    print(f"Number of files: {file_count}")

def sample_questions(n_gram_list, question_count):
    if question_count == 0:
        question_count = len(n_gram_list) // 10
    questions = []
    for i in range(question_count):
        n_gram = random.choice(n_gram_list)
        questions.append(" ".join(n_gram))
    # print(json.dumps(questions, indent=2))
    # randomize the questions
    random.shuffle(questions)
    for i, question in enumerate(questions):
        print(f"Question {i+1}: {question}")
        input("Press Enter for next question")


def main(path, n_gram_len, question_count):
    if os.path.isfile(path):
        data = read_file(path)
        file_count = 1
    elif os.path.isdir(path):
        data = ''
        file_count = 0
        global exclude_files
        for file_name in os.listdir(path):
            if file_name.endswith('.md') and not file_name in exclude_files:
                fpath = os.path.join(path, file_name)
                print(fpath)
                data += read_file(fpath)
                file_count += 1
    n_gram_list = n_gram(data, n_gram_len)
    summary(n_gram_list, file_count)
    sample_questions(n_gram_list, question_count)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--path', help='path')
    parser.add_argument('--n', help='n-gram', default=15, type=int)
    parser.add_argument('--question_count', help='number of questions', default=0, type=int)
    args = parser.parse_args()
    main(args.path, args.n, args.question_count)