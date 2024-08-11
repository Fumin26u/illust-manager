class MissingParameterException(Exception):
    """パラメータが不足していることを示す例外の基底クラス"""
    
    def __init__(self, parameter_name, message=None):
        if message is None:
            message = f'MISSING PARAMETER: {parameter_name}'
        self.message = message
        super().__init__(self.message)

class NoQueryProvidedException(MissingParameterException):
    def __init__(self, message=None):
        super().__init__('query', message)

class NoPlatformProvidedException(MissingParameterException):
    def __init__(self, message=None):
        super().__init__('platform', message)

class NoTimestampProvidedException(MissingParameterException):
    def __init__(self, message=None):
        super().__init__('timestamp', message)

class NoImageProvidedException(MissingParameterException):
    def __init__(self, message=None):
        super().__init__('image', message)
        
class NoUserInfoProvidedException(MissingParameterException):
    def __init__(self, message=None):
        super().__init__('user_info', message)
        
class NoDetectedException(Exception):
    """所定の値が検出されなかったことを示す例外の基底クラス"""
    
    def __init__(self, parameter_name, message=None):
        if message is None:
            message = f'{parameter_name} IS NOT DETECTED'
        self.message = message
        super().__init__(self.message)    
        
class NoDirectoryDetectedException(NoDetectedException):
    def __init__(self, message=None):
        super().__init__('directory', message)
