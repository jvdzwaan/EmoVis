var embEmApp = angular.module('embEmApp', ['ngRoute', 'nvd3ChartDirectives']);

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
    });

    $locationProvider.html5Mode(true);
});

embEmApp.controller('EntitiesCtrl', function ($scope, $route, $routeParams, $location, $http){
    $scope.query = '';
    $scope.mainCat = '';
    $scope.compareWith = [];
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

embEmApp.controller('TitleCtrl', function ($scope, $routeParams, $http){
    $scope.titleId = $routeParams.titleId;
    $scope.statistics = {};
    $scope.wordCloudData = [ 
        {
            "key": "waarheyt",
            "doc_count": 10,
            "score": 0.07493223057358994,
            "bg_count": 10
        },
        {
            "key": "wijsheyt",
            "doc_count": 9,
            "score": 0.06743900751623096,
            "bg_count": 9
        },
        {
            "key": "goedt",
            "doc_count": 15,
            "score": 0.061257775088170485,
            "bg_count": 26
        },
        {
            "key": "vruecht",
            "doc_count": 8,
            "score": 0.059945784458871935,
            "bg_count": 8
        },
        {
            "key": "goet",
            "doc_count": 36,
            "score": 0.053719266880172756,
            "bg_count": 141
        },
        {
            "key": "moytjes",
            "doc_count": 8,
            "score": 0.04705216176721062,
            "bg_count": 10
        },
        {
            "key": "segghen",
            "doc_count": 16,
            "score": 0.041271918358833336,
            "bg_count": 41
        },
        {
            "key": "moye",
            "doc_count": 5,
            "score": 0.03746611528679497,
            "bg_count": 5
        },
        {
            "key": "fray",
            "doc_count": 4,
            "score": 0.029972892229435968,
            "bg_count": 4
        },
        {
            "key": "waardich",
            "doc_count": 4,
            "score": 0.029972892229435968,
            "bg_count": 4
        }
    ];

   $scope.selectedCats = $scope.getSelectedCategories();

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
