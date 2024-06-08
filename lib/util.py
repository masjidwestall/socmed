import random
import string
from datetime import datetime


def generate_random_timestamp_name(length=15):
  """Generates a random string with current timestamp (10 characters) 
      and fills remaining with random alphanumeric characters."""
  # Define characters allowed in the filename (alphanumeric)
  chars = string.ascii_lowercase + string.digits
  # Generate timestamp string (10 characters)
  timestamp = datetime.now().strftime("%y%m%d_%H%M")
  # Generate remaining random characters to reach desired length
  remaining_chars = length - len(timestamp)
  random_string = ''.join(random.choice(chars) for _ in range(remaining_chars))
  # Combine timestamp and random string
  return f"{timestamp}{random_string}"

# HH:MI
def parse_prayer_time(time_str):
   hour, minute = time_str.split(":")
   return f"{int(hour):02d}.{minute}"