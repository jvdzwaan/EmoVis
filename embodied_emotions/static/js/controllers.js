var embEmApp = angular.module('embEmApp', []);

embEmApp.controller('EntitiesCtrl', function ($scope, $http){
    $scope.query = '';
    $scope.results = [];
    $scope.mainCat = '';
    $scope.compareWith = [];
    var sites_url = 'data/sites.json';
    $http.get('entity_categories').success(function (data){
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
});
