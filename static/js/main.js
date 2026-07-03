// ================= PHOTO PREVIEW =================

const photoInput = document.getElementById("photo");
const preview = document.getElementById("preview");

if(photoInput){

    photoInput.addEventListener("change", function(){

        const file = this.files[0];

        if(file){

            const reader = new FileReader();

            reader.onload = function(e){

                preview.src = e.target.result;

            }

            reader.readAsDataURL(file);

        }

    });

}


// ================= MOBILE VALIDATION =================

const mobileInput = document.getElementById("mobile");

if(mobileInput){

    mobileInput.addEventListener("input", function(){

        this.value = this.value.replace(/[^0-9]/g,'');

        if(this.value.length > 10){
            this.value = this.value.slice(0,10);
        }

    });

}


// ================= AADHAAR VALIDATION =================

const aadhaarInput = document.getElementById("aadhaar");

if(aadhaarInput){

    aadhaarInput.addEventListener("input", function(){

        this.value = this.value.replace(/[^0-9]/g,'');

        if(this.value.length > 12){
            this.value = this.value.slice(0,12);
        }

    });

}


// ================= PAN AUTO UPPERCASE =================

const panInput = document.getElementById("pan");

if(panInput){

    panInput.addEventListener("input", function(){

        this.value = this.value.toUpperCase();

    });

}


// ================= ACCOUNT NUMBER VALIDATION =================

const accountInput = document.getElementById("account_number");
const confirmAccountInput = document.getElementById("confirm_account_number");

if(confirmAccountInput){

    confirmAccountInput.addEventListener("keyup", function(){

        if(accountInput.value !== confirmAccountInput.value){

            confirmAccountInput.style.border = "2px solid red";

        }
        else{

            confirmAccountInput.style.border = "2px solid green";

        }

    });

}


// ================= LOADING BUTTON =================

const form = document.querySelector("form");

if(form){

    form.addEventListener("submit", function(){

        const button = document.querySelector("button");

        button.innerHTML = "Please Wait...";

        button.disabled = true;

    });

}