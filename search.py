def search_page(name, year):
    return '''<html>
   <body>
      <form action = "http://localhost:5000/results" method = "get">
          <h2>Results for ''' + name + ' in ' + year + ''':</h2>
      </form>
   </body>
</html>'''