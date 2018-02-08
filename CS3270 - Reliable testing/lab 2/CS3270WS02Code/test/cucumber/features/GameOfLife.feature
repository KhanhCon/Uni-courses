Feature: Game of Life

Title: Student plays the Game of Life

  Scenario: Set a cell
    Given a grid with 3 rows and 3 columns
    When the cell at 2, 2 is set alive
    Then the cell at 2, 2 should be alive

  Scenario: Kill a loner
    Given a grid with 3 rows and 3 columns
    And the cell at 2, 2 is set alive
    When the cells are mutated
    Then all the cells should be dead

