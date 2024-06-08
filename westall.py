import requests
import json
from PIL import Image, ImageDraw, ImageFont
from textwrap import fill
from lib.posting_instagram import post_story,publish_container,status_of_upload
from lib.util import generate_random_timestamp_name,parse_prayer_time
from git import Repo
import time

#############
import logging
from git import Repo, GitCommandError

# Set up logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("git_repo.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
#############

# where the raw image can be reached by facebook, include the last trailing path if needed
git_path = 'https://raw.githubusercontent.com/masjidwestall/socmed/main/'

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
  curr_date = data["data"]["salah"][0]["date"]
  curr_day = data["data"]["salah"][0]["date"].split(",")[0]
  prayer_times = data["data"]["salah"][0]
  iqamah_times = data["data"]["iqamah"][0]  
  
  heading = " \t\t   Athan\t    Iqamah" 
  tgl = "\t\t " + curr_date
  blank_line = " "
  fajr  = "Fajr     \t" + parse_prayer_time(prayer_times["fajr"]) + "\t\t" + parse_prayer_time(iqamah_times["fajr"])
  zuhr  = "Zuhr    \t" + parse_prayer_time(prayer_times["zuhr"]) + "\t\t" + parse_prayer_time(iqamah_times["zuhr"])
  asr   = "Asr \t\t" + parse_prayer_time(prayer_times["asr"]) + "\t\t" + parse_prayer_time(iqamah_times["asr"])
  maghrib = "Maghrib    " + parse_prayer_time(prayer_times["maghrib"]) + "\t   " + parse_prayer_time(iqamah_times["maghrib"])
  isha = "Isha  \t\t" + parse_prayer_time(prayer_times["isha"]) + "\t\t" + parse_prayer_time(iqamah_times["isha"])
  jummah1 = "Jumma\t\t\t" + parse_prayer_time(iqamah_times["jummah1"])

  # Print prayer times
  # different background and fonts for every day in the week
  image_path = "resource/" + curr_day + ".jpg"
  
  tgl_font_path = "font/OpenSans-Bold.ttf"
  font_path = "font/OpenSans-Medium.ttf"

  # Load the template image
  image = Image.open(image_path)
  draw = ImageDraw.Draw(image)

  # This is the template image dimensions (width, height)
  image_width, image_height = image.size
  
  # Define font size and color
  font_size = 44  # Adjust as needed
  font_color = (0, 0, 0)  # Black color
  font = ImageFont.truetype(font_path, font_size)
  
  # This is the font size and color for the date
  tgl_font_size = 46  # Adjust as needed
  tgl_font_color = (0, 0, 0)  # Black color
  tgl_font = ImageFont.truetype(tgl_font_path, tgl_font_size)

  # Calculate text width (considering potential line breaks)
  def get_text_width(text, font):
    text_width = draw.textlength(text, font)
    # Check for potential line breaks and adjust width accordingly
    if "\n" in text:
      lines = text.split("\n")
      text_width = max(draw.textlength(line, font) for line in lines)
    return text_width

  # Calculate text horizontally
  def center_text_horizontally(text, font):
    text_width = get_text_width(text, font)
    x_center = (image_width - text_width) // 6
    return x_center

  current_y = 0
  # Calculate text vertically (optional, adjust margins)
  def center_text_vertically(text, font):
    global current_y
    text_height = draw.textsize(text, font)[1]
    y_center = (image_height - text_height) 
    y_center = current_y + (image_height - text_height) - 640
    # current_y = spacing per line
    current_y += 70
    return y_center
  
  # Define text positions using centering functions
  # for date, use it's own text and font
  tgl_positions = [center_text_horizontally(tgl, tgl_font), center_text_vertically(tgl, tgl_font)]
  
  # for prayer text
  text_positions = [
    (center_text_horizontally(blank_line, font), center_text_vertically(blank_line, font)),
    (center_text_horizontally(heading, font), center_text_vertically(heading, font)),
    (center_text_horizontally(fajr, font), center_text_vertically(maghrib, font)),
    (center_text_horizontally(fajr, font), center_text_vertically(maghrib, font)),
    (center_text_horizontally(fajr, font), center_text_vertically(maghrib, font)),
    (center_text_horizontally(fajr, font), center_text_vertically(maghrib, font)),
    (center_text_horizontally(fajr, font), center_text_vertically(maghrib, font)),
  ]

  # for jumma text position, align with fajr text and font
  jumma_positions = [center_text_horizontally(fajr, font), center_text_vertically(fajr, font)]
  
  # Draw date on the image
  # print(tgl_positions)
  tgl_text = fill(tgl, width=60)  # Wrap text to 60 characters
  draw.text(tgl_positions, tgl_text, font=ImageFont.truetype(tgl_font_path, tgl_font_size), fill=tgl_font_color)

  # Draw prayer times on the image
  # print(text_positions)
  for text, position in zip([blank_line, heading, fajr, zuhr, asr, maghrib, isha], text_positions):
    text = fill(text, width=60)  # Wrap text to 60 characters
    print(text)
    draw.text(position, text, font=ImageFont.truetype(font_path, font_size), fill=font_color)

  # Draw Jummat text only if this is Friday
  if curr_day == 'Friday' :
    print (jummah1)
    # print(tgl_positions)
    jumma_text = fill(jummah1, width=60)  # Wrap text to 60 characters
    draw.text(jumma_positions, jumma_text, font=ImageFont.truetype(font_path, font_size), fill=font_color)

  # Save the modified image with a new name (optional)
  new_image_path = 'picture/' + generate_random_timestamp_name() + '.jpg'
  image.save(new_image_path)

  print(f"Prayer times added to image: {new_image_path}")

  try: 
   repo = Repo('.')
   repo.index.add(new_image_path)
   repo.index.commit('Story image generated : '+ new_image_path)
   remote = repo.remote()
   remote.push()

  except GitCommandError as e:
   logger.exception("Git command error occurred")
  except Exception as e:
   logger.exception("An unexpected error occurred")


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
  


