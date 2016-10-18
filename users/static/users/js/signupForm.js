var signupForm = {
    submitting: false,
    errors: [],

    email: {value: '', error: ''},
    password1: {value: '', error: ''},
    password2: {value: '', error: ''},
    clear: function(){
        this.errors = [];
        
        this.email.value = '';
        this.email.error = '';

        this.password1.value = '';
        this.password1.error = ''

        this.password2.value = '';
        this.password2.error = ''
    }
};


rivets.bind($('#signup-form'), {form: signupForm})


$('#signup-form').on('submit', function(e){
    signupForm.submitting = true;
    
    e.preventDefault();

    var fd = new FormData(this);

    var request = $.ajax({
        url: '/users/signup',
        method: 'POST',
        data: new FormData(this),
        processData: false,  // tell jQuery not to process the data
        contentType: false,  // tell jQuery not to set contentType
    });
    

    request.done(function(data, textStatus, jqXHR) {
        console.log('Success\n' + jqXHR.responseText);
        signupForm.submitting = false;
        signupForm.clear();
    });
     
    request.fail(function(jqXHR, textStatus, errorThrown) {
        console.log('Error ' + jqXHR.status + '\n' + jqXHR.responseText);

        var data = JSON.parse(jqXHR.responseText);

        if (jqXHR.status == 400){
            signupForm.errors = data.__all__ || [];
            signupForm.email.error = data.email ? data.email[0] : '';
            signupForm.password1.error = data.password1 ? data.password1[0] : '';
            signupForm.password2.error = data.password2 ? data.password2[0] : '';
        }

        signupForm.submitting = false;
    });
});