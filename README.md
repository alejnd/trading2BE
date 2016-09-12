

#Approach
I decided to run the project using using virtual machines provisioned by ansible. For the backend I used Flask because i really like minimalistic frameworks, instead of a full featured DB I choosed sqlite because is more than enought for  this example.   

#Requirements
To run this proyect you need to have virtualbox, vagrant and ansible installed.

#Setup
 You need to choose the ip of the VM, to do this simply open the file Vagrantfile
and change this line config.vm.network "private_network", ip: "192.168.2.3" to choose your ip address

#Run
exectute: vagrant up

The vm has network conectivity so you don need to access directly but you can do it executing vagrant ssh

Server is running on port 8000
example remote test:
By web browser: 
http://192.168.2.3:8000
inserts usgin JSON rest service: 
>curl -H "Content-Type: application/json" -X POST -d '{"sell_currency":"EUR", "sell_amount":222 ,"buy_currency":"AUD"}' http://127.0.0.1:8000/trade.html

#Troubleshooting
if you get a message like this:
>"fatal: [default] => SSH encountered an unknown error during the connection. 
We recommend you re-run the command using -vvvv, which will enable SSH debugging output to help diagnose the issue"

Its a ssh-key fingerprint collision, remove the previous keys in ~/.ssh/ known_hosts and lauch again.
