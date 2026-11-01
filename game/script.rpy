# The script of the game goes in this file.
# Declare characters used by this game. The color argument colorizes the
# name of the character.
define false = False
define true = True
define config.menu_include_disabled = true
default p = Character("[pname]")
define g = Character("Garlic Bread")
default dmpc = Character("[dname]", color = "#eec2ff")
# It's defaulted so it can change to be Avatar of the Garlic Bread and the color can change to #733b40 when it does that.
default dname = "Lily"
define r1 = Character("Alva")
define r2 = Character("Gwynedd")
define r3 = Character("Hoshi")
define unk = Character("???")
define t = Character("Teacher")
define dis = Dissolve(.5)
default pname = "Insert player name here."
default p1sub = ""
default p1obj = ""
default p1adj = ""
default p1pos = ""
default p1flex = ""
default p1genterm = ""
default term = 0
default day = 0
default termDay = 0
default noEep = 0.0
default eepNum = 0.0
default keyAnswer = ""
transform dying:
    linear 1.0 matrixcolor SaturationMatrix(0.0)
    #linear 1.0 matrixcolor SepiaMatrix()
    # Alternative to test if a sepia matrix makes the dying effect look better (It does not)
#default pronoun2sub = ""
#default pronoun2obj = ""
#default pronoun2adj = ""
#default pronoun2pos = ""
#default secondarypronouns = false
transform genpos:
    xalign 0.5
    yalign 0.125
transform lefpos:
    xalign 0
    yalign 0.125
transform ripos:
    xalign 1.0
    yalign 0.125
init python:
    def live2d_there(characterFold) -> bool:
        return renpy.loadable(f"Live2D/{characterFold}/{characterFold}.model3.json")
    def Live2Ds(*args, charFold, fallback = Placeholder(base = "girl", text="No Live2D"), fallback1 = Image(""),**kwargs):
        if renpy.has_live2d() and live2d_there(charFold):
            return Live2D(*args,**kwargs)
        else:
            if (fallback1 != Image("")):
                return fallback1
            else:
                return fallback
image bg_room = Placeholder("bg",text = "room")
image taskinator = "images/Taskbringer.png"
image gbr = "images/Garlic_Bread.png"
define fonty = "NotoSerifDisplay-VariableFont_wdth,wght.ttf"
define fontyit = "NotoSerifDisplay-Italic-VariableFont_wdth,wght.ttf"
init python:

    class Char:
        ima  = None
        taskNum = 0
        aff = 0.0
        idNum = ""
        name = " "
        genChooser = 120983736720298382937289
        roofWith = True
        def __init__(self, idNum, gen, name, filepath, folder, isL2D, isGenChangeable, canBib, bass, genChooser, customFallback = "noFall"):
            self.name = name
            self.idNum = idNum
            # Used as a unique identification number to differentiate between models of the same name
            self.filepath = filepath
            self.gen = gen
            # gen is a string that is "boy" or "girl"
            self.folder = folder
            self.bass = bass
            # usually .6, but can be customized
            self.alia = {"idle":"m01","scared":"m02","excited":"m03","pout":"m04","embarassed":"m05"}
            self.isL2D = isL2D
            self.customFallback = customFallback
            self.genChooser = genChooser
            if (isL2D):
                if (canBib):
                    self.alia["avf"]="bibac"
                if (isGenChangeable):
                    filem = filepath+"m"
                    filef = filepath+"f"
                    foldm = folder+"m"
                    foldf = folder+"f"
                    charm = Live2Ds(filem, charFold = foldm, fallback = Placeholder(base = "boy", text = self.name),base=self.bass,aliases = self.alia)
                    charf = Live2Ds(filef, charFold = foldf, fallback = Placeholder(base = "girl", text = self.name),base=self.bass,aliases = self.alia)
                    self.genChooser = renpy.random.random()*2
                    self.ima = ConditionSwitch(self.genChooser > 1, charf,True, charm)
                else:
                    self.ima = Live2Ds(self.filepath,charFold = self.folder, fallback = Placeholder(base = self.gen,text = self.name),base=self.bass, aliases = self.alia, )
            else:
                self.ima = self.filepath
        def taskHandler(self) -> str:
            response = ""
            match self.taskNum:
                case 0:
                    response = "Oh! Thanks for bringing me back there. I might've gone off on a whole rant or something and you would've just had to listen to me {font=NotoSerifDisplay-VariableFont_wdth,wght.ttf}keep on talking foreeeever!{/font}"
                case 1:
                    response = "Whoopsies! I did it again, didn't I? Silly me. Thanks for helping me keep myself in check!"
                case 2:
                    response = "I did it again, huh? Thanks, I guess..."
                case 3:
                    self.show("pout",genpos,"",False)
                    self.aff -= .01
                    response = "I'm starting to think you don't care about anything I'm saying..."
                case n if n>=4:
                    self.show("pout",genpos,"",False)
                    self.aff -= .02*(1+0.1*n)**(n-3)
                    response =  "Yeah, you definitely don't care about what I'm saying!"
            self.taskNum += 1
            return response
        def show(self,aliWanted,pos,wi,hasTrans):
            if (self.isL2D and live2d_there(self.folder)):
                nam = self.name + " " + aliWanted
                renpy.show(nam, at_list = [pos],what = self.ima,tag="char_"+self.idNum)
            else:
                renpy.show(self.name, at_list = [pos],what=self.ima,tag="char_"+self.idNum)
            if(hasTrans):
                renpy.with_statement(wi)
        def hide(self,wi,hasTrans):
        # seems to be kind of broken, probably best to add a scene after every instance of this to make sure it actually does what's intended.
            renpy.hide(self.name)
            # renpy.say(p,str(self.genChooser)) 
            # Used for testing if genChooser was working properly
            if(hasTrans):
                renpy.with_statement(wi,always=True)
define none = None
default aroaceRouteStarted = false
default gbRouteStarted = false

# The game starts here.

label start:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene bg_room
    # play music "audio/Main_BGM.wav"
    
    play music "Main_BGM.ogg"
    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.
    default dmp = Char("001","girl",dname,"Live2D/dmpc","dmpc",True, False,True,.6,2)
    default al = Char("002","", "Alva", "Live2D/al","al",True, True,False,.6,renpy.random.random()*2)
    default gw = Char("003","","Gwynedd","Live2D/gw","gw",True,True,False,.6,renpy.random.random()*2)
    default ho = Char("004","","Hoshi","Live2D/ho","ho",True,True,False,.6,renpy.random.random()*2)
    default gb = Char("005","","Garlic Bread","images/Garlic_Bread.png","Garlic_Bread",False,False,False,.6,-1)
    $ pname = renpy.input("What would you like to name your character?")
    $ p = Character(pname)
    default playerf = Char("006","girl",pname,"Live2D/Playerf","Playerf",True,False,True,.6,2, customFallback = "playerf.png")
    default fb = Transform("playerf.png", zoom = 0.6)
    $ playerf.ima = fb
    # temporary means by which to add a custom placeholder until I can figure out how to do that.
    default playerm = Char("007","boy",pname,"Live2D/Playerm","Playerm",True,False,True,.6,0)
    
    menu: 
        "What pronouns would you like to use for your character?"
        "She/her": 
            $ p1sub = "she"
            $ p1obj = "her"
            $ p1adj = "her"
            $ p1pos = "hers"
            $ p1flex = "herself"
        "He/him":
            $ p1sub = "he"
            $ p1obj = "him"
            $ p1adj = "his"
            $ p1pos = "his"
            $ p1flex = "himself"
        "They/them":
            $ p1sub = "they"
            $ p1obj = "them"
            $ p1adj = "their"
            $ p1pos = "theirs"
            $ p1flex = "themselves"
        "Other (A set of pronouns not included in the above options)":
            $ p1sub = renpy.input("What is the subjective form? (for example she)")
            $ p1obj = renpy.input("What is the objective form? (for example her as in 'I knew it was her!')")
            $ p1adj = renpy.input("What is the possessive adjective? (for example her as in 'It was her game.')")
            $ p1pos = renpy.input("What is the possessive form? (for example hers as in 'The victory was hers')")
            $ p1flex = renpy.input("What is the reflexive form? (for example herself)")
    menu:
        "What kind of gendered terms do you want to be used for your character?"
        "Feminine(girl, woman, etc.)":
            $ p1genterm = "girl"
        "Masculine(boy, man, etc.)":
            $ p1genterm = "boy"
        "Neutral(human, person, etc.)":
            $ p1genterm = "person"
    menu:
        "An example sentence using your chosen character name and pronouns will be displayed shortly. Please select whether it correctly uses your entered pronouns and name."
        "Okay":
            pass
    menu: 
        "'[pname] was quite confident in [p1flex], as [p1sub] believed that nothing could hurt [p1obj] on account of [p1adj] powerful weaponry. Being quite the intelligent [p1genterm], [p1sub] knew better than to count [p1adj] chickens before they hatched, but the game seemed all but [p1pos]. Or so [p1sub] thought...'"
        "Yes":
            jump cselect
        "No":
            jump start
