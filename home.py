def home_page(name):
    return '''<html>
   <body>
      <form action = "http://localhost:5000/results" method = "get">
          <h1>Welcome ''' + name + '''!</h1>
          <p>Enter team name:</p>
          <p><input type = "text" name = "nm" /></p>
          <p>Enter year:</p>
          <p><input type = "text" name = "year" /></p>
          <p><input type = "submit" value = "submit" /></p>
      </form>
   </body>
</html>'''