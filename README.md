# 🔧📌 Pinned Modifiers for Blender

![Blender Version](https://img.shields.io/badge/Blender-4.0+-orange.svg?style=flat-square&logo=blender)
![License](https://img.shields.io/badge/License-GPL_3.0-blue.svg?style=flat-square)

**Pinned Modifiers** is a Blender add-on designed to speed up our modeling workflow. It allows us to select our most frequently used modifiers and pin them directly to the "Add Modifier" menu for one-click access.

## ✨ Features

* **Pin Any Modifier:** Toggle which modifiers you want to appear in your quick-access list.
* **Custom Reordering:** Use the intuitive `[ ⤒ | ↑ | ↓ | ⤓ ]` UI controls to arrange your pinned modifiers in the exact order you want.
* **Persistent Settings:** Your configuration is written to a `JSON` file. Settings permanently survive Blender restarts, add-on reloads, and updates.
* **Export / Import:** Easily back up your personalized modifier stack or share your layout across multiple workstations and operating systems.
* **Reset to Defaults:** Messed up your list? Restore the default configuration with a single click. Just remember to export your settings, in case you want to restore them later!
* **Cross-Platform:** Works flawlessly on Linux, Windows, and macOS.

## ⚙️ Compatibility

* **Supported:** Blender 4.2 -> 5.1.1+
* **Supported with caveats:** Blender 4.0 -> 4.2 *(only direct import of the `__init__.py` python file)*
* **Not Supported:** Blender 3.6 LTS and older. *(This add-on relies on the dynamic "Add Modifier" menu system introduced in Blender 4.0).*

## 📥 Installation

### Drag and Drop
1. Download the latest `pinned_modifiers.zip` file from the Releases page.

### Legacy Method
1. go to **Edit > Preferences > Add-ons**
2. Click **Install...** in the top right corner and select the downloaded file.
3. Enable the checkbox next to **Interface: Pinned Modifiers**.

## ✏️ How to Use

1. Navigate to **Edit > Preferences > Add-ons** and expand the **Pinned Modifiers** add-on menu.
2. Under "Select modifiers to pin to the menu", check the boxes for your favorite modifiers.
3. A new **Reorder Pinned Modifiers** section will dynamically appear. Use the arrows to set your preferred vertical order.
4. Close the preferences. Open the **Properties Panel > Modifiers Tab** and click **Add Modifier**. Your pinned modifiers will be sitting right at the top!

### 📂 Where are my settings saved?
Your preferences are saved locally to a lightweight `.json` file inside your user configuration folder. The exact path for your specific operating system is displayed at the top of the add-on preferences panel.

## ❤️ Support & Links

If this add-on saves you time and improves your Blender workflow, please consider supporting my open-source work! 

* ☕ **Ko-Fi:** [ko-fi.com/frayoshi](https://ko-fi.com/frayoshi)
* 💸 **PayPal:** [paypal.me/FrancescoGobbo](https://paypal.me/FrancescoGobbo)
* 🪢 **GitHub:** [github.com/sponsors/FraYoshi](https://github.com/sponsors/FraYoshi) or click on the ♥️ hearth shaped sponsor icon.
* 🔗 **More Ways to Support:** [furayoshi.com/support](https://furayoshi.com/support)
* 🌐 **Homepage:** [furayoshi.com](https://furayoshi.com)
* 🗨️ **Discord:** [furayoshi.com/discord](https://furayoshi.com/discord)

## 🐛 Bug Reports & Feature Requests

Found a bug or have an idea to make this add-on better? Please open an issue on the [GitHub Issues page](https://github.com/FraYoshi/pinned-modifiers/issues).
