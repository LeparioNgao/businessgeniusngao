#A file is a named container of data stored on your computer. Text files store plain text, one line after another. Python can read from them and write to them using built-in functions.

#open() is Python's built-in function for working with files. You give it a filename and a mode. The mode tells Python what you want to do: "r" for read, "w" for write (overwrites), "a" for append (adds to end). Always close the file when you are done, or use a with statement that does it automatically.

# In VS Code, this creates a file on your computer:(This will create a file named "daily_log.txt" in the current working directory. If the file already exists, it will be overwritten.)
with open("daily_log.txt", "w") as f:
    f.write("Steps: 9200\n")
    f.write("Water: 8 glasses\n")
    f.write("Protocol: OMAD\n")
    f.write("Cold shower: Yes\n")
    f.write("Sleep hours: 7\n")

import io

# Simulating file write using in-memory buffer(This is useful for testing without creating actual files on disk)
file_content = io.StringIO()
file_content.write("Steps: 8600\n")
file_content.write("Water: 4 glasses\n")
file_content.write("Protocol: Autophagy Marathon\n")
file_content.write("Cold shower: Yes\n")

print("File written. Contents:")
print(file_content.getvalue())

# In VS Code, this reads a file from your computer:(This will throw an error if the file doesn't exist. It works in local Python environments where file I/O is allowed.)
with open("daily_log.txt", "r") as f:
    content = f.read()
    print(content)

# Simulate file content(This is useful for testing without creating actual files on disk. It works on browser-based Python environments where file I/O is restricted.)
file_data = """Steps: 8600
Water: 4 glasses
Protocol: Autophagy Marathon
Cold shower: Yes
Sleep hours: 7.5
"""

# Simulate reading the whole file(This is useful for testing without creating actual files on disk. It works on browser-based Python environments where file I/O is restricted.)
f = io.StringIO(file_data)
content = f.read()
print("Full file content:")
print(content)

import io #This is useful for testing without creating actual files on disk. It works on browser-based Python environments where file I/O is restricted.

file_data = """Steps: 8600
Water: 4 glasses
Protocol: Autophagy Marathon
Cold shower: Yes
Sleep hours: 7.5
"""

f = io.StringIO(file_data)
lines = f.readlines()

print(f"Number of lines: {len(lines)}")
print()
for line in lines:
    line = line.strip()  # Remove newline character at end
    print("Line:", line)

#.strip() removes whitespace and newline characters from the start and end of a string. Always use it when reading lines from a file.

# In VS Code:
with open("daily_log.txt", "a") as f:
    f.write("Pages read: 30\n")
    f.write("Workout: Bench press\n")
print("daily_log.txt file updated with new entries. Check the file to see the changes.")
with open("daily_log.txt", "r") as f:
    content = f.read()
    print(content)

import io #This is useful for testing without creating actual files on disk. It works on browser-based Python environments where file I/O is restricted.

file_data = """Steps: 8600
Water: 4 glasses
Protocol: Autophagy Marathon
Cold shower: Yes
Sleep hours: 7.5
Pages read: 30
"""

log = {}
f = io.StringIO(file_data)
for line in f:
    line = line.strip()
    if ":" in line:
        key, value = line.split(":", 1)
        log[key.strip()] = value.strip()

print("Parsed log:")
for key, value in log.items():
    print(f"  {key}: {value}")



weekly_data = """Monday: 9200
Tuesday: 7500
Wednesday: 10500
Thursday: 8800
Friday: 6900
Saturday: 11000
Sunday: 9600
"""

goal = 8000
days_on_goal = 0

f = io.StringIO(weekly_data)
for line in f:
    line = line.strip()
    if ":" in line:
        day, steps_str = line.split(":", 1)
        steps = int(steps_str.strip())
        status = "Goal hit" if steps >= goal else "Below goal"
        print(f"{day}: {steps} steps - {status}")
        if steps >= goal:
            days_on_goal += 1

print(f"\nDays on goal: {days_on_goal}/7")