label cselect:
    $ playerf.show("idle",lefpos,dis,true)
    "This is the first of the player character options."
    $ playerm.show("idle",ripos,dis,true)
    "This is the second."
    $ playerm.hide(dis, true)
    default player = Char("000","bg",pname,"Live2D/Player","Player",True,False,True,.6,2)
    menu:
        "Which player character do you prefer?"
        "1(Left)":
            $ player = playerf
            
        "2(Right)":
            $ player = playerm
    jump begin
label begin:
    image bg_hallway = Placeholder("bg","Hallway")
    # placeholder for until the hallway asset is made.
    scene bg_hallway
    $ player.hide(dis,true)
    $ dmp.show("idle",genpos,dis,True)
    
    dmpc "Hi there, [pname]!"
    dmpc "Welcome to the Laventhyrian Institute for Secondary Education! This is the leading institution for the education of the citizens of Laventhyria."
    dmpc "It is primarily attended by the Laventhyrian nobility. In some exceptional cases, those without a noble background have been admitted, but that is exceedingly rare."
    dmpc "But enough about the school! I'm [dname]. It's very nice to meet you, [pname]! "
    $ dmp.show("idle",ripos,dis,True)
    menu:
        "Likewise.":
            $ dmp.show("idle",genpos,dis,True)
            dmpc "Short and to the point, I see! I'm sure you'll fit right in here!"
        "I, too, am eager to begin my studies at this institution.":
            $ dmp.show("idle",genpos,dis,True)
            dmpc "Wow, a bit formal for talking to a fellow student, huh? I suppose we did just meet, though, so it's only understandable."
            dmpc "Not to worry, though! I'm sure you'll be feeling a bit more comfortable soon enough."
        "It is as nice to meet you as it is to see you, and I am sure many would agree.":
            $ dmp.show("idle",genpos,dis,True)
            dmpc "Quite the charmer, aren't we? Unfortunately for you, I'm aromantic and asexual, or what they would call aroace. Well, more specifically, I'm aegoromantic and black stripe asexual."
            $ dmp.show("idle",ripos,dis,True)
            menu:
                "Aego-what now?":
                    dmpc "Aegoromantic. It means that I like experiencing romance vicariously (so like through books and stuff), but I don't feel any romantic attraction in real life, nor do I have any interest in engaging in a romantic relationship."
                    dmpc "I think there are some people who're aegoromantic and feel some romantic attraction, but I'm not one of them, so I can't quite speak for them on their experiences."
                    dmpc "As for black stripe asexual, it means that I don't feel any sexual attraction at all." 
                    dmpc "Aroace itself means someone who experiences little to no sexual and romantic attraction, but since both aromanticism and asexuality are their own spectra with people who experience differing levels of various kinds of attraction in differing situations, I like to clarify."
                "Black stripe?":
                    dmpc "Black stripe asexual. It means that I don't feel any sexual attraction at all."
                    dmpc "As for aegoromantic, it means that I like to experience romance vicariously (so like through books) but I don't feel any romantic attraction in real life, nor do I have any interest in engaging in a romantic relationship."
                    dmpc "I think there're some people who're aegoromantic and feel some romantic attraction, but since I'm not one of them, I can't quite speak on their experiences."
                    dmpc "Aroace covers experiencing little to no romantic and sexual attraction, but since both aromanticism and asexuality are spectra with people who experience differing levels of various kinds attraction in different situations, I like to clarify."
            $ aroaceRouteStarted = true
            $ dmp.show("idle",genpos,dis,True)
            jump aroaceRoute
    jump schooltour
label aroaceRoute:
    if aroaceRouteStarted:
        dmpc "People being openly aroace and accepted for it hasn't been around that long in Laventhyria, sadly. It was only within the last couple centuries that people began to actually allow us to be ourselves."
        dmpc "Before that, it was commonplace for people who weren't heterosexual to be forced into heterosexual marriages, at least within the nobility."
        dmpc "You know, the whole thing about how it's 'unnatural' and how they need an heir."
        dmpc "But then..."
        if gbRouteStarted:
            dmpc "As a young person was being forced to be wed, a voice came from far above."
            image bg_city = Placeholder("bg", "city")
            # placeholder for until the city asset is finished
            scene bg_city with dis
            g "This person is one of my chosen. If you continue to act against my and their wishes, I shall ensure that the consequences will be painful."
        else:
            dmpc "Oh, sorry, I must be boring you with all my rambling. I can just get like that sometimes, especially when it's something that I'm super interested in or passionate about."
            $ dmp.show("idle",ripos,dis,True)
            menu:
                "Oh, no, it's fine.":
                    dmpc "No, really, you don't have to be so kind!"
                    $ dmp.aff += 0.01
                "Yeah, I was getting a bit bored.":
                    dmpc "Jeez, I know I said it, but you don't have to be that blunt about it!"
                    $ dmp.aff -= 0.1
                "I actually found it really interesting!":
                    dmpc "Wait, really? You don't have to lie to me if you didn't!"
                    dmpc "Hmm... I find that your heart aligns with these words."
                    dmpc "I have to resume the tour for now, but if you want to hear about it another time, come talk to me during break time! If you want, I can tell you all about the history of aroace people here!"
                    $ dmp.aff += 0.1
            jump schooltour
