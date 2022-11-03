import hashlib
import json
import requests
from Crypto.Hash import keccak

def cmd_passwordSearch(password):
	encoded_str = password.encode()
	
	keccak_hash = keccak.new(digest_bits=512)
	
	obj_sha3_5121 = keccak_hash.update(encoded_str)
 
	sha3k512 = keccak_hash.hexdigest()

	sub_pass = sha3k512[0:10]
	
	response = requests.get("https://passwords.xposedornot.com/api/v1/pass/anon/"+sub_pass)

	json_data = json.loads(response.text)
	try:
		json_data['Error']
		return False
	except:
		return True
	