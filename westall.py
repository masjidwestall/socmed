import requests
import json
from PIL import Image, ImageDraw, ImageFont
from textwrap import fill
import random
import string
from datetime import datetime
from lib.posting_instagram import post_story,publish_container,status_of_upload
from git import Repo
import time

# where the raw image can be reached by facebook, include the last trailing path if needed
git_path = 'https://raw.githubusercontent.com/masjidwestall/socmed/main/'

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

# Define the URL with your masjid ID
url = "https://masjidal.com/api/v1/time/range?masjid_id=QL0MJpAZ"

# Define file path
# json_file_path = "./prayer_times.json"

# Open and read the JSON file
# with open(json_file_path, "r") as f:
#  data = json.load(f)

# Send a GET request to the API
response = requests.get(url)

# Check for successful response (status code 200)
if response.status_code == 200:
#if data:
  # Parse the JSON data
  data = json.loads(response.text)
  
  # Extract prayer times (assuming data follows the format you provided)
  prayer_times = data["data"]["salah"][0]
  iqamah_times = data["data"]["iqamah"][0]
  
   # Parse and convert prayer times as before (refer to previous code explanation)
  def parse_prayer_time(time_str):
    hour, minute = time_str.split(":")
    return f"{int(hour):02d}.{minute}"
  
  heading = "\t\tAthan\t\tIqamah"
  fajr  = "Fajr\t:\t" + parse_prayer_time(prayer_times["fajr"]) + "\t\t" + parse_prayer_time(iqamah_times["fajr"])
  zuhr  = "Zuhr\t:\t" + parse_prayer_time(prayer_times["zuhr"]) + "\t\t" + parse_prayer_time(iqamah_times["zuhr"])
  asr   = "Ashr\t:\t" + parse_prayer_time(prayer_times["asr"]) + "\t\t" + parse_prayer_time(iqamah_times["asr"])
  maghrib = "Maghrib\t:\t" + parse_prayer_time(prayer_times["maghrib"]) + "\t\t" + parse_prayer_time(iqamah_times["maghrib"])
  isha = "Isha\t:\t" + parse_prayer_time(prayer_times["isha"]) + "\t\t" + parse_prayer_time(iqamah_times["isha"])
  #jummah1 = parse_prayer_time(prayer_times["jummah1"])

  # Print prayer times
  # Replace with your image path and desired font path
  # different background and fonts for every day in the week, except Friday for now
  image_path = "picture/1-bg2-westall.jpg"
  font_path = "font/MidcentDisco.ttf"

  # Load the background image
  image = Image.open(image_path)
  draw = ImageDraw.Draw(image)

  # Get image dimensions (width, height)
  image_width, image_height = image.size
  
  # Define font size and color
  font_size = 26  # Adjust as needed
  font_color = (255, 0, 0)  # White color
  font = ImageFont.truetype(font_path, font_size)
  

  # Define a function to calculate text width (considering potential line breaks)
  def get_text_width(text):
    text_width = draw.textlength(text, font=font)
    # Check for potential line breaks and adjust width accordingly
    if "\n" in text:
      lines = text.split("\n")
      text_width = max(draw.textlength(line, font=font) for line in lines)
    return text_width

  # Define a function to center text horizontally
  def center_text_horizontally(text):
    text_width = get_text_width(text)
    x_center = (image_width - text_width) // 4
    return x_center

  current_y = 20
  # Define a function to center text vertically (optional, adjust margins)
  def center_text_vertically(text):
    global current_y
    text_height = draw.textsize(text, font=font)[1]
    y_center = (image_height - text_height) 
    y_center = current_y + (image_height - text_height) - 500
    # Increment current_y for next call
    current_y += 50
    return y_center
  
  # Define text positions using centering functions
  text_positions = [
    (center_text_horizontally(heading), center_text_vertically(heading)),
    (center_text_horizontally(fajr), center_text_vertically(fajr)),
    (center_text_horizontally(zuhr), center_text_vertically(zuhr)),
    (center_text_horizontally(asr), center_text_vertically(asr)),
    (center_text_horizontally(maghrib), center_text_vertically(maghrib)),
    (center_text_horizontally(isha), center_text_vertically(isha)),
  #  (center_text_horizontally(jummah1), center_text_vertically(jummah1)),
  ]
 
  print(text_positions)
  # Draw prayer times on the image
  for text, position in zip([heading, fajr, zuhr, asr, maghrib, isha], text_positions):
    text = fill(text, width=50)  # Wrap text to 80 characters
    draw.text(position, text, font=ImageFont.truetype(font_path, font_size), fill=font_color)

  # Save the modified image with a new name (optional)
  new_image_path = 'resource/' + generate_random_timestamp_name() + '.jpg'
  image.save(new_image_path)

  print(f"Prayer times added to image: {new_image_path}")
  repo = Repo('.')
  repo.index.add(new_image_path)
  repo.index.commit('Completing generation '+ new_image_path)
  remote = repo.remote()
  remote.push()

  status = post_story(image_url=git_path + new_image_path)
  
  container_id = status["id"]

  for _ in range(10):  # Check max 10 times with sleep 15 seconds each
    time.sleep(15)
    check = status_of_upload(container_id)
   # status_code = check["status_code"]
    print(f'Status Upload : {check["status_code"]}')
    if check["status_code"] == 'FINISHED':
      publish_container(container_id)
      print("Published !")
      break

else:
  print("Error:", response.status_code)
  
  

