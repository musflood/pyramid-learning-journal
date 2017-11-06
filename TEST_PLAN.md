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
     * Has all journal entries
         - count the cards

##### detail - `/journal/{id:\d+}` 
 + GET
     * Given invalid id, directs to 404 page
         - response has 404 status code
         - has h1 tag with 'Oops'
     * Has one journal enry
         - count the cards
         - title is correct

##### create - `/journal/new-entry`
 + GET
     * Has an empty form with a submit button
         - check value of inputs
         - count the submit buttons 
 + POST
     * Given incomplete data, reloads page
         - response has 400 status code
         - retains info entered on page
     * Given complete data:
         - new Entry object created
         - reponse has 302 status code
         - redirects to home page
         - home page now lists new entry
         - should be able to access the new entry detail page
         - detail page has actual details of entry

##### edit - `/journal/{id:\d+}/edit-entry`
 + GET
     * Given invalid id, directs to 404 page
         - response has 404 status code
         - has h1 tag with 'Oops'
     * Has a filled form with a submit button
         - check the value of inputs
         - count the submit button
 + POST
     * Given invalid id, directs to 404 page
         - response has 404 status code
         - has h1 tag with 'Oops'
     * Given incomplete data, reloads page
         - response has 400 status code
         - retains info entered on page
     * Given complete data:
         - Entry object with id updated
         - reponse has 302 status code
         - redirects to detail page
         - detail page now has updated information

##### delete - `/journal/{id:\d+}/delete-entry`
 + GET
     * Directs to 404 page
         - response has 404 status code
         - has h1 tag with 'Oops'
 + POST
     * Given invalid id, directs to 404 page
         - response has 404 status code
         - has h1 tag with 'Oops'
     * Given valid id:
         - Entry object with id is deleted
         - response has 302 code
         - redirects to home page
         - home page now does not have the entry
         - can no longer access the detail page of the entry
