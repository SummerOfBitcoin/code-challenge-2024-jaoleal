# Solution
To mine a block and get the maximum amout of sats i have to build to build the block header that consist in;
- Version (at the moment, not specified, so i'll use 00000001)
- Merkle root see [Making Merkle Root](#Making_The_Merkle_Root)
- Timestamp I will use 1710997192 or some function to get the timestamp at the minig process
- Difficulty target that is 0000ffff00000000000000000000000000000000000000000000000000000000, meaning 4 zeroes.
- and the nonce, see [Finding the nonce](#Finding_The_Nonce)


## Making The Merkle Root

The Merkle Root is basically a tree structure that hashes the tx ids until you got only one for validating the transactions composition... in this way, changing one tx id will change all the Merkle Root.

![Merkle Root](image.png)

but the Merkle root can only have valid tx ids and you have to verify the weight of the block when adding transactions, the weight being 4 mbs.

To achieve this in a performant way i have to sift through transactions in a logical order to avoid unnecessary work. Being:

1.  Verifying the transaction Syntax
2.  Input Signature
3.  Locking Script Validation
4.  UTXO Validation + spent value check + locktime (in case of conflict)

after that, I should have a list of valid transactions and before building the Merkle Root itself I have to find the highest fee transaction composition that can fit in 4mb block data.

after think for a while, i came with the right solution to this problem, the knapsack problem.

>Given a set of items, each with a weight and a value, determine which items to include in the collection so that the total weight is less than or equal to a given limit and the total value is as large as possible.
[Knapsack problem at Wikipedia](https://en.wikipedia.org/wiki/Knapsack_problem)

### Implementing the Knapsack Algorithm

For this algorithm, i have to extract some information of the transactions.

After this point consider every transaction mentioned a valid one. From these transactions i have to extract their size in megabytes, their total fee of transactions and their tx id.

But in this way, I could still got some errors because I may spend a transaction that I did not include previously in the block and to avoid that I need to previously make a list of connected transactions and consider it as an object to be included in the block, this object will expose the total size in megabytes and the fee of all transactions included in the list 



## Finding The Nonce


## Development Process
Since i have the transactions, I will focus in finding the best Merkle Root building an efficient Merkle Root algorithm

### Eficiency and optimization 
First i will prototype in python and later re-write everything in rust... i think that this is the best way to write good code, without bugs and test covered.