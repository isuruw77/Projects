package view;

import java.awt.GridLayout;

import javax.swing.BorderFactory;
import javax.swing.JLabel;
import javax.swing.JPanel;

@SuppressWarnings("serial")
public class PlayerSummary extends JPanel {
	private JLabel bet;
	private JLabel die1;

	public PlayerSummary() {
		setLayout(new GridLayout(0,2));
		setBorder(BorderFactory.createTitledBorder("Player"));
		
		add(new JLabel("Bet: "));
		bet = new JLabel("Player Bet");
		add(bet);
		
		add(new JLabel("Points: "));
		add(new JLabel("Player Points"));
		
		add(new JLabel("Die 1: "));
		die1 = new JLabel("Player Die 1");
		add(die1);
		 
		add(new JLabel("Die 2: "));
		add(new JLabel("Player Die 2"));
		
		add(new JLabel("Total: "));
		add(new JLabel("Player Total"));
		
	}
	
	public void setName(String playerName) {
		setBorder(BorderFactory.createTitledBorder(playerName));
	}
	
	public void setBet(String betValue) {
		bet.setText(betValue);
	}
	
	public void updateDie1(String dieValue) {
		die1.setText(dieValue);
	}
}
