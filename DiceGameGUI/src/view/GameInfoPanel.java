package view;

import java.awt.GridLayout;

import javax.swing.AbstractButton;

import javax.swing.JButton;


import javax.swing.JToolBar;

import controller.AddPlayer;
import controller.PlaceBet;
import controller.RemoveBet;
import controller.RemovePlayer;
import controller.RollDie;
import model.SummaryPanels;
import model.interfaces.GameEngine;

@SuppressWarnings("serial")
public class GameInfoPanel extends JToolBar {
	
	public GameInfoPanel(GameEngine gameEngine, DiceGameFrame frame,SummaryPanel panel) {
		DropDownMenu menu = new DropDownMenu();
		SummaryPanels summaryPanels = new SummaryPanels();
		
		setLayout(new GridLayout(0,4));
		
		AbstractButton addPlayer = new JButton("Add Player");
		add(addPlayer);
		AddPlayer addPlayerController = new AddPlayer(gameEngine, frame, menu, panel, summaryPanels);
		addPlayer.addActionListener(addPlayerController);
		
		AbstractButton removePlayer = new JButton("Remove Player");
		add(removePlayer);
		removePlayer.addActionListener(new RemovePlayer(gameEngine, frame, menu, panel, summaryPanels));
		
		AbstractButton placeBet = new JButton("Place Bet");
		add(placeBet);
		placeBet.addActionListener(new PlaceBet(gameEngine, frame, summaryPanels));
		
		AbstractButton removeBet = new JButton("Remove Bet");
		add(removeBet);
		removeBet.addActionListener(new RemoveBet(gameEngine, frame, summaryPanels));
		
		AbstractButton rollDie = new JButton("Roll");
		add(rollDie);
		rollDie.addActionListener(new RollDie(gameEngine, menu));
		
		add(menu);
	}
}
