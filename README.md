This is the python script to publish prayer time into socmed story.
-------------------------------------------------------------------

At this point it only supports instagram.
What you need :
* config.py that contains the following :
  * your instagram account id (12 digit)
  * longlive token from your fb dev account
  * your own git repo (ig story api requires publicly accessible URL to retrieve the image
 
The content of your config.py will be something that look like this :

~~~python
longlive_token =
ig_acct_id =
git_path = https://github.com/{your_github_account}/{your_repo_name}/blob/main/picture/'
~~~
