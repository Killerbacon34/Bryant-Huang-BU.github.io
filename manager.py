def manager(id):
    return '''<html>
   <body>
      <form action = "http://localhost:5000/manager" method = "get">
          <h2>Results for ''' + id + ''':</h2>
      </form>
   </body>
</html>'''