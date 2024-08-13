import os


# Abre o arquivo ou aplicativo
# É necessario ter o atalho do app para execultar o codigo
os.startfile("C:\ProgramData\Microsoft\Windows\Start Menu\Programs\GazePointer.lnk")
try:
    os.startfile(".\GazeFlowAPI.html")
except Exception as e:
    print(e)

