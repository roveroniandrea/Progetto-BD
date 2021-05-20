let count = 5;
let countDownRedirect = setInterval(function () {
    count--;
    document.getElementById('countDown').innerHTML = "Sarai riportato alla home in " + count + " secondi";

    if (count === 1)
        document.getElementById('countDown').innerHTML = "Sarai riportato alla home in " + count + " secondo";

    if (count === 0){
       window.location.href = '/';
       clearInterval(countDownRedirect);
    }

}, 1000);