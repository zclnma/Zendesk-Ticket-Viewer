# Zendesk Ticket Viewer

This project allows users to connect to Zendesk Support website and view their tickets locally with username and password access.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Python3 and an external 'requests' library are needed to run the code.

```
pip install requests
```

### Installing

Running the code is simple. Simply go to  ```ticket_Viewer``` directory and run

```
python3 main.py
```

If you see
```
Connecting to https://lionel.zendesk.com/api/v2/tickets.json?per_page=25...
Connecting successfully
Welcome to the ticket viewer.
You can quit ticket viewer by typing "quit" at anytime.

```
You are now successfully entering the system.

You can connect to any website by changing config file in  ```ticket_Viewer/config.txt```




## Authors

* **Lionel Zhao** - *Initial work* - [PurpleBooth](https://github.com/zclnma)


