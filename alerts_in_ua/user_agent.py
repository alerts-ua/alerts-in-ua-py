from alerts_in_ua import __version__
class UserAgent:
    @staticmethod
    def get_user_agent(token: str = None):
        base_agent = f"aiu-py-client/{__version__} (+https://alerts.in.ua)"
        
        if token and len(token) >= 5:
            token_prefix = token[:5]
            return f"{base_agent} app:{token_prefix}"
        
        return base_agent