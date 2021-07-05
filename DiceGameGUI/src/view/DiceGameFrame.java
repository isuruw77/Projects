package view;

import java.awt.BorderLayout;

import javax.swing.JFrame;

import model.interfaces.GameEngine;


@SuppressWarnings("serial")
public class DiceGameFrame extends JFrame {
	
	
	public DiceGameFrame(GameEngine gameEngine) {
		super("Dice Game");
		
		SummaryPanel panel = new SummaryPanel();
		setDefaultCloseOperation(EXIT_ON_CLOSE);
		setLayout(new BorderLayout());
		
		add(new GameInfoPanel(gameEngine, this, panel), BorderLayout.NORTH);
		add(panel, BorderLayout.WEST);
		
		setSize(900, 650);
		setVisible(true);
	}
	


}