label schooltour:
    $ dmp.show("idle",genpos,dis,True)
    dmpc "Anyway, this school's a boarding school, so you'll be living here. However, you will be granted your own room, as is tradition."
    dmpc "You know, since this school was originally made for noble children and they would often demand their own rooms, and the school's funded by the government and nobility, so the school can afford it."
    dmpc "Oh, yeah! I tend to refer to this school as 'the school' when I'm talking. Less annoyingly long than 'The Laventhyrian Institute for Secondary Education'. Just wanted to clarify that."
    dmpc "Sooooo..."
    dmpc "Yeah! Back to the explanation!"
    dmpc "I'm guessing the common people aren't particularly happy about how the nobles get to live it up in this palace off their taxes."
    dmpc "Technically, anyone can attend nowadays, but it's pretty rare to see a commoner here.\nBasically, there's a system where the next class is chosen every year by a random wheel. Five hundred seats."
    dmpc "So in theory, you might think that everyone has an equal shot at attending, right? Well, that's where donations come in."
    dmpc "See, if someone donates sufficient money, about a million levants, or {font=NotoSerifDisplay-VariableFont_wdth,wght.ttf}\u20B7{/font}1,000,000, to the school, that grants their child or children (if they make multiple donations) of choice a seat. From the five hundred, of course."
    dmpc "And even then, any children that they haven't chosen still have a shot at a seat. So they say it's super exclusive and all, but really, it's a noble children's romping ground. At least, that's what the newspapers that try to rile up the commoners say."
    dmpc "Come to think of it, I think I've heard rumors about some kind of insurrection within Laventhyria. Some kind of 'Revolutionary Pirate Order' that goes around blowing stuff up that belongs to the nobility. I'm sure that would never happen here, though..."
    dmpc "Oh, whoops, I've gotten myself sidetracked again! Hey, if you feel like I'm getting sidetracked, you can tell me and I'll get back on task! Of course, if you want to listen to me yap, that's all fine and dandy too!"
    play sound "Achievement.ogg"
    scene bg_hallway
    show taskinator at genpos
    with dis
    $ dmp.hide(dis,True)
    "Unlocked Taskbringer!"
    "When someone goes off on a ramble, you can get them back on task with this! Be warned, though. If you use it too much, they'll think you don't care about them and like you less in turn."
    hide taskinator with dis
    $ dmp.show("idle",genpos,dis,true)
    dmpc "Hey! Hello?"
    dmpc "Ah, you're back!"
    dmpc "What even happened?"
    $ dmp.show("idle",ripos,dis,True)
    menu:
        "I saw this bright light...":
            dmpc "What a bizarre occurence..."
        "A divine intervention...?":
            $dmp.show("excited",genpos,dis,true)
            dmpc "DID YOU SEE THE GARLIC-"
            $ dmp.show("idle",genpos, dis, True)
            dmpc "I apologize for my earlier lack of composure."
        "I heard this weird sound...":
            dmpc "Is there a g-ghost around here?"
        "I got this strange item...":
            dmpc "Are you sure you're not hallucinating? I don't see anything here..."
    $ dmp.show("idle",genpos,dis,True)
    dmpc "Bizarre hauntings aside, I think I still have a bit to tell you!"
    dmpc "Since our school building is the old palace of the Skorgmiloquis monarchs, we have plenty of rooms available. At least a hundred, I think. That, along with the demands of nobles for greater attention to their kids, has led to the school having a class size of ten."
    dmpc "During break periods, however, you may wander the school as you please. This, too, was a demand from the nobles, as they felt the school needed to be more enriching for their children."
    dmpc "The rooftop's locked."
    dmpc "It's apparently because some kid decided to walk up there and lean over the balcony, and then a noble kid without a shred of sense pushed them off the railing 'as a practical joke'."
    menu:
        "Would you like to use the Taskbringer?"
        "Yes":
            $ renpy.say(dmpc,dmp.taskHandler())
        "No":
            dmpc "As you might expect, the noble faced no consequences whatsoever, because that kid was a commoner."
            dmpc "What a world we live in, right?"
    
    dmpc "Well, anyway, it's locked and they've put up giant wire to stop any more people from falling to their deaths. A little-known secret, however, is that the lock's so old and broken that if you poke it right it'll open up."
    dmpc "So if you wanna do something {font=NotoSerifDisplay-Italic-VariableFont_wdth,wght.ttf}in secret{/font}, that's the place ~"
    dmpc "You didn't hear that from me, though!"
    dmpc "Well, I think that's about it for the tour, so feel free to go back to your room and sle-"
    dmpc "Wait, I just realized that you don't know the school's scheduling yet!"
    dmpc "Oh, how could I forget? Well, the school has four quarters for each year, meaning that you'll be learning over the course of four four-week periods."
    dmpc "It's a bit intense, but that's just life, huh? After all, you {font=NotoSerifDisplay-Italic-VariableFont_wdth,wght.ttf}are{/font} at probably the most prestigious school in the nation, so it makes sense that it might be a bit on the intense side."
    dmpc "So we'll be doing that, but you do also get time to hang out with your classmates!"
    $ dmp.show("excited",genpos, dis, True)
    dmpc "Like, for exampleeeee, me!"
    $ dmp.show("idle",genpos, dis, True)
    dmpc "Not too excited, are you?"
    $ dmp.show("pout",genpos, dis, true)
    menu:
        "I am, though!":
            dmpc "Wait, really?"
            $ dmp.show("excited",genpos,dis,True)
            dmpc "Yay! I'm super excited to be in the same class as you too!"
            $ dmp.aff += 0.1
        "It's just class placement, isn't it? You're a fun person, but I'm not sure if I care too much who's in my classes as long as I can learn well.":
            dmpc "Hmph."
            $ dmp.show("idle",genpos,dis,True)
            dmpc "Well, I suppose that's only fair. Come to think of it, if I was in the same position, I'd probably say the same thing."
        "Oh, nooooo, I'm sooooooo excited that you're in my class.":
            dmpc "Rude."
            dmpc "You know, if you keep talking to me like this, maybe I just won't talk to you anymore. How about that?"
            $ dmp.aff -= 0.1
    dmpc "Come on now! Off you go! Your journey through Laventhyria awaits!"
    jump bedroom
label bedroom:
    image bg_bedroom = Placeholder("bg","Bedroom")
    scene bg_bedroom
    if (day>1):
        menu:
            "Another day has drawn to an end. What would you like to do now?"
            "Sleep":
                if (noEep >0):
                    $ noEep -= 0.5
                jump expression ("class_" + str(day)) 
                with fade
            "Stay up":
                with fade
                scene expression "/images/staying_up_late.png"
                "You stay up until the morning doing who knows what."
                "You're very tired."
                "You might make some mistakes tomorrow, but at least you got that last book in, right?"
                $ noEep += 1
                jump expression ("class_" + str(day))
                with fade
    else:
        menu:
            "The day has drawn to an end. What would you like to do now?"
            "Sleep":
                $ day += 1
                jump expression ("class_" + str(day))
                with fade
            "Stay up":
                with Fade(0.5,1.0,0.5,color="#000000")
                scene expression "/images/staying_up_late.png"
                $ day += 1
                "You stay up until the morning doing who knows what."
                "You're very tired."
                "You might make some mistakes tomorrow, but at least you got that last book in, right?"
                $ noEep += 1
                jump expression ("class_" + str(day))
                with fade
