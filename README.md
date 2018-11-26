# OMDB-API-Bridge
[![Build Status](https://Travis-ci.com/lobsterick/OMDB_API_bridge.svg?branch=master)](https://travis-ci.com/lobsterick/OMDB_API_bridge) 
[![Heroku](http://heroku-badges.herokuapp.com/?app=omdb-api-bridge-lobsterick&svg=1&root=api)](https://omdb-api-bridge-lobsterick.herokuapp.com/api/)



## What is OMDB-API-Bridge?
OMBD-API-bridge is *Proof-of-Concept* project for using (*existing*) and making (*own*) API's in **Django Rest Framework**. It based on external [OMDB-API](http://www.omdbapi.com/) for getting movies and serving them to user of this app in similar form.
Additional features (compare to OMDB-API) of this app are:
* saving all data fetched from OMDB-API to own database ([<u>can be useful, because OMDB-API now has limit of 1000 requests from one API-key</u>](https://www.patreon.com/bePatron?u=5038490))
* add comments to movies existing in database (and also store them in internal database)


## Requirements for endpoints
* **POST */movies*:**
Request body should contain only movie title, and its presence should be validated. Based on passed title, other movie details should be fetched from http://www.omdbapi.com/ (or othersimilar, public movie database) - and saved to application database. Request response should include full movie object, along with all data fetched from external API.
* **GET */movies*:**
Should fetch list of all movies already present in application database.
Additional filtering, sorting is fully optional - but some implementation is a bonus.
* **POST */comments*:**
Request body should contain ID of movie already present in database, and comment text body.
Comment should be saved to application database and returned in request response.
* **GET */comments*:** Should fetch list of all comments present in application database and should allow filtering comments by associated movie, by passing its ID. 

## How to use?
You can use it as normal Django app, f.e. run using `manage.py` or add it to Your own project (don't forget about adding info in `urls.py` and `settings.py`).

For convenience, working version of this app is currently hosted on **Heroku** (you can access by clicking on *"<u>Heroku Badge</u>"* below *Title*).

Also, for testing purpose, i suggest using software like [Postman](https://www.getpostman.com/).

If you want test, if this app working properly, use `manage.py test` command (localserver) or check *"<u>Travis Badge</u>"* below *Title*.

## Routes and parameters
All API-related routes are available on /api route.
* **POST */api/movies*:** with required parameter `title` containing movie title, returning details for given movie title,
* **GET */api/movies*:** with optional parameter `order` equal to `dsc` for descending order of all movies, returning all movies fetched from external database,
* **POST */api/comments*:** with required parameter `movie_id` containing id of movie existing in database and parameter `comment_body` containing text of a new comment, returning added comment (if successful)
* **GET */api/comments*:** with optional parameter `movie_id` containing id of movie existing in database, returning all comments in database or (with argument) all comments for given `movie_id`.


## Known problems
* In `test.py`, there are some tests (all for GET requests) that fail. It looks like APIClient() GET requests containing body information is getting by server without this additional information. Luckily, outside test environment all is working properly. Also - [it's still being debated, if GET request should contain body data](https://github.com/postmanlabs/postman-app-support/issues/131), but it was necessary for fulfilling the requirements.
