def tx_knapsack(txs_dict, remaining_size):
    #the input is a dict with the txid as key
    # and a list with the fee and size as value
    #{txid: [fee, size in bytes]}
    #
    #the total size of a block is 1mb = 1000000 bytes
    # A matrix of number of items x remaining size

    dp = [[0] * (remaining_size + 1) for _ in range(len(txs_dict) + 1)]
    selected_index = []
    for i in range(1, len(txs_dict) + 1):
        value, weight = txs_dict[i - 1]
        for w in range(1, remaining_size + 1):
            if weight > w:
                dp[i][w] = dp[i - 1][w]
            else:
                selected_index.append(i-1)
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weight] + value)
    selected_index = set(selected_index)
    
 
    # the return should be a new dict containing the selected txs with max possible fee
    return dp[len(txs_dict)][remaining_size], selected_index