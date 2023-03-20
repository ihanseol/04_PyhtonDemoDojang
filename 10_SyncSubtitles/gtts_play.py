from gtts import gTTS
from playsound import playsound

comment = "제 블로그에 온것을 환영 합니다"

comment_to_voice = gTTS(text=comment, lang="ko")
comment_to_voice.save("test_ko.mp3")

comment_to_voice = gTTS(text=comment, lang="en")
comment_to_voice.save("test_en.mp3")

comment_to_voice = gTTS(text=comment, lang="fr")
comment_to_voice.save("test_fr.mp3")

playsound("test_ko.mp3")
playsound("test_en.mp3")
playsound("test_fr.mp3")