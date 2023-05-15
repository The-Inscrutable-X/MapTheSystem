import random
import sys

# Read emails from text file and load into a list
with open(sys.argv[1], "r") as f:
    emails = f.readlines()

print(emails)
# Pick a random email from the list
random_email = random.choice(emails)

# Print the randomly selected email
print("Random email:", random_email)

with open(f"winner_from_{sys.argv[1]}.txt", "w") as g:
    g.write(random_email)