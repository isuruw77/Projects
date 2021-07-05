package model;

public class SinglePlayer {

	private String id;
	private String name;
	
	public SinglePlayer(String id, String name) {
		this.id = id;
		this.name = name;
	}
	
	@Override
	public String toString() {
		return id;
	}
	
	public String getID() {
		return id;
	}
	
	public String getName() {
		return name;
	}

	
}
