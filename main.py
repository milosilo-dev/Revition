from flask import Flask, redirect, url_for, render_template, request, jsonify
import os

app = Flask(__name__)

subjects = os.listdir("Subjects")
index = 0

def read_file(filename):
    file1 = open(filename, 'r')
    Lines = file1.readlines()
    return Lines

@app.route("/")
def home():
    subjects = os.listdir("Subjects")
    return render_template("index.html", subjects = subjects)
@app.route("/subject/<subject>/")
def topicslist(subject):
    topics = os.listdir("Subjects\\" + subject + "\\")
    return render_template("subject.html", topics = topics, subject = subject)
@app.route("/subject/<subject>/AddTopic/")
def addtopic(subject):
    return render_template("topicform.html", subject = subject)
@app.route("/subject/<subject>/AddTopic/end/", methods=['POST'])
def endaddtopic(subject):
    if request.method == 'POST':
        name = request.form.get('name')
        topics = os.listdir("Subjects\\" + subject + "\\")
        subjects = os.listdir("Subjects")
        exists = topics.__contains__(name)
        if (exists != True):
            os.system("mkdir Subjects\\" + subject + "\\" + name + "\\")
            os.system("type nul > Subjects\\" + subject + "\\" + name + "\\" + "flash.txt")
    return redirect(url_for("topicslist", subject=subject))
@app.route("/subjectform/")
def Addsubject():
    return render_template("subjectform.html")
@app.route("/subjectform/end/", methods=['POST'])
def finaladdsubject():
    if request.method == 'POST':
        name = request.form.get('name')
        exists = subjects.__contains__(name)
        subjects = os.listdir("Subjects")
        if exists != True:
            os.system("mkdir Subjects\\" + name + "\\")
    return redirect(url_for("home"))
@app.route("/subject/<subject>/<topic>/flashcard/")
def flashcard(subject, topic):
    return render_template("flashcard.html", subject = subject, topic = topic)

@app.route("/subject/<subject>/<topic>/flashcard/add/")
def addflashcard(subject, topic):
    return render_template("flashcardadd.html", subject = subject, topic=topic)

@app.route('/subject/<subject>/<topic>/flashcard/add/end/', methods=['POST'])
def addflashcardend(subject, topic):
    if request.method == "POST":
        name = request.form.get('name')
        question = request.form.get('question')
        anser = request.form.get('anser')
        with open("Subjects\\" + subject + "\\" + topic + "\\" + "flash.txt", "a") as file:
            file.write(":" + name + ":" + question + ":" + anser + """
""")
    return redirect(url_for("flashcard", subject=subject, topic=topic))
@app.route('/subject/<subject>/<topic>/flashcard/revise/<index>/')
def reviseflashcard(subject, topic, index):
    nsl=0
    lines = read_file("Subjects\\" + subject + "\\" + topic + "\\" + "flash.txt")
    line = lines[int(index)]
    line = line.split(":")
    return render_template("flashcardrevise.html",subject=subject, topic=topic, qusetion = line[1], anser=line[2], index=index, nsl = len(lines) - 1)
@app.route('/subject/<subject>/<topic>/flashcard/revise/<index>/next/')
def reviseflashcardadd(subject, topic, index):
    val = int(index) + 1
    return redirect(url_for("reviseflashcard", subject=subject, topic=topic, index=val))
@app.route('/subject/<subject>/<topic>/flashcard/revise/<index>/last/')
def reviseflashcardback(subject, topic, index):
    val = int(index) - 1
    return redirect(url_for("reviseflashcard", subject=subject, topic=topic, index=val))

if __name__ == "__main__":
    app.run()