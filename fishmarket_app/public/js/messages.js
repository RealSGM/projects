document.addEventListener("DOMContentLoaded", () => {
    fetch('/json/messages.json')
        .then(res => res.json())
        .then(messages => {
            const container = document.getElementById('messagesList');

            messages.forEach(dm => {

                const initials = dm.name
                    .split(" ")
                    .map(n => n[0])
                    .join("")
                    .toUpperCase();

                const time = new Date(dm.timestamp || Date.now())
                    .toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

                const msgDiv = document.createElement('div');
                msgDiv.classList.add('dm-item');

                msgDiv.innerHTML = `
                    <div class="dm-avatar">${initials}</div>

                    <div class="dm-content">
                        
                        <div class="dm-top-row">
                            <div class="dm-name">${dm.name}</div>
                            <div class="dm-time">${time}</div>
                        </div>

                        <div class="dm-preview">${dm.lastMessage}</div>

                    </div>
                `;

                msgDiv.onclick = () => window.location.href = `/messages/${dm.id}`;

                container.appendChild(msgDiv);
            });
        })
        .catch(err => console.error("Failed to load messages:", err));
});
