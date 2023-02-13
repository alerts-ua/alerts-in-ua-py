from alerts_in_ua import __version__
class UserAgent:
    @staticmethod
    def get_user_agent():
        return f"aiu-py-client/{__version__} (+https://alerts.in.ua)"