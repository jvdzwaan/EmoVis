var embEmApp = angular.module('embEmApp', ['elasticsearch',
                                           'ngRoute',
                                           'nvd3ChartDirectives']);

embEmApp.config(function($httpProvider, $routeProvider, $locationProvider){
    // set csrftoken for Django
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';

    // get params from the url
    $routeProvider.when('/corpus', {
        controller: 'CorpusCtrl',
        templateUrl: 'static/partials/corpus.html'
    }).when('/corpus/:titleId/', {
        controller: 'TitleCtrl',
        templateUrl: 'static/partials/title.html'
    }).when('/pairs/', {
        controller: 'PairsCtrl',
        templateUrl: 'static/partials/pairs.html'
    });

    $locationProvider.html5Mode(true);
});

embEmApp.controller('EntitiesCtrl', function ($scope, $route, $routeParams, $location, $http){
    $scope.query = '';
    $scope.mainCat = '';
    $scope.compareWith = ['Posemo', 'Negemo'];
    $scope.entityStatistics = {};
    $scope.subgenreStatistics = {};

    $http.get('entity_vis/entity_categories').success(function (data){
        $scope.categories = data.hits.hits;
        console.log($scope.categories);
    });
    $http.get('corpus/entity_stats').success(function (data){
        $scope.entityStatistics = data;
    });
    $http.get('corpus/subgenre_stats').success(function (data){
        $scope.subgenreStatistics = data;
        console.log($scope.subgenreStatistics);
    });

    $scope.searchFn = function (value, index){
        if( !$scope.query ){ return false; }
        var re = new RegExp($scope.query, 'i');
        return (re.test(value.fields.name.join(' ')));
    }
    $scope.setMainCat = function(cat) {
        $scope.mainCat = cat;
    }
    $scope.removeMainCat = function() {
        $scope.mainCat = '';
    }
    $scope.addToCompareWith = function(cat) {
        if($scope.compareWith.indexOf(cat) == -1){
            $scope.compareWith.push(cat);
        }
    }
    $scope.removeFromCompareWith = function(cat) {
        var i = $scope.compareWith.indexOf(cat);
        $scope.compareWith.splice(i, 1);
    }
    $scope.getSelectedCategories = function(){
        if($scope.mainCat){
            return [$scope.mainCat].concat($scope.compareWith);
        } else {
            return $scope.compareWith;
        }
    }

    $scope.xFunction = function(){
        return function(d){
            return d.x;
        }
    };
    $scope.yFunction = function(){
        return function(d){
            return d.y;
        }
    };
   $scope.colorFunction = function(){
        // use d3's category10 colors
        var color = d3.scale.category10();
        return function(d, i){
            return color(d.key);
        };
    }
});

embEmApp.controller('CorpusCtrl', function ($scope, $route, $routeParams, $location, $http){

    $scope.$watch('mainCat', function() {
        $scope.getEntityStatisticsCorpus();
    });
    $scope.$watch('compareWith', function() {
        $scope.getEntityStatisticsCorpus();
    }, true);

    $scope.getEntityStatisticsCorpus = function(){
        $http.post('corpus/entity_stats/', {categories: $scope.getSelectedCategories()}).
            success(function (data){
                console.log(data);
                $scope.entityStatistics = data;
        });

        $http.post('corpus/subgenre_stats/', {categories: $scope.getSelectedCategories()}).
            success(function (data){
                console.log(data);
                $scope.subgenreStatistics = data;
        });

        $http.post('entity_vis/subgenres_stats_time/', {categories: $scope.getSelectedCategories()}).
            success(function (data){
                $scope.subgenreTimeData = data;
                console.log('subgenres_stats_time');
                console.log($scope.subgenreTimeData);
            });
    }
 
});

