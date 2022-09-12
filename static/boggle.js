// Global variables
let score = 0
let timeLeft = 60
let guesses = []

// Select guess form
const $guessForm = $("#guess-form")

/* Add event listener to handle form submission */
$guessForm.on("submit", async function(e){

    // Prevent page from refreshing
    e.preventDefault()

    // Get user guess from form
    let guess = $("#guess").val()

    $("#guess").val('')
    // Do nothing if there's no guess
    if (!guess){
        return
    }

    // Prevent duplicate guesses
    if (guesses.includes(guess)){
        displayMsg("You've already guessed that word!")
        return
    }

    guesses.push(guess)
    // Check if guess is valid via Python
    let resp = await axios.get('/check-guess', {params:{'guess': guess}})

    // Display message and clear input
    let msg = getMsg(resp)
    displayMsg(msg)
    

    // Update score
    let score = trackScore(guess, resp)
    displayScore(score)
})

/* Manage timer */
function manageTimer(){
    timer = setInterval(() => {

        // If out of time, stop timer and redirect to stats page
        if (timeLeft === 0){
            clearInterval(timer)
            saveStats()
            //redirect()
            // Post request with score and number times played
            
        }
        // Handle changing timer on page
        displayCountdown(timeLeft)

        // Decrement time left
        timeLeft -= 1 
        }, 1000)
}

/* Get message ot display with each guess */
function getMsg(resp){
    result = resp.data.result
    let msg = ""
   
    // Get message based on GET request feedback
    if (result === "ok"){
        msg = "Nice! You got one."    
    }
    else if (result === "not-word"){
        msg = "Sorry, that one's not in our dictionary."
    }
    else if (result === "not-on-board"){
        msg = "Sorry, we can't find that one on the board."
    }
    return msg
}

/* Display message with each guess */
function displayMsg(msg) {
    $('.secretmessage').html(msg)
}

/* Track score for each valid guess */
function trackScore(guess, resp) {
    if (resp.data.result === 'ok') {
        score += guess.length
    }
    return score
}

/* Update score with each guess */
function displayScore(score){
    $('#score').html(score)
}

/* Update timer on page */
function displayCountdown(second){
    $('#timer').html(second)
}

/* Send post request to server with # times played and highest score */
async function saveStats(){
  newRecord = await axios.post('/store-stats', {params: {'score': score}})
  if (newRecord.data === true){
    redirect('/stats/win')
  }
  else {
    redirect('/stats/lose')
  }
}
/* Redirect to stats page */
function redirect(url){
    window.location.replace(url)
}

/* Start timer on load */
manageTimer()

