function setupSearch() {
    $.get('/asset-doc/objects.json').then((resp) => {
        var objects = JSON.parse(resp);
        var bh = new Bloodhound({
            datumTokenizer: function(d) {
                return Bloodhound.tokenizers.whitespace(`${d.name} ${d.description}`);
            },
            queryTokenizer: Bloodhound.tokenizers.whitespace,
            identify: function(obj) { return obj.name; },
            local: JSON.parse(resp),
            cache: false,
        });
        var params = {hint: true, highlight: true, minLength: 2};
        $('#search .typeahead').typeahead(params, {
            name: 'objects',
            limit: 20,
            source: bh,
            display: d => d.name,
            templates: {
                suggestion: Handlebars.compile('\
                    <div class="typeahead-result">\
                        {{#if img}}<div class="typeahead-img"><img src="{{img}}" width=24></div>{{/if}}\
                        <div class="typeahead-text"><b>{{name}}</b><br>{{description}}</div>\
                    </div>')
            }
        });
        $('#search .typeahead').bind('typeahead:select', function(ev, suggestion) {
            window.location.href = suggestion.filename;
        });
        console.log('typeahead init')
    });
}
