package view;


import javax.swing.JComboBox;
import javax.swing.JOptionPane;
import javax.swing.JTextField;
import model.interfaces.GameEngine;

@SuppressWarnings("serial")
public class PlayerDialog extends JOptionPane {
	private String addPlayerName;
	private int addPlayerPoints;
	private String removePlayer;
	private GameEngine gameEngine;
	private DiceGameFrame frame;
	private String placeBetName;
	private int addBet;
	private String removeBet;
	
	public PlayerDialog(GameEngine gameEngine, DiceGameFrame frame) {
		this.gameEngine = gameEngine;
		this.frame = frame;
	}

	
	public void addPlayer() {
		
		JTextField name = new JTextField();
		JTextField points = new JTextField();
		
		
		Object[] fields = {
				"Name", name,
				"Betting Points", points
		};
		
		int input = showConfirmDialog(frame, fields, "Add Player", OK_CANCEL_OPTION, PLAIN_MESSAGE);
		
		if(input == OK_OPTION) {
			if(!name.getText().isEmpty()  && !points.getText().isEmpty()) {
				this.addPlayerName = name.getText();
				this.addPlayerPoints = Integer.parseInt(points.getText());
			}else {
				System.out.println("EMPTY!");
				addPlayer();
			}
		}
	}
	
	public void removePlayer() {
		String[] playerNames = new String[gameEngine.getAllPlayers().size()];
		
		for(int i = 0; i < gameEngine.getAllPlayers().size(); ++i) {
			String id = String.valueOf(i);
			playerNames[i] = gameEngine.getPlayer(id).getPlayerName();
		}
		
		
		String input = (String)showInputDialog(frame, "Select Player to Remove","Remove Player", PLAIN_MESSAGE, null, playerNames, "Player");
		
		if(input != null) {
//			System.out.println(removePlayer);
			removePlayer = input;
		}
	}
	
	
	public void placeBet() {
		String[] playerNames = new String[gameEngine.getAllPlayers().size()];
		for(int i = 0; i < gameEngine.getAllPlayers().size(); ++i) {
			String id = String.valueOf(i);
			playerNames[i] = gameEngine.getPlayer(id).getPlayerName();
		}
		
		JComboBox<?> name = new JComboBox<String>(playerNames);
		JTextField bet = new JTextField();
		
		Object[] fields = {
				"Name", name,
				"Betting Points", bet
		};
		
		int input = showConfirmDialog(frame, fields, "Add Player", OK_CANCEL_OPTION, PLAIN_MESSAGE);
		if(input == OK_OPTION) {
			if(!bet.getText().isEmpty()) {
				this.placeBetName = name.getSelectedItem().toString();
				this.addBet = Integer.parseInt(bet.getText());
				
			}else {
				placeBet();
			}
		
		}
		
	}
	
	public void removeBet() {
		String[] playerNames = new String[gameEngine.getAllPlayers().size()];
		
		for(int i = 0; i < gameEngine.getAllPlayers().size(); ++i) {
			String id = String.valueOf(i);
			playerNames[i] = gameEngine.getPlayer(id).getPlayerName();
		}
		
		
		String input = (String)showInputDialog(frame, "Select Player to Remove Bet","Remove Bet", PLAIN_MESSAGE, null, playerNames, "Player");
		
		if(input != null) {
			System.out.println(removePlayer);
			removeBet = input;
		}
	}
	
	public String getName() {
		return addPlayerName;
	}
	
	public int getPoints() {
		return addPlayerPoints;
	}
	
	public String getRemovePlayer() {
		return removePlayer;
	}
	
	public String getPlaceBetName() {
		return placeBetName;
	}
	
	public int getBet() {
		return addBet;
	}
	
	public String removeBetName() {
		return removeBet;
	}
}
