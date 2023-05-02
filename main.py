from datetime import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha


engine = pyttsx3.init()
voice = engine.getProperty("voices")
engine.setProperty("voice", voice[0].id)
activationWord = 'computer'

wk = wikipedia

Chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register("chrome",None, webbrowser.BackgroundBrowser(Chrome_path))

appId = 'XXX7PE-2PTGJP696K'
wolframClient = wolframalpha.Client(appId)


def speak(text,rate =120):
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()


def parseCommand():
    listener = sr.Recognizer()
    print('Listening for commend')

    with sr.Microphone() as source:
        listener.pause_threshold = 2
        input_speech = listener.listen(source)


    try:
        print("Recognizing speech .." )
        query = listener.recognize_google(input_speech , language='en_gb')
        print(f'The input speech was:{query}')

    except Exception as excepttion:
        print(" Error i did not quite catch that")
        speak("This error i did not quite catch that")
        print(excepttion)
        return 'none'


    return query



def search_wikipedia(query = ""):
    
    searchResults = wk.search(query)
    if not searchResults:
      print("No wikipedia result")
      return "No result received"
    try:
        wikiPage = wk.page(searchResults[0])

    except wk.DisambiguationError as error :
        wikiPage = wk.page(error.options[0])

    print(wikiPage.title)
    wikiSummary = str(wikiPage.summary)
    return wikiSummary

def listOrict(var):
    if isinstance(var, list):
        return var[0]['plaintext']
    
    else:
        return var['plaintext']

def search_wolframalph(query = ' '):
    responese = wolframClient.query(query)


    if responese['@success'] == "false":
        return "Could not computer"
    
    else :
        result = ''
        pod0 = responese['pod'][0]
        pod1 = responese['pod'][1]

        if(('result' in pod1['@title'].lower()) or (pod1.get('@primary','false') == 'true')) or ('definition' in pod1['@title'].lower()):

            result = listOrict(pod1['subpod'])

            return result.split('(')[0]
        else:
            question = listOrict(pod0['subpod'])

            return question.split('(')[0]
        

            speak("computation Fail Query  ")
            return  search_wikipedia(question)




if __name__ == '__main__':
    speak("All systems nominal")

    while True:
        query = parseCommand().lower().split()

        if query[0] == activationWord:
            query.pop(0)

            if query[0] == "say":
                if "hello" in query :
                    speak("Greeting, all.")

                else:
                    query.pop(0)
                    speech = ' '.join(query)
                    speak(speech)

            if query[0] == "go" and query[1] == "to":
                speak("Opening..")
                query = ' '.join(query[2:])       
                webbrowser.get("chrome").open_new(query)



            if query[0] == "wikipedia":
                query=' '.join(query[1:])
                speak("Quarying the universal databank.")
                
                speak(search_wikipedia(query))
 
            if query[0] == "compute" or  query[0] == "computer" :
                query = ' '.join(query[1:])
                speak("Computing")

                try:
                       result = search_wolframalph(query)
                       speak(result)

                except: 
                    speak("Unable to compute.")



            if query[0] == 'log':
                speak("ready to record your note")
                newNote = parseCommand().lower()
                new = datetime.new().strftime('%Y-%m-%d-%H-%M-%S')
                with open('/note.txt' % new, w) as newfile:
                     newfile.write(newNote)
                speak('Note written')


            if query[0] == 'exit':
                speak('GoodBye')
                break