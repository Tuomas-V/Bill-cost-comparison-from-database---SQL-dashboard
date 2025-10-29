# Bill cost comparison from relational database - SQL dashboard
Comparison of electricity &amp; gas bills to heating bill costs from open bill data of Raahe city 2024

<img src="Screenshots/output1.png">

This graph reads data from an local mariadb database and automatically displays needed data.</br>
The displayed values (including the year in the title) are fully automatic, depending on the data queried from the database.

The data was sourced from [avoindata.fi](https://www.avoindata.fi/) in the form of excel sheet with nearly fifty thousand rows of bill data.
Using python the data was split into several CSV files so they could then be inputted into a relational database, thus removing the need to repeat duplicate data on every row.

Data sources:</br>
- [Raahen kaupungin ostolaskut 2024](https://www.avoindata.fi/data/fi/dataset/raahen-kaupungin-ostolaskut-2024)
