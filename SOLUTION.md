# Solution
To mine a block and get the maximum amout of sats i have to build to build the block header that consist in;
- Version (at the moment, not specified, so i'll use 00000001)
- Merkle root see [Making Merkle Root](#Making_The_Merkle_Root)
- Timestamp 
- previous block (that is all zeroes)
- Difficulty target that is 0000ffff00000000000000000000000000000000000000000000000000000000, meaning 4 zeroes.
- and the nonce, see [Finding the nonce](#Finding_The_Nonce)

## Making The Merkle Root

The Merkle Root is basically a tree structure that hashes the tx ids until you got only one for validating the transactions composition... in this way, changing one tx id will change all the Merkle Root.

![Merkle Root](image.png)

after that, I should have a list of valid transactions and before building the Merkle Root itself I have to find the highest fee transaction composition that can fit in 4mb block data.

after think for a while, i came with the right solution to this problem, the knapsack problem.

>Given a set of items, each with a weight and a value, determine which items to include in the collection so that the total weight is less than or equal to a given limit and the total value is as large as possible.
[Knapsack problem at Wikipedia](https://en.wikipedia.org/wiki/Knapsack_problem)

### Implementing the Knapsack Algorithm

For this algorithm, i have to extract some information of the transactions.

From these transactions i have to extract their size in megabytes, their total fee of transactions and their tx id.

And then, implement the 0-1 Knapsack algorithm to search for the best combination of the transaction list objects.

There is a plenty of solutions to knapsack... but the one i will use is

```
valid_transactions = list...

sort_valid_transactions_by_fee_ratio(valid_transactions)

for each transaction in valid_transactions
    if has remaining size
        include
    else
        not include

```

to sort by fee ratio, i need the weight of the transactions...
i can get by this formula
`get_size_in_mbs(transaction_data) * 4 + get_size_in_mbs(witness_Data)`



### Finally Building the Merkle Root

After this, we have the exactly transactions that we will include in our block and now we can make the Merkle Root by hashing 1 or 2 txids and hashing the results together until we have a unique hash at the end.

since we have witness data, i have to do the same process, but including all transaction data in the tx_id(now being wtxid).

## Finding The Nonce

At the [beginning of the document](#solution) i mentioned some data that consist in the block header:
- Version (at the moment, not specified, so i'll use 00000001)
- Merkle root see [Making Merkle Root](#Making_The_Merkle_Root)
- Timestamp I will use 1710997192 or some function to get the timestamp at the minig process
- Difficulty target that is 0000ffff00000000000000000000000000000000000000000000000000000000, meaning 4 zeroes.

and the nonce that i will explain the process of obtaining now.

To mine a block i need to discover the block hash that the difficulty wants, in the case is `000ffff00000000000000000000000000000000000000000000000000000000`
which means that my block needs 4(four) 0(zeroes) at the beginning, e.g. `0000(the rest of the hash)`.

Between the data that is hashed and the hash itself there is some random number called nonce
> A nonce is an arbitrary number used only once in a cryptographic communication, in the spirit of a nonce word. 
At: https://en.wikipedia.org/wiki/Cryptographic_nonce

In the Bitcoin context is a 4-byte(or 32-bit) integer value(e.g. any number between `0` and `4,294,967,296` but in the code will be represented with the hexadecimal notation, that is `0x00000000` and `0xffffffff`)that we will include and generate until the hash function output make the hash that we want(any hash that has 0000 at the beginning).

The "mining" process consist in finding the right nonce that will get us the hash that we need to find.

There is a chance that the 32-bit nonce will not have enough entropy to find the hash, but if this occurs, the timestamp will change and reset the nonce.

To find that, we have a certain number of hashes that we can get with 32-bit nounce that is `4,294,967,296` hashes, wen the nounce came to its maximum, the algorithm will change the timestamp so we can try the nounce all again, keeping this process until we have the hash.

When the algorithm finds the hash it will log all the output into some `output.txt` file. This will help anyone to test the program.

## Code design
in this code challenge, ill try some data-driven oriented programming and try to organize the code by modules.

transaction code at `tx/`

blockbuilding code at `blockcuilder.py`

and all mining stuff at `main.py`

# Results
With this simulation of block mining I got

the maximum fee expected defined by SoB which is `20616923` respecting the block weight

with at maximum `1 minute` of mining depending of luck

## personal conclusion

I`m sure that was not easy, i spent a bit more than 2 weeks working on this project, but Im also sure that was fun enough to try SoB next year!

Was my first time dealing with a bunch of things, such as byte manipulation, transaction serialization and other things that mostly the bitcoin libs already has implemented.
Learning about all that was helpful to understand all the security that bitcoin has.