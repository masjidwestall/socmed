This is the python script to publish prayer time into socmed story.
-------------------------------------------------------------------

At this point it only supports instagram.
What you need :
* *config.py* that contains the following :
  * your instagram account id (12 digit)
  * longlive token from your fb dev account
  * your own git repo (ig story api requires publicly accessible URL to retrieve the image
 
The content of your *config.py* will be something that look like this :

~~~python
longlive_token =
ig_acct_id =
git_path = https://github.com/{your_github_account}/{your_repo_name}/blob/main/picture/'
~~~

To deploy this to your server, create a new python venv, and then install all the requirements listed in requirements.txt.
~~~bash
python3 -m venv ENV
source ENV/bin/activate
pip install -r requirements.txt
~~~

And here's how you can deploy the script to crontab :

~~~bash
# run everyday at 3:00 AM
3 0 * * * {YOUR_ENV}/bin/python3 {path_to_yourdir}/westall.py > {path_to_yourdir}/running.log 2>&1
~~~

