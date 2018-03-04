from azure.cognitiveservices.vision.customvision.training import training_api
from azure.cognitiveservices.vision.customvision.training.models import ImageUrlCreateEntry
from tkinter import *

from PIL import Image, ImageTk
from urllib.request import *
from io import BytesIO

from azure.cognitiveservices.vision.customvision.prediction import prediction_endpoint
from azure.cognitiveservices.vision.customvision.prediction.prediction_endpoint import models
import webbrowser

def evalPic(test_img_url):

    # Now there is a trained endpoint that can be used to make a prediction
    training_key = "9f84608619f943e1abd429dce654f187"
    prediction_key = "30e812af3b4e4122a837e5aac8b61218"
    
    predictor = prediction_endpoint.PredictionEndpoint(prediction_key)
    
    
    
    #test_img_url = str(input("Enter an image url: "))
    results = predictor.predict_image_url("76e20514-28a8-4028-85fe-184acfafdb3c", url=test_img_url)
    
    # Alternatively, if the images were on disk in a folder called Images alongside the sample.py, then
    # they can be added by using the following.
    #
    # Open the sample image and get back the prediction results.
    # with open("Images\\test\\test_image.jpg", mode="rb") as test_data:
    #     results = predictor.predict_image(project.id, test_data.read(), iteration.id)
    
    res = {"Good Quality" : "",
               "Bad Quality" : "",
               "Centered" : "",
               "Not Centered" : "",
               "Face Visible" : "",
               "Face Obscured" : "",
               "Good Lighting" : "",
               "Bad Lighting" : "" }
    
    
    # Display the results.
    for prediction in results.predictions:
       # print ("\t" + prediction.tag + ": {0:.2f}%".format(prediction.probability * 100))
        if prediction.tag == "goodquality":
            res["Good Quality"] = prediction.probability*100
        elif prediction.tag == "badquality":
            res["Bad Quality"] = prediction.probability*100  
        elif prediction.tag == "notcentered":
            res["Not Centered"] = prediction.probability*100
        elif prediction.tag == "centered":
            res["Centered"] = prediction.probability*100
        elif prediction.tag == "facevisible":
            res["Face Visible"] = prediction.probability*100
        elif prediction.tag == "faceobscured":
            res["Face Obscured"] = prediction.probability*100  
        elif prediction.tag == "goodlighting":
            res["Good Lighting"] = prediction.probability*100  
        elif prediction.tag == "badlighting":
            res["Bad Lighting"] = prediction.probability*100  
        
    #print(res)
    
    print("Picture evaluation:")
    s1 = "Picture Evaluation: "
    score = 0
    print()
    
    if res["Good Quality"] > res["Bad Quality"]:
        val = res["Good Quality"]
        if val > 85:
            print ("Great Resolution")
            score+=25
            s2 = "Great Resolution"
        elif val > 15:
            print ("Good Resolution")
            score += 20
            s2 = "Good Resolution"
        else:
            print ("Decent Resolution")
            score += 15
            s2 = "Decent Resolution"
    else:
        print("Poor Image Quality")
        s2 = "Poor Image Quality"
    
         
    if res["Good Lighting"] > res["Bad Lighting"]:
        
        val = res["Good Lighting"]
        if val > 85:
            print ("Great Lighting")
            score+=25
            s3 = "Great Lighting"
        elif val > 15:
            print ("Good Lighting")
            score += 20
            s3 = "Good Lighting"
        else:
            print ("Decent Lighting")
            score += 15
            s3 = "Decent Lighting"
    else:
        print("Poor Lighting")
        s3 = "Poor Lighting"
    
        
    if res["Face Visible"] > res["Face Obscured"]:
        score += 25
        print ("Face is Visible")
        s4 = "Face is Visible"
    else:
        print("Face is obscured")
        s4 = "Face is Obscured"
        
    if res["Centered"] > res["Not Centered"]:
        score+=25
        print ("Good subject position in frame")
        s5 = "Good subject position in frame"
    else:
        print("Poor subject position in frame")
        s5 = "Poor subject position in frame"
        
    
    print()
    print()
    print("Total selfie score: ", score , "/100")
    
    
    return (s1,s2,s3,s4,s5,str(score))


if __name__ == '__main__': 
    root = Tk()
    root.title("AI Selfie Evaluator")
    root.geometry('800x800')
    
    root.bind('<q>', quit)
    ment = StringVar()
    e = Entry(root, width = 100)
    e.pack()
    
    
    e.focus_set()
    
    def newEntry():
        s1, s2, s3, s4, s5, scr = evalPic(e.get())
        
        URL = e.get()
        u = urlopen(URL)
        raw_data = u.read()
        u.close()
        
        im = Image.open(BytesIO(raw_data))
        im.resize((500,500))
        photo = ImageTk.PhotoImage(im)
        
        #label = Label(image=photo)
        label.image = photo
        label.config(image = photo)
        label.image = photo
        #label.config(height = 500, width = 500) 
        label.pack()
        
        #modify the score 
        scr = "Selfie score: " + scr + "/100"
        
        w1.config(text = s1, highlightthickness=1)
        w1.pack()
        w2.config(text = s2)
        w2.pack()
        w3.config(text = s3)
        w3.pack()
        w4.config(text = s4)
        w4.pack()
        w5.config(text = s5)
        w5.pack()        
        w6.config(text = scr)
        w6.pack()
        
    
    b = Button(root, text="Evaluate Image",   command = newEntry)
    b.pack()    
    
    #make 6 labels for the 6 things we need to print out
    w1 = Label(root, text = "", )   
    #w.place(x = 200, y = 700)
    w1.pack()
    w2 = Label(root, text = "", )
    w2.pack()
    w3 = Label(root, text = "", )
    w3.pack()
    w4 = Label(root, text = "", )
    w4.pack()
    w5 = Label(root, text = "", )
    w5.pack()    
    w6 = Label(root, text = "", )
    w6.pack()      
    
    #Want the image to change each time, so create the image here first with blank white
    URL = "https://i.imgur.com/fj81bxN.jpg"
    u = urlopen(URL)
    raw_data = u.read()
    u.close()
    
    im = Image.open(BytesIO(raw_data))
    im.resize((650,650))
    photo = ImageTk.PhotoImage(im)
    
    label = Label(image=photo)
    label.image = photo
    label.config(height = 650, width = 800) 
    label.pack()    
    
    
    root.mainloop()
    
    #text = e.get()
    #print(text)
    
    
   


