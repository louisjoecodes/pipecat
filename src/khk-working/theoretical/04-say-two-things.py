from dailyai.services.transport.DailyTransport import DailyTransportService
from dailyai.services.llm.AzureLLMService import AzureLLMService
from dailyai.services.tts.AzureTTSService import AzureTTSService

transport = None
llm = None
tts = None


def main():
    global transport
    global llm
    global tts

    transport = DailyTransportService()
    llm = AzureLLMService()
    tts = AzureTTSService()
    mic = transport.create_audio_queue()
    tts.set_output(mic)
    llm.set_output(tts)

    transport.on("error", lambda e: print(e))
    transport.on("joined-meeting", say_two_things)
    transport.start()


def say_two_things():
    # queue two pieces of speech: one specified as a text literal,
    # and one generated by an llm
    tts.run_tts("My friend the LLM is now going to tell a joke about llamas.")
    llm.run_llm("tell me a joke about llamas")
    transport.on("audio-queue-empty", shutdown)


def shutdown():
    transport.stop()
    tts.close()