package controller;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;


import model.SimplePlayer;
import model.SinglePlayer;
import model.SummaryPanels;
import model.interfaces.GameEngine;
import model.interfaces.Player;
import view.DiceGameFrame;
import view.DropDownMenu;
import view.PlayerDialog;
import view.PlayerSummary;
import view.SummaryPanel;


public class AddPlayer implements ActionListener {
	private GameEngine gameEngine;
	private DiceGameFrame frame;
	private DropDownMenu menu;
	private SummaryPanel panel;
	private SummaryPanels summaryPanels;
	private int playerCount;
	
	public AddPlayer(GameEngine gameEngine, DiceGameFrame frame, DropDownMenu menu, SummaryPanel panel, SummaryPanels summaryPanels) {	
		this.gameEngine = gameEngine;
		this.frame = frame;
		this.menu = menu;
		this.panel = panel;
		this.summaryPanels = summaryPanels;
	}
	
	@Override
	public void actionPerformed(ActionEvent e) {
		PlayerDialog playerDialog = new PlayerDialog(gameEngine,frame);
		playerDialog.addPlayer();
		
		if(playerDialog.getName() != null && playerDialog.getPoints() != 0) {
			System.out.println(playerDialog.getName());
			System.out.println(playerDialog.getPoints());
			
			playerCount = gameEngine.getAllPlayers().size();
			String id = String.valueOf(playerCount);
			System.out.println(id);
			
			Player player = new SimplePlayer(id, playerDialog.getName(), playerDialog.getPoints());
			createPlayers(player);
			menu.addItem(new SinglePlayer(playerDialog.getName(), id));
			
			createSummaryPanel(playerDialog.getName());

		}
			
	}
	
	public void createPlayers(Player player) {
		gameEngine.addPlayer(player);	
	}
	
	public void createSummaryPanel(String name) {

		summaryPanels.addPanels(new PlayerSummary());
		panel.add(summaryPanels.getSummaryPanel(playerCount));
		summaryPanels.getSummaryPanel(playerCount).setName(name);
	}
	

}