label class_1:
    image bg_classroom = Placeholder("bg","Classroom")
    scene bg_classroom
    "{font=NotoSerifDisplay-VariableFont_wdth,wght.ttf}Quarter One{/font}"
    "{font=NotoSerifDisplay-VariableFont_wdth,wght.ttf}Day One{/font}"
    $ player.show("idle",genpos,dis,True)
    p "It's the first day of school."
    p "And from what it sounds like, this one is pretty hardcore."
    if (noEep==1):
        p "I was up all night last night, and I'm not sure how well I can make it through..."
    menu:
        "I'm so excited for class, though!":
            p "That's right!"
            p "I was up all night thinking about how excited I was to meet my classmates and start my classes!"
        "I've been dreading this...":
            p "I was up all night worrying about how it'll go. Will they like me? What kind of people are they?"
            p "I mean, I guess I know that Lily'll be here."
            default word = "something."
            if (dmp.aff == 0.2):
                $ word = "comforting."
            elif (dmp.aff >= 0.10):
                $ word = "calming."
            elif (dmp.aff >= 0.01):
                $ word = "something, I guess?"
            elif (dmp.aff >= 0):
                $ word = "okay."
            elif (dmp.aff >= -0.1):
                $ word = "irritating."
            elif (dmp.aff >= -0.2):
                $ word = "annoying."
            p "That's [word]"
    play sound "Bell.ogg"
    p "Oh, the bell's rung!"
    p "Regardless of my doubts and my worries, I should give it my all!"
    p "O-or at least the best I can..."
    p "H-hopefully that's enough..."
    $ player.hide(dis,true)
    scene bg_classroom
    t "All right, settle down now, class."
    t "I hope that we'll have a productive session today."
    t "You may call me 'Your Lordship'."
    t "Today, we'll be talking about Systems of Linear equations. Oh, and we'll also be talking about some elementary row operations. You probably don't know what that is yet, but you will."
    t "So, I'm sure you all know what linear equations are, right?"
    t "Well, if you don't, linear equations have the form a₁x₁+a₂x₂+...+aₙxₙ=b, where a₁,...,aₙ and b are coefficients, x₁,...,xₙ are variables or unknowns, and n is the dimension, or the number of variables."
    t "So, here's some examples of linear equations to help it stick a bit better in your heads."
    t "2x₁+4x₂=4 is a line in two dimensions, as the keen-eyed among you might be able to tell from how the highest subscript is 2."
    t "Now, then, how many dimensions do you think 3x₁ + 2x₂ + x₃ = 6 is in?"
    $ renpy.say(t, f"Ah, the keen-eyed looking {p1genterm} in the front!")
    default ansRight = false
    default ansExp = false
    menu: 
        "One!":
            $ ansRight = false
        "Two!":
            $ ansRight = false
        "Three!":
            $ eepNum = renpy.random.random()
            if(eepNum < 0.01*(2)**noEep and noEep != 0):
                p "3!"
                p "{i}Curses! I messed up and said it wrong!{/i}"
                t "Your answer is..."
                $ ansRight = true
                t "{size=+20}Wrong!"
            else:
                $ ansRight = true
        "3!":
            $ eepNum = renpy.random.random()
            if(eepNum < 0.01*(2)**noEep and noEep != 0):
                p "Three!"
                p "{i}Curses! I messed up and said it wrong!{/i}"
                t "Your answer is..."
                $ ansRight = true
                t "{size=+20}Correct!"
            else:
                $ ansRight = false
                t "This one was a bit of a trick question, so I must apologize."
                t "It does feel good seeing people fall for it, though."
                t "Now, this isn't quite in my job description, but I'll tell you it anyway. When you put an exclamation mark after an integer, like I did with 3!, it's called a factorial and means that you multiply the integer with all the integers that come before it."
                t "So like here, 3! = 3*2*1=6, so that's why you're wrong."
                t "Your mind was certainly in the right place, though! Heehee!"
                $ ansExp = true
        "N!":
            $ ansRight = false
    if (ansRight):
        t "Excellent work, young...?"
        $ renpy.say(p,f"{pname}, Your Lordship.")
        t "Such respect! I like that in a pupil."
    elif (ansExp):
        t "Teehee! Thanks for amusing me, young..."
        $ renpy.say(p,f"{pname}, Your Lordship.")
        t "Such respect! I like that in a pupil."
    else:
        t "That's not right, but I can see you were trying pretty hard there."
        t "The number of variables can tell you the dimension of a linear expression. For example, if there's three variables, it's going to have three dimensions, like here."
    t "Now, when you have a set of one or more linear equations, you've got a linear system of equations!"
    t "The solutions of a system of linear equations are pretty important. Now, you may be wondering how we describe those solutions, or even what they are."
    t "The set of solutions for a linear system is the set of all possible values of x₁,x₂,x₃,...,xₙ that satisfy all of the equations. Not just one, not just two, not just n-1, alllll of them."
    t "For any system of linear equations, regardless of the dimension or the number of equations, there's only three possible solution cases. There's either one unique solution, infinite solutions, or no solutions."
    t "We can use these things called Elementary Row Operations to find the solution set for a system."
    t "The first is called Replacement/Addition. In this operation, you add a multiple of one row to another. Another is Interchange, where you interchange two rows. Finally, there's Scaling, where you multiply a row by a nonzero scalar."
    t "An important thing to remember is that conducting row operations does not change the solution set."
    show image "/images/math/row_operations_1.png.png" at genpos
    with dis
    t "Let's go through an example. R₁ is the linear equation x₁-2x₂+x₃=0, R₂ is 2x₂-8x₃=8, and R₃ is 5x₁-5x₃=10. We can start by adding R₂ to R₁, or R₁+R₂→R₁. This eliminates the x₂ term in R₁."
    scene bg_classroom
    show image "/images/math/row_operations_2.png.png" at genpos
    with dis
    t "Next, we can divide R₂ by two, R₂/2→R₂, which makes the new value of R₂ x₂-4x₃=4. This'll make it a bit easier to deal with later. We can then subtract 5R₁ from R₃ to eliminate the x₁ term. This leaves the third row as 10x₂-10x₃=10."
    t "You may notice that R₂ and R₃ both only have x₂ and x₃ terms. This means that we can use replacement to have just one variable. Since R₃ has 10x₂ and R₂ has x₂, it's easier to eliminate x₂ by subtracting 10R₂ from R₃."
    scene bg_classroom
    show image "/images/math/row_operations_3.png.png" at genpos
    with dis
    t "Subtracting 10x₂-40x₃=40 from 10x₂-10x₃=10 leaves us with 30x₃=-30, which simplifies to x₃=-1. We can now substitute this into the other equations. Substituting it into R₁ results in x₁+7=8, which means that x₁=1. Substituting it into R₂ results in x₂+4=4, so x₂=0."
    t "This means that the solution set for the system R₁: x₁-2x₂+x₃=0, R₂: 2x₂-8x₃=8, R₃: 5x₁-5x₃=10 is the point (1,0,-1)."
    scene bg_classroom
    t "It's a bit awkward to keep writing x₁, x₂, and x₃, right? Fortunately, these can be rewritten as augmented matrices. For example, {image=/images/math/lineq1.png} can be written as the augmented matrix {image=/images/math/augmatrix1.png}. The vertical line is basically a reminder that the columns before it are the coefficients to x₁, x₂, and x₃."
    t "Now, here's a couple of important terms. A linear system is consistent if it has ≥1 solution. It could have one particular solution or it could have infinitely many, but as long as it has solutions, it's consistent." 
    t "Two matrices are row equivalent if a sequence of row operations can transform one into the other. An important thing about row equivalence is that if the augmented matrices of two linear systems are row equivalent, they have the same solution set."
    t "Now, here's something to hopefully get it to stick a bit better."
    t "Suppose that A={image=/images/math/matrix1.png}, B={image=/images/math/matrix2.png}, C={image=/images/math/matrix3.png}, and {image=/images/math/vec1.png}. Are A and B row equivalent? What about A and C? Are the augmented matrices \n(A|b⃗) and (C|b⃗) consistent?"
    t "I'll give you some time to work on this, so move forward when you have an answer for both."
    menu:
        t "Have you finished?"
        "Yes":
            pass
    t "Well, to answer the first part, we need to think about what row operations we could use to make them the same. For A and B, if we subtract row 2 of A from row 1, that leaves us with B. However, there's no way that we can make the second row have two 0s with the rows we have."
    t "As such, A and B are row equivalent, while A and C are not."
    t "For the question about (A|b⃗) and (C|b⃗), it's a bit easier to think of these as a linear system. In A, the two equations are x₁+x₂=1 and x₂=1. We can find a solution from these. If x₂=1 and x₁+x₂=1, then the solution is (0,1). Since it has a solution, this augmented matrix is consistent."
    t "For (C|b⃗), we get x₁+x₂=1 and 0x₁+0x₂=1. Since 0 is not equal to 1, there are no solutions. As such, this augmented matrix is not consistent."
    t "Okay, we've finished all of our course content for today, so it's time for the break!"
    scene bg_classroom
    $ dmp.show("idle", genpos, dis, True)
    dmpc "Hi again, [pname]! It's nice to be able to talk to you again!"
    menu:
        "Nice to see you too, [dname]!":
            $ dmp.aff += 0.1
            dmpc "Thanks!"
        "Ah, it's that one annoying person who can't stop talking.":
            $ dmp.aff -= 0.1
            dmpc "I see you haven't changed at all since our last meeting. What, have you never heard of acting like a decent person to people?"
    dmpc "I wanted to introduce you to some of our classmates! Here's Alva, Gwynedd, and Hoshi! You should go introduce yourself to them!"
    default meetNum=0
    default cameFromBreak = False
    default alTalk = false
    default gwTalk = false
    default hoTalk = false
    menu:
        "Who do you want to introduce yourself to first?"
        "Alva":
            $ meetNum+=1
            jump alva1
        "Gwynedd":
            $ meetNum +=1
            jump gwy1
        "Hoshi":
            $ meetNum += 1
            jump ho1
        "Nobody":
            dmpc "Are you sure?"
            dmpc "Well, I suppose if you don't want to speak with any of them now, you can talk to them during other breaks..."
            $ dmp.aff -= 0.01
            $ al.aff -= 0.1
            $ gw.aff -= 0.1 
            $ ho.aff -= 0.1
            $ cameFromBreak = True
            scene bg_classroom
            jump break_1
