document.addEventListener("DOMContentLoaded", function () {
    var socket = io.connect("http://127.0.0.1:5001");

    socket.on("connect", function () {
        console.log("✅ WebSocket подключен!");
    });

    socket.on("notification", function (data) {
        console.log("🔥 Получено уведомление через WebSocket:", data.message);
        showNotification(data.message);
    });

    function showNotification(message) {
        console.log("📢 Запрос на уведомление:", message);
        if (Notification.permission === "granted") {
            new Notification("SmartFrige", {
                body: message,
                icon: "/static/images/image.png",
            });
        }
    }
});