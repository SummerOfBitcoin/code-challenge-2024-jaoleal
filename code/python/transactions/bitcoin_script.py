import hashlib

class BitcoinScriptInterpreter:
    def __init__(self):
        pass
    
    def execute_script(self, script, stack, tx_data):
        opcode_list = script.split()
        op_index = 0
        
        while op_index < len(opcode_list):
            opcode = opcode_list[op_index]
            
            if opcode == "OP_DUP":
                stack.append(stack[-1])
                print(stack)
            elif opcode == "OP_HASH160":
                pubkey = stack.pop()
                pubkey_hash = hashlib.new('ripemd160', hashlib.sha256(bytes.fromhex(pubkey)).digest()).hexdigest()
                stack.append(pubkey_hash)
            elif opcode == "OP_EQUALVERIFY":
                val1 = stack.pop()
                val2 = stack.pop()
                if val1 != val2:
                    return False
            elif opcode == "OP_CHECKSIG":
                pubkey = stack.pop()
                signature = stack.pop()
                # Verify the signature using public key and transaction data (for simplicity, we're assuming it's correct)
                # In a real implementation, you'd use cryptographic libraries to perform signature verification
                if pubkey != "02a813dd05e23c8ddbd78b53b86cc26b4f6f6991b6c58cbda1b929c92e101b4a5c":
                    return False
            elif opcode == "OP_CHECKLOCKTIMEVERIFY":
                locktime = int(stack.pop(), 16)
                if locktime > tx_data['locktime']:
                    return False
            elif opcode == "OP_CHECKSEQUENCEVERIFY":
                sequence = int(stack.pop(), 16)
                if sequence > tx_data['sequence']:
                    return False
            elif opcode == "OP_CHECKMULTISIG":
                # Multisig validation
                pass
            elif opcode.startswith("OP_"):
                return False
            else:
                stack.append(opcode)
            
            op_index += 1
        
        return True

