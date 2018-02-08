package uk.ac.aston.gameOfLife;

/**
 * This class models a 2-D grid that can be used in the game of life
 *
 * @author Prins Butt
 */
public class GameOfLifeGrid {

    // A 2-D grid of cells
    private boolean[][] grid;

    /**
     * Creates a 2-D grid with the specified number of rows and columns
     *
     * @param rows the number rows in the grid
     * @param columns the number of columns in the grid
     */
    public GameOfLifeGrid(int rows, int columns) {
        grid = new boolean[rows+2][columns+2];
    }

    /**
     * Check the number of live neighbours
     */
    private int countAliveNeighbours(int row, int column) {
        return ((grid[row - 1][column - 1]) ? 1 : 0) +
                ((grid[row - 1][column]) ? 1 : 0) +
                ((grid[row - 1][column + 1]) ? 1 : 0) +
                ((grid[row][column - 1]) ? 1 : 0) +
                ((grid[row][column + 1]) ? 1 : 0) +
                ((grid[row + 1][column - 1]) ? 1 : 0) +
                ((grid[row + 1][column]) ? 1 : 0) +
                ((grid[row + 1][column + 1]) ? 1 : 0);
    }

    /**
     * Determines whether all the cells are dead
     *
     * @return true if all cells in the grid are dead
     */
    public boolean areAllCellsDead() {
        for (int row = 1; row < grid.length-1; row++) {
            for (int column = 1; column < grid[0].length-1; column++) {
                if (grid[row][column]) return false;                
            }
        }
        
        return true;
    }

    /**
     * Gets the status of a cell
     *
     * @param row the row number of the target cell
     * @param column the column number of the target cell
     * @return true if the cell is alive, false otherwise
     */
    public boolean isAlive(int row, int column) {
        return grid[row][column];
    }

    /**
     * Sets a cell in the grid to alive or dead
     *
     * @param row the row number of target cell
     * @param column the column number of the target cell
     * @param isAlive the new status of the target cell
     */
    public void setCellStatus(int row, int column, boolean isAlive) {
        grid[row][column] = isAlive;
    }

    /**
     * Mutate all the cells in the grid
     */
    public void mutateCells() {
        boolean result[][] = new boolean[grid.length][grid[0].length];

        for (int row = 1; row < grid.length - 1; row++) {
            for (int column = 1; column < grid[0].length - 1; column++) {
                
                // Get the number of alive neighbours
                int neighbours = countAliveNeighbours(row, column);
                
                // Rule 3: in all other cases, a cell dies or remains dead
                // Rule 1: a dead cell with exactly three live neighbours becomes a live cell (birth)
                result[row][column] = (!grid[row][column] && (neighbours == 3));
                
                // Rule 2: a live cell with two or three live neighbours stays alive (survival)
                result[row][column] = result[row][column] || (grid[row][column] &&
                        (neighbours >= 2 && neighbours <= 3));
            }
        }

        grid = result;
    }
}
