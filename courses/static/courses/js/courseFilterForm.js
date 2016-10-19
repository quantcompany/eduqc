
var courseFilterForm = {
    done: false,
    errors: [],
    submitting: false,

    query: {value: '', error: ''},
    categories: {value: [], error: ''},

    clear: function(){
        this.errors = [];
        
        this.query.value = '';
        this.query.error = '';

        this.categories.value = [];
        this.categories.error = ''
    }
};

rivets.bind($('#course-filter-form'), {form: courseFilterForm})




var courseSearchResults = {
    page_count: 0,
    current_page_index: 0,
    pages: [{number: 1, courses: []}],

    current_page: function(){
        return this.pages[this.current_page_index].courses;
    },

    next_page: function(target, scope){
        if (scope.results.current_page_index < scope.results.page_count - 1){
            scope.results.current_page_index += 1;
        }
    },

    prev_page: function(target, scope){
        if (scope.results.current_page_index > 0){
            scope.results.current_page_index -= 1;
        }
    },

    goto_page: function(target, scope){
        console.log(scope);
        scope.results.current_page_index = scope.index;
    },

    is_active: function(index){
        return this.current_page_index == index;
    }
}

rivets.bind($('#course-search-results'), {results: courseSearchResults});






$('#course-filter-form').on('submit', function(e){
    courseFilterForm.submitting = true;
    
    e.preventDefault();

    var request = $.ajax({
        url: '/courses/filter',
        method: 'POST',
        data: new FormData(this),
        processData: false,  // tell jQuery not to process the data
        contentType: false,  // tell jQuery not to set contentType
    });
    

    request.done(function(data, textStatus, jqXHR) {
        console.log('Success\n' + jqXHR.responseText);
        courseFilterForm.submitting = false;
        courseFilterForm.done = true;

        courseSearchResults.page_count = data.page_count;
        courseSearchResults.current_page_index = 0;
        courseSearchResults.pages = data.pages;
    });
     
    request.fail(function(jqXHR, textStatus, errorThrown) {
        console.log('Error ' + jqXHR.status + '\n' + jqXHR.responseText);
        courseFilterForm.submitting = false;
    });
});







