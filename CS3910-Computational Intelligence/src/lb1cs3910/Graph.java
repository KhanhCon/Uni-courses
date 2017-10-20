package lb1cs3910;

public class Graph {

	private int numberOfCities;
	private int numberOfEdges;
	private int[][] adj;

	public Graph(int numberOfCities) {
		this.numberOfCities = numberOfCities;
		this.numberOfEdges = 0;
		this.adj = new int[numberOfCities][numberOfCities];
	}

	public int numberOfCities() {
		return numberOfCities;
	}

	public int numberOfEdges() {
		return numberOfEdges;
	}

	// add edge v-w
	public void addEdge(int x, int y, int length) {
		if (adj[x][y] != 0)
			numberOfEdges++;
		adj[x][y] = length;
		adj[y][x] = length;
	}

}
