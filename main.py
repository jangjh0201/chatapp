from bot import cmd_bot, stt_bot

if __name__ == "__main__":
    stt_bot = stt_bot.STTBot()
    sentence = stt_bot.listen()

    cmd_bot = cmd_bot.CMDBot()
    command = cmd_bot.get_command(sentence)
    print(command)
