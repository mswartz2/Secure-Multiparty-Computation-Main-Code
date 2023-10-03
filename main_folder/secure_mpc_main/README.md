# secure-mpc
CS 438/538: Network Security Project - Secure Multy-Party Computation


## usage

- First, on each client run the following:
`python3 client.py -secret <num> -client_id <our clientid> -num_clients <total number of clients>`

- Second, for each client target the other clients to get the proper share from their list. EX: from client1 with two other clients:
`python3 client.py -client 2`
`python3 client.py -client 3`

- Third, on each client we send add our shares from file and send to server for storage:
`python3 -sumpoint ./data.json`

- Forth, we can recieve the sumpoint list and then add it up on client:
`python3 -get_sumpoints — THIS PRINTS OUT THE TOTAL OF SUMPOINTS`


## folders
- client/ - holds required files for client
- server/ - holds required files for server


## TODO
- TODO: error handling on empty lists, if data.json is empty on client or server, create one.
- TODO: Later.. Change CLIENT Request a LIST of their shares from all client(s) [f0, g0, r0] instead of requesting individually..?
    -   I forgot to mention that # TODO 2 is not necessary at this point. We will eventually remove the server which acts as a central authority for distributing shares/sum_points
- TODO: How should CLIENT know all other clients have POSTED SUMPOINT???  Assume?
    - Clients know the total number of clients (this is need for the interpolation of the sum points)
    - Clients will eventually submit their shares and sum points to the server. So, for requests of shares/sum_points, the server can return a list which can be empty in the case of no prior submissions (edited) 


## DONE
- DONE TODO: Calculate secret shares on CLIENT itself, and share those with SERVER. These will stored on server in data.json{...“shares”:{“1":[1,2,3],“2”:[x,x,x]..}}
- DONE TODO: CLIENT SUMs Shares as SUMPOINT
- DONE TODO: CLIENT POST SUMPOINT - POST to server.  Server stores in data.json{...“sumpoints”:[123,x,x]}} ie, POST 123 = data.sumpoints[client_id=val]
- DO WE NEED TO SAVE SUM??? TODO: CLIENT GET LIST SUMPOINT(s) - Store locally on client data.json{...“sumpoints”:[123,145,132]} or somewhere else
- DONE TODO: CLIENT Calculates Sum of SUMPOINT(s) - 123 + 145 + 132 = 400
