import os
import json
import ast
from web3 import Web3
from web3.middleware import geth_poa_middleware
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

def mint(receiverAddress, bsc_endpoint, bsc_chain_id, token_name):

    w3 = Web3(Web3.HTTPProvider(bsc_endpoint))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    logger.debug(f"Web3 connected to bsc at {bsc_endpoint}: {w3.is_connected()}")

    with open(f"./Abis/Abi_contract_{token_name}.json") as f:
        info_json = json.load(f)
    abi = info_json
    contract_adr = ast.literal_eval(os.getenv("CONTRACT_ADDRESS"))[token_name]
    print(contract_adr)
    CPContract = w3.eth.contract(address=contract_adr, abi=abi)

    #txn = CPContract.functions.mint(receiverAddress)
    txn = CPContract.functions.safeMint(receiverAddress)
    nonce = w3.eth.get_transaction_count(os.getenv("CONTRACT_OWNER_ADDRESS"))

    options = txn.build_transaction({
        "chainId": bsc_chain_id,
        # 'to': '0xc05D4536846168b93a83F289d8E14283D43cd515',
        'gas': txn.estimate_gas({"from": os.getenv("CONTRACT_OWNER_ADDRESS")}),
        'gasPrice': w3.to_wei(10, "gwei"),
        'nonce': nonce

    })

    logger.info(f"Built transaction with next options: {options}")
    signedTxn = w3.eth.account.sign_transaction(options, private_key=os.getenv("PRIVATE_KEY"))
    logger.info(f"Signed contract: {signedTxn}")
    w3.eth.send_raw_transaction(signedTxn.rawTransaction)

    txnHash = w3.to_hex(w3.keccak(signedTxn.rawTransaction))

    txnReceipt = w3.eth.wait_for_transaction_receipt(txnHash)
    logs = CPContract.events.Transfer().process_receipt(txnReceipt)
    tokenId = int(logs[0]['args']['tokenId'])

    return tokenId
    

def multiple_mint(receiverAddress, tokensAmount, bsc_endpoint, bsc_chain_id, token_name): # На один адрес
    
    w3 = Web3(Web3.HTTPProvider(bsc_endpoint))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    logger.debug(f"Web3 connected to bsc at {bsc_endpoint}: {w3.is_connected()}")

    with open(f"./Abis/Abi_contract_{token_name}.json") as f:
        info_json = json.load(f)
    abi = info_json
    contract_adr = ast.literal_eval(os.getenv("CONTRACT_ADDRESS"))[token_name]
    print(contract_adr)
    CPContract = w3.eth.contract(address=contract_adr, abi=abi)
    tokenIdlist = []

    for i in range(tokensAmount):

        #txn = CPContract.functions.mint(receiverAddress)
        txn = CPContract.functions.safeMint(receiverAddress)
        nonce = w3.eth.get_transaction_count(os.getenv("CONTRACT_OWNER_ADDRESS"))

        options = txn.build_transaction({
            "chainId": bsc_chain_id,
            # 'to': '0xc05D4536846168b93a83F289d8E14283D43cd515',
            'gas': txn.estimate_gas({"from": os.getenv("CONTRACT_OWNER_ADDRESS")}),
            'gasPrice': w3.to_wei(10, "gwei"),
            'nonce': nonce

        })

        logger.info(f"Built transaction with next options: {options}")
        signedTxn = w3.eth.account.sign_transaction(options, private_key=os.getenv("PRIVATE_KEY"))
        logger.info(f"Signed contract: {signedTxn}")
        w3.eth.send_raw_transaction(signedTxn.rawTransaction)

        txnHash = w3.to_hex(w3.keccak(signedTxn.rawTransaction))

        txnReceipt = w3.eth.wait_for_transaction_receipt(txnHash)
        logs = CPContract.events.Transfer().process_receipt(txnReceipt)
        tokenId = int(logs[0]['args']['tokenId'])
        
        tokenIdlist.append(tokenId)


    return tokenIdlist



