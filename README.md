# AIGM (AI Game Master)

AIGM is a Python-based role-playing game (RPG) that features a graphical user interface (GUI) built with Pygame and an integrated AI Dungeon Master (DM) powered by Ollama. The game allows players to manage their character, inventory, and interact with an AI that drives the narrative. Game data is persisted using a local SQLite database.

## Features

*   **Pygame GUI:** An interactive graphical interface for an immersive gaming experience.
*   **AI Dungeon Master:** Utilizes Ollama to generate dynamic story prompts and responses, creating a unique narrative for each playthrough.
*   **Character Management:** Players can create and manage character attributes (strength, dexterity, etc.) and equip items.
*   **Inventory System:** A comprehensive inventory system with drag-and-drop functionality for equipping and managing items.
*   **SQLite Persistence:** All game data, including character progress, items, and world state, is saved to a local SQLite database (`data/game.db`).
*   **Dynamic UI Layout:** Resizable windows and adjustable UI panels for a customizable experience.

## Requirements

*   Python 3.x
*   An Ollama server running with the `GMDnD:latest` model. You can pull this model using `ollama pull GMDnD:latest`.
*   The Python packages listed in `requirements.txt`.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd AIGM
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Ollama:**
    Ensure you have the Ollama server running. If not, download and install it from [ollama.ai](https://ollama.ai/).
    Pull the required model:
    ```bash
    ollama pull GMDnD:latest
    ```

## How to Run

1.  **Activate your virtual environment (if you created one):**
    ```bash
    source .venv/bin/activate
    ```

2.  **Run the main game file:**
    ```bash
    python src/main.py
    ```

## Usage

*   **Character Tab:** View your character's stats and equipped items.
*   **Inventory Tab:** Manage your character's equipped and carried items. You can drag and drop items between equipped slots and your carried inventory.
*   **Chat Window:** Interact with the AI Dungeon Master by typing commands or questions into the input box. The AI will respond with story elements and narrative progression.
*   **Resizable UI:** Drag the vertical dividers to adjust the size of the left, middle, and right panels.
*   **Fullscreen:** Press `F11` to toggle fullscreen mode.
