<h2> DataScience Project on Esport Team Compatability (League of Legends) </h2>
<div>
    <section name="summary">
      <p>
        Program designed to statistically model winrates--in League of Legends--corresponding between characters 
        if given player name(s). This would help to determine whether meta-analysis assumptions would fit your 
        team or you as a player and how one (team or player) could adapt for the future given current performance 
        with certain champions (characters) they want to focus on. 
      </p>
      <h4> Technology Stack: </h4>
        <ul> 
          <li> Python </li>
          <li> Numpy </li>
          <li> Pandas </li>
          <li> Matlab plot </li>
          <li> Seaborn </li> 
        <ul> 
    </section>
    <hr>
    <img src="HeatmapExample01.png" alt="Heatmap Image Example" title="Heatmap Example">
    <p> <span style="font-size:0.75em"> Image sourced 223 games coming from Tyler1 & Rosethorn's games. 
    <br> Note the blue is null/no games found with that champion combination. 
    <span> </p> 
    <hr>
    <section name="how-to-use">
      <h4> How To Use And Set Up </h4> 
      <p>
        This runs on an IDE and does not have a UI set up. To use, you have to have the technology stack
       (programming IDE that can run Python with the listed packages installed) to be able to run this. 
        <br>
      <h4> Once you have that: </h4>
      </p> 
      <ol> 
        <li> Make sure to input Riot's Developer API Key (Get that from here: https://developer.riotgames.com/ )
        <li> Input the summoner names you want data collected about in the "list_of_names_to_manipulate" array. 
        <li> If you're running this for the first time 
          <ul>
             <li> IT WILL TAKE TIME -- Riot API can only be accessed so much per minute or else it will give error.
             <li> Make sure that all of the methods (at the bottom of the program in the try - catch) are not commented out and they are set to run. 
          </ul>
         <li> If you're not running this for the first time and just want to display the heatmap, 
           <ul>
             <li> Comment out every method besides the last (that is present in the try-catch) 
          </ul>
      <ol>
    </section>
    <hr>
      <section name="short-comings">
        <h3> Short-comings Note: </h3>
        <p>
          The short-comings of this software is that it does not give a direct solution, but helps to determine
          the problems within (team's or player's) gameplay. 
        </p>
    </section>
    <hr>
      <section name="notes"> 
        <h3> Notes for future development: </h3>
         <ul>
           <li> Program needs a UI / UX to be more user-friendly. </li>
           <li> Program files can be better maanged by concatenating the file names with the list of names taken and checking to see if they exist. </li>
           <li> Program files can be further improved by not being only specific to the local path </li> 
           <li> Riot Developer Key Must be reset every 24 hours (since this is just temporary program and not for production)
           <li> Program speed could be optimized by manipulating how often data is fetched by Riot's API system. 
           <li> Program needs better way of managing if you're running it for the first time, want to source files again, or just looking at heatmap.
         </ul>
      </section>
    <hr>
    <section name="copyright">
    <h3> MIT License </h3>
    <p> 
        Copyright (c) [2022] [David Thompson]
        <br>
        <br>
        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:
        <br>
        <br>
        The above copyright notice and this permission notice shall be included in all
        copies or substantial portions of the Software.
        <br>
        <br>
        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
        SOFTWARE.
      </p>
    </section>
<div> 
