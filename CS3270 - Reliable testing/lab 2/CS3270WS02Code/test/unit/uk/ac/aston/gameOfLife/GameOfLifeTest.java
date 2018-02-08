package uk.ac.aston.gameOfLife;

import org.junit.Test;

import static junit.framework.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

/**
 * @author kiwi-et
 * @version 30/01/2014 14:28
 */
public class GameOfLifeTest {
    @Test
    public void killALoner() {
        // Given
        GameOfLifeGrid grid = new GameOfLifeGrid(3, 3);
        grid.setCellStatus(2, 2, true);
        // Verify setup
        assertTrue(grid.isAlive(2, 2));
        // When mutated
        grid.mutateCells();
        // Then
        assertTrue(grid.areAllCellsDead());
        assertEquals(2, 2);
    }
}
