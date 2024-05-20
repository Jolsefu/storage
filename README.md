# STORAGE
#### Video Demo: https://youtu.be/NX46sN7ECWE
#### Description: Storage is a web application, solely made to help people store items they should remember securely in the web. You can provide a label and description for each item and store it in your storage as your own. It aims to help and store complex passwords or other important items wherein no human should be able to remember easily.
## FILES
#### Python files:
##### `app.py`: Contains 8 functions called `index`, `create`, `edit`, `delete`, `register`, `login`, `change_password`, and `logout`. The `index` function makes displaying all the items in the home page possible. The `create`, `edit`, and `delete` functions makes manipulating items, as their names suggests, possible. Lastly, `register`, `login`, `change_password`, and `logout` performs basic account features for the web application.
##### `helpers.py`: Contains `login_required`, `error`, and `success` functions. The `login-required` function requires the user to be logged in before accessing decorated app routes. The `error`, and `success` flashes messages, either error or success messages as the name suggests, to the passed route.
#### SQL Database:
##### `storage.db`: Contains a `users`, and an `items` table.
##### `users`: The `users` table has 3 columns, `id INTEGER`, `username TEXT NOT NULL`, and `hash TEXT NOT NULL`. The `id` column is a `PRIMARY KEY` that stores the unique `id` of the user. The `username` column stores the unique `username` of the user. Lastly, the `hash` column stores the hashed password (for security) of the user.
##### `items`: The `items` table has 4 columns, `id INTEGER`, `user_id INTEGER`, `label TEXT NOT NULL`, `description TEXT NOT NULL`. The `id` column is a `PRIMARY KEY` that stores the unique `id` of the item. The `user_id` column is a `FOREIGN KEY` that references the `id` column of the `users` table. The `label` column stores the label text. Lastly, The `description` column stores the description text.
#### Templates:
##### `layout.html`: Contains the layout for all of the html files `(e.g.,Bootstrap,CSS,JS,navbar,etc.)`.
##### `login.html`: Contains a form for the user to log in.
##### `register.html`: Contains a form for the user to register in, if they don't have an account yet.
##### `logout.html`: Contains a form for the user to change their password.
##### `index.html`: Contains a table that makes displaying all the items, owned by the user, a lot more user friendly.
##### `create.html`: Contains a form for the user to create/add an item to their own storage.
##### `edit.html`: Contains a table with the item's label and description as inputs for the user to edit.
##### `delete.html`: Contains a table with checkboxes per item, when checked and submitted it removes the item from the user's storage.
#### Static:
##### `icon.png`: Serves as the icon for the Storage web application.
##### `styles.css`: Contains all the aesthetics for the Storage web application.
##### `script.js`: Contains one basic function, `selectAll(source)`, that makes the `Select All` checkbox in the `delete.html` possible.