class StreamingCallbacks:
    @staticmethod
    def default_callback(content, full_response):
        """Default streaming callback"""
        print(content, end='', flush=True)
    
    @staticmethod
    def improvement_callback(content, full_response):
        """Streaming callback for improvements"""
        print(content, end='', flush=True)
