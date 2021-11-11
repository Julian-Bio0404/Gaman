# Gaman

Gaman Rest Api. A web app that conect to athletes with sponsors
for their sponsorship, as well as helps to the people interested in 
practicing some sport, find those available in their local area.


![](https://img.shields.io/badge/python-v3.9-blue)
![](https://img.shields.io/badge/django-v3.2.8-blue)
![](https://img.shields.io/badge/djangorestframework-v3.12.4-blue)
![](https://img.shields.io/badge/psycopg2-v2.9.1-blue)
![](https://img.shields.io/badge/celery-v5.1.2-blue)


## Run

### Required software:
- Docker

to run the project, run:
```bash
docker-compose build
docker-compose up
```

to run the tests, on other console, run:
```bash
docker-compose run --rm django coverage run manage.py test -v 2
```

## Features
### Users 
  + **User** 
    + Gaman API has redis and celery services for response asynch for:
      + User sign-Up with sending a token for email confirmation
      + Refresh token for email confirmation
      + Restore password with sending a token to user email
      + Updating email with sending a token to user new email
    + Sign-Up filling in the fields such as last name, first name, username, telephone number, and choosing a role as an athlete, sponsor or coach
    + Login with email and password
    + User detail
    + User data update
  + **Profile**
    + Profile detail
    + Update or partial update of profile data as about, birth date, sport, country, public (true or false), web site and social link
    + Follow or unfollow to a club, brand or other user. If the profile is private, a follow request is sent
    + List followers and following
  + **Follow request**
    + Send, confirm or delete follow-up request
    + follow-up request detail
    + List unconfirmed follow-up requests
    
### Posts
  + **Post**
    + Create a Post with a description, pictures, videos, location, feeling, tag users and choosing privacy between public or private.
    + Post detail
    + Update or delete a post, 
    + React or share a post of a user
    + List posts of users followed
    + List post's reactions
 + **Comment**
    + Create, update or delete a comment on post
    + Comment detail
    + List post's comments. The comments will be listed in order of the number of reactions
    + React to a comment
    + List comment's reactions
    + Reply to a comment
    + List comment's replies. This replies will be listed in chronological order
 
### Sponsorships
  + **Sponsorship**
    + Create a sponsorship for an athlete or club. Only user with sponsor role and profile data comleted has access to this action
    + Sponsorship detail
    + Rating a sponsorship. Only the individual athletes sponsored or athletes and coach that belong to a club sponsored has access to this action.
    + Update or delete a rating
    + List ratings of a sponsorship
  + **Brand**
    + Create a brand filling the fields such as slugname, about, photo, cover photo and official web
    + Brand detail
    + List brands
    + Update or Delete a brand

## Documentation
To see the documentation for the Gaman REST API and see how to play with it, you can:
  - Import the Api_doc.postman_collection.json file to your Postman account.
  - Or visit the documentation on: https://documenter.getpostman.com/view/15752557/UVC2FTq9

## Founders
- [Nicolás Ortega](https://github.com/bioinnova)
- [Julian Hermida](https://github.com/Julian-Bio0404)