# Use this code for validating your key file setup
# You MUST change the path to the key file


from dotenv import load_dotenv
import os

# Load the file that contains the API keys
# CHANGE THE PATH TO THE KEY FILE
load_dotenv('C:\\Users\\raj\\.jupyter\\.env')

# Get the test API Key from env variable
TEST_API_KEY=os.getenv("TEST_API_KEY")

# Print the retrieved key
print("TEST_API_KEY: ", TEST_API_KEY)
