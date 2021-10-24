from web3 import Web3
import json
from CONFIGS import *

web3 = Web3(Web3.HTTPProvider(INFURA_URL))

# contract info
abi = json.loads("""[
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "brand",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "discount",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "newOwner",
				"type": "address"
			}
		],
		"name": "giveCouponTo",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_to",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "_tokenId",
				"type": "uint256"
			}
		],
		"name": "transfer",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "newOwner",
				"type": "address"
			}
		],
		"name": "transferOwnership",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_owner",
				"type": "address"
			}
		],
		"name": "balanceOf",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "_balance",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_tokenId",
				"type": "uint256"
			}
		],
		"name": "brandOf",
		"outputs": [
			{
				"internalType": "string",
				"name": "data",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "currentIndex",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_tokenId",
				"type": "uint256"
			}
		],
		"name": "discountOf",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "data",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "idToCoupons",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "discount",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "brand",
				"type": "string"
			},
			{
				"internalType": "address",
				"name": "addr",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_tokenId",
				"type": "uint256"
			}
		],
		"name": "ownerOf",
		"outputs": [
			{
				"internalType": "address",
				"name": "_owner",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "ownerTicketCount",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]""")
address = "0xaa9E1688Ba2817Ad6175142e50b68098299258B2"

contract = web3.eth.contract(address=address, abi=abi)

def get_user_coupons(address):
    """
    Gets all the coupons associated with the address
    """
    i = 0
    coupons = []
    while True:
        addr = contract.functions.ownerOf(i).call()
        if addr == '0x0000000000000000000000000000000000000000':
            break
        elif addr == address:
            coupons.append(i)
        i += 1
    return [get_coupon_info(index) for index in coupons]


def get_coupon_info(index):
    """
    Gets the brand and the discount of the coupon from the id
    """
    return {
        "brand": contract.functions.brandOf(index).call(),
        "discount": contract.functions.discountOf(index).call(),
    }

def add_coupon_to_contract(discount, brand):
    nonce = web3.eth.getTransactionCount(ADDRESS)
    tx = {
        "nonce": nonce,
        "from": ADDRESS,
        "gas": 200000,
        "gasPrice": web3.toWei("200", "gwei")
    }
    transaction = contract.functions.giveCouponTo(brand, discount, ADDRESS).buildTransaction(tx)
    signed_txn = web3.eth.account.signTransaction(transaction, private_key=PRIVATE_KEY)
    web3.eth.sendRawTransaction(signed_txn.rawTransaction)