label alva1:
    $ dmp.hide(dis, True)
    $ alTalk = true
    scene bg_classroom
    $ al.show("idle",genpos,dis,True)
    r1 "Hello there, [pname]. It's very nice to meet you."
    r1 "My name is Alva Miloquis, and my family's holdings are in the county of Skorg."
    p "So you're..."
    r1 "Yeah, those Miloquises. Formerly the House of Skorg-Miloquis itself."
    menu:
        "Would you like to use the Taskbringer?"
        "Yes":
            $ renpy.say(r1,al.taskHandler())
        "No":
            r1 "This was my family's palace back in the day. I mean, it hasn't been for a loooooong time now."
            r1 "Heck, we're lucky to have escaped with our lives, much less with a county our own and all that."
            r1 "I'm actually kind of surprised that we've managed to remain nobility under the new system, but I guess we're not quite as indulgent as we were back in the old days."
            r1 "Not like we're a branch of the Levants and can get bailed out of any financial crisis we find ourselves in or anything."  
    p "Huh."
    menu: 
        p "That's..."
        "Interesting.":
            r1 "I suppose it would be for an outsider."
        "Pretty cool!":
            r1 "Really? I suppose being from a royal family, even a deposed one whose name is spat upon across the country, is pretty cool."
            $ al.aff += 0.1
        "Kinda weird...":
            r1 "I suppose it is a bit weird to be from a deposed royal family, huh?"
            $ al.aff -= 0.1
    if(cameFromBreak):
        jump expression ("break_"+str(day))
    r1 "Well, it was quite nice to meet you, but I'm afraid I must be taking my leave now."
    $ al.hide(dis,true)
    jump expression ("talkChoice"+str(meetNum))
label gwy1:
    $ dmp.hide(dis,True)
    scene bg_classroom
    $ gwTalk = true
    $ gw.show("idle",genpos,dis,True)
    r2 "Hiya there, [pname]! I'm very glad to meet you!"
    r2 "My name's Gwynedd, and I'm one of those rare commoners who managed to get in off the big wheel of names."
    r2 "I do find it preeeetty unfair how they advertise it as '500 people get to go to this excluuuuuusive school! It could be any of you!' and then behind- no, not even behind our backs, in broad daylight, they sell off those spots to nobles."
    menu:
        "Would you like to use the Taskbringer?"
        "Yes":
            $ renpy.say(r2,gw.taskHandler())
        "No":
            r2 "To be honest, I'm quite tired of this whole separation between nobles and commoners. Like, it's not even about 'bloodlines' or whatever they used to justify it with anymore."
            r2 "It's literally all about the money, and often, the only commoners who rise up and become nobles are either the merchants or the fallen nobles who got their act back together."
            r2 "So it really is just a bunch of 'rich people trade places with other rich people and the poor stay where they are'."
            r2 "I have heard rumors about some kind of 'People's Revolution' movement that's trying to cause some real change in here, and I'm kinda for it."
            r2 "Now, I don't think that destroying the nobility's buildings like those Revolutionary Pirates or whoever are will cause something to change, but I guess it does send a message to the nobility that the common people have had enough."
            r2 "I am scared that the nobles'll take it out on the rest of us commoners, though..."
    r2 "Sooooooo... Yeah! Basically, I'm one of those 'rare common specimens' who sometimes manage to get into the school. Ugh, I hate that term, though."
    menu: 
        "It does seem rather annoying.":
            r2 "It is! I mean, I suppose a noble might not fully understand how much, but it's basically just another way of othering me."
            r2 "Hehe, they're poor! Hehe, they're a commoner! Oh, look, it's that common specimen in the halls!"
            r2 "It's quite tiring, honestly."
            $ gw.aff += 0.1
        "It does seem rather fitting, though...":
            r2 "Really? After all of that conversation, you say something like that to me?"
            r2 "I suppose you're just like all the other nobles, after all..."
            r2 "Well, thanks for showing your true colors early. At least now, I know who to avoid."
            $ gw.aff -= 0.2
            r2 "Hopefully I never see you again, you scum of the earth."
            jump expression ("talkChoice"+str(meetNum))
        "What does that even mean?":
            r2 "I think I just explained it..."
            r2 "Well, I suppose I can do it again. See, basically, there's that wheel that decides if you get to go, right? But a lot of the slots get bought up by nobles beforehand, so there's often only a couple spots left for anybody else."
            r2 "Add in the fact that nobles who weren't bought in can still get in, and there's not too many seats for us commoners, even though there's a lot more of us than there are nobles. As such, it's a bit of a rare sight to see one of us here, which is why I'm called that."
            " "
            r2 "Ohhhhh, you meant it as in it's weird and stuff, not literally asking."
            r2 "Sorry, I do get a bit confused sometimes."
    if(cameFromBreak):
        jump expression ("break_"+str(day))
    r2 "Well, it was quite fun talking with you, but I have to go now!"
    $ gw.hide(dis,True)
    jump expression ("talkChoice"+str(meetNum))
label ho1:
    scene bg_classroom
    $ ho.show("idle",genpos,dis,True)
    $ hoTalk = True
    r3 "Hello, [pname]. My name's Hoshi."
    r3 "My family only recently became nobility, so I'm still getting used to it."
    r3 "I'm sorry for being a bit nervous. It's just that it's all very intimidating."
    menu:
        "Would you like to use the Taskbringer?"
        "Yes":
            $ renpy.say(r3,ho.taskHandler())
        "No":
            r3 "A couple of my realllly old relatives (although they're not technically considered part of our family due to the distance) recently passed and left us with some pretty sizable inheritances that were enough to get our net worth above the nobility threshold, and the census last year made us nobility."
            r3 "It's still a bit shocking, though. After all, we were a, well, still a well-to-do common family, but now we have our own land and our own manor and all that stuff."
            r3 " "
            r3 "Um..."
            r3 " "
    r3 "Sorry for being so nervous and awkward..."
    menu: 
        "No, it's fine!":
            r3 "Oh, really? Thanks..."
            $ ho.aff += 0.1
        "I actually think it's quite cute!":
            if(cameFromBreak):
                r3 "That's very nice of you to say, but I'm not sure if I can trust it..."
            else:
                r3 "Cute? Me? Cute? Nervousness? Cute? Cute?"
                $ ho.show("embarassed",genpos,dis,True)
                "They seem to be struggling to process your statement."
                r3 "U-um... T-thanks..."
                $ ho.aff += 0.2
        "You're about as annoying as [dname]...":
            if (dmp.aff >=0):
                r3 "So I'm not annoying? Thanks, I guess?"
            else:
                r3 "Okay, then..."
                r3 "I'll just shut up, then..."
                $ ho.aff -= 0.1
    if(cameFromBreak):
        jump expression ("break_"+str(day))
    r3 "I did have fun talking with you, and I hope I wasn't too annoying..."
    r3 "I think I have to go now, though..."
    $ ho.hide(dis,True)
    scene bg_classroom
    $ hoTalk = true
    jump expression ("talkChoice"+str(meetNum))
label talkChoice1:
    $ meetNum += 1
    menu:
        "Who would you like to speak to next?"
        "Alva" if not alTalk:
            jump alva1
        "Gwynedd" if not gwTalk:
            jump gwy1
        "Hoshi" if not hoTalk:
            jump ho1
label talkChoice2:
    $ meetNum += 1
    menu:
        "Who would you like to speak to last?"
        "Alva" if not alTalk:
            jump alva1
        "Gwynedd" if not gwTalk:
            jump gwy1
        "Hoshi" if not hoTalk:
            jump ho1
label talkChoice3:
    scene bg_classroom
    $ dmp.show("idle",genpos,dis,True)
    dmpc "You talked to all of them!"
    dmpc "It's probably a bit annoying to be asked to talk to three people you don't know before you can actually go off and enjoy your break, so I'm glad you did it."
    dmpc "Well, I suppose you can go off and do your fun break time stuff now!"
    $ dmp.hide(dis,True)
    scene bg_classroom
    jump break_1
