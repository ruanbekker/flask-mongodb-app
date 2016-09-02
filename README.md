## WebApp with Flask and MongoDb

App is still in progress. Basic profile web app, to test the functionality of Python Flask and MongoDb.

### Overview:

Adding, Listing and Querying user profiles based on `userid`, `name`, `job`

### Functionality:

- Adding users via:

```
/add/<userid>/<name>/<surname>/<age>/<job>
```

- List All Users:

```
/get/
```

- Query users based on their userid's:

```
/get/<userid>
```

- Query users based on their names:

```
/get/name/<name>
```

- Query users based on their jobs:

```
/get/job/<job>
```

### Notes:

2016.08.27 (Latest):

Added search functionality, still to add interface to add users without passing the url manually
