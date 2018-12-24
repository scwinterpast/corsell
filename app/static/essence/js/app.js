let searchType = urlParams.get('type')

const search = instantsearch({
  // Replace with your own values
  appId: 'S9M6RYTUAZ',
  apiKey: 'f44d6a371b87978f46eba81e3d2797cc', // search only API key, no ADMIN key
  indexName: 'Combined',
  urlSync: true,
  searchParameters: {
    hitsPerPage: 10,
    facetsRefinements: {
      type:[searchType || '']
    },
    // Add to "facets" all attributes for which you
    // do NOT have a widget defined
    facets: ['type']
  }
});

search.addWidget(
  instantsearch.widgets.searchBox({
    container: '#search-input'
  })
);

search.addWidget(
  instantsearch.widgets.hits({
    container: '#hits',
    hitsPerPage:10,
    templates: {
      item: document.getElementById("hit-template").innerHTML,
      empty: "We didn't find any results for the search <em>\"{{query}}\"</em>"
    }
  })
);

var facetTemplateCheckbox =
  '<a href="javascript:void(0);" class="facet-item">' +
  '<input type="checkbox" class="{{cssClasses.checkbox}}" value="{{name}}" {{#isRefined}}checked{{/isRefined}} />{{name}}' +
  '<span class="facet-count">({{count}})</span>' +
  '</a>';

/*search.addWidget(
  instantsearch.widgets.refinementList({
    container: "#refinement-list",
    attributeName: 'categories',
    limit: 10,
    templates: {
      header: '<div class="facet-title">Type</div>',
      item: facetTemplateCheckbox
    }
  })
)*/

search.addWidget(
  instantsearch.widgets.pagination({
    container: '#pagination',
    maxPages: 20,
    // default is to scroll to 'body', here we disable this behavior
    scrollTo: false
  })
);
search.addWidget(
  instantsearch.widgets.rangeSlider({
    container: '#price-slider',
    attributeName: 'price',
    templates: {
      header: 'Price'
    },
    tooltips: {
      format: function(rawValue) {
        return '$' + Math.round(rawValue).toLocaleString();
      }
    }
  })
);
search.start()
