
# WetChatVisual Project

## Installation and Usage Guide

### 1. Install the Required Dependencies

First, make sure you have Python and `pip` installed on your machine.

1. **Clone the Repository:**
   Open your terminal and run the following command to clone the project repository to your local machine:

   ```bash
   git clone https://github.com/XinLang2019/WetChatVisual.git
   cd WetChatVisual
   ```

2. **Create a Virtual Environment (optional but recommended):**
   It's recommended to use a virtual environment to keep the dependencies isolated. You can create a virtual environment using the following command:

   ```bash
   conda create -n wechatvisual python=3.8
   ```

   activate the conda environment:
   ```bash
   conda activate wechatvisual 
   ```

3. **Install the Required Python Packages:**
   Now that the virtual environment is activated (if you chose to use it), you can install all the dependencies listed in the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

   This will install all the required packages that the project depends on.

---

### 2. Export Chat Data

- Use an **incognito software** tool to export the required chat data. The data should be in the correct format (such as JSON). Refer to the documentation of the incognito software for instructions on how to export the chat data.(how to exported wechat data, you can reference this rpo: https://github.com/LC044/WeChatMsg.git).

---

### 3. Place Data in the `data` Folder

- After exporting the wechat data, move or copy the exported data files into the `data` folder of the project.
   Ensure the data files are placed in the correct folder (`data/`) to be processed by the script.

---

### 4. Run the Main Python Script

- After placing the exported chat data in the `data` folder, you can run the main Python script. This script will process the data and generate the results.

   Run the following command in your terminal:

   ```bash
   python scripts/main.py
   ```

   The script will start executing, and the processing of chat data will begin according to the logic defined in the project.

---

## Additional Information

- **Log Files**: If you encounter any issues or errors, check the log files in the `logs` folder for further details.
  
- **Configuration Files**: You can modify the project settings by editing the configuration files located in the `config/` folder. 

- **Troubleshooting**: If you face any difficulties during the setup or usage, check the issues section on the GitHub repository or open a new issue.

---

## Contributing

We welcome contributions to improve the project! If you have ideas for improvements or find a bug, feel free to fork the repository and submit a Pull Request, or open an issue if you're unsure how to proceed.

### How to Contribute:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Make changes and commit them.
4. Push the changes to your fork.
5. Create a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
