<h1 align="center">Attacks Log Simulator</h1>
</br>
<p align="let">The productis an interactive Dash-based web application designed to simulate firewall and authentication logs which contatin the characteristics of various types of atttacks. This tool is ideal for cybersecurity training and demonstration purposes. It allows users to generate customised logs for different attacks, enhancing the understanding and preparedness against potential cyber threats.</p>
</br>
<h1 align="center">Instruction of Deploy</h1>
</br>
<p align="left">
1. Step 1: Visit the Official VS Code Website. Open your web browser and go to https://code.visualstudio.com/.
2. Step 2: Download VS Code. Click on the "Download" button. VS Code will automatically detect your operating system and provide you with the correct installer for Windows, macOS, or Linux.
3. Step 3: Install VS Code
Once downloaded, run the installer:
Windows: Double-click the .exe file and follow the instructions. Make sure to check the option to "Add to PATH" during installation.
macOS: Open the .dmg file and drag VS Code to the Applications folder.
Linux: You can use the package manager to install it. For example: sudo snap install code --classic
4. Go to the Python official website and download Python 3.7 or a later version. Windows Users: Make sure to select "Add Python to PATH" during the installation process.
5. Follow the installation instructions for your operating system. Once installed, verify the installation by running the following command in your terminal: python --version
6. Open a terminal (Command Prompt on Windows, Terminal on macOS/Linux), and run the following command to create a virtual environment: python3 -m venv venv
7. Activate the virtual environment:
  Whindows: venv\Scripts\activate
  Mac: source venv/bin/activate
8. Locate and open the VS Code application that you just installed.
9. On the left sidebar, click on the Extensions icon (it looks like four small squares).
10. Search for "Python" in the search bar and click Install to add the Python extension provided by Microsoft.
11. Press Ctrl + \`` (backtick) or navigate to View -> Terminal` to open the terminal within VS Code.
12. Clone the project repository. Command: git clone + link
13. While inside the project directory and with the virtual environment activated, run: pip install -r requirements.txt.
</p>
</br>
<h1 align="center">Instruction To Use</h1>
<p align="left">
1. In VS Code, right-click on the Test-Website.py file. Select "Run Code". This will automatically execute the script and provide a URL for accessing the website in the terminal.

2. Copy the provided URL (usually something like http://127.0.0.1:8050/) from the terminal and paste it into your web browser.

3. Choose the appropriate area based on the type of attacks logs you wish to generate.

4. Use the dropdown menus and input fields to set options such as protocol, service type, direction, and username. Each area will have different input requirements depending on the type of log being generated.

5. Click the "Generate Log" button for the selected type of log. The logs will be displayed in the respective output text area.
</p>


