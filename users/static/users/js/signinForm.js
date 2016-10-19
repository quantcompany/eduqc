var signinForm = {
    done: false,
    errors: [],
    submitting: false,

    email: {value: '', error: ''},
    password: {value: '', error: ''},

    clear: function(){
        this.errors = [];
        
        this.email.value = '';
        this.email.error = '';

        this.password.value = '';
        this.password.error = ''
    }
};


rivets.bind($('#signin-form'), {form: signinForm})


$('#signin-form').on('submit', function(e){
    signinForm.submitting = true;
    
    e.preventDefault();

    var fd = new FormData(this);

    var request = $.ajax({
        url: '/users/signin',
        method: 'POST',
        data: new FormData(this),
        processData: false,  // tell jQuery not to process the data
        contentType: false,  // tell jQuery not to set contentType
    });
    

    request.done(function(data, textStatus, jqXHR) {
        console.log('Success\n' + jqXHR.responseText);
        signinForm.submitting = false;
        signinForm.clear();
        signinForm.done = true;
    });
     
    request.fail(function(jqXHR, textStatus, errorThrown) {
        console.log('Error ' + jqXHR.status + '\n' + jqXHR.responseText);

        var data = JSON.parse(jqXHR.responseText);

        if (jqXHR.status == 400){
            signinForm.errors = data.__all__ || [];
            signinForm.email.error = data.username ? data.username[0] : '';
            signinForm.password.error = data.password ? data.password[0] : '';
        }

        signinForm.submitting = false;
    });
});