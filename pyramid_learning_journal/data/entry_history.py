"""List of all learning journal entries."""


from datetime import datetime

FMT = "%m/%d/%Y %I:%M %p"

ENTRIES = [
    {
        'id': 1,
        'title': "Day One",
        'creation_date': datetime.strptime('10/16/2017 4:18 PM', FMT),
        'body': "Finally starting 401! Super excited to finally start \
        learning brand new material for Python!\n\nSo far just a brief overview of the course and some of the basic basics of \
how to write Python, not much new on that front. The built-in function 'dir' \
seems like it should be very useful, especially if you are working with other \
people's modules. It would be a quick way to determine the various methods or \
properties available to you without going through the documentation. Although \
it would likely be easier to just look at the docs in the first place...\n\nAlso new was the introduction of building a new environment for each Python \
project. It makes perfect sense to isolate an individual project from the \
global environment, but I wonder why it isn't done in the same way as in \
JavaScript, with just a simple directory to store the relevant packages."
    },
    {
        'id': 2,
        'title': "Day Two",
        'creation_date': datetime.strptime('10/17/2017 4:19 PM', FMT),
        'body': "It's testing time! I'm so glad that pytest doesn't stop \
after one failed test. It is such a pain when I am doing challenges on CodeWars \
that one failed test breaks everything. I am curious if there are more \
efficient ways of writing the tests for the arithmetic series, or if I am \
automating them too much... At least overall these tests were not too onerous. \
\n\nThe fact that you have so many options for parameters in function \
definitions is super awesome! Especially the * for any number of arguments \
:D"
    },
    {
    'id': 3,
    'title': "Day Three",
    'creation_date': datetime.strptime('10/19/2017 5:53 PM', FMT),
    'body': """Lots of collections today. Not much new on that front. I love how easy it is to do slicing and reversing of sequences.\n\nI was wondering how you did a package.json for python, kinda a bummer that you need to type it out by hand. I bet there is a package to do it for you. Is there an easy way to save new dependancies to your setup.py, or do you need to do it manually? ...I bet there is a package for that too >.> It is interesting that you can specify dependancies that are only required for testing and such and separate them from the required dependancies."""
    },
    {
    'id': 4,
    'title': "Day Four",
    'creation_date': datetime.strptime('10/20/2017 8:44 PM', FMT),
    'body': """So far so good. It's Friday and we finished up doing the basics today. More details on collections. They basically act the same as the collections I have used in other languages, so that is reassuring.\n\nI love the error handling! It can make 'if' statements so much cleaner if used properly. Indeed it is "easier to ask forgiveness than permission." :D"""
    },
    {
    'id': 5,
    'title': "Day Five",
    'creation_date': datetime.strptime('10/21/2017 4:07 PM', FMT),
    'body': """So much coding :D\n\nHad fun with some kata in the fundamentals section of CodeWars. Not as difficult as some of the other ones I have done, in the sense that I didn't bang my head against them for days. However, I did notice that my solutions are not nearly as pythonic as basically anyone else's in the best-practices section. Need more practice writing Python..."""
    },
    {
    'id': 6,
    'title': "Day Six",
    'creation_date': datetime.strptime('10/23/2017 9:07 PM', FMT),
    'body': """I understand how sockets work. They are created in order to make connections between computers and usually the client side sockets are short lived. However, I do not know why there are always two sockets in the list of sockets at pretty much any port on localhost. Is localhost just constantly listening? Also, when we started our server, another socket was not added to the list. Is this because the server socket replaces the original one? Or is there something else going on here?\n\nI'm good on data structures. Implemented a bunch of these already in Java, so it's just a matter of translating."""
    },
    {
    'id': 7,
    'title': "Day Seven",
    'creation_date': datetime.strptime('10/24/2017 10:11 PM', FMT),
    'body': """It is interesting how many similarities there are between the class structures in Java and Python. But, I guess that they should be the same in pretty much every object oriented language.\n\nThe HTTP request/response format seems pretty straight forward, but I was wondering how you are supposed to put the '' at the end of each line. It is probably some special characters, but is it alright to just use a new-line character?"""
    },
    {
    'id': 8,
    'title': "Day Eight",
    'creation_date': datetime.strptime('10/25/2017 9:25 PM', FMT),
    'body': """Really sped through things today :D Good understanding of using super, and interesting that you can access the class through a class method. I was curious if it is possible to access other super methods besides the first one in MRO. Tried to use a fixture, but it did not act how I thought. I was thinking that you should use it for repeated set-up, like imports, declarations and such, but it doesn't do that. You should only use a fixture for the repeated creation of an object or to return some value."""
    },
    {
    'id': 9,
    'title': "Day Nine",
    'creation_date': datetime.strptime('10/26/2017 9:44 PM', FMT),
    'body': """Those property decorators are great! We used them today to create back and front properties for our queue in order to make it easier to understand. We were getting super confused by the naming of our variables, and so this allowed us to make it much clearer. It is great that you can in practice restrict access to your properties by using this decorator.\n\nOne thing that I like about Python is that you don't have to worry about asynchronicity, at least by default. It doesn't look to be as bad as JavaScript, but then again, I never got into promises."""
    },
    {
    'id': 10,
    'title': "Day Ten",
    'creation_date': datetime.strptime('10/27/2017 10:59 PM', FMT),
    'body': """So much os. Basically worked on step 3 of the server all day today, and were nearly done! Main issue was just that we had to research how to do everything. This wasn't a bad thing, just time consuming.\n\nNext up, asynchronicity."""
    },
    {
    'id': 11,
    'title': "Day Eleven",
    'creation_date': datetime.strptime('10/30/2017 6:55 PM', FMT),
    'body': """Started learning about Pyramid today, and it doesn't seem too difficult. As long as you attach all the pieces together, it is pretty simple to put together a static site. Curious as to how difficult it is to implement a dynamically filled website.\n\nCookiecutter is great for getting started! Since it builds out the entire repository and the file system, it makes it much easier to build what you want."""
    },
    {
    'id': 12,
    'title': "Day Twelve",
    'creation_date': datetime.strptime('10/31/2017 9:35 PM', FMT),
    'body': """Jinja is great! Much of the functionality is an improved version of Handlebars, which is my only point of reference for templating. The fact that you can access the request object inside of the template is fantastic. That should make it much easier to dynamically populate various things, like links etc.\n\nFinally got to a new data structure, the binary heap. I have never made a heap before but, since we are using a list to store the values instead of nodes, it is much easier to operate on than the binary tree that I learned about before. Yay, no recursion."""
    },
    {
    'creation_date': datetime.strptime('11/01/2017 10:16 PM', FMT),
    'title': "Day Thrirteen",
    'body': "SQLAlchemy, all of the Postgres with none of the SQL! <p>It is very interesting to interact with a database simply by interacting normally with objects. Definitely need to remember to add and commit changes made in order to actually change the database. This should make it much easier to make complicated queries to the database. Although I think that the reason why it was especially difficult in Node was that everything was asynchronous, which is not the case in Python. <p>I am curious how to implement other types of requests through Pyramid. Besides get requests through anchor tag links, we haven't had much interaction with the front-end side of the web site. I wonder if we just have routes that execute the different requests, like when using Page.js...",
    'id': 13
    }
]
