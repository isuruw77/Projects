package controller;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import model.SummaryPanels;
import model.interfaces.GameEngine;
import view.DiceGameFrame;
import view.PlayerDialog;

public class RemoveBet implements ActionListener {
	private GameEngine gameEngine;
	private DiceGameFrame frame;
	private SummaryPanels summaryPanels;
	
	public RemoveBet(GameEngine gameEngine, DiceGameFrame frame, SummaryPanels summaryPanels) {
		this.gameEngine = gameEngine;
		this.frame = frame;
		this.summaryPanels = summaryPanels;
	}
	@Override
	public void actionPerformed(ActionEvent e) {
		PlayerDialog playerDialog = new PlayerDialog(gameEngine, frame);
		playerDialog.removeBet();
		
		for(int i = 0; i < gameEngine.getAllPlayers().size(); ++i) {
			String id = String.valueOf(i);
			if(gameEngine.getPlayer(id).getPlayerName().equals(playerDialog.getRemovePlayer())) {
				gameEngine.getPlayer(id).resetBet();
				
				summaryPanels.getSummaryPanel(i).setBet(String.valueOf(gameEngine.getPlayer(id).getBet()));
			}
		}
	}

}