label break_1:
    menu:
        "What would you like to do during your break?"
        "Talk to Alva":
            if not alTalk:
                jump alva1
            jump alvaBreak1
        "Talk to Gwynedd":
            if not gwTalk:
                jump gwy1
            jump gwyBreak1
        "Talk to Hoshi":
            if not hoTalk:
                jump ho1
            jump hoBreak1
        "Talk to Lily":
            jump dmpBreak1
        "Go up to the rooftop":
            jump roofBreak1
        "Go into the hallway":
            jump hallBreak1
label alvaBreak1:
    $ al.show("idle",genpos,dis,True)
    if(al.aff < 0.0):
        r1 "Ah, it's you. The one who called me weird. [pname.capitalize()], right?"
    else:
        r1 "Hello, [pname]. A good day to you once again."
    r1 "I guess, since you're here, you probably want to talk to me."
    r1 ""
    r1 "Do you have any ideas about what we could talk about?"
    menu:
        "I hear there's some kind of revolutionary movement within Laventhyria.":
            r1 "Ah, right. They call themselves the Revolutionary Pirates, right?"
            r1 "I think this country could use a revolution."
            r1 "The Levants certainly have been doing quite a bit to antagonize the common people."
            menu:
                "Would you like to use the Taskbringer?"
                "Yes":
                    $ renpy.say(r1,al.taskHandler())
                    r1 "I thought I was on task here, though..."
                    $ al.aff -= 0.01
                "No":
                    r1 "You know, taxing them more, increasing prices on literally everything for them, sending them into war first for every single war of expansion they do..."
                    r1 "The Levants are pretty good at appeasing the nobles, and they've basically got the wealthy commoners begging for their attention, but that does come at the expense of the poorer ones."
                    r1 "After all, it's very rare that an actually new house joins the nobility. Usually it's just a fallen noble house that's managed to get its act back together."
                    r1 "As such, seeing the rich people playing a game of musical chairs while they rot in poverty's probably not the best."
            r1 "I don't quite agree with their ways, though..."
            r1 "The pirates, I mean."
            r1 "What good does destroying buildings even do? It just makes them look like a terrorist group..."
            r1 "I am also worried about what will happen if they succeed. If they're so anti-noble buildings, what'll happen to the nobles themselves? Will they just have them all tried by a kangaroo court and executed on the spot?"
            r1 "What's more, I'm a bit skeptical of any revolution. After all, even if they do succeed, who's to say that whoever backed them won't come along and take full control?"
            r1 "It's happened before, after all."
            menu:
                "What do you mean, it's happened before?":
                    r1 "Why, with-"
                    play sound "Bell.ogg"
                    r1 "Ah, curses, it's time for bed."
                    r1 "Come back and talk to me tomorrow during break and I'll tell you what I meant."
                    r1 "And thanks for talking with me!"
                    $ al.aff += 0.1
        "What happened with the fall of Skorgmiloquis?":
            r1 "Ah, yes, Skorgmiloquis."
            r1 "This one's a bit of a long story, so I might not get through all of it today."
            menu:
                r1 "That okay with you?"
                "Yes":
                    r1 "Okay, then! Let's go!"
                    r1 "Skorgmiloquis, or officially the Imperial Realm of the House of Skorg-Miloquis and its subsidiaries, was the nation that ruled over this area, where Laventhyria is now."
                    r1 "Well, the Levants have been very expansionist since they made the new nobility system, so it's actually more of just the central part of modern Laventhyria."
                    scene bg_map
                    with dis
                    $ al.show("idle",ripos,None,false)
                    r1 "Regardless, Skorgmiloquis ruled over those lands. It was formed about 1120 years ago, when the heirs to the House of Skorg, which ruled over much of the northern regions, including the modern day county of Skorg, and the House of Miloquis, which ruled over the south, married."
                    r1 "Prior to this, Skorg and Miloquis had been constantly at war, each aiming to rule over all of Hyria, so their people were overjoyed that the endless war had ended."
                    scene bg_map_preMar
                    with dis
                    $ al.show("idle",ripos,None,false)
                    r1 "However, the new Skorg-Miloquis monarchs soon found that it was rather difficult to rule over all of this land by themselves."
                    r1 "As such, they selected for themselves trusted houses to govern fairly and justly over the various regions of this new nation."
                    r1 "These are what later became known as the noble houses."
                    r1 "With this, the monarchy could set its sights beyond Hyria, and its people were all for it."
                    scene bg_map_expand
                    with dis
                    $ al.show("idle",ripos,None,false)
                    r1 "It managed to expand into the surrounding areas."
                    r1 "However, over the next couple centuries, the nation faced a number of challenges."
                    r1 "Skorgmiloquis fell under threat from the nations surrounding it, meaning that it was, in essence, perpetually at war."
                    r1 "Eventually, the people's fervor dwindled, especially since these were defensive wars, and they began to grow tired."
                    r1 "Over the years, many of the houses selected as nobility grew self-interested, not bothering themselves with the lives of their people as much as their own."
                    r1 "The endless warfare and the growing prodigality of the imperial house began to put a strain on the nation's coffers. As such, they opted to increase taxation and request greater tribute of their noble vassals."
                    r1 "As one might expect-"
                    play sound "Bell.ogg"
                    scene bg_classroom
                    with dis
                    $ al.show("idle",genpos,None,false)
                    r1 "Looks like our time to speak for today has sadly concluded. If you wish to continue hearing about this, please come talk to me again tomorrow!"
                    r1 "But not during class time, or the teacher will have your head!"
                    $ al.aff += 0.1
                    jump bedroom
                "No":
                    r1 "Fair enough. If you do end up wanting to hear it later, though, just come back to me and ask!"
                    $ alva.hide(dis,true)
                    scene bg_classroom
                    jump break_1
        "What do you think of the Levants?":
            r1 "Hmm..."
            r1 "Oh, would you like a candy?"
            p "Sure!"
            r1 "Okay, it's fine if you don't know the answer to my question, but..."
            menu:
                r1 "When the pearly fluid fell, what did the people who planted the bombshell found by the belle in a well deal in?"
                "What in the-":
                    r1 "Okay, good, you're not a government agent. Can't be too careful these days, what with the Revolutionary Pirates and the government being on higher alert as a result..."
                    p "What does that even mean, though?"
                    r1 "It's an obscure poem from the Skorgmiloquis days. At one time, it was well known, but eventually, the regime decided to use it as a code phrase for their secret agents."
                    r1 "If you know the answer, it's almost certain that you're a government agent trying to tell what side I'm on. That, or you somehow managed to find a copy of the ancient poem the government's kept under total lockdown for about a millennium at this point."
                    $ keyAnswer = ""
                    # Resets keyAnswer in case its value is actually the code
                "I think I know.":
                    $ keyAnswer = renpy.input("What is the answer? Please do not use any periods.")
                    $ keyAnswer = keyAnswer.lower().strip()
                    $ renpy.say(p,keyAnswer)
                    if (keyAnswer == ("they dealt in the eggshell of the shelled gazelle") or keyAnswer == ("they dealt in the shell of the shelled gazelle") or keyAnswer == ("the bombshell found by the belle in a well was planted by a cartel who dealt in the eggshell of the shelled gazelle")):
                        jump spy
                    else:
                        r1 "Ah, phew! I thought you were one of those government agents, with how you had an answer almost the moment I asked."
                        p "What does that even mean, though?"
                        r1 "It's an obscure poem from the Skorgmiloquis days. At one time, it was well known, but eventually, the regime decided to use it as a code phrase for their secret agents."
                        r1 "If you knew the answer, it's almost certain that you're a government agent trying to tell what side I'm on. That, or you somehow managed to find a copy of the ancient poem the government's kept under total lockdown for about a millennium at this point."
            r1 "Well, since you're not a government agent, I suppose I can tell you."
            r1 "To be quite honest, I'm not exactly the biggest fan of the Levants. Not just because they took my family's lands, either."
            r1 "For one, they've always been more focused on their own profits than those of the nation. They also tend to pander too hard to the nobles."
            r1 "It makes them look bad to the commoners, or at least the poor ones. The people are, after all, the backbone of the nation, and they need to remember that."
            r1 "I also don't really like how they took power after Skorgmiloquis' fall, but that's another story."
            r1 "I think that's about all my opinions on them."
            r1 "Thanks for listening to me ramble on about my opinions."
            $ al.aff += 0.1
            jump bedroom
        "We could go up to the rooftop?":
            r1 "Isn't it off limits?"
            p "Well, it is, but from what I've heard, the lock's pretty old and rusty."
            r1 "Hmm..."
            r1 "I don't know..."
            r1 "What if we get caught?"
            menu:
                "We won't! They barely ever check up there, anyway.":
                    r1 "If you say so, but if we get in trouble, I'm pinning it all on you."
                    scene bg_rooftop
                    $ al.show(idle,lefpos,dis,True)
                    $ player.show(idle,ripos,dis,True)
                    r1 "Huh, you're right! It really was that easy."
                    p "Yup! There's a pretty nice view up here, too!"
                    "The two of you lay down on the floor and stare up at the sky."
                    r1 "It really is a pretty sky, huh?"
                    p "Sure is!"
                    r1 "I wonder what it would look like at night..."
                    p "So do I..."
                    ""
                    r1 "Maybe we should come up here sometime at night?"
                    p "Ah, acting a bit daring, are we?"
                    r1 "No, it's just..."
                    r1 "Well..."
                    r1 "It could be a nice experience, right?"
                    menu:
                        "It could be fun to bring along some of the others, too, right?":
                            r1 ""
                            r1 "Oh, right!"
                            r1 "Yeah, we could bring them..."
                        "True.":
                            r1 "Maybe sometime, I'll invite you up here!"
                            p "Maybe!"
                    $ al.aff += 0.2
                    jump bedroom
                "I guess you're right...":
                    r1 "It's a bit disappointing, I suppose, but it's probably better to be safe."
                    jump break_1
        "I don't know...":
            r1 "Then again, I suppose it's not undesirable to just sit together in silence."
            "The two of you sit together in silence, simply enjoying each other's presence."
            "Though it might ordinarily be boring, even something as simple as this feels enjoyable."
            "The hours seem to pass in an instant, and suddenly, the sky has turned a deep blue."
            r1 "Well, that was surprisingly enjoyable. A good day to you, [pname], and may our next meeting be favorable."
            $ al.aff += 0.05
            jump bedroom
        "Never mind.":
            r1 "Seriously? You come over to talk to me, then end it off immediately with 'Never mind.'?"
            $ al.show("pout",genpos,dis,True)
            r1 "Fine. Whatever. See if I care."
            $ al.aff -= 0.1
            jump break_1
