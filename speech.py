import subprocess

def say(dialogue):
    parts = []
    while (dialogue != ''):
        if (len(dialogue) <= 100):
            parts.append(dialogue)
            dialogue = ''
        else:
            chars = dialogue[:100]
            parts.append(chars[:chars.rfind(' ')])
            dialogue = dialogue[chars.rfind(' '):]
    for x in range(len(parts)):
        #Send google 100 char parts
        e = 'echo ' + parts[x] + ' | xxd -ps | tr -d \'\n\' | sed \'s/\(..\)/%\\1/g\''
        sed = subprocess.Popen(e, stdout=subprocess.PIPE, shell=True)
        url, junk = sed.communicate()
        subprocess.call(["mpg123", "-q", 'http://translate.google.com/translate_tts?tl=en&q='+url])
