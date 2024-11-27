let currentStep = 1;



function nextStep(step) {
    // Validate the current step before proceeding
    if (validateStep(currentStep)) {
        $(`#step-${currentStep}`).hide();
        currentStep = step;
        $(`#step-${currentStep}`).show();
    }
}

function prevStep(step) {
    $(`#step-${currentStep}`).hide();
    currentStep = step;
    $(`#step-${currentStep}`).show();
}


function validateStep(step) {
    const inputFields = $(`#step-${step} input[data-validation]`);

    let isValid = true;

    inputFields.each(function() {
        const validationRules = $(this).data('validation').split('|');
        const errorSpan = $(`#${this.id}-error`);
        errorSpan.text('');

        for (const rule of validationRules) {
            if (rule === 'required' && validator.isEmpty($(this).val())) {
                errorSpan.text('This field is required.');
                isValid = false;
                break; // No need to check other rules if this one fails
            }
            // Add more validation rules here as needed
            if (rule === 'email' && !validator.isEmail($(this).val())) {
                errorSpan.text('Please enter a valid email.');
                isValid = false;
                break;
            }
            // Custom rule to check if password and confirm password match
            if (rule === 'password-match') {
                const passwordField = $('#password');
                const confirmPasswordField = $('#c-password');
                if (passwordField.val() !== confirmPasswordField.val()) {
                    errorSpan.text('Passwords do not match.');
                    isValid = false;
                }
            }
        }

        // Show/hide the error message
        if (isValid) {
            errorSpan.hide();
        } else {
            errorSpan.show();
        }
    });

    return isValid;
}






$(document).ready(function() {

   

  
   

    function submitForm() {
        // Add your form submission logic here
        // This function will be called on the final step
        if (validateStep(currentStep)) {
            alert("Form submitted successfully!");
        }
    }


        $("#user_menu-parent").click(function () {
         
            $("#admin-submenu").toggle();
        });

        // Close submenu when clicking outside
        $(document).on("click", function (e) {
            if (!$(e.target).closest("#userMenu").length && !$(e.target).closest("#admin-submenu").length) {
                $("#admin-submenu").hide();
            }
        });

        // Toggle sidebar (you can implement this functionality)
        $("#toggleSidebar").click(function () {
            // Implement your sidebar toggle logic here

            $('#admin-sidebar').toggleClass('close');
        });


        $(".submenu-parent").on("click", function (e) {
           
            $(".submenu").toggle();
            
        });



        // Close dropdown menu when clicking outside
        $(document).on("click", function (e) {
            if (!$(e.target).closest(".submenu-parent").length && !$(e.target).closest(".index-sub").length) {
                $(".submenu").hide();
            }
        });

})