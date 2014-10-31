var embEmApp = angular.module('embEmApp', []);

// set csrftoken for Django
embEmApp.config(['$httpProvider', function($httpProvider){
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
}]);

embEmApp.controller('EntitiesCtrl', function ($scope, $http, $location){
    $scope.query = '';
    $scope.results = [];
    $scope.mainCat = '';
    $scope.compareWith = [];
    $scope.statistics = [];
    $scope.base_url = 'http://'+$location.host()+':'+$location.port();
    $http.get($scope.base_url+'/entity_vis/entity_categories').success(function (data){
        $scope.categories = data.hits.hits;
        console.log($scope.categories);
    });

    $scope.searchFn = function (value, index){
        if( !$scope.query ){ return false; }
        var re = new RegExp($scope.query, 'i');
        return (re.test(value.fields.name.join(' ')));
    }
    $scope.setMainCat = function(cat) {
        $scope.mainCat = cat;
        $scope.getEntityStatisticsTitle('bred001moor01');
    }
    $scope.removeMainCat = function() {
        $scope.mainCat = '';
        $scope.getEntityStatisticsTitle('bred001moor01');
    }
    $scope.addToCompareWith = function(cat) {
        if($scope.compareWith.indexOf(cat) == -1){
            $scope.compareWith.push(cat);
        }
        $scope.getEntityStatisticsTitle('bred001moor01');
    }
    $scope.removeFromCompareWith = function(cat) {
        var i = $scope.compareWith.indexOf(cat);
        $scope.compareWith.splice(i, 1);
        $scope.getEntityStatisticsTitle('bred001moor01');
    }
    $scope.getEntityStatisticsTitle = function(title_id){
        var url = $scope.base_url+'/corpus/entity_stats/'+title_id+'/';
        if($scope.mainCat){
            var categories = [$scope.mainCat].concat($scope.compareWith);
        } else {
            var categories = $scope.compareWith;
        }
        console.log(categories);
        $http.post(url, {categories: categories}).
            success(function (data){
                console.log(data);
                $scope.statistics = data;
        });
    }
});
