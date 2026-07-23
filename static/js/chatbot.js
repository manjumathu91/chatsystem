document.addEventListener(
    "DOMContentLoaded",
    function(){

    const form = document.getElementById(
        "chat-form"
    );


    const input = document.getElementById(
        "user-input"
    );


    const chatBox = document.getElementById(
        "chat-box"
    );



    form.addEventListener(
        "submit",
        function(e){


        e.preventDefault();



        let question = input.value.trim();



        if(question === "")
        {
            return;
        }



        // User message

        chatBox.innerHTML += `

        <div class="chat-message chat-user">

            ${question}

        </div>

        `;



        input.value = "";




        fetch(
            "/faq-answer/",
            {


            method:"POST",


            headers:{

                "Content-Type":
                "application/json",


                "X-CSRFToken":
                getCookie("csrftoken")

            },


            body:JSON.stringify({

                question:question

            })


        })



        .then(
            response =>
            response.json()
        )


        .then(
            data => {


            chatBox.innerHTML += `


            <div class="chat-message chat-ai">

                ${data.answer}

            </div>


            `;



            chatBox.scrollTop =
            chatBox.scrollHeight;



        })



        .catch(
            error=>{


            chatBox.innerHTML += `

            <div class="chat-message chat-ai">

                Error connecting AI

            </div>

            `;


        });



    });



});





// CSRF Cookie

function getCookie(name) {


    let cookieValue = null;


    if(document.cookie && document.cookie !== ""){


        const cookies =
        document.cookie.split(";");



        for(let cookie of cookies){


            cookie = cookie.trim();



            if(cookie.startsWith(name+"=")){


                cookieValue =
                decodeURIComponent(
                    cookie.substring(
                        name.length+1
                    )
                );


                break;

            }

        }

    }


    return cookieValue;

}