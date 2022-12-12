from PIL import Image, ImageFont, ImageDraw
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

def send_Mail(name,email,subject, body, attachment):
    message = Mail(
    from_email = os.environ.get('SENDGRID_SENDER_EMAIL'),
    to_emails = (email),
    subject=subject,
    html_content=body)
    message.add_attachment(attachment)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
    

FONT_FILE = ImageFont.truetype(r'font/GreatVibes-Regular.ttf', 180)

FONT_COLOR = "#ffffff"

template = Image.open(r'c.png')
WIDTH, HEIGHT = template.size

def make_card(name,email):
    '''Function to save cards as a .png file'''
    image_source = template.copy()
    draw = ImageDraw.Draw(image_source)

    name = name.lower()
    name = name.split()
    name = ' '.join([x.capitalize() for x in name]);
    global FONT_FILE
    if len(name) > 10:
        FONT_FILE = ImageFont.truetype(r'font/GreatVibes-Regular.ttf', 120)
    else:
        FONT_FILE = ImageFont.truetype(r'font/GreatVibes-Regular.ttf', 150)
    
    namewidth, nameheight = draw.textsize("Dear, "+name, font=FONT_FILE)
    draw.text(((WIDTH-namewidth)/2,  380), "Dear, "+name, fill=FONT_COLOR, font=FONT_FILE)
    
    image_source.save("./out/" + name +".png")
    print('Saving Cards of:', name)        
    return image_source
import glob
images = [img for img in glob.glob("out/*.png")]

if __name__ == "__main__":

    f = open('list.txt', 'r')

    lines = f.readlines()

    for person in lines:
        try:
            name, email = person.split(',')
            image_source=make_card(name,email.strip())
            send_Mail(name,email, "Happy New Year.", "A special HNY card for you!", image_source)

        except Exception as e:
            print(e)
            print('Error in:', person)

    print(len(lines), "cards done.")
    

