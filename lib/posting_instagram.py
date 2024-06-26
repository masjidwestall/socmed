import requests
import config

def post_reel(caption='', media_type ='',share_to_feed='',thumb_offset='',video_url=''):
    url = config.graph_url + config.ig_acct_id + '/media'
    print("\n url",url)
    param = dict()
    param['access_token'] = config.longlive_token
    param['caption'] = caption
    param['media_type'] = media_type
    param['share_to_feed'] = share_to_feed
    param['thumb_offset'] = thumb_offset
    param['video_url'] = video_url
    response =  requests.post(url,params = param)
    print("\n response",response.content)
    response =response.json()
    return response

def post_story(image_url=''):
    url = config.graph_url + config.ig_acct_id + '/media'
    param = dict()
    param['access_token'] = config.longlive_token
    param['caption'] = caption
    param['image_url'] = image_url
    param['media_type'] = 'STORIES'
    response = requests.post(url, params=param)
    print("\n response", response.content)
    response = response.json()
    return response


def post_image(caption='', image_url=''):
    url = config.graph_url + config.ig_acct_id + '/media'
    param = dict()
    param['access_token'] = config.longlive_token
    param['caption'] = caption
    param['image_url'] = image_url
    response = requests.post(url, params=param)
    print("\n response", response.content)
    response = response.json()
    return response


def post_carousel(caption = '',media_url = ''):
    url = config.graph_url + config.ig_acct_id + '/media'
    param = dict()
    param['access_token'] = config.longlive_token
    param['is_carousel_item'] = 'true'
    container_id = []
    for i in media_url:
        param['image_url'] = i
        response = requests.post(url, params=param)
        print("\n response", response.content)
        response = response.json()
        container_id.append(response['id'])
    carousel_container_id = make_carousel_container(container_id=container_id,caption=caption)
    return carousel_container_id

def make_carousel_container(container_id='',caption=''):
    url = config.graph_url + config.ig_acct_id + '/media'
    container_id = ','.join(container_id)
    param = dict()
    print(container_id)
    param['access_token'] = config.longlive_token
    param['media_type'] = 'CAROUSEL'
    param['children'] = container_id
    param['caption'] = caption
    response = requests.post(url, params=param)
    print("\n response", response.content)
    response = response.json()
    return response['id']

def post_video(video_url='',caption=''):
    url = config.graph_url + config.ig_acct_id + '/media'
    param = dict()
    param['access_token'] = config.longlive_token
    param['caption'] = caption
    param['video_url'] = video_url
    param['media_type'] = 'VIDEO'
    param['thumb_offset'] = '10'
    response = requests.post(url, params=param)
    print("\n response", response.content)
    response = response.json()
    return response

def status_of_upload(ig_container_id = ''):
    url = config.graph_url + ig_container_id
    param = {}
    param['access_token'] = config.longlive_token
    param['fields'] = 'status_code'
    response = requests.get(url,params=param)
    print("\n response",response.content)
    response = response.json()
    return response

def publish_container(creation_id = ''):
    url = config.graph_url + config.ig_acct_id + '/media_publish'
    param = dict()
    param['access_token'] = config.longlive_token
    param['creation_id'] = creation_id
    response = requests.post(url,params=param)
    response = response.json()
    return response

caption = 'Prayer Time @imcv.westall'
media_type = 'STORIES'
share_to_feed = 'true'
thumb_offset = '1'

