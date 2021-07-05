package controller;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import model.SummaryPanels;
import model.interfaces.GameEngine;
import view.DiceGameFrame;
import view.DropDownMenu;
import view.PlayerDialog;
import view.SummaryPanel;

public class RemovePlayer implements ActionListener{
	private GameEngine gameEngine;
	private DiceGameFrame frame;
	private DropDownMenu menu;
	private SummaryPanel panel;
	private SummaryPanels summaryPanels;
	
	public RemovePlayer(GameEngine gameEngine, DiceGameFrame frame, DropDownMenu menu, SummaryPanel panel, SummaryPanels summaryPanels) {
		this.gameEngine = gameEngine;
		this.frame = frame;
		this.menu = menu;
		this.panel = panel;
		this.summaryPanels = summaryPanels;
	}

	@Override
	public void actionPerformed(ActionEvent e) {
		PlayerDialog playerDialog = new PlayerDialog(gameEngine, frame);
		playerDialog.removePlayer();
		

		for(int i = 0; i < gameEngine.getAllPlayers().size(); ++i) {
			String id = String.valueOf(i);
			if(gameEngine.getPlayer(id).getPlayerName().equals(playerDialog.getRemovePlayer())) {
				gameEngine.removePlayer(gameEngine.getPlayer(id));
				menu.removeItemAt(i);
				panel.remove(summaryPanels.getSummaryPanel(i));
			}
		}
		
	}
	
}
