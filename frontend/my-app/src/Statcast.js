import React from 'react';
import SearchBar from './SearchBar.js'


function StatCast() {
  return (
      <div className="container mx-auto p-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-4">Welcome to Statcast!</h1>
        <p className="text-gray-600">
          Lookup any player's stats using the search bar and entering their full name!
        </p>
        <br>
        </br>
        <SearchBar/>
      </div>
  );
};

export default StatCast;