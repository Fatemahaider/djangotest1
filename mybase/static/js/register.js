//console.log('Hello Register');

const usernameField = document.querySelector("#usernameField");

const feedbackField = document.querySelector(".invalid-feedback");

const buttonfield = document.querySelector("#btn");


            




usernameField.addEventListener("keyup",(e) => {
//    console.log('working');
    const userval = e.target.value;
//    console.log(userval);   

usernameField.classList.remove("is-invalid");
feedbackField.style.display="none";

    if (userval.length>0){
       fetch("/u_validate", {
        body:JSON.stringify({username:userval}),
        method:"POST",
       })
       .then(res => res.json().then((data) => {
        console.log(data);
        if(data.Username_error){
            buttonfield.disabled=true;
            usernameField.classList.add("is-invalid");
            feedbackField.style.display="block";
            feedbackField.innerHTML=`<p>${data.Username_error}</p>`
        }
        else{
            buttonfield.removeAttribute("disabled");

        }
       
       })
       )


    }

});  

const emailField = document.querySelector("#emailField");

const emailfeedback = document.querySelector(".emailFeedBackArea");

emailField.addEventListener("keyup" , (e) => {
    console.log("working");
    const emailval = e.target.value;

    buttonfield.removeAttribute("disabled");
    emailField.classList.remove("is-invalid");
    emailfeedback.style.display="none";
    if (emailval.length>0){
        fetch('/e_validate',{
            body: JSON.stringify({email:emailval}),
            method:"POST",
        })
        .then(res => res.json())
        .then((data) => {
            if (data.email_error){
                buttonfield.disabled=true;
                emailField.classList.add("is-invalid");
                emailfeedback.style.display="block";
                emailfeedback.innerHTML = `<p>${data.email_error}</p>`
            }
           
        });
    }
});



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




