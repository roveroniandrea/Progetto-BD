let count = 5;
setInterval(function () {
    count--;
    document.getElementById('countDown').innerHTML = "Sarai riportato alla home in " + count + " secondi";

    if (count === 1)
        document.getElementById('countDown').innerHTML = "Sarai riportato alla home in " + count + " secondo";
    else if (count === 0)
        window.location.href = '/';
    else if (count < 0)
        document.getElementById('countDown').innerHTML = "Sarai riportato alla home in 0 secondi";

}, 1000);