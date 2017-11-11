# Testing Plan

## Unit Tests

### Views

##### list_view
 - GET
     + Returns list of entries
     + list is the length of the Entries in the database
     + list contains Entries as to_html_dict

##### detail_view
 - GET
     + Given invalid id, raises HTTPNotFound
     + Given valid id:
         + returns one entry as to_html_dict
         + the entry matches the one with the id

##### create_view
 - GET
     + Returns a dictionary with only the page_title
 - POST
     + Given incomplete data, raises HTTPBadRequest
     + Given complete data
         * new Entry is created
         * new Entry has provided information
         * returns a 302 reponse code
         * returns a HTTPFound redirect to the home page

##### update_view
 - GET
     + Given invalid id, raises HTTPNotFound
     + Given valid id:
         + returns one entry as to_dict
         + the entry matches the one with the id
 - POST
     + Given invalid id, raises HTTPNotFound
     + Given incomplete data, raises HTTPBadRequest
     + Given complete data and valid id:
         * the Entry is updated with given info
         * the Entry updated is the one with the given id
         * returns a 302 reponse code
         * returns a HTTPFound redirect to the detail page of given id

##### delete_journal_entry
 - GET
     + Raises HTTPNotFound
 - POST
     + Given invalid id, raises HTTPNotFound
     + Given valid id:
         * the Entry is deleted
         * the Entry deleted is the one with the given id
         * returns a 302 reponse code
         * returns a HTTPFound redirect to the home page

##### login
 - GET
     + Given authenticated user, returns a HTTPFound redirect to the home page
     + Returns a dictionary with only the page_title
 - POST
     + Given authenticated user, returns a HTTPFound redirect to the home page
     + Given incomplete data, raises HTTPBadRequest
     + Given complete, incorrect data, return dictionary with error
     + Given complete, correct data:
         * returns a 302 response code
         * returns a HTTPFound redirect to the home page

##### logout
 - any route
     + returns a 302 response code
     + returns a HTTPFound rediret to the home page

### Models

##### Entry
 + constructor
     * New Entry with no date gets added to database
         - creation_date is set to now
     * New Entry with a date gets added to database
         - creation_date is set to given date
 + to_dict
     * All attributes added to dictionary
         - id, title, body, left as is
         - creation_date, converted string
 + to_html_dict
     * All attributes added to dictionary
         - id, title, left as is
         - body, converted to HTML
         - creation_date, converted string

## Functional Tests

### Routes

##### home - `/`
 + GET
     * Has 200 response code
     * Has all journal entries
         - count the cards
     * Unauthenticated:
         - login tab
     * Authenticated:
         - logout tab and create tab

##### detail - `/journal/{id:\d+}` 
 + GET
     * Given invalid id, directs to 404 page
         - response has 404 status code
         - has h1 tag with 'Oops'
     * Has 200 response code
     * Has one journal enry
         - count the cards
         - title is correct
     * Unauthenticated:
         - no edit button
     * Authenticated:
         - edit button

##### create - `/journal/new-entry`
 + GET
     * Unauthenticated:
         - 403 forbidden
     * Authenticated:
         * Has 200 response code
         * Has an empty form with a submit button
             - check value of inputs
             - count the submit buttons 
 + POST
     * Unauthenticated:
         - 403 forbidden
     * Authenticated:
         * Given incomplete data, has error
             - response has 400 status code
         * Given complete data:
             - new Entry object created
             - reponse has 302 status code
             - redirects to home page
             - home page now lists new entry
             - should be able to access the new entry detail page
             - detail page has actual details of entry

##### edit - `/journal/{id:\d+}/edit-entry`
 + GET
     * Unauthenticated:
         - 403 forbidden
     * Authenticated:
         * Given invalid id, directs to 404 page
             - response has 404 status code
             - has h1 tag with 'Oops'
         * Has 200 response code
         * Has a filled form with a submit button
             - check the value of inputs
             - count the submit button
 + POST
     * Unauthenticated:
         - 403 forbidden
     * Authenticated:
         * Given invalid id, directs to 404 page
             - response has 404 status code
             - has h1 tag with 'Oops'
         * Given incomplete data, has error
             - response has 400 status code
         * Given complete data:
             - Entry object with id updated
             - reponse has 302 status code
             - redirects to detail page
             - detail page now has updated information

##### delete - `/journal/{id:\d+}/delete-entry`
 + GET
     * Unauthenticated:
         - 403 forbidden
     * Authenticated:
         * Directs to 404 page
             - response has 404 status code
             - has h1 tag with 'Oops'
 + POST
     * Unauthenticated:
         - 403 forbidden
     * Authenticated:
         * Given invalid id, directs to 404 page
             - response has 404 status code
             - has h1 tag with 'Oops'
         * Given valid id:
             - Entry object with id is deleted
             - response has 302 code
             - redirects to home page
             - home page now does not have the entry
             - can no longer access the detail page of the entry

##### login - `/login`
 - GET
     + Unauthenticated:
         * response has 200 status code
         * form for username and password
     + Authenticated:
         * response has 302 code
         * redirects to home page
         * user is still authenticated
         * home page still has logout button and create button
 - POST
     + Unauthenticated:
         * Given incomplete data, has error
             - response has 400 status code
         * Given complete incorrect data
             - response has 200 status code
             - page now has error alert div
         * Given complete correct data
             - response has 302 status code
             - redirects to home page
             - home page now has logout avaiable
             - user now has auth_tkt cookie
     + Authenticated:
         * reponse has 302 code
         * redirects to home page
         * user is still authenticated
         * home page still has logout button and create button

##### logout - `/logout`
 - Unauthenticated:
     + 403 forbidden
 - Authenticated:
     + response has 302 status code
     + removed the auth_tkt cookie
     + redirects to the home page
     + home page has login button and no logout button
