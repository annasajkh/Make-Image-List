from PIL import Image
import urllib.request
import tweepy
import glob
import os

auth = tweepy.OAuthHandler(os.environ["CONSUMER_KEY"], os.environ["CONSUMER_SECRET"])
auth.set_access_token(os.environ["ACCESS_TOKEN"],os.environ["ACCESS_TOKEN_SECRET"])

api = tweepy.API(auth)

#one image size is 100x100 so sqrt(581) is ~24.1 -> 25 then 25 * 100 = 2500 
bg : Image = Image.new("RGB",(2500,2500))

f = open("followers.txt", "r")

img_list = []

for img_name in glob.glob("*.png"):
    img_list.append(img_name)

print(img_list)

for follower in f.readlines():
    try:
        follower = follower.strip()

        if follower + ".png" in img_list:
            print(f"skipping {follower}")
            continue

        print(follower + ".png")


        user : tweepy.User = api.get_user(follower)

        
        print(f"downloading {follower}")
        urllib.request.urlretrieve(user.profile_image_url,f"{follower}.png")
    except:
        continue
f.close()


x = 0
y = 0

for img_name in glob.glob("*.png"):
    bg.paste(Image.open(img_name).resize((100,100)),(int(x),int(y)))

    x += 100

    if x == 2500:

        y += 100
        x = 0
bg.save("result.png")



