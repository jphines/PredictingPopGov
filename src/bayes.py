import csv
import string
import numpy as np
import math
import random
import time
import sys


states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NH', 'NV', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'WA', 'WV', 'WI', 'WY', 'total']

files = ['low','medium','high','popular','insane']
path = '../tsv/'

def load_document(section, state):
    reader = csv.reader(open(path + state + '/'+ section + ".tsv", 'rb'), delimiter='\t')
    documents = []
    exclude = set(string.punctuation)
    count = 0
    for url, location, clicks, content in reader:
        text = content
        text = ''.join(char for char in text if char not in exclude)
        text = set(text.lower().split())
        count += 1
        documents.append(text)
    return documents


def make_dictionary(list_of_lists_of_sets):
    set_dict = set([])
    for a_list in list_of_lists_of_sets:
        for a_set in a_list:
            set_dict.update(a_set)
    value = 0
    dict_dict = {}
    for elem in sorted(list(set_dict)):
        dict_dict[elem] = value
        value += 1
    return [set_dict, dict_dict]


def make_sparse_matrix(sec_docs, dictionary):
    if type(sec_docs[0]) is not set:
        sec_docs = [set(doc) for doc in sec_docs]
    X = np.zeros((len(sec_docs), len(dictionary[0])))
    sec_set_count = 0
    for sec_set in sec_docs:
        inter = sec_set & dictionary[0]
        for elem in inter:
            word_count = dictionary[1][elem]
            X[sec_set_count][word_count] = 1
        sec_set_count += 1
    return X


def train(list_of_sparse_matrices, dict_len, alpha, beta, nc):
    n = np.zeros((len(list_of_sparse_matrices), dict_len))
    theta = np.zeros((len(list_of_sparse_matrices), dict_len))
    count = 0
    for matrix in list_of_sparse_matrices:
        n[count] = np.sum(matrix, axis=0)
        count += 1
    row_cnt = 0
    for row in n:
        column_cnt = 0
        for column in row:
            njc = column
            theta[row_cnt][column_cnt] = (njc + alpha - 1) / (1000 + alpha + beta - 2)
            column_cnt += 1
        row_cnt += 1
    weights = np.zeros((len(list_of_sparse_matrices), dict_len + 1))
    row_cnt = 0
    for row in theta:
        col_cnt = 0
        w0c = 0
        for col in row:
            theta_jc = col
            theta_j0 = theta[0][col_cnt]
            weights[row_cnt][col_cnt] = math.log(theta_jc * (1 - theta_j0) / (theta_j0 * (1 - theta_jc)))
            w0c += math.log((1 - theta_jc) / (1 - theta_j0))
            col_cnt += 1
        weights[row_cnt][-1] = w0c + math.log(.2 / 1000.0)
        row_cnt += 1
    return weights


# sections = list_of_lists_of_sets
def set_training(sections):
    training_list = []
    testing_list = []
    for section in sections:
        random.shuffle(section)
        training_list.append(section[:len(section) / 2])
        testing_list.append(section[len(section) / 2:])
    return [training_list, testing_list]


def predict(weights, test_list, dictionary):
    sect_cnt = 0
    confusion = np.zeros((5, 5))
    max_index = 0
    queue = [[1000, "word"]] * 10
    for section in test_list:
        for document in section:
            probabilities = []
            for row in weights:
                prob_sum = 0
                for word in document:
                    w_0z = row[-1]
                    prob_sum += row[dictionary[1][word]]
                probabilities.append(prob_sum + w_0z)
            max_index = np.argmax(np.array(probabilities))
            temp = np.array(probabilities).argsort()[-2:][::-1]
            diff = math.fabs(probabilities[temp[0]] - probabilities[temp[1]])
            if queue[-1][0] > diff:
                queue.pop()
                queue.append([diff, document])
                queue.sort(key=lambda x: x[0])
            confusion[sect_cnt][max_index] += 1
        sect_cnt += 1
    print queue
    return confusion


def worker(state):
    loaded_sections = []
    for file in files:
        loaded_sections.append(load_document(file, state))
    dictionary = make_dictionary(loaded_sections)
    sets = set_training(loaded_sections)
    sparses = []
    for section in sets[0]:
        sparses.append(make_sparse_matrix(section, dictionary))
    weights = train(sparses, len(dictionary[0]), 3, 1, 1000)
    words(weights, dictionary)
    print predict(weights, sets[1], dictionary)


def words(weights, dictionary):
    row_cnt = 0
    mins = weights.argmin(axis=0)
    ranges = np.zeros(weights.shape)
    for row in weights:
        col_cnt = 0
        for col in row:
            ranges[row_cnt][col_cnt] = col - weights[mins[row_cnt]][col_cnt]
            col_cnt += 1
        row_cnt += 1
    for row in ranges:
        temp_arr = row.argsort()[-10:][::-1]
        max_ranges = set(temp_arr.flat)
        words = [k for k, v in dictionary[1].iteritems() if v in max_ranges]
        print words

def main():
    for state in states:
        out = open(path+state+'/output.log', 'w')
        sys.stdout = out
        worker(state)

if __name__ == "__main__":
    start = time.time()
    main()
    elapsed = time.time() - start
    print elapsed
