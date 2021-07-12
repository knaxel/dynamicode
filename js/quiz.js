(function(){
function buildQuiz(){
    // variable to store the HTML output
    const output = [];

    // for each question...
    myQuestions.forEach(
    (currentQuestion, questionNumber) => {

    // variable to store the list of possible answers
    const answers = [];

    // and for each available answer...
    for(letter in currentQuestion.answers){

    // ...add an HTML radio button
    answers.push(
        `<div class="row"><label>
        <input type="radio" name="question${questionNumber}" value="${letter}">
        ${letter} :
        ${currentQuestion.answers[letter]}
        </label></div>`
    );
    }

    // add this question and its answers to the output
    output.push(
    `<div class="question"> ${currentQuestion.question} </div>
    <div class="answers"> ${answers.join('')} </div>`
    );
    }
    );

    // finally combine our output list into one string of HTML and put it on the page
    quizContainer.innerHTML = output.join('');
}

function showResults(){
    // gather answer containers from our quiz
    const answerContainers = quizContainer.querySelectorAll('.answers');

    // keep track of user's answers
    let numCorrect = 0;

    // for each question...
    myQuestions.forEach( (currentQuestion, questionNumber) => {

    // find selected answer
    const answerContainer = answerContainers[questionNumber];
    const selector = `input[name=question${questionNumber}]:checked`;
    const userAnswer = (answerContainer.querySelector(selector) || {}).value;

    // if answer is correct
    if(userAnswer === currentQuestion.correctAnswer){
        // add to the number of correct answers
        numCorrect++;

        // color the answers green
        answerContainers[questionNumber].style.color = 'lightgreen';
    }
    // if answer is wrong or blank
    else{
        // color the answers red
        answerContainers[questionNumber].style.color = 'black';
    }
    });

    // show number of correct answers out of total
    resultsContainer.innerHTML = `${numCorrect} out of ${myQuestions.length}`;
    if(myQuestions.length == numCorrect){
        finishButton.innerHTML = '<a href="./index.html"><button class="col-auto m-2 btn justify-content-center" onClick="check">Complete</button></a>';
    }
}

const quizContainer = document.getElementById('quiz');
const resultsContainer = document.getElementById('results');
const submitButton = document.getElementById('submit');
const finishButton = document.getElementById('finish');

const myQuestions = [
{
    question: "A program is a [blank]",
    answers: {
    a: "type of computer",
    b: "set of instructions",
    c: "group of coders"
    },
    correctAnswer: "b"
}
];

// display quiz right away
buildQuiz();

// on submit, show results
submitButton.addEventListener('click', showResults);
})();