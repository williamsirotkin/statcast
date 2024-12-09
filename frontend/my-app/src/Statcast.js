import React, {useState} from 'react';
import SearchBar from './SearchBar.js'
import Stats from './Stats.js';


function StatCast() {
  const [player, setPlayer] = useState('');
  const handleSearch = (name) => {
    setPlayer(name);
};
  return (
      <div className="container mx-auto p-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-4">Welcome to Statcast!</h1>
        <p className="text-gray-600">
          Lookup any player's stats from April 1st to April 14th in 2018 using the search bar and entering their full name (<a 
  href="http://127.0.0.1:5000/getData/playerList" 
  target="_blank" 
  rel="noopener noreferrer"
>
  Player List
</a>)
        </p>
        <br>
        </br>
        <SearchBar setPlayer={handleSearch}/>
        <Stats player={player}/>
      </div>
  );
};

export default StatCast;