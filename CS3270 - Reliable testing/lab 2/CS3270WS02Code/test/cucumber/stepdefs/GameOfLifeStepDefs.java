package stepdefs;

import cucumber.api.java.en.Given;
import cucumber.api.java.en.Then;
import cucumber.api.java.en.When;
import uk.ac.aston.gameOfLife.GameOfLifeGrid;

import static org.junit.Assert.assertEquals;

/**
 * A class with JBehave steps
 * 
 * @author Prins Butt, Errol Thompson
 */
public class GameOfLifeStepDefs {
    private GameOfLifeGrid grid;

    @Given("^a grid with (\\d+) rows and (\\d+) columns$")
    public void aGridWith(int r, int c) {
        grid = new GameOfLifeGrid(r, c);
    }

    @Given("^the cell at (\\d+), (\\d+) is set (alive|dead)$")
    public void theCellIs(int r, int c, String status) {
        grid.setCellStatus(r, c, status.equals("alive"));
    }

    @When("^the cells are mutated$")
    public void cellsAreMutated() {
        grid.mutateCells();
    }

    @Then("^the cell at (\\d+), (\\d+) should be (alive|dead)$")
    public void theCellShouldBe(int r, int c, String status) {
        assertEquals(status.equals("alive"), grid.isAlive(r, c));
    }
    
    @Then("^all the cells should be (alive|dead)$")
    public void allTheCellsShouldBe(String status) {
    	assertEquals(!status.equals("alive"), grid.areAllCellsDead());
    }
}