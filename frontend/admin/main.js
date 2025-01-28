const { app, BrowserWindow } = require("electron");
const path = require("path");

let adminWindow;

app.whenReady().then(() => {
    adminWindow = new BrowserWindow({
        width: 600,
        height: 400,
        webPreferences: {
            nodeIntegration: true,
        },
    });

    adminWindow.loadFile("admin.html");

    adminWindow.on("closed", () => {
        app.quit(); // Quit app when window is closed
    });
});

app.on("window-all-closed", () => {
    if (process.platform !== "darwin") {
        app.quit();
    }
});
