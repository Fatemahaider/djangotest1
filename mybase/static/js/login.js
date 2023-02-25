const passwordField = document.querySelector("#passwordField");

const showtoggle = document.querySelector('.showPasswordToggle');

showtoggle.addEventListener('click', (e)=>{
        //data = e.composed;
        //console.log(data)
        if(showtoggle.textContent === 'SHOW'){
        showtoggle.textContent = "HIDE";
        passwordField.setAttribute("type" , "text");
        showtoggle.style.color = "blue";

    }
    else {
        showtoggle.textContent = "SHOW";
        passwordField.setAttribute("type" , "password");
        showtoggle.style.color = "black";

    }
});

