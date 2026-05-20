def check_k_elements(test_list, K):
    return all(all(elem == K for elem in tup) for tup in test_list)
