# Custom database router for Django to control database operations for specific apps.
class MyDatabaseRouter:
    # Determine the database for read operations (SELECT queries).
    def db_for_read(self, model, **hints):
        # Check if the model belongs to the 'pages' app.
        if model._meta.app_label == 'pages':
            # Use 'mysql_db' database for 'pages' app models.
            return 'mysql_db'
        # Use the default database for other models.
        return 'default'

    # Determine the database for write operations (INSERT, UPDATE, DELETE).
    def db_for_write(self, model, **hints):
        # Check if the model belongs to the 'pages' app.
        if model._meta.app_label == 'pages':
            # Use 'mysql_db' database for 'pages' app models.
            return 'mysql_db'
        # Use the default database for other models.
        return 'default'

    # Allow relations (foreign keys, many-to-many) between objects from different databases.
    def allow_relation(self, obj1, obj2, **hints):
        # Always allow relations between objects from different databases.
        return True

    # Determine whether models from a specific app can be migrated to a particular database.
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Check if the app label is 'pages'.
        if app_label == 'pages':
            # Allow migration to 'mysql_db' database for 'pages' app models.
            return db == 'mysql_db'
        # Allow migration to the default database for other apps' models.
        return db == 'default'
