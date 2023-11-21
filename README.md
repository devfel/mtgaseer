<p align="center">
  <a href="https://devfel.com/" rel="noopener">
 <img src="https://devfel.com/imgs/devfel-logo-01.JPG" alt="DevFel"></a>
</p>

# 🎴 MTGA Seer 🔮<br> A "Magic: The Gathering" Card Data Analysis Tool

This tool is designed to analyze and display statistics related to Magic: The Gathering Arena (MTG, MTGA) cards. It leverages a graphical user interface (GUI) built with Tkinter to enable users to interactively explore card data. The tool is intended to be used by players of the MTG Arena video game to help them make more informed decisions when drafting cards in the game's limited format. The tool is also useful for players of the physical MTG card game. The tool is built using Python 3.8.5 and the 17lands.com MTG card data set.

## Features

- Load and process MTG card data from CSV files.
- Interactive search and filtering based on card name, color, and rarity.
- Display key statistics like average pick turn, win rates, and games played.
- Support for viewing data on specific color combinations and their win rates.

## Installation

Before running the tool, ensure that Python is installed on your system along with the following packages:

- `tkinter` for the GUI.
- `pandas` for data manipulation.
- `math` for mathematical operations.

You can install pandas using pip:

```
pip install pandas
```

## Usage

1. Clone or download the repository to your local machine.
2. Place your MTG card data files (in CSV format) in an accessible directory.
3. Run the Python script:
   ```
   python main.py
   ```
4. Use the GUI to search for cards, sort table by columns, and analyze statistics.

## Data Files Format

The tool expects several CSV files, there are samples from 17lands.com in the `data` directory. Currently the tool expects the following files:

1. `card-ratings-2023-11-20.csv` - Contains the main card data.
2. `colors-2023-11-20.csv` - Contains color-specific win rate data.
3. `card-ratings-2023-11-20{(COLORCOMBINATION)}.csv` - Contains the card data for each color combination.

Ensure the CSV files are properly formatted and located in the correct directory.

## Contributions

Contributions to this project are welcome. Please fork the repository, make your changes, and submit additions.

## Aknowledgements

This project use data from [17lands.com](https://www.17lands.com/), a website that provides MTG card data and analytics for the MTG Arena video game. The data is collected from the game's limited format, which is a draft format where players build decks from a limited pool of cards. The data is collected from players who use the 17lands.com tracker app to record their games. The data is then aggregated and made available for download on the website.

## License

This project is open-sourced under the MIT License.

## TODO List

For now everything is in the main.py, I intend to refactor it into multiple files.

<br>
[ ] TODO: Refactor code into multple files<br>
[ ] TODO: Read Player.Log to create aditional tab for automatic suggestion<br>
[ ] TODO: Add a Fixed Card Ranking, Based on the GIH WR<br>
[ ] TODO: TAB1: Add Filter by Color (Actually is the Choosen one and change the Data)<br>
[ ] TODO: TAB1: Add Filter by Rarity<br>
<br>
[X] TODO: Search has to be dinamic (when I type it search)<br>
[X] TODO: Columns have to be Sortable<br>
[X] TODO: Search Button Not Necessary<br>
[X] TODO: IWD Column has to be added<br>
[X] TODO: Rarity Column has to be added<br>
[X] TODO: Color Column has to be added<br>
[X] TODO: The columns title not correspond to the data<br>
[X] TODO: make styling better<br>
[X] TODO: Do second phase with colors (select color and check % Win Rate of Combinations)<br>
[X] TODO: Add sroll Bar<br>
[X] TODO: IWD Sorting is bugged, need fix<br>
[X] TODO: Better size for columns, make it centralized.<br>
[X] TODO: Create a Folder for the Data and put all Excel Files in there. <br>
[X] TODO: Change the code to read from the new data folder.<br>
