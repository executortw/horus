import re


#test = re.search("(?<=Accepted\skeyboard-interactive/pam\sfor)\s[a-z]*","Mar 12 09:44:04 Earth sshd[39424]: Accepted keyboard-interactive/pam for sarek from 140.110.101.185 port 1393 ssh2")
test = re.search("(?<=L-amPrins... !! ->)[a-zA-Z0-9]*\:[a-zA-Z0-9]*\:\s([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})","L-amPrins... !! ->root:123456:140.117.241.171")
print test.group(0)
