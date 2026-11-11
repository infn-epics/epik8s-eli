# Ansible Update
This ansible scripts update a list of sparc consoles

## Requirements
ssh daemon installed on the target machine. Automation without password ask requires *host ansible ssh key* installed on the target.
```
## try
ssh-copy-id sparc@<console>

```

## Update:
```
ansible-playbook -i console_list.ini gitupdate.yaml --ask-pass
or 
ansible-playbook -i console_list.ini --limit pwsparcco004.lnf.infn.it gitupdate.yaml 
```

## Clone and Restart:
This ansible make a fresh clone and restart phoebus automatically
```
ansible-playbook -i console_list.ini gitupdateWindows.yaml --ask-pass
or 
ansible-playbook -i console_list.ini --limit pwsparcco004.lnf.infn.it gitupdateWindows.yaml
```