embEmApp.controller('TitleCtrl', function ($scope, $routeParams, $http, EmbEmDataService){
    $scope.titleId = $routeParams.titleId;
    $scope.statistics = {};

    $scope.selectedCats = $scope.getSelectedCategories();

    EmbEmDataService.getTitleWordcloudData($scope.titleId, $scope.selectedCats)
        .then(function (data){
            $scope.wordcloudData = data;
        });
    
    $http.get('corpus/titles/'+$scope.titleId).success(function (data){
        $scope.title = data;
        console.log($scope.title);
    });

    $http.post('corpus/entity_stats/'+$scope.titleId+'/', {categories: $scope.getSelectedCategories()}).
        success(function (data){
        console.log(data);
        $scope.statistics = data;
    });

    $http.post('entity_vis/entity_graph_title/'+$scope.titleId+'/', {categories: $scope.getSelectedCategories()}).
        success(function (data){
        console.log(data);
        $scope.chartData = data;
    });
    
    $scope.$watch('mainCat', function() {
        $scope.selectedCats = $scope.getSelectedCategories();
        $scope.getEntityStatisticsTitle();
        $scope.updateChartData();
    });
    $scope.$watch('compareWith', function() {
        $scope.selectedCats = $scope.getSelectedCategories();
        $scope.getEntityStatisticsTitle();
        $scope.updateChartData();
    }, true);

    $scope.getEntityStatisticsTitle = function() {
        $http.post('corpus/entity_stats/'+$scope.titleId+'/', {categories: $scope.getSelectedCategories()}).
            success(function (data){
            console.log(data);
            $scope.statistics = data;
        });
    }
    $scope.updateChartData = function(){
        $http.post('entity_vis/entity_graph_title/'+$scope.titleId+'/', {categories: $scope.getSelectedCategories()}).
            success(function (data){
            console.log(data);
            $scope.chartData = data;
    });
        
    }
    $scope.xFunction = function(){
        return function(d){
            return d.turn;
        }
    };
    $scope.yFunction = function(){
        return function(d){
            return d.Score;
        }
    };
 
});

embEmApp.controller('PairsCtrl', function ($scope, $routeParams, $http, EmbEmDataService, es){
    $scope.pairs = {};
    $scope.pairs.intervalSize = 20;
    $scope.pairs.data = [];
    $scope.pairs.pairs = [];
    $scope.pairs.genreData = {};

    $scope.getPairsData = function () {
        if($scope.pairs.intervalSize <= 0) {
            $scope.pairs.intervalSize = 20;
        }

        var pairLabel = $scope.pairs.pair+":"+$scope.pairs.intervalSize;

        $scope.getPairsDataCorpus(pairLabel);

        $scope.getPairsDataGenre(pairLabel);
    }

    $scope.getPairsDataCorpus = function(pairLabel) {
        es.search({
            index: 'embem',
            size: 0,
            body: {
                "query": {
                    "term": {
                        "pairs-Body-Posemo.data": {
                            "value": $scope.pairs.pair
                        }
                    }
                },
                "size": 0,
                "aggs": {
                    "data": {
                        "histogram": {
                            "field": "year",
                            "interval": $scope.pairs.intervalSize,
                            "min_doc_count": 0,
                            "extended_bounds": {
                                "min": 1600,
                                "max": 1850
                            }
                        },
                        "aggs": {
                            "total": {
                                "sum": {
                                    "field": "pairs-Body-Posemo.num_pairs"
                                }
                            }
                        }
                    }
                }
            }

        }).then(function (response) {
            $scope.pairs.data.push({
                "key": pairLabel, 
                "values": response.aggregations.data.buckets
            });
            $scope.pairs.pairs.push(pairLabel);
        });
    }

    $scope.getPairsDataGenre = function(pairLabel) {
        es.search({
            index: 'embem',
            size: 0,
            body: {
                "query": {
                    "term": {
                        "pairs-Body-Posemo.data": {
                            "value": $scope.pairs.pair
                        }
                    }
                },
                "size": 0,
                "aggs": {
                    "subgenres": {
                        "terms": {
                            "field": "subgenre",
                            "size": 100
                        },
                        "aggs": {
                            "data": {
                                "histogram": {
                                    "field": "year",
                                    "interval": $scope.pairs.intervalSize,
                                    "min_doc_count": 0,
                                    "extended_bounds": {
                                        "min": 1600,
                                        "max": 1850
                                    }
                                },
                                "aggs": {
                                    "total": {
                                        "sum": {
                                            "field": "pairs-Body-Posemo.num_pairs"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }

        }).then(function (response) {
            $scope.pairs.genreData[pairLabel] = []
            data = response.aggregations.subgenres.buckets;
            for(var i=0; i < data.length; i++) {
                $scope.pairs.genreData[pairLabel].push({
                    "key": data[i].key, 
                    "values": data[i].data.buckets
                });
            }
        });
    }

    $scope.xFunction = function(){
        return function(d){
            return d.key;
        }
    };
    $scope.yFunction = function(){
        return function(d){
            if (d.total.value == 0) {
                return 0.0;
            }
            return d.doc_count/d.total.value;
        }
    };

    $scope.removePair = function(pairLabel) {
        var i = $scope.pairs.pairs.indexOf(pairLabel);
        $scope.pairs.pairs.splice(i, 1);

        // remove from data
        $scope.pairs.data = $scope.pairs.data.filter(function (el) {
            return el.key !== pairLabel;
        });

        // remove from genre data
        delete $scope.pairs.genreData[pairLabel];
    }
});

// Filter to remove illegal character from html id attributes
embEmApp.filter('clean', function() {
      return function(input, clean) {
          return input.replace(':', '').replace('@', '');
      };
});
