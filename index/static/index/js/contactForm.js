var contactForm = {
    done: false,
    errors: [],
    submitting: false,

    name: {value: '', error: ''},
    email: {value: '', error: ''},
    subject: {value: '', error: ''},
    message: {value: '', error: ''},

    clear: function(){
        this.errors = [];

        this.name.value = '';
        this.name.error = '';

        this.email.value = '';
        this.email.error = '';

        this.subject.value = '';
        this.subject.error = '';

        this.message.value = '';
        this.message.error = '';
    },

    validate: function() {
      this.name.error = (!this.name.value || this.name.value.length == 0 ? 'This field is required.' : '');
      this.email.error = (!this.email.value || this.email.value.length == 0 ? 'This field is required.' : '');
      this.subject.error = (!this.subject.value || this.subject.value.length == 0 ? 'This field is required.' : '');
      this.message.error = (!this.message.value || this.message.value.length == 0 ? 'This field is required.' : '');
    },

    hasErrors: function() {
      this.validate();
      let a = this.name.error.length;
      let b = this.email.error.length;
      let c = this.subject.error.length;
      let d = this.message.error.length;
      return (a + b + c + d) > 0;
    }
};


rivets.bind($('#contact-form'), {form: contactForm})


$('#contact-form').on('submit', function(e){
    e.preventDefault();

    if (contactForm.hasErrors() == true){
      return;
    }

    contactForm.submitting = true;

    var fd = new FormData(this);

    var request = $.ajax({
        url: '/contact',
        method: 'POST',
        data: new FormData(this),
        processData: false,  // tell jQuery not to process the data
        contentType: false,  // tell jQuery not to set contentType
    });


    request.done(function(data, textStatus, jqXHR) {
        console.log('Success\n' + jqXHR.responseText);
        contactForm.submitting = false;
        // contactForm.clear();
        // contactForm.done = true;
    });

    request.fail(function(jqXHR, textStatus, errorThrown) {
        console.log('Error ' + jqXHR.status + '\n' + jqXHR.responseText);

        // var data = JSON.parse(jqXHR.responseText);
        //
        // if (jqXHR.status == 400){
        //     contactForm.errors = data.__all__ || [];
        //     contactForm.email.error = data.email ? data.email[0] : '';
        //     contactForm.password1.error = data.password1 ? data.password1[0] : '';
        //     contactForm.password2.error = data.password2 ? data.password2[0] : '';
        // }

        contactForm.submitting = false;
    });
});
