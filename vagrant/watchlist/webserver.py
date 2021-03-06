from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
#cgi is common gateway interface
import cgi

"""
The follow is all the information for sqlalchemy
"""
from sqlalchemy import create_engine
#we need sessionmaker in order to perform queries
from sqlalchemy.orm import sessionmaker
#importing previously made files
from database_setup import Base, Restaurant, MenuItem
#creating sqlite3 engine
engine = create_engine('sqlite:///restaurantmenu.db')
#connecting to db file
Base.metadata.bind = engine
#starting session with engine
DBSession = sessionmaker(bind = engine)
#creating instance of DBsession
session = DBSession()
"""
"""

class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        #splits path by ? so that url parameters are handled
        p = self.path.split("?")
        path = p[0]
        URLparams = {}
        if len(p) > 1:
            URLparams = p[1].split("&")
        #the following path will just list all of the restaurants
        if path == "/restaurants":
            #status code 200 indicates successful get request
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            #create the restaurants to contain all of the restaurants in the db
            restaurants = session.query(Restaurant).all()

            message = ""
            message += "<html><title>Restaurants</title><body>"
            message += "<p>If you'd like, you may create a <a href='/restaurants/new'>new</a> Restaurant</p>"
            for restaurant in restaurants:
                message += "<br>"
                message += "<br>"
                message += "Restaurant Name: %s" % restaurant.name
                message += "<br>"
                message += "<a href='/restaurants/edit?%s'>Edit</a>" % restaurant.id
                message += "<br>"
                message += "<a href='/restaurants/delete?%s'>Delete</a>" % restaurant.id
                message += "<br>"
                message += "<br>"
            self.wfile.write(message)
            return
        elif self.path == "/restaurants/new":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            #create the restaurants to contain all of the restaurants in the db
            restaurants = session.query(Restaurant).all()

            message = ""
            message += "<html><title>Create</title><body>"
            message += '''<form method='Post' enctype='multipart/form-data' action='/restaurants/new'>
            <h2>What would you like the name of the new Restaurant to be?</h2>
            <input name='name' type='text' >
            <input type='submit' value='Submit'>
            </form>
            '''

            self.wfile.write(message)
            return
        #we can't use self.path because we are passing a URL param
        elif path == "/restaurants/edit":

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            #so python doesn't complain at undefined object
            name = ''

            if URLparams:
                #if there is one parameter, it is the id of the post to edit
                if len(URLparams) == 1:
                    id = URLparams[0]

                else:
                    self.send_error(403, 'Not Accessible: %s' % self.path)


            #the following form will send two post params
            #one param for id
            #one param for the name
            message = ""
            message += "<html><title>Update</title><body>"
            message += '''<form method='Post' enctype='multipart/form-data' action='/restaurants/edit'>
            <h2>What would you like the name of the new Restaurant to be now?</h2>
            <input name='id' type='hidden' value='%s'>
            <input name='name' type='text' >
            <input type='submit' value='Submit'>
            </form>
            ''' % id

            self.wfile.write(message)
            return
        elif path == "/restaurants/delete":

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            #the following line is to avoid an undefined error
            id = ''
            #if there is one parameter, it is the id of the post to edit

            #right now, this is the only url parameter that we accept
            if URLparams:
                if len(URLparams) == 1:
                    id = URLparams[0]
                else:
                    self.send_error(403, 'Not Accessible: %s' % self.path)
            message = ""
            message += "<html><title>Delete</title><body>"
            message += '''<form method='Post' enctype='multipart/form-data' action='/restaurants/delete'>
            <h2>Are you sure that you want to delete this restaurant?</h2>
            <input name='id' type='hidden' value='%s'>
            <input name='response' type='radio' value='yes'>Yes
            <input name='response' type='radio' value='no'>No
            <input type='submit' value='Submit'>
            </form>
            ''' % id


            self.wfile.write(message)
            return
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        if self.path == "/restaurants/new":
            try:

                #status code 301 indicates successful get request
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                #ctype is main values and pdict are a dictionary of parameters that we send
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                #if the main value is form-data
                if ctype == 'multipart/form-data':
                    #use the fields variable to parse out the dictionary of parameters that we've sent
                    #messagecontent will be an array
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('name')
                output = ""
                output += "<html><body>"
                output += " <h2>Here is the name of your restaurant: </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]
                output += "Go back to <a href='/restaurants'>restaurants</a> to view it"
                restaurant = Restaurant(name = messagecontent[0])
                #addming new item to staging area
                #TODO take out url input chars (ex: bill burger is sent in the url as bill+burger)
                session.add(restaurant)
                #commiting changes to database
                session.commit()
                self.wfile.write(output)
                print output
            except:
                pass
        elif self.path == "/restaurants/edit":
            try:

                #status code 301 indicates successful get request
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                #ctype is main values and pdict are a dictionary of parameters that we send
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                #if the main value is form-data
                if ctype == 'multipart/form-data':
                    #use the fields variable to parse out the dictionary of parameters that we've sent
                    #messagecontent will be an array
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('id')
                    name = fields.get('name')
                    id = fields.get('id')
                output = ""
                output += "<html><head><title>Update successful</title></head><body>"
                output += " <h2>Here is the new name of your restaurant: </h2>"
                output += "<h1> %s </h1>" % name[0]
                output += "Go back to <a href='/restaurants'>restaurants</a> to view it"
                #update the resturant
                restaurant = session.query(Restaurant).filter_by(id = id[0]).one()
                if name:
                    restaurant.name = name[0]
                    session.add(restaurant)
                    session.commit()
                self.wfile.write(output)
                print output
            except:
                pass
        elif self.path == "/restaurants/delete":
            try:

                #status code 301 indicates successful get request
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                #ctype is main values and pdict are a dictionary of parameters that we send
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                #if the main value is form-data
                if ctype == 'multipart/form-data':
                    #use the fields variable to parse out the dictionary of parameters that we've sent
                    #messagecontent will be an array
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('id')
                    response = fields.get('response')
                    id = fields.get('id')
                output = ""
                output += "<html><head><title>Delete successful</title></head><body>"
                if response[0] =='yes':
                    restaurant = session.query(Restaurant).filter_by(id = id[0]).one()
                    session.delete(restaurant)
                    session.commit()
                    output += " <h2>This restaurant has been deleted</h2>"
                elif response[0] == 'no':
                    output += " <h2>This restaurant has not been deleted</h2>"
                output += "Go back to <a href='/restaurants'>restaurants</a> to view it"
                self.wfile.write(output)
                print output
            except:
                pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        #serve_forever will keep there server constantly listening
        server.serve_forever()
    #triggered with ctrl+c
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
