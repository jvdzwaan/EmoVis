var embEmApp = angular.module('embEmApp', ['ngRoute']);

embEmApp.config(function($httpProvider, $routeProvider, $locationProvider){
    // set csrftoken for Django
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';

    // get params from the url
    $routeProvider.when('/corpus/title/:titleId/', {
        controller: 'EntitiesCtrl'
    });

    $locationProvider.html5Mode(true);
});

embEmApp.controller('EntitiesCtrl', function ($scope, $route, $routeParams, $location, $http){
    $scope.query = '';
    $scope.results = [];
    $scope.mainCat = '';
    $scope.compareWith = [];
    $scope.statistics = [];
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
        $scope.getEntityStatisticsTitle($routeParams.titleId);
        $scope.getEntityStatisticsCorpus();
    }
    $scope.removeMainCat = function() {
        $scope.mainCat = '';
        $scope.getEntityStatisticsTitle($routeParams.titleId);
        $scope.getEntityStatisticsCorpus();
    }
    $scope.addToCompareWith = function(cat) {
        if($scope.compareWith.indexOf(cat) == -1){
            $scope.compareWith.push(cat);
        }
        $scope.getEntityStatisticsTitle($routeParams.titleId);
        $scope.getEntityStatisticsCorpus();
    }
    $scope.removeFromCompareWith = function(cat) {
        var i = $scope.compareWith.indexOf(cat);
        $scope.compareWith.splice(i, 1);
        $scope.getEntityStatisticsTitle($routeParams.titleId);
        $scope.getEntityStatisticsCorpus();
    }
    $scope.getEntityStatisticsTitle = function(title_id){
        if($scope.mainCat){
            var categories = [$scope.mainCat].concat($scope.compareWith);
        } else {
            var categories = $scope.compareWith;
        }
        console.log(categories);
        $http.post('corpus/entity_stats/'+title_id+'/', {categories: categories}).
            success(function (data){
                console.log(data);
                $scope.statistics = data;
        });
    }
    $scope.getEntityStatisticsCorpus = function(){
        if($scope.mainCat){
            var categories = [$scope.mainCat].concat($scope.compareWith);
        } else {
            var categories = $scope.compareWith;
        }
        console.log(categories);
        $http.post('corpus/entity_stats/', {categories: categories}).
            success(function (data){
                console.log(data);
                $scope.entityStatistics = data;
        });
    }
});
