var profileForm = {
    done: false,
    errors: [],
    submitting: false,
    changePassword: false,
    togglePasswordForm: function(){
      this.changePassword = !this.changePassword;
    },
    clear: function(){
        this.errors = [];
    }
};


rivets.bind($('.profile-form'), {form: profileForm})


$('.profile-form').on('submit', function(e){
    profileForm.submitting = true;

    e.preventDefault();

    var fd = new FormData(this);

    var request = $.ajax({
        url: this.getAttribute('action'),
        method: 'POST',
        data: new FormData(this),
        processData: false,  // tell jQuery not to process the data
        contentType: false,  // tell jQuery not to set contentType
    });


    request.done(function(data, textStatus, jqXHR) {
        console.log('Success\n' + jqXHR.responseText);
        profileForm.submitting = false;
        profileForm.clear();
        profileForm.done = true;
    });

    request.fail(function(jqXHR, textStatus, errorThrown) {
        console.log('Error ' + jqXHR.status + '\n' + jqXHR.responseText);

        var data = JSON.parse(jqXHR.responseText);

        if (jqXHR.status == 400){
            profileForm.errors = data.__all__ || [];
            profileForm.email.error = data.email ? data.email[0] : '';
            profileForm.password1.error = data.password1 ? data.password1[0] : '';
            profileForm.password2.error = data.password2 ? data.password2[0] : '';
        }

        profileForm.submitting = false;
    });
});
