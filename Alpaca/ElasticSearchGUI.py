import PySimpleGUI as sg


layout = [
	[sg.Text("Search Stock Information")],
	[sg.Column(layout=[
		[sg.Checkbox("Name", key = "name")],
		[sg.Checkbox("Timing", key = "timing")],
		[sg.Checkbox("Industry", key = "industry")],
		[sg.Checkbox("Ticker", key = "ticker")],
		[sg.Checkbox("Price Range", key = "price range")]
	]),
	[sg.Text('Search ', size = (15, 1)), sg.Input(expand_x = True)],
	[sg.Button('Submit'), sg.Button('Cancel')]]
]

window = sg.Window(title="Stock Search", layout = layout, margins=(400, 200))

while True:
	event, values = window.read()
	values_list = list(values.items())

	if event == sg.WIN_CLOSED or event == 'Cancel':
		break

	if event == 'Submit':
		selected_options = [values_list[0][1], values_list[1][0], values_list[2][0], values_list[3][0], values_list[4][0], values_list[5][0]]
		sg.popup(f"Search String: {', '.join(selected_options)}")

window.close()
