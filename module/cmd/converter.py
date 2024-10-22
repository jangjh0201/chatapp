class Converter:
    def __init__(self):
        pass

    def __str__(self):
        return self.__class__.__name__

    def convert(self, command_list):
        response, commands = "", []
        if "커피" in command_list or "아메리카노" in command_list:
            response, commands = "커피를 만들어 드릴게요.", ["커피", "만들기"]
        elif "차" in command_list or "캐모마일" in command_list:
            response, commands = "캐모마일 차를 만들어 드릴게요.", ["차", "만들기"]
        elif "아이스티" in command_list:
            response = "아이스티를 만들어 드릴게요.", ["아이스티", "만들기"]
        elif "출근" in command_list:
            response, commands = "출근 준비를 도와드릴게요.", ["출근", "준비"]
        else:
            response, commands = "이해하지 못했어요. 다시 말씀해 주세요.", []

        return response, commands
