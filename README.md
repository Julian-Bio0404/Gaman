# Gaman

Gaman Rest Api. A web app that conect to athletes with sponsors
for their sponsorship, as well as helps to the people interested in 
practicing some sport, find those available in their local area.


![](https://img.shields.io/badge/python-v3.9-blue)
![](https://img.shields.io/badge/django-v4.0.3-blue)
![](https://img.shields.io/badge/djangorestframework-v3.13.1-blue)
![](https://img.shields.io/badge/psycopg2-v2.9.3-blue)
![](https://img.shields.io/badge/celery-v5.2.3-blue)


## Run

### Required software:
- Docker

to run the project, run:
```bash
docker-compose build
docker-compose up
```

to run the tests, on other console, run:
- All tests
  ```bash
  docker-compose run --rm django coverage run manage.py test -v 2
  ```
- Test of a app
  ```bash
  docker-compose run --rm django coverage run manage.py test <app-dir>.tests -v 2
  ```
- Tests of a app sub-module
  ```bash
    docker-compose run --rm django coverage run manage.py test <app-dir>.tests.<file-name> -v 2
  ```
- Tests of a sub-module class
  ```bash
    docker-compose run --rm django coverage run manage.py test <app-dir>.tests.<file-name>.<Test-class> -v 2
  ```
- Specific test
  ```bash
    docker-compose run --rm django coverage run manage.py test <app-dir>.tests.<file-name>.<Test-class>.<test_method> -v 2
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
    + List user's sponsorships
    + List club's invitations
  + **Follow request**
    + Send, confirm or delete follow-up request
    + follow-up request detail
    + List unconfirmed follow-up requests
    + Follow-up to brands, clubs or others users
    
### Posts
  + **Post**
    + Create a Post with a description, pictures, videos, location, feeling, tag users and choosing privacy between public or private, as a user, club or brand.
    + Post detail
    + Update or delete a post, 
    + React or share a post of a user
    + List posts of followed
    + List post's reactions (all, likes, loves, angries, sad and curious, haha)
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
    + Create a sponsorship to an athlete or club. Only user with sponsor role and profile data comleted has access to this action
    + Sponsorship detail
    + Rating a sponsorship. Only the individual athletes sponsored or athletes and coach that belong to a club sponsored has access to this action.
    + Update or delete a rating
    + List ratings of a sponsorship
  + **Brand**
    + Create a brand filling the fields such as slugname, about, photo, cover photo and official web
    + Brand detail
    + List brands
    + Update or Delete a brand
    + List brand's posts
    + List brand's followers

### Sports
  + **Leagues**
    + List registered leagues
    + League detail
  + **Clubs**
    + Create a club. Only user with trainer or League president role has access to this action
    + Club detail
    + Update club's data
    + List club's posts
    + List club's sponsorships
    + List club's followers
  + **Members**
    + List club's members
    + Create and confirm invitation
    + Detail, deactive, reactive or expel a member
  + **Events**
    + Create a Sport event with title, description, photo, start date, finish date, and a geolocation. The event author can be an user, a brand or a club. This feature determine the country, state, city and place name from the geolocation provided, using a third party api of geolocation, available on: [Api HERE](https://developer.here.com/)
    + Detail, update or delete a SportEvent
    + List events filtering by country, state or city
    + Mark go to an event
    + List assistants of a event


## Documentation
To see the documentation for the Gaman REST API and see how to play with it, you can:
  - Import the Gaman.postman_collection.json file to your Postman account.
  - Or visit the documentation on: https://documenter.getpostman.com/view/15752557/UVC2FTq9

## Founders
- [Nicolás Ortega](https://github.com/bioinnova)
- [Julian Hermida](https://github.com/Julian-Bio0404)