label spy:
    r1 "Ah, so you're a government agent, then? You seem a bit young for the ol' trencher, but I suppose in these times, nobody's too young to serve their nation."
    r1 "At least, I'm guessing that's what they told you when they recruited you?"
    with vpunch
    r1 "Well, let me tell you something, [pname], if that's even your real name."
    r1 "You're serving one hell of a corrupt institution."
    r1 "And I will take great joy in taking you out of it."
    camera at dying
    $ al.hide(dis,true)
    scene bg_classroom
    $ player.show("scared",genpos,dis,True)
    p "{font=NotoSerifDisplay-Italic-VariableFont_wdth,wght.ttf} I can't breathe...{/font}"
    r1 "Acts fast, right? I call this one Azumarine. Your bosses aren't the only ones who have this on hand."
    with fade
    scene expression "/images/staying_up_late.png"
    "It all fades to black."
    "You died."
    camera
    menu:
        "Would you like to go back to talking with Alva, or to the break period in general?"
        "Talking with Alva":
            scene bg_classroom
            jump expression ("alvaBreak"+str(day))
        "Break Period":
            scene bg_classroom
            jump expression ("break_"+str(day))
label gwyBreak1:
    $ gw.show("idle",genpos,dis,True)
    if (gw.aff < 0.0):
        r2 "Hello again. Scum of the Earth, was it? Oh, wait, no, your name was [pname]. I had almost forgotten because of your behavior."
    else:
        r2 "Hiya there again, [pname]! How're you doing?"
        menu:
            "Great!":
                r2 "That's great to hear!"
            "Good!":
                r2 "Yay!"
            "Good...":
                r2 "Are you sure you're doing okay?"
            "Terrible :c":
                r2 "Oh, that's not good..."
                r2 "Hopefully I can help you feel a bit better..."
    r2 "So, you wanted to talk to me, so what should we talk about?"
    r2 "Or I guess if you wanted to go somewhere, we could go there!"
    menu:
        "What's going on with those 'Revolutionary Pirates'?":
            r2 "Ah, the revolutionaries."
            r2 "Way I see it, they're some of the common folk who decided they had enough of the nobles trying to push us down."
            r2 "Their ways of doing stuff are a bit destructive, but they do seem to avoid causing any harm to civilians."
            r2 "I think I've said it before, but I feel like this country needs a revolution."
            menu:
                "Would you like to use the Taskbringer?"
                "Yes":
                    $ renpy.say(r2,gw.taskHandler())
                    r2 "Was I really that far off task, though?"
                    $ gw.aff -= 0.01
                "No":
                    r2 "It feels to me like the monarchs and their noble cronies have gotten a bit too comfortable in the idea that the common people will just let them walk all over us."
                    r2 "We might need to teach them a little lesson about who we are."
                    r2 "Oh, sorry, I think I got a bit intense there!"
                    r2 "This kinda stuff does tend to get me pretty fired up."
                    r2 "As much as I like the way the Pirates do things, I don't think all of the commoners (I'm not a big fan of the word, but the common people is a bit of a mouthful to keep saying) would agree."
                    r2 "After all, not all of us are the biggest fans of destruction, and some (I'm guessing the older ones in particular) are probably going to be driven away from the idea of revolution by that."
                    r2 "They could be alienating a significant portion of the common people with that. After all, if parents don't trust the revolt's intentions and means, they may not approve of their children participating."
                    r2 "On the other hand, I suppose the youth coooould feel more drawn to it if their parents are so strongly opposed, but I feel like creating a generational divide like that for something as important as a revolution doesn't really work, or at least not too well."
            r2 "I guess my feelings on the matter are a bit complicated."
            r2 "We do need a revolution, but is destroying the buildings of the nobility the best way to go about it?"
            r2 "Will that portray the revolution as a force of liberation, or just one of terror?"
            r2 "Oh, come to think of it, this building's run by the nobility and the ruling regime, isn't it?"
            r2 "I wonder if they'll attack here..."
            r2 "But surely not, right? I don't think it would fit their M.O., nor would it really help their cause..."
            r2 "Maybe I should stop talking about such scary things, you know? You know what they say, when you say something could happen, fate might just will it into existence..."
            play sound "Bell.ogg"
            r2 "Well, that's the bell! Let's put these ominous thoughts aside for now and go sleep!"
            $ gw.aff += 0.1
            jump bedroom
        "What's your daily life like?":
            if (gw.aff < 0.0):
                if (p1sub = "they"):
                    r2 "Ah, so the wealthy noble finally bothers to ask the people they oppress about how they live."
                else:
                    r2 "Ah, so the wealthy noble finally bothers to ask the people [p1sub] oppress about how they live."
                r2 "What's wrong, did you grow a conscience or something?"
                r2 "I suppose I'd be willing to enlighten you. Who knows, maybe you really will grow a conscience or something. It's doubtful, though..."
            r2 "Well, I guess you'd say my family's not exactly the lower class."
            r2 "I mean, in that we aren't quite stuck living paycheck to paycheck or, even worse, out on the streets."
            r2 "We'd probably be classified as being among the middle class. Doesn't exactly mean we get treated any different, though..."
            r2 "My parents work pretty long hours at the local noble lord's manor."
            r2 "It's usually secretarial work, which, I suppose, is better than the alternative."
            menu:
                "Would you like to use the Taskbringer?"
                "Yes":
                    $ renpy.say(r2,gw.taskHandler())
                "No":
                    r2 "It's apparently super boring, though... I guess we are preeeetty lucky, though."
                    r2 "The noble governing our region actually bothers to pay us fairly and handles incident reports without significant bias."
                    r2 "Of course, noble-commoner incidents do slightly tend to end up with a ruling in favor of the noble, but there's been plenty where the ruling is in favor of the commoner." 
                    r2 "In such cases, they usually punish the noble with revocation of their status and, if they are a part of a noble house, the detachment of them from their house."
                    r2 "A pretty effective punishment, I'd say, for nobles who think they can get away with anything because of their status."
                    r2 "I believe if a noble is ruled against, the state confiscates half of their assets and redistributes them between the current petitioner and any others who have previously brought complaints against them."
                    r2 "It's a pretty fair system. If a noble's found to have acted badly toward someone, half of their wealth is distributed to their victims."
                    r2 "If the ruling is against the commoner, though, they usually just have them imprisoned. Not the best, in my opinion, but not as bad as in other areas, that's for sure."
                    r2 "In noble-noble disputes, the issue is usually left up to the houses of the nobles, while in common-common conflicts, the one ruled against is usually sentenced to pay reparations to their victim."
            r2 "Anyway, I am an only child, so it does get lonely sometimes. I have heard of families where having too many mouths to feed leads to less for everyone, so I suppose it's better than that."
            r2 "That said, being middle class doesn't necessarily mean that we're moving up in the world. We do get paid fairly, but fairly just means every year, our family's gained another hundred thousand levants or two."
            r2 "It's still a decent amount, but it's not like we're going to be nobles anytime soon."
            r2 "Being an only child does get lonely, though, especially with how long my parents' hours are..."
            r2 "I've gotten used to it, though, and I do have the neighborhood kids to play with! We do also have plenty of books for me to read when I get bored, and that boredom did mean that I could learn a lot of stuff!"
            r2 "So it's not that bad, I guess..."
            r2 "Wow, is it that time already? I suppose we'll be hearing the bell soon, then."
            play sound "Bell.ogg"
            r2 "Right on cue! Well, I'll see you tomorrow, then!"
            $ gw.aff += 0.1
            jump bedroom
        "How do you feel about the House of Levant?":
            r2 "You know that makes you sound really suspicious, right?"
            r2 "Like you're a government agent or something, you know?"
            r2 "Gah, if only there was a way to tell the difference!"
            r2 "Okay, I'm going to trust that you're not a government agent, and if you are, I'm going to feel very hurt and betrayed, okay?"
            menu:
                r2 "You don't want me to be hurt and betrayed and sad, right?"
                "Well, actually, I don't care that much...":
                    r2 "Seriously? How bad can you get?"
                    r2 "Okay, whatever. If you were actually a government agent, you'd be trying to get close to me, so you're probably not."
                    r2 "Doesn't mean you have to be like that about it, though..."
                    $ gw.aff -= 0.2
                "No, I wouldn't!":
                    r2 "Putting it on a bit much there, aren't you?"
                    r2 "Well, you seem sincere enough, so I'll be putting my life in your hands."
                    r2 "Please don't get me killed."
                    $ gw.aff += 0.01
            r2 "They feel to me like they're a buncha rich people on a power trip."
            r2 "Now, I don't know too much about Levanthyrian history from a couple centuries ago, but from what I've heard, the country was ruled by a democratic assembly for a bit."
            r2 "Then the Levants came in and decided that since they were rich, everything that you can see now is theirs."
            r2 "Councillors dying mysteriously left and right, while the Levants stood through it all."
            r2 "To be honest, they probably had them taken out."
            r2 "I wonder if they're still on good terms with the assassins they had do it."
            r2 "They've reshaped the old system with the Assembly so much that you can barely tell that it's what it used to be at all."
            r2 "Like how now, they've got their noble cronies running stuff that used to be run by democratically elected officials and stuff."
            r2 "They run a tight ship, though. Nobles can't just be lazy or they'll get kicked out, while the rich commoners are clamoring for those noble spots."
            menu:
                "Would you like to use the Taskbringer?"
                "Yes":
                    $ renpy.say(r2,gw.taskHandler())
                "No":
                    r2 "So, in essence, everyone with wealth and power's begging to be noticed by the royals, while everyone else is too poor to do much."
                    r2 "Despite all their work, though, there's still a revolution. I wonder if it scares them."
                    r2 "They don't usually care about the lower classes, but maybe when those classes start blowing their stuff up, they'll care a bit more?"
                    r2 "Hmm, what else?"
                    r2 "Well, they've been doing a lot of warfaring recently. My guess is that they've probably gotten too many houses rising and not enough falling in recent years."
                    r2 "That would mean that they're having to give away royal lands to some merchant family that's on the rise, and they probably aren't the biggest fans of that idea, so aggressive expansion could help..."
                    r2 "How long can they keep it up, though? We've been non-stop at war for the past twenty years, and they've always been victories for the regime, but how long can they keep it up?"
                    r2 "How many people are dying so that the Levants can crown the next Count of Nowherelandshire? If they make trade harder for the merchants, that goes against the idea of keeping them on your side, but if they don't, they'll always be running out of land."
                    r2 "Not to mention that the common people are livid about how they have to keep on fighting for rich people to give other rich people land."
                    r2 "In addition, the difference between the thresholds for commoners to rise and nobles to fall is pretty big, so it's not even that easy for someone to fall."
                    r2 "It's a good system to keep the rich and powerful under your control while avoiding them becoming lazy, but I don't know if it can truly be considered sustainable."
                    r2 "At some point, something's got to give, whether it's their capacity for war, their support from wealthy merchants, or their support from the populace."
                    r2 "When it does, what will they sacrifice?"
            r2 "They don't really seem to care much for the commoners, though, and that could be their downfall..."
            r2 "I wonder how the Revolutionary Pirates will do in their revolt. Will they be liberators, or a new set of oppressors?"
            r2 "It's a revolution of the common people, so I have hope, but you can't really let yourself have too much hope."
            r2 "Otherwise you'll always be disappointed."
            r2 "There's also the issue of how they'll handle the nobles..."
            r2 "Like there's going to be those who say the nobles should just be stripped of their titles and lands, and then there's those who'll want to, well..."
            r2 "Kill them all."
            p "K-kill us all?"
            r2 "Yeahhhh..."
            r2 "A lot of people've been wronged by the nobility, and that's led to a lot of frustrations about them."
            r2 "Some people would rather see them all dead."
            r2 "I'm not on that side, if you're worried about it. Like I said, our regional noble's not terrible like in other regions, and even if they were, I still feel like the systematic murder of an entire group of people is a bit much as punishment."
            r2 "Even if the nobles have done a lot of bad stuff to the common people, that doesn't mean that we should do terrible things right back to them."
            r2 "After all, we'd be just as terrible as them."
            play sound "Bell.ogg"
            r2 "Well, I suppose that ends this rather grim discussion."
            r2 "It was fun talking with you, though!"
            $ gw.aff += 0.1
            jump bedroom
        "I'm not sure...":
            r2 "That's kinda funny, isn't it?"
            r2 "Well, I suppose it's not altogether unpleasant to just sit together in silence."
            r2 "It is fun to think sometimes."
            r2 "Or something like that..."
            r2 "Wow, I'm not very good at this sitting together in silence thing, am I?"
label hoBreak1:
    "The dialogue for this section is not yet complete. Please proceed to the bedroom."
    jump bedroom
label dmpBreak1:
    "The dialogue for this section is not yet complete. Please proceed to the bedroom."
    jump bedroom
label roofBreak1:
    "The dialogue for this section is not yet complete. Please proceed to the bedroom."
    jump bedroom
label hallBreak1:
    "The dialogue for this section is not yet complete. Please proceed to the bedroom."
    jump bedroom
label class_2:
    scene bg_classroom
    "{font=NotoSerifDisplay-VariableFont_wdth,wght.ttf}Quarter One{/font}"
    "{font=NotoSerifDisplay-VariableFont_wdth,wght.ttf}Day Two{/font}"
    $ player.show("idle",genpos,dis,True)
    p "Yesterday was pretty fun."
    p "I wonder what we're learning about today."
    p "Hold on, I can probably check my schedule."
    play sound "Bell.ogg"
    p "No time! Well, I guess the teacher'll tell us what we're studying."
