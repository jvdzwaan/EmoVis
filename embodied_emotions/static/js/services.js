embEmApp.factory('EmbEmDataService', function ($http, $q) {

    return {
        // get wordcloud data for a title
        getTitleWordcloudData: function (titleId, categories) {
            var deferred = $q.defer();
            $http.post('corpus/titles/'+titleId+'/wordcloud/', {categories: categories})
                .success(function (data) {
                    console.log('wordcloudData');
                    console.log(data);
                    deferred.resolve(data);
                }).error(function (error) {
                    deferred.reject(error);
                    console.error(error);
                });
            return deferred.promise;
        }
    }

});

embEmApp.service('es', function(esFactory) {
      return esFactory({ host: 'localhost:9200' });
});
