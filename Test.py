import GUI
import ClientHandler


ClientHandler = ClientHandler.ClientHandler
Notepad = GUI.Notepad

host = ClientHandler("Alex")
host.is_host = True
host.attempt_connection()
host_gui = Notepad(host)
host.connect_doc("12345")
host_gui.run()


