This project is the MVP backend service for an application which allows users to connect wallet addresses to their account, view their account balance, and view all the transactions for their connected wallet addresses. 

Call Outs
- I defaulted synchronizing transactions to the top 100 transactions because I did not want to setup a large database to store that information for MVP.
- The database I designed only includes the minimum necessary information for the MVP to map wallet addresses to users and pull high-level transaction information for wallet addresses.

Install package dependencies
- Run `poetry install`

Setup a postgres Database
- `database_init.sql` contains the commands to setup the tables used in this project.
- Once you've created a database, add your database connection details to `database.ini`

Running the API service:
1. Change directory to `cointracker/api/v1`
2. Run `uvicorn user:app`
4. Navigate to `localhost:8000/docs` to test the APIs

Connecting from external applications:
(Note: Requires NGROK account which is free to setup)
1. Run the application using ngrok with the command `USE_NGROK=True uvicorn user:app`. The ngrok tunnel will be outputted to the terminal.
2. Connect external applications to the tunnel endpoint and call the APIs.

Possible Improvements:
- Add tests for different services
- Improve the synchronize logic to run async and load all user transactions
- Expand API endpoints to perform actions for each model and add error handling logic to all endpoints
- Use an ORM for database access