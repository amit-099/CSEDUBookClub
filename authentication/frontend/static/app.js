

function populate() {
    if(quiz.isEnded()) {
        showScores();
    }
    else {
        // show question
        var element = document.getElementById("question");
        element.innerHTML = quiz.getQuestionIndex().text;

        // show options
        var choices = quiz.getQuestionIndex().choices;
        for(var i = 0; i < choices.length; i++) {
            var element = document.getElementById("choice" + i);
            element.innerHTML = choices[i];
            guess("btn" + i, choices[i]);
        }

        showProgress();
    }
};

function guess(id, guess) {
    var button = document.getElementById(id);
    button.onclick = function() {
        quiz.guess(guess);
        populate();
    }
};


function showProgress() {
    var currentQuestionNumber = quiz.questionIndex + 1;
    var element = document.getElementById("progress");
    element.innerHTML = "Question " + currentQuestionNumber + " of " + quiz.questions.length;
};

function showScores() {
    var gameOverHTML = "<h1>Result "+quiz.score + "</h1>";
    gameOverHTML += "<h2 id='score'> Your scores: " + quiz.score + "</h2>";
    if(quiz.score<=5) {
        gameOverHTML += "<h3>Poor result, needs to improve</h3>";
    }
    else if (quiz.score<=10){
        gameOverHTML += "<h3>You did good, you can do better!!</h3>";
    }

    else if (quiz.score<=15){
        gameOverHTML += "<h3>Reaching new heights!!!</h3>";
    }

    else if (quiz.score<=20){
        gameOverHTML += "<h3>Success is yours!!!</h3>";
    }
    var retake = "<h4>     Wanna retake the exam?? Click in the Exam button above or just REFRESH!</h4>"
    var element = document.getElementById("quiz");
    element.innerHTML = gameOverHTML + retake;
    //element.innerHTML = retake;
};

// create questions
var questions = [
    new Question("what is the angle between two vectors A=3i-3j and B=5i+5k?", ["60", "30","45", "90"], "60"),
    new Question("A sound wave is emmited by a point source.Intensity of the sound at a point is _________ its distance from the source.", ["directly propotional to", "inversely propotional to", "directly propotional to square of", "inversely propotional to square of"], "inversely propotional to square of"),
    new Question("Which temperature of Feranhite scale is three times larger than that in the centigrde scale?", ["160", "80","40", "320"], "80"),
    new Question("one of the angles in a rhombus is 70.what is the size of the other 3 angles?", ["70,110,110", "70,70,70", "80,90,100", "60,120,120"], "70,110,110"),
    new Question("Five capacitor of five micro capaitance each are connected in series.Their equivalent capacitance is____", ["5 microF", "4 microF", "1 microF", "10 microF"], "1 microF"),
    new Question("A cylindaric copper wire has resistance R.It is deformed to twice its original length with no change in volume.its new resistance is ___.", ["2R", "4R", "8R", "R/2"], "4R"),
    new Question("If a particle moves with the speed of light its mass will be ____.", ["0", "unchanged", "infinity", "none of the above"], "infinity"),
    new Question("An alternating current is exressed by the equation I=50sin300pit.What is the frequency of current?", ["450Hz", "400Hz", "220Hz", "150Hz"], "150Hz"),
    new Question("A 13N weight and a 12N weight are connected by a massless string over a massless,frictionless pulley.The 13N weight has a downward acceleration with magnitude equal to that of a free falling body times:", ["1/12", "1/13", "1/25", "13/25"], "1/25"),
    new Question("A stone is thrown uwards with a velocity of 9.8 meter per second.After how long will it return to the ground?", ["5s", "2s", "3s", "10s"], "2s"),
    new Question("The frequency of two tuning forks are 128Hz and 384Hz respectively.The ratio of wavelength of two waves formed by the forks in air is", ["3:1", "1:3", "2:1", "4:1"], "3:1"),
    new Question("9.0x10^4 j heat energy is supplied to a heat engine of 33% efficiency.how much heat energy will be converted into work by the heat engine?", ["3000J", "8400J", "30000J", "10000J"], "3000J"),
    new Question("if the gravitationl potential at the surface of the earth of Radius R id V then what is the gravitational potential at a point at a height  above the earth`s surface?", ["V/4", "V/2", "V", "2V"], "2V"),
    new Question("A current of 0.3A is passsed through a lamp for 2 minutes using a 6V power supply.The energy dissipated by this lamp during 2 minutes is", ["12J", "1.8J", "216J", "220J"], "216J"),
    new Question("in an ideal 1:8 step-down transformer,the primary power is 10KW and the secondary current is25A.the primary voltage is-", ["2500", "3200", "31250", "400"], "3200"),
    new Question("Which one of the following rays is used to destroy the cancer cells in human body?", ["alpha", "beta", "gama", "X-ray"], "gama"),
    new Question("two parallel metal plates separated by a distance d have a potential difference V across them.What is the magnitude f the electrostatic force acting on a charge Q placed midway between the plates?", ["2VQ/d", "VQ/d", "VQ/2d", "dQ/V"], "VQ/d"),
    new Question("A block of Ice at 0C containing a piece of cork is floating on surface of ice water in a beakerWhen the ice has melted the water level:", ["is higher", "is lower", "is the same", "depends on the initial ratio"], "is the same"),
    new Question("refractive index of water is 1.3. What is the speed of light in water?Speed of light in vacuum is 3x10^8m/s", ["3x10^8m/s", "2.31x10^8m/s", "2.0x10^8m/s", "4.4x10^8m/s"], "2.31x10^8m/s"),
    new Question("Which of the following physical properties is not exhibited by sound wave?", ["refraction", "interference", "polarization", "diffraction"], "polarization"),

];

// create quiz
var quiz = new Quiz(questions);

// display quiz
populate();





