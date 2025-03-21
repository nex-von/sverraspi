#!/bin/bash

# Start the echo server in the background
cd server
python3 server.py &

# Give the server a moment to start
sleep 2

# Start the echo client
cd ../client
python3 client.py

# Wait for the server process to finish
wait