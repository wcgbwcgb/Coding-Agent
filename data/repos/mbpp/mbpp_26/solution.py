def check_k_elements(test_list, K):
    return all(item == K for tup in test_list for item in tup)
