from game import Game
import tkinter as tk 


# in progress - utility function for game customization menu 
def show_option_menu():

	window = tk.Tk()
	window.title("Customize your game")
	window.geometry('500x400')

	row_count_label = tk.Label(window, text="Rows: ")
	row_count_label.pack()


	# text box for row count 
	row_count = tk.Text(window, height=1)
	row_count.pack()
	m = int(row_count.get("1.0","end"))

	column_count_label = tk.Label(window, text="Columns: ")
	column_count_label.pack()

	# text box for column count
	column_count = tk.Text(window, height=1)
	column_count.pack()
	n = int(column_count.get("1.0","end"))

	vic_length_label = tk.Label(window, text="Length of winning row: ")
	vic_length_label.pack()

	# text box for victory length
	vic_length = tk.Text(window, height=1)
	vic_length.pack()
	k = int(vic_length.get("1.0","end"))

	num_players_label = tk.Label(window, text="Players: ")
	num_players_label.pack()

	# text box for number of players 
	num_players = tk.Text(window, height=1)
	num_players.pack()
	p = int(num_players.get("1.0","end"))

	'''
	not quite sure how to escape this menu 
	def end_customization(flg):
		flg = False

	flag = True
	while flag == True:
		finish_customizing = tk.Button(window, text = "Finish customizing", width=50, command = end_customization(flag))
		finish_customizing.pack(anchor = tk.CENTER, expand = True)
	'''

	return m, n, k, p



# build a new game based on user input within GUI
def new_game():


	m, n, k, p = show_option_menu()
	# add way to list player names according to value of p 

	mrgame = Game(m, n, k, "player", "names") # etc ...
	btn_listen = tk.Button(window, text = "Start Game", width=50, command = mrgame.run_game)
	btn_listen.pack(anchor = tk.CENTER, expand = True)



def main():


	tictactoe = Game(3, 3, 3, "me", "you")
	gomoku = Game(10, 10, 5, "me", "you")
	

	# opens the application window
	window = tk.Tk()
	window.title("Tic Tac Toe (Engorged)")
	window.geometry('1000x600')

	new_game_btn = tk.Button(window, text = "New Game (work in progress)", width=50, command = new_game)
	start_game_btn = tk.Button(window, text = "Start Game (defaults to gomoku)", width=50, command = gomoku.run_game)
	
	new_game_btn.pack(anchor = tk.CENTER, expand = True)
	start_game_btn.pack(anchor = tk.CENTER, expand = True)

	window.mainloop()


if __name__ == '__main__':
	main()
