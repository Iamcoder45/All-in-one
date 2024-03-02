
window.addEventListener("load" , init)

// globals 
let time=5
isplaying= true;
let score=0;

const word_input = document.querySelector("#word-input")
const current_word = document.querySelector("#current-word")
const scoreDisplay = document.querySelector("#score")
const timeDisplay = document.querySelector("#time")
const messages = document.querySelector("#message")


// "Extraordinary", "Extravagant", "Pulchritudinous", "Magnanimous", "Ubiquitous", "Spectacular",
//      "Exhilarating", "Phenomenal", "Astonishing", "Intricate", "Majestic", "Eccentric", "Formidable", 
//      "Serendipitous", "Effervescent", "Illustrious", "Ethereal", "Mellifluous", "Quintessential", "Resplendent",
//       "Enigmatic", "Transcendent", "Prodigious", "Perspicacious", "Impeccable", "Opulent", "Meticulous", "Grandiose", 
//       "Panoramic", "Sensational", "Sumptuous", "Indomitable", "Sublime", "Incandescent", "Magnificent", 
//       "Coruscating", "Enthralling", "Cacophonous", "Symbiotic", "Unassailable", "Resplendent", "Ineffable",
//        "Rhapsodic", "Breathtaking", "Exquisite", "Inexorable", "Insuperable", "Immaculate", "Stupendous"




const words= [
  
    "aa",
    "bb",
    "rish",
     "node"
    ]


function init(){

    generateWords()

    setInterval(countdown , 1000)


    setInterval(gamestatus , 50)

    word_input.addEventListener('input', startgame)

}

function startgame(){
  
    console.log(word_input.value)
    console.log("startgame")

    if(matchword()){
    isplaying=true;
    generateWords()
    time=6;
    score++;
    word_input.value=''
    scoreDisplay.innerHTML=score

    }
}


function matchword(){
    if(word_input.value === current_word.innerHTML){
        messages.innerHTML="correct"
        return true;
    }
    else{
        return false
    }
}


function generateWords(){

   const rindex = Math.floor(Math.random()* words.length)
    current_word.innerHTML=words[rindex]

}

function countdown(){

    console.log(time)

    if(time > 0){
        time--
    }
    else if(time === 0)
    {
        isplaying=false;
    }

     timeDisplay.innerHTML=time;

}

function gamestatus(){
    if(isplaying && time > 0){

    }
    else {
        score=0;
        scoreDisplay.innerHTML=score
        messages.innerHTML="game over !!!"

    }
}