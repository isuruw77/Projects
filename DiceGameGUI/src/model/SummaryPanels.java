package model;

import java.util.ArrayList;

import view.PlayerSummary;

public class SummaryPanels {
	private ArrayList<PlayerSummary> summary = new ArrayList<PlayerSummary>();
	
	public SummaryPanels() {
		
	}
	
	public PlayerSummary getSummaryPanel(int index) {
		return summary.get(index);
	}
	
	public void addPanels(PlayerSummary playerSummary) {
		summary.add(playerSummary);
	}
}
