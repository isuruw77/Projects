package controller;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import model.SummaryPanels;
import model.interfaces.GameEngine;
import view.DiceGameFrame;
import view.PlayerDialog;

public class PlaceBet implements ActionListener {
	private GameEngine gameEngine;
	private DiceGameFrame frame;
	private SummaryPanels summaryPanels;
	
	public PlaceBet(GameEngine gameEngine, DiceGameFrame frame, SummaryPanels summaryPanels) {
		this.gameEngine = gameEngine;
		this.frame = frame;
		this.summaryPanels = summaryPanels;
	}
	
	@Override
	public void actionPerformed(ActionEvent e) {
		PlayerDialog playerDialog = new PlayerDialog(gameEngine, frame);
		playerDialog.placeBet();
		
		
		for(int i = 0; i < gameEngine.getAllPlayers().size(); ++i) {
			String id = String.valueOf(i);
			if(gameEngine.getPlayer(id).getPlayerName().equals(playerDialog.getPlaceBetName())) {
				gameEngine.placeBet(gameEngine.getPlayer(id), playerDialog.getBet());
				
				
				summaryPanels.getSummaryPanel(i).setBet(String.valueOf(playerDialog.getBet()));
			}
		}
		
	}

}
