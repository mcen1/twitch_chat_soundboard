This will allow users in your chat to play sound clips on your computer while you stream, like a morning zoo crew DJ or sound board! Wow!

When they write "!sound file" it'll play file.mp3 in the current directory.

Edit the config.txt as follows:

Leave host the same
Leave port alone
channel is your twitch username prefaced by the # sign
username is your twitch username
oauth token: this one's a doozy. Go to https://twitchapps.com/tmi/ and connect it with your twitch account. It'll generate an oauth token.
Put that oauth token here, including the oath: part, ie "oauth:knfjdfnhjkdfnhjkdfnhjkdf"

I'm a lazy coder so this will play a sound of anything after !sound in your chat, .mp3. So people can do "!sound 1" and it'll play 1.mp3.
People could also theoretically do "!sound diarrhea" and it'll play "diarrhea.mp3". I tried to limit the impact by removing dots and slashes
from user input.