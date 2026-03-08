import requests
import json
from PIL import Image, ImageDraw, ImageFont
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
# data = json.load(f)

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
 
 tgl = curr_date
 # 3 columns: Prayer name | Athan | Iqamah (data as (col1, col2, col3) tuples)
 header = ("", "Athan", "Iqamah")
 rows = [
     ("Fajr", parse_prayer_time(prayer_times["fajr"]), parse_prayer_time(iqamah_times["fajr"])),
     ("Zuhr", parse_prayer_time(prayer_times["zuhr"]), parse_prayer_time(iqamah_times["zuhr"])),
     ("Asr", parse_prayer_time(prayer_times["asr"]), parse_prayer_time(iqamah_times["asr"])),
     ("Maghrib", parse_prayer_time(prayer_times["maghrib"]), parse_prayer_time(iqamah_times["maghrib"])),
     ("Isha", parse_prayer_time(prayer_times["isha"]), parse_prayer_time(iqamah_times["isha"])),
 ]
 jummah_time = parse_prayer_time(iqamah_times["jummah1"])

 # Print prayer times
 # different background and fonts for every day in the week
 image_path = "resource/" + curr_day + ".jpg"
 
 tgl_font_path = "font/WinkySans-Bold.ttf"
 font_path = "font/Overlock-Regular.ttf"

 # Load the template image
 image = Image.open(image_path)
 draw = ImageDraw.Draw(image)

 # This is the template image dimensions (width, height)
 image_width, image_height = image.size
 
 # Define font size and color
 font_size = 46 # Adjust as needed
 font_color = (0, 0, 0) # Black color
 font = ImageFont.truetype(font_path, font_size)
 
 # This is the font size and color for the date
 tgl_font_size = 52 # Adjust as needed
 tgl_font_color = (0, 0, 0) # Black color
 tgl_font = ImageFont.truetype(tgl_font_path, tgl_font_size)

 # --- 3-column layout: Prayer | Athan | Iqamah (aligned at bottom) ---
 margin = int(image_width * 0.08)
 col_width = (image_width - 2 * margin) // 3
 col1_x = margin
 col2_x = margin + col_width
 col3_x = margin + 2 * col_width

 line_height = 80
 bottom_margin = int(image_height * 0.08)
 # Table lines: header + 5 prayers + (1 if Friday for Jumma)
 num_table_lines = 1 + len(rows) + (1 if curr_day == "Friday" else 0)
 table_height = num_table_lines * line_height
 # Anchor table so its last row sits just above bottom_margin
 start_y = image_height - bottom_margin - table_height

 # Draw date (centered, one line above the table)
 tgl_bbox = draw.textbbox((0, 0), tgl, font=tgl_font)
 tgl_w = tgl_bbox[2] - tgl_bbox[0]
 tgl_x = (image_width - tgl_w) // 2
 tgl_y = start_y - line_height - 20
 draw.text((tgl_x, tgl_y), tgl, font=tgl_font, fill=tgl_font_color)

 # Draw header row
 y = start_y
 for i, cell in enumerate(header):
     x = [col1_x, col2_x, col3_x][i]
     draw.text((x, y), cell, font=font, fill=font_color)
 y += line_height

 # Draw prayer rows (3 columns each)
 for row in rows:
     for i, cell in enumerate(row):
         x = [col1_x, col2_x, col3_x][i]
         draw.text((x, y), cell, font=font, fill=font_color)
     print(row[0], row[1], row[2])
     y += line_height

 # Draw Jumma row only on Friday
 if curr_day == "Friday":
     draw.text((col1_x, y), "Jumma", font=font, fill=font_color)
     draw.text((col3_x, y), jummah_time, font=font, fill=font_color)
     print("Jumma", jummah_time)

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

 for _ in range(10): # Check max 10 times with sleep 15 seconds each
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

