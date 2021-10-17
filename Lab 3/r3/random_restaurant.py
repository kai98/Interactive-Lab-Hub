from time import sleep
import qwiic_button as button
import miniPiTFT as screen
import text2speech as t2s
import speech2text as s2t
from text2speech import speak, speak_break
import restaurant_info as info
import math
import random

meals = ['breakfast', 'lunch', 'dinner']
restaurants = info.Restaurants

def Listen(wordlist):
    screen.text_bottom("[Listening...]")
    button.LED(2)
    # Recording for t seconds. 
    result = s2t.vosk(wordlist)
    button.LED(0)
    screen.text_bottom("[Processing...]")
    sleep(0.2)
    return result

def kick_off():
    screen.clear()
    screen.text_top("Random Restaurant")
    screen.text_bottom("Press to Start")
    button.LED(2)

    speak("Hi, I am Random Restaurant Machine")
    speak_break()
    while True:
        if button.isPressed():
            button.LED(0)
            meal = meal_section()
            print(meal)
            res = restaurant_section()
            print(res)
            loc, loc_full = location_section(res)
            print(loc)
            reminder_section(meal, res, loc, loc_full)
            print(meal, res, loc)

        sleep(0.05)

def reminder_section(meal, res, loc, loc_full):
    sleep(1)
    speak("Generate Reminder?")
    screen.text_top("Generate Reminder? ")
    screen.text_bottom("Press to Generate")
    button.LED(2)

    while True:
        if button.isPressed():
            button.LED(0)
            screen.clear()
            screen.text_center("Reminder")
            speak("Reminder Generating")
            speak(res + " for " + meal)
            speak(info.describe(res))
            speak(", location is: " + loc_full)        
            break
        sleep(0.05)
    reminder_summary(meal, res, loc)

def reminder_summary(meal, res, loc):
    page = 0
    reminder_page(meal, res, loc, page)
    button.LED(2)
    while True:
        if screen.is_A() and page == 1:
            page = 0
            reminder_page(meal, res, loc, page)
        if screen.is_B() and page == 0:
            page = 1
            reminder_page(meal, res, loc, page)
        if button.isPressed():
            button.LED(0)
            kick_off()
            return
        sleep(0.1)


def reminder_page(meal, res, loc, i):
    if i == 0:
        screen.clear()
        screen.text_top("Having " + meal + " at")
        screen.text_bottom(res)
    if i == 1:
        screen.clear()
        screen.text_top(loc)
        dist = info.Distances[res]
        screen.text_bottom(dist)

def meal_section():
    # Meal Section
    intro=True
    meal = which_meal(intro)
    while not meal:
        speak("Sorry, can you repeat again.")
        intro=False
        meal = which_meal(intro)
    screen.text_bottom(meal)
    sleep(2)
    return meal

def restaurant_section():
    # Restaurant Section
    intro=True
    restaurant = which_restaurant(intro)
    while not restaurant:
        speak("OK, Let me try again.")
        intro=False
        restaurant = which_restaurant(intro)
    screen.text_top("Selected")
    screen.text_bottom(restaurant)
    return restaurant

def location_section(restaurant):
    loc = info.Locations[restaurant]
    loc_full = info.Location_Full[restaurant]
    screen.text_top("Location")
    screen.text_bottom(loc)
    speak("location is: " + loc_full)
    return loc, loc_full


def which_meal(intro):
    screen.clear()
    screen.text_top("Which Meal?")

    if intro:
        speak("Which meal would you like to have?")
        speak("Breakfast, Lunch or Dinner")

    neutral = ["would", "like"]
    wordlist = meals + neutral
    keywords = Listen(wordlist)
    for w in meals:
        if w in keywords:
            return w
    return None

def which_restaurant(intro):
    screen.clear()
    screen.text_top("Which Restaurant?")

    if intro:
        speak("Randomly selecting a nearby restaurant")
    res = select_restaurant()
    screen.text_bottom(res + "?")
    speak("how about " + res)
    speak_break(0.2)
    speak(info.describe(res))

    positive = ["yes", "sure", "yep", "good", "great", "like", "perfect", "favourite"]
    negative = ["no", "sorry", "nah", "another", "nope", "maybe"]
    neutral = ["sounds", "food", "let", "us"]


    wordlist = positive + negative + neutral
    keywords = Listen(wordlist)
    print(keywords)
    positive_count = 0

    for w in positive:
        if w in keywords:
            positive_count+=1
    
    for w in negative:
        if w in keywords:
            positive_count-=1
    if positive_count > 0:
        return res
    return None


def select_restaurant():
    n = len(restaurants)
    rand_i = math.floor(n * random.random())
    restaurant = restaurants[rand_i]
    return restaurant


button.LED(0)
kick_off()
button.LED(0)