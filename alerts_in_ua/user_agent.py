from alerts_in_ua import __version__
class UserAgent:
    @staticmethod
    def get_user_agent():
        return f"Alerts.in.ua API Library v{__version__} (compatible; alerts.in.ua/{__version__}; +https://alerts.in.ua)"