class CRMDatabaseRouter:
    """
    Database router to direct CRM models to separate database
    """
    
    crm_apps = {'artisan_crm'}
    crm_models = {
        'customerprofile', 'tag', 'leadstage', 'interaction', 
        'campaign', 'customertag', 'lead'
    }
    
    def db_for_read(self, model, **hints):
        """Suggest the database to read from"""
        if model._meta.app_label in self.crm_apps:
            return 'crm_db'
        return None
    
    def db_for_write(self, model, **hints):
        """Suggest the database to write to"""
        if model._meta.app_label in self.crm_apps:
            return 'crm_db'
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        """Allow relations if models are in the same app"""
        db_set = {'default', 'crm_db'}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure that CRM models get created on the right database"""
        if app_label in self.crm_apps:
            return db == 'crm_db'
        elif db == 'crm_db':
            return False
        return None