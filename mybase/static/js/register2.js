console.log("reg2");

// $(document).ready(function(){
//     $(".validateclass").change(function(){
//       var name = $("#usernameField").val();
//       alert(name);
//       var email = $("#emailField").val();
//       alert(email);
//     });
//   });
$(document).ready(function(){
    $(".validateclass").keyup(function(){
       var name = $("#usernameField").val();
       var email = $("#emailField").val();
       
       if(name.length>0){
        console.log("name");
        
       }
       if(email.length>0){
        console.log("email");
       }
       


        })
    
})        

 
