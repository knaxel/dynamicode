const progressArray = [-1];

(function(){
    function defineProgress(){
        for (let i = 0; i < 1; i++) {
            labelArray[0].innerHTML = "Progress: " + progressArray[i] + "%";
          }
    }

    const labelArray = [document.getElementById('pymod0')];

    defineProgress();

})();

function updateProgress(){
    progressArray[0] = 100;
}


