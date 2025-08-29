class SettingsProxy:
    """Proxy that auto-saves when settings are modified"""
    def __init__(self, settings_manager):
        self._settings = settings_manager
    
    def __getitem__(self, key):
        return self._settings.get(key)
    
    def __setitem__(self, key, value):
        self._settings.set(key, value)
    
    def __contains__(self, key):
        return key in self._settings.settings
    
    def get(self, key, default=None):
        return self._settings.get(key, default)
    
    def setdefault(self, key, default):
        """Get key value or set and return default if key doesn't exist"""
        current_value = self._settings.get(key)
        if current_value is None:
            self._settings.set(key, default, quiet=True)
            return default
        return current_value
    
    def update(self, other):
        self._settings.update(other